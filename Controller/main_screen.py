from typing import NoReturn
import importlib
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import View.MainScreen.main_screen
from applib.xml_import import get_node, getText
from kivymd.utils import asynckivy
from applib.dialogs.dialogs import DialogLoadKvFiles
from xml.dom.minidom import parse
from applib.db_functions import Comic, start_db
import xmltodict

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.MainScreen.main_screen)


class MainScreenController:
    """
    The `MainScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.main_screen.MainScreenModel
        self.view = View.MainScreen.main_screen.MainScreenView(controller=self, model=self.model)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            #previous=True,
        )
        self.dialog_load_comicrack_data = None
    def load_xml_data(self, path):
        import os
        if os.path.exists("ComicRackAPIServer2.db"):
            Comic.drop_table()
            Comic.create_table()
        else:
            print("The file does not exist")
        async def _load_xml_data():
            await asynckivy.sleep(0)
            # Load the xml file
            datasource = open(path,"r")
            xml_content= datasource.read()
            my_ordered_dict=xmltodict.parse(path)
            root = my_ordered_dict['ComicDatabase']
            books = root['Books']['Book']
            #dom2 = parse(datasource)  # parse an open file
            #books = dom2.getElementsByTagName("Book") # get <Books>
            #comiclists = dom2.getElementsByTagName("Item")
            totalCount = len(books)
            self.dialog_load_comicrack_data.text_method = "Loading Books"
            for book in books:
                await asynckivy.sleep(0)
                number = 0
                sId = book['@Id']
                number = book['Number']
                sfile = book['@File']
                series =  book['Series']
                volume =  book['Volume']
                year = book['Year']
                month = book['Month']
                pagecount = book['PageCount']
                currentpage = book['CurrentPage']
                lastpageread = book['LastPageRead']
                summary = book['Summary']
                print(f'ID={sId} File={sfile} Number={number}')
                comic, created = Comic.get_or_create(
                    Id = sId,
                    Number = number,
                    Series = series,
                    Volume = volume,
                    Year = year,
                    Month = month,
                    PageCount = pagecount,
                    FilePath = sfile,
                    LastPageRead = lastpageread,
                    CurrentPage = currentpage,
                    Summary = summary,
                    )
                self.dialog_load_comicrack_data.name_kv_file = f"{sId}\n {series} #{number} volume:{volume} "
                self.dialog_load_comicrack_data.percent = str(
                    i * 100 // int(totalCount)
                )
                i += 1
                if created == True:
                    print ("created")
                else:
                    print ("not created")
            # self.dialog_load_comicrack_data.text_method = "Loading Reading Lists"
            # totalCount = len(comiclists)
            # i = 1
            # for item in comiclists:
            #     print("##########################################")
            #     print(f"item {item}")
            #     await asynckivy.sleep(0)
            #     sId = item.getAttribute('Id')
            #     stype = item.getAttribute("xsi:type")
            #     print(f"ID:{sId} type:{stype}")
            #     self.dialog_load_comicrack_data.name_kv_file = f"{sId}\n {series} #{number} volume:{volume} "
            #     self.dialog_load_comicrack_data.percent = str(
            #         i * 100 // int(totalCount)
            #     )
            #     i += 1
            self.dialog_load_comicrack_data.dismiss()
        asynckivy.start(_load_xml_data())
    def on_tap_fmopen(self) -> NoReturn:
        """Called when the `Load ComicRack DB xml file` button is pressed."""
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True
    
   
    def get_view(self) -> View.MainScreen.main_screen.MainScreenView:
        return self.view

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        self.dialog_load_comicrack_data = DialogLoadKvFiles()
        self.dialog_load_comicrack_data.text_method = "Loading xml file"
        self.dialog_load_comicrack_data.open()
        self.load_xml_data(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
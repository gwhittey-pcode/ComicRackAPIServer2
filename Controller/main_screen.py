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
            os.remove("ComicRackAPIServer2.db")
            start_db()
        else:
            print("The file does not exist")
        async def _load_xml_data():
            await asynckivy.sleep(0)
            datasource = open(path)
            dom2 = parse(datasource)  # parse an open file
            books = dom2.getElementsByTagName("Book")
            i = 1
            totalCount = len(books)
            self.dialog_load_comicrack_data.text_method = "Loading Books"
            for book in books:
                await asynckivy.sleep(0)
                number = 0
                sId = book.getAttribute('Id')
                number = get_node(book,"Number")
                sfile = book.getAttribute('File')
                series =  get_node(book,"Series")
                volume =  get_node(book,"Volume")
                year = get_node(book,"Year")
                month = get_node(book,"Month")
                pagecount = get_node(book, "PageCount")
                currentpage = get_node(book,"CurrentPage")
                lastpageread = get_node(book,"LastPageRead")
                summary = get_node(book,"Summary")
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
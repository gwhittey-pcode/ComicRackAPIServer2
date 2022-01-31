"""
Script for managing hot reloading of the project.
For more details see the documentation page -

https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/create_project/

To run the application in hot boot mode, execute the command in the console:
DEBUG=1 python main.py
"""

import importlib
import os
from typing import NoReturn
from kivy import Config
from kivy.uix.screenmanager import ScreenManager
from applib.db_functions import start_db
from PIL import ImageGrab
from kivy.core.window import Window
from functools import partial
from kivy.clock import Clock
# TODO: You may know an easier way to get the size of a computer display.
# resolution = ImageGrab.grab().size

# Change the values of the application window size as you need.
# Config.set("graphics", "height", resolution[1])
# Config.set("graphics", "width", "400")

from kivy.core.window import Window

# Place the application window on the right side of the computer screen.
# Window.top = 0
# Window.left = resolution[0] - Window.width

from kivymd.tools.hotreload.app import MDApp


class ComicRackAPIServer2(MDApp):
    KV_FILES = {
        os.path.join(
            os.getcwd(),
            "View",
            "MainScreen",
            "main_screen.kv",
        ),
    }

    def build_app(self) -> ScreenManager:
        """
        In this method, you don't need to change anything other than the
        application theme.
        """

        import View.screens

        start_db()
        self.theme_cls.primary_palette = "Orange"
        self.manager_screens = ScreenManager()
        Window.bind(on_key_down=self.on_keyboard_down)
        importlib.reload(View.screens)
        screens = View.screens.screens
        # menuitems = (("Show App", None, Clock.schedule_once(self.show_app)),("Hide App", None, Clock.schedule_once(self.hide_app)),)
        # systray = SysTrayIcon("icon.ico", "Example tray icon", menuitems)
        # systray.start()
        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)
        return self.manager_screens

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers) -> NoReturn:
        """
        The method handles keyboard events.

        By default, a forced restart of an application is tied to the
        `CTRL+R` key on Windows OS and `COMMAND+R` on Mac OS.
        """

        if "meta" in modifiers or "ctrl" in modifiers and text == "r":
            self.rebuild()

    # def show_app(self,instance_trayicon):
    #     print("Show")
    #     Window.show()

    # def hide_app(self,instance_trayicon):
    #     print("Hide")
    #     Window.hide()
    # def on_quit_callback(self, systray):
    #     self.stop()

ComicRackAPIServer2().run()

# After you finish the project, remove the above code and uncomment the below
# code to test the application normally without hot reloading.

# """
# The entry point to the application.
#
# The application uses the MVC template. Adhering to the principles of clean
# architecture means ensuring that your application is easy to test, maintain,
# and modernize.
#
# You can read more about this template at the links below:
#
# https://github.com/HeaTTheatR/LoginAppMVC
# https://en.wikipedia.org/wiki/Model–view–controller
# """
#
# from typing import NoReturn
#
# from kivy.uix.screenmanager import ScreenManager
#
# from kivymd.app import MDApp
#
# from View.screens import screens
#
#
# class ComicRackAPIServer2(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.load_all_kv_files(self.directory)
#         # This is the screen manager that will contain all the screens of your
#         # application.
#         self.manager_screens = ScreenManager()
#
#     def build(self) -> ScreenManager:
#         """
#         Initializes the application; it will be called only once.
#         If this method returns a widget (tree), it will be used as the root
#         widget and added to the window.
#
#         :return:
#             None or a root :class:`~kivy.uix.widget.Widget` instance
#             if no self.root exists.
#         """
#
#         self.theme_cls.primary_palette = "Amber"
#         self.generate_application_screens()
#         return self.manager_screens
#
#     def generate_application_screens(self) -> NoReturn:
#         """
#         Creating and adding screens to the screen manager.
#         You should not change this cycle unnecessarily. He is self-sufficient.
#
#         If you need to add any screen, open the `View.screens.py` module and
#         see how new screens are added according to the given application
#         architecture.
#         """
#
#         for i, name_screen in enumerate(screens.keys()):
#             model = screens[name_screen]["model"]()
#             controller = screens[name_screen]["controller"](model)
#             view = controller.get_view()
#             view.manager_screens = self.manager_screens
#             view.name = name_screen
#             self.manager_screens.add_widget(view)
#
#
# ComicRackAPIServer2().run()

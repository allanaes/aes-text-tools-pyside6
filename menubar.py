from PySide6.QtGui import QAction

from rsc_icons import Icons
from window_message import msg_about_app


def create_app_menu(self):
    create_actions(self)
    create_menus(self)
    create_connections(self)


# 1. Actions
def create_actions(self):
    # File
    # File -> Exit -> ()
    self.act_exit = QAction(Icons.EXIT.icon(), "Exit", self)

    # About -> ()
    self.act_about = QAction("&About", self)


# 2. Menus
def create_menus(self):
    menubar = self.menuBar()

    # File
    file_menu = menubar.addMenu("&File")
    # File -> Exit
    file_menu.addAction(self.act_exit)

    # About
    menubar.addAction(self.act_about)


# 3. Connections
def create_connections(self):
    # File -> Exit -> ()
    self.act_exit.triggered.connect(self.app_exit)

    # About -> ()
    self.act_about.triggered.connect(lambda: msg_about_app(self))

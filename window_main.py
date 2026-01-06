from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app_changecase import ChangeCase
from app_digitizer import Digitizer
from app_npwpformatter import NPWPFormatter
from menubar import create_app_menu
from rsc_icons import Icons


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AES Text Tools")

        main_tab = QTabWidget()
        main_layout = QVBoxLayout()
        main_container = QWidget()

        main_tab.addTab(Digitizer(), "Digitizer")
        main_tab.addTab(NPWPFormatter(), "NPWP Formatter")
        main_tab.addTab(ChangeCase(), "Change Case")

        main_layout.addWidget(main_tab)
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

        create_app_menu(self)

        self.setWindowIcon(Icons.APP.icon())
        self.setMinimumWidth(480)
        self.setMinimumHeight(320)

    def app_exit(self):
        self.close()

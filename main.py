from PyQt6.QtWidgets import (QGridLayout, QApplication, QPushButton,
                             QLabel, QLineEdit, QWidget, QComboBox, QMainWindow)
from PyQt6.QtGui import QAction
import sys


class Notebook(QMainWindow):
    def __int__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")

        # Creating menu bar
        file_menu = self.menuBar().addMenu("&File")
        create_subject_action = QAction("Create New Subject", self)
        create_page_action = QAction("Create New Page", self)
        file_menu.addAction(create_subject_action)
        file_menu.addAction(create_page_action)
        create_subject_action.setMenuRole(QAction.MenuRole.NoRole)
        create_page_action.setMenuRole(QAction.MenuRole.NoRole)

        edit_menu = self.menuBar().addMenu("&Edit")
        rename_action = QAction("Rename", self)
        delete_action = QAction("Delete", self)
        edit_menu.addAction(rename_action)
        edit_menu.addAction(delete_action)
        rename_action.setMenuRole(QAction.MenuRole.NoRole)
        delete_action.setMenuRole(QAction.MenuRole.NoRole)


app = QApplication(sys.argv)
ai_notebook = Notebook()
ai_notebook.show()
sys.exit(app.exec())

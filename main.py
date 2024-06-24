from PyQt6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow, QPushButton,
                             QTextEdit, QComboBox, QListWidget, QDialog, QVBoxLayout)
from PyQt6.QtGui import QAction
import sys


class Notebook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Notebook App")
        self.setMinimumSize(1125, 900)

        # Create Menu Bar
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background-color: grey")
        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        create_subject_action = QAction("Create Subject", self)
        create_page_action = QAction("Create Page", self)
        save_page_action = QAction("Save", self)
        save_page_action.setShortcut("Ctrl+S")
        exit_page_action = QAction("Exit", self)
        exit_page_action.setShortcut("Ctrl+E")
        file_menu_item.addAction(create_subject_action)
        create_subject_action.triggered.connect(self.subject)
        file_menu_item.addAction(create_page_action)
        file_menu_item.addAction(save_page_action)
        file_menu_item.addAction(exit_page_action)

        rename_action = QAction("Rename", self)
        delete_action = QAction("Delete", self)
        edit_menu_item.addAction(rename_action)
        edit_menu_item.addAction(delete_action)

        # Create UI Labels
        note_label = QLabel("Place-holder (Notes)", self)
        note_label.setGeometry(690, 30, 200, 21)
        note_label.setStyleSheet("text-align: center; font-size:12pt")

        subject_label = QLabel("Subject", self)
        subject_label.setGeometry(130, 30, 200, 21)
        subject_label.setStyleSheet("text-align: center; font-size:12pt")

        # Create Subject combo box
        subject_box = QComboBox(self)
        subject_box.addItems([""])
        subject_box.setGeometry(70, 60, 200, 40)

        # Create Note Input
        note_area = QTextEdit(self)
        note_area.setGeometry(340, 60, 750, 810)

        # Create Note List
        note_list = QListWidget(self)
        note_list.addItem("test")
        note_list.setGeometry(40, 140, 255, 729)

    def subject(self):
        dialog = CreateSubject()
        dialog.exec()


class CreateSubject(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Subject")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Create Subject Input
        self.subject = QLineEdit(self)
        self.subject.setPlaceholderText("Subject")
        layout.addWidget(self.subject)

        # Create Add Button
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_subject)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_subject(self):
        subject = self.subject.text()
        self.close()
        return subject





app = QApplication(sys.argv)
notebook_app = Notebook()
notebook_app.show()
sys.exit(app.exec())

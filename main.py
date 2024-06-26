from PyQt6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow, QPushButton,
                             QTextEdit, QComboBox, QListWidget, QDialog, QVBoxLayout)
from PyQt6.QtGui import QAction
import json
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
        create_page_action.triggered.connect(self.page)
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
        self.subject_box = QComboBox(self)
        self.load_subjects()
        self.subject_box.setGeometry(70, 60, 200, 40)

        # Create Note Input
        note_area = QTextEdit(self)
        note_area.setGeometry(340, 60, 750, 810)

        # Create Note List
        note_list = QListWidget(self)
        note_list.addItem("test")
        note_list.setGeometry(40, 140, 255, 729)

    def load_data(self):
        with open("subjects/data.json", "r") as file:
            content = file.read()
        data = json.loads(content)
        return data

    def subject(self):
        dialog = CreateSubject()
        dialog.exec()

    def page(self):
        dialog = CreatePage()
        dialog.exec()

    def new_subject(self):
        with open("subjects/subject.txt", "r") as file:
            subject = file.read()
        new_subject = subject.split(sep=",")
        new_subject = new_subject[-2]
        self.subject_box.addItem(new_subject)

    def load_subjects(self):
        with open("subjects/subject.txt", "r") as file:
            subject = file.read()
        subject_list = subject.split(sep=",")
        subject_list = subject_list[:-1]
        self.subject_box.addItems(subject_list)

    def subject_list(self):
        with open("subjects/subject.txt", "r") as file:
            subject = file.read()
        subject_list = subject.split(sep=",")
        subject_list = subject_list[:-1]
        return subject_list


class CreatePage(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Page")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.subject_box = QComboBox(self)
        with open("subjects/subject.txt", "r") as file:
            subject = file.read()
        subject_list = subject.split(sep=",")
        subject_list = subject_list[:-1]
        self.subject_box.addItems(subject_list)
        layout.addWidget(self.subject_box)

        self.page = QLineEdit(self)
        self.page.setPlaceholderText("Page Title:")
        layout.addWidget(self.page)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_page)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_page(self):
        subject_name = self.subject_box.itemText(self.subject_box.currentIndex())
        subject_list = notebook_app.subject_list()
        page_name = self.page.text()
        self.assign_page(subject_list, subject_name, page_name)
        self.close()

    def assign_page(self, subject_list, subject_name, page_name):
        subject_dict = {}
        for subject in subject_list:
            subject_dict.update({subject: ""})
            if subject_name == subject:
                subject_dict[subject] = page_name
        with open("subjects/data.json", "w") as file:
            data = str(subject_dict)
            data_filtered = data.replace("'", '"')
            file.write(data_filtered)


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
        with open("subjects/subject.txt", "a") as file:
            file.write(f"{subject.title()},")
        notebook_app.new_subject()
        self.close()


app = QApplication(sys.argv)
notebook_app = Notebook()
notebook_app.show()
sys.exit(app.exec())

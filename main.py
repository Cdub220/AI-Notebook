from PyQt6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow, QPushButton,
                             QTextEdit, QComboBox, QListWidget, QDialog, QVBoxLayout)
from PyQt6.QtGui import QAction, QPixmap
import json
import sys
import os


class Notebook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Notebook App")
        self.setMinimumSize(1125, 900)
        self.current_note = {"Subject": "", "Page": ""}

        # Create Menu Bar
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background-color: grey")
        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # (File) Menu Bar
        create_subject_action = QAction("Create Subject", self)
        create_page_action = QAction("Create Page", self)
        save_page_action = QAction("Save", self)
        save_page_action.setShortcut("Ctrl+S")
        save_page_action.triggered.connect(self.save_note)
        exit_page_action = QAction("Exit", self)
        exit_page_action.setShortcut("Ctrl+E")
        exit_page_action.triggered.connect(exit)
        file_menu_item.addAction(create_subject_action)
        create_subject_action.triggered.connect(self.subject)
        file_menu_item.addAction(create_page_action)
        create_page_action.triggered.connect(self.page)
        file_menu_item.addAction(save_page_action)
        file_menu_item.addAction(exit_page_action)

        # (Edit) Menu Bar
        rename_action = QAction("Rename", self)
        delete_action = QAction("Delete", self)
        edit_menu_item.addAction(rename_action)
        rename_action.triggered.connect(self.rename)
        edit_menu_item.addAction(delete_action)

        # Create UI Labels
        note_label = QLabel("Place-holder (Notes)", self)
        note_label.setGeometry(690, 30, 200, 21)
        note_label.setStyleSheet("text-align: center; font-size:12pt")
        subject_label = QLabel("Subject", self)
        subject_label.setGeometry(130, 30, 200, 21)
        subject_label.setStyleSheet("text-align: center; font-size:12pt")

        # Create Note Input
        self.note_area = QTextEdit(self)
        self.note_area.setGeometry(340, 60, 750, 810)

        # Create Note List
        self.note_list = QListWidget(self)
        self.note_list.itemSelectionChanged.connect(self.open_note)
        self.note_list.setGeometry(40, 140, 255, 729)

        # Create Subject combo box
        self.subject_box = QComboBox(self)
        self.subject_box.currentIndexChanged.connect(self.load_pages)
        self.load_subjects()
        self.subject_box.setGeometry(70, 60, 200, 40)

    def load_pages(self):
        self.note_list.clear()
        data_file = "subjects/data.json"
        file_size = os.path.getsize(data_file)
        if file_size != 0:
            data = self.load_data()
            current_subject = self.subject_box.itemText(self.subject_box.currentIndex())
            subject_pages = data[current_subject]
            for page in subject_pages:
                self.note_list.addItem(page)
            self.current_note["Subject"] = current_subject

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

    def rename(self):
        dialog = Rename()
        dialog.exec()

    def new_subject(self):
        with open("subjects/subject.txt", "r") as file:
            subject = file.read()
        new_subject = subject.split(sep=",")
        new_subject = new_subject[-2]
        self.subject_box.addItem(new_subject)

    def load_subjects(self):
        self.subject_box.clear()
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

    def open_note(self):
        subject = self.subject_box.itemText(self.subject_box.currentIndex())
        page = self.note_list.currentItem().text()
        self.current_note["Page"] = page
        if not os.path.exists(f"notes/{subject}"):
            os.makedirs(f"notes/{subject}")
        if os.path.exists(f"notes/{subject}/{page}"):
            with open(f"notes/{subject}/{page}", "r") as file:
                content = file.read()
            self.note_area.setText(content)
        else:
            self.note_area.clear()

    def save_note(self):
        subject = self.current_note["Subject"]
        page = self.current_note["Page"]
        content = self.note_area.toPlainText()
        with open(f"notes/{subject}/{page}", "w") as file:
            file.write(content)


class Rename(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rename")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.subject_box_class = QComboBox(self)
        layout.addWidget(self.subject_box_class)
        self.subject_box_option = QComboBox(self)
        layout.addWidget(self.subject_box_option)

        class_list = ["Subject", "Page"]
        self.subject_box_class.addItems(class_list)
        self.subject_box_class.currentIndexChanged.connect(self.load_pages)

        self.setLayout(layout)
        self.load_pages()

    def load_pages(self):
        class_picked = self.subject_box_class.itemText(self.subject_box_class.currentIndex())
        self.subject_box_option.clear()
        subjects = []
        pages = []
        with open("subjects/data.json", "r") as file:
            content = file.read()
            subject_dict = json.loads(content)
        if class_picked == "Subject":
            for subject in subject_dict:
                subjects.append(subject)
            self.subject_box_option.addItems(subjects)
        elif class_picked == "Page":
            for subject in subject_dict:
                pages += subject_dict[subject]
            self.subject_box_option.addItems(pages)


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
        with open("subjects/data.json", "r") as file:
            content = file.read()
            subject_dict = json.loads(content)
        subject_dict[subject_name].append(page_name.title())
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
        self.add_subject_to_data(subject.title())
        notebook_app.new_subject()
        self.close()

    def add_subject_to_data(self, new_subject):
        data_file = "subjects/data.json"
        file_size = os.path.getsize(data_file)
        subject_dict = {}
        if file_size != 0:
            subject_dict = self.load_data()
        with open("subjects/subject.txt", "r") as file:
            subjects_list = file.read()
            subjects_list = subjects_list.split(",")
        for subject in subjects_list:
            if subject == new_subject:
                subject_dict[subject] = list()
        if "" in subject_dict:
            del subject_dict[""]
        with open("subjects/data.json", "w") as file:
            data = str(subject_dict)
            data_filtered = data.replace("'", '"')
            file.write(data_filtered)

    def load_data(self):
        with open("subjects/data.json", "r") as file:
            content = file.read()
        data = json.loads(content)
        return data


app = QApplication(sys.argv)
notebook_app = Notebook()
notebook_app.show()
sys.exit(app.exec())

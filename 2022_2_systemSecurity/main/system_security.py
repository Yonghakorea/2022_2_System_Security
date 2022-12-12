from PyQt5.Qt import *
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import system_security2
import sys
import os
import shutil
import functools
import tkinter
import hashlib
import pyautogui as df


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.config_window()
        self.create_widgets()
        self.config_widgets()
        self.create_menubar()
        self.bind_widgets()
        self.show_widgets()

    def config_window(self): #제목창
        self.setWindowTitle('System Security')
        self.setMinimumHeight(600)
        self.setMinimumWidth(1000)

    def create_widgets(self): #상단 위젯
        self.central_widget = QWidget()
        self.main_layout = QGridLayout()
        self.moveup_button = QPushButton('Collapse all', self)
        self.goto_lineedit = QLineEdit('C:\\', self)
        self.goto_button = QPushButton('Go', self)
        self.folder_view = QTreeView(self)
        self.file_view = QTreeView(self)
        self.folder_model = QFileSystemModel(self)
        self.file_model = QFileSystemModel(self)

    def config_widgets(self):
        self.main_layout.addWidget(self.moveup_button, 0, 0)
        self.main_layout.addWidget(self.goto_lineedit, 0, 1, 1, 2)
        self.main_layout.addWidget(self.goto_button, 0, 3)
        self.main_layout.addWidget(self.folder_view, 1, 0, 1, 2)
        self.main_layout.addWidget(self.file_view, 1, 2, 1, 1)

        self.central_widget.setLayout(self.main_layout)

        # 단추 "위로"
        self.moveup_button.setMaximumWidth(100)

        # 단추 "이동"
        self.goto_button.setMaximumWidth(70)
        self.setCentralWidget(self.central_widget)

        self.folder_model.setRootPath(None)
        self.folder_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        self.folder_view.setModel(self.folder_model)
        self.folder_view.setRootIndex(self.folder_model.index(None))
        self.folder_view.clicked[QModelIndex].connect(self.clicked_onfolder)
        self.folder_view.hideColumn(1)
        self.folder_view.hideColumn(2)
        self.folder_view.hideColumn(3)

        self.file_model.setFilter(QDir.Files)
        self.file_view.setModel(self.file_model)
        self.file_model.setReadOnly(False)
        self.file_view.setColumnWidth(0,200)
        self.file_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def clicked_onfolder(self, index):
        selection_model = self.folder_view.selectionModel()
        index = selection_model.currentIndex()
        dir_path = self.folder_model.filePath(index)
        self.file_model.setRootPath(dir_path)
        self.file_view.setRootIndex(self.file_model.index(dir_path))

    def open_file(self):
        index = self.file_view.selectedIndexes()
        if not index:
            return
        else:
            index = index[0]
        file_path = self.file_model.filePath(index).replace('/', '\\')
        print(file_path)
        extention = os.path.splitext(file_path)[-1]
        print(extention)
        if extention in ['.txt']:
            system_security2.Application.main(file_path)
        self.file_view.update()

    def new_file(self):
        index = self.folder_view.selectedIndexes()
        if len(index) > 0:
            path = self.folder_model.filePath(index[0])
            for i in range(1, 9999999999999999):
                if not os.path.isfile(os.path.join(path, "Newfile{}.txt".format(i))):
                    file_name = os.path.join(path, "Newfile{}.txt".format(i))
                    break
            file_name = os.path.abspath(file_name)
            open(file_name, 'w').close()
        else:
            print("Please, select folder")

    def delete_file(self):
        indexes = self.file_view.selectedIndexes()
        for i in indexes:
            self.file_model.remove(i)

    def rename_file(self):
        index = self.file_view.selectedIndexes()
        if not index:
            return
        else:
            index = index[0]
        self.file_view.edit(index)

    def copy_file(self):
        print("COPY")
        ask = QFileDialog.getExistingDirectory(self, "Open Directory", "/home",
                                               QFileDialog.ShowDirsOnly |
                                               QFileDialog.DontResolveSymlinks)
        new_path = ask.replace('\\', '/')
        indexes = self.file_view.selectedIndexes()[::4]
        for i in indexes:
            new_filename = new_path + '/' + self.file_model.fileName(i)
            shutil.copy2(self.file_model.filePath(i), new_filename)

    def check_file(self):
        print("Checking malware via VirusTotal...")
        index = self.file_view.selectedIndexes()
        if not index:
            return
        else:
            index = index[0]
        file_path = self.file_model.filePath(index).replace('/', '\\')
        print(file_path)
        file = file_path

        f = open(file, 'rb')
        data = f.read()
        f.close()

        print("MD5: " + hashlib.md5(data).hexdigest())
        print("SHA-1: " + hashlib.sha1(data).hexdigest())
        print("SHA-256: " + hashlib.sha256(data).hexdigest())
        driver = webdriver.Chrome(executable_path='C:\\Users\\yongh\\Downloads\\chromedriver_win32(1)\\chromedriver.exe')
        driver.get('https://www.virustotal.com/gui/home/search')
        time.sleep(1)
        df.typewrite(hashlib.sha256(data).hexdigest())
        df.typewrite(["enter"])
        time.sleep(10)
        return

    def colapse(self):
        self.folder_view.collapseAll()

    def go_to(self):
        dir_path = self.goto_lineedit.text().replace('\\', '/')
        print(dir_path)
        self.file_model.setRootPath(dir_path)
        self.file_view.setRootIndex(self.file_model.index(dir_path))

        #self.file_model.setRootPath()

    def move_file(self):
        print("MOVE")
        ask = QFileDialog.getExistingDirectory(self, "Open Directory", "/home",
                                               QFileDialog.ShowDirsOnly |
                                               QFileDialog.DontResolveSymlinks)
        if ask == '':
            return
        new_path = ask.replace('\\', '/')
        indexes = self.file_view.selectedIndexes()[::4]
        for i in indexes:
            new_filename = new_path + '/' + self.file_model.fileName(i)
            shutil.move(self.file_model.filePath(i), new_filename)

    def new_folder(self):
        index = self.folder_view.selectedIndexes()
        if len(index) > 0:
            path = self.folder_model.filePath(index[0])
            for i in range(1, 9999999999999999):
                if not os.path.isdir(os.path.join(path, "Newfolder{}".format(i))):
                    file_name = os.path.join(path, "Newfolder{}".format(i))
                    break
            file_name = os.path.abspath(file_name)
            os.mkdir(file_name)
        else:
            print("Please, select folder")

    def delete_folder(self):
        indexes = self.folder_view.selectedIndexes()
        for i in indexes:
            self.folder_model.remove(i)

    def rename_folder(self):
        index = self.folder_view.selectedIndexes()
        if not index:
            return
        else:
            index = index[0]
        self.folder_view.edit(index)

    def exit_application(self):
       print("EXIT")
       self.close()

    def about_program(self, event=None):
        w = tkinter.Tk()
        w.title("About program")
        w.minsize(width=400, height=100)
        options = dict(padx=10, pady=14, sticky=tkinter.W+tkinter.N)

        tkinter.Label(w, text='프로그램 이름 :').grid(column=0, row=0, **options)
        tkinter.Label(w, text="파일관리자").grid(column=1, row=0, **options)

        tkinter.Label(w, text='작성자 :').grid(column=0, row=1, **options)
        tkinter.Label(w, text="김용하, 한겨레").grid(column=1, row=1, **options)


        tkinter.Label(w, text='설명 :').grid(column=0, row=3, **options)
        tkinter.Label(w, text="파일 관리자(File Manager)는 컴퓨터 프로그램입니다.\n"
                              "이 프로그램은 파일 텍스트 편집을 위한 인터페이스를 제공합니다. \n"
                              "이 프로그램은 다음과 같은 기능들이 있습니다 : \n"
                              "파일 이름 수정, 파일 삭제, 새 폴더, 폴더 이동, \n"
                              "폴더 복사, 폴더 삭제, 폴더 이름 수정, 파일 악성코드 검사\n").grid(column=1, row=3, **options)

        w.mainloop()

    def bind_widgets(self):
        self.open_file_action.triggered.connect(self.open_file)
        self.new_file_action.triggered.connect(self.new_file)
        self.delete_file_action.triggered.connect(self.delete_file)
        self.rename_file_action.triggered.connect(self.rename_file)
        self.copy_file_action.triggered.connect(self.copy_file)
        self.check_file_action.triggered.connect(self.check_file)
        self.move_file_action.triggered.connect(self.move_file)
        self.exit_action.triggered.connect(self.exit_application)

        self.new_folder_action.triggered.connect(self.new_folder)
        self.delete_folder_action.triggered.connect(self.delete_folder)
        self.rename_folder_action.triggered.connect(self.rename_folder)
        self.about_action.triggered.connect(self.about_program)


        self.goto_button.clicked.connect(functools.partial(self.go_to))
        self.moveup_button.clicked.connect(functools.partial(self.colapse))

    def create_menubar(self):

        self.exit_action = QAction('Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')

        self.new_file_action = QAction('New file', self)
        self.new_file_action.setShortcut('F4')

        self.open_file_action = QAction('Open file', self)
        self.open_file_action.setShortcut('F3')

        self.rename_file_action = QAction('Rename file', self)
        self.rename_file_action.setShortcut('F2')

        self.delete_file_action = QAction('Remove file', self)
        self.delete_file_action.setShortcut(QKeySequence.Delete)

        self.check_file_action = QAction('Check file', self)
        self.check_file_action.setShortcut('Ctrl+Z')

        self.copy_file_action = QAction('Copy file/folder', self)
        self.copy_file_action.setShortcut(QKeySequence.Copy)

        self.move_file_action = QAction('Move file/folder', self)
        self.move_file_action.setShortcut(QKeySequence.Cut)

        self.new_folder_action = QAction('New folder', self)
        self.new_folder_action.setShortcut('Ctrl+Shift+N')

        self.delete_folder_action = QAction('Delete folder', self)
        self.delete_folder_action.setShortcut('Ctrl+Shift+Del')

        self.rename_folder_action = QAction('Rename folder', self)
        self.rename_folder_action.setShortcut('Ctrl+Shift+R')

        self.about_action = QAction('About program', self)
        self.about_action.setShortcut('F1')

        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu('File')
        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.rename_file_action)
        self.file_menu.addAction(self.delete_file_action)
        self.file_menu.addAction(self.copy_file_action)
        self.file_menu.addAction(self.move_file_action)
        self.file_menu.addAction(self.check_file_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.folder_menu = self.menubar.addMenu('Folder')
        self.folder_menu.addAction(self.new_folder_action)
        self.folder_menu.addAction(self.delete_folder_action)
        self.folder_menu.addAction(self.rename_folder_action)

        self.about_menu = self.menubar.addMenu('About')
        self.about_menu.addAction(self.about_action)

    def show_widgets(self):
        self.setLayout(self.main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec_()
    app.exit()
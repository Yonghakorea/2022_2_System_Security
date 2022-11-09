from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
import text_editor
import sys
import os
import shutil
import functools
import tkinter

class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.config_window()
        self.create_widgets()
        self.config_widgets()
        self.show_widgets()

    def config_window(self):
        self.setWindowTitle('System Security')
        self.setMinimumHeight(600)
        self.setMinimumWidth(1000)

    def create_widgets(self):
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
        self.main_layout.addWidget(self.file_view, 1, 2, 1, 2)

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




    def about_prog(self, event=None):
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
                              "이 프로그램은 파일 편집을 위한 인터페이스를 제공합니다. \n"
                              "이 프로그램은 다음과 같은 기능들이 있습니다 : \n"
                              "파일 이름 수정, 파일 삭제, 새 폴더, 폴더 이동, \n"
                              "폴더 복사, 폴더 삭제, 폴더 이름 수정\n").grid(column=1, row=3, **options)

        w.mainloop()



    def show_widgets(self):
        self.setLayout(self.main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MyMainWindow()
    mw.show()
    app.exec_()
    app.exit()
import sys, os, shutil
from PyQt5.QtWidgets import QWidget, QApplication, QTreeView, QFileSystemModel, QVBoxLayout, QPushButton, QInputDialog,\
    QLineEdit

class main(QWidget):
    def __init__(self):
        # 변수 여러 가지 지정
        super().__init__()
        self.path = "C:"    # 경로
        self.index = None   # 현재 선택한 내 파일 또는 디렉토리의 위칮

        self.tv = QTreeView(self)   # ui 상에서 계층적인 표시를 할 수 있게끔 하는 것
        self.model = QFileSystemModel() # ui 상에서 파일의 구조를 나타나게 함

        self.layout = QVBoxLayout() # 세로로 ui 박스를 쌓을 수 있게끔 사용하는 기능

        self.setUi()
        self.setSlot()  # setUi, setSlot 함수 선언

    def setUi(self):
        self.setGeometry(300, 300, 700, 350)    # ui의 위치와 크기 지정
        self.setWindowTitle("System security")
        self.model.setRootPath(self.path)   # c드라이브를 root path로 설정
        self.tv.setModel(self.model)    # treeview에서 보여줄 모델을 지정(c드라이브를 root로 가지고 있는 모델에 treeview를 지정)
        self.tv.setColumnWidth(0, 250)  # 0번째 열(ui 상에서는 name)을 250으로 설정해 넓혀준다.

        self.layout.addWidget(self.tv)  # treeview 레이아웃 추가

        self.setLayout(self.layout) # 추가한 레이아웃을 기본 레이아웃으로 설정

    def setSlot(self):
        self.tv.clicked.connect(self.setIndex)  # treeview를 클릭할 때마다 setIndex 함수를 호출


    def setIndex(self, index):
        self.index = index  # 파일이나 디렉토리를 선택할때마다 인덱스가 바뀌기 때문에 선택한 인덱스값을 저장(파일 삭제, 이름바꾸기할때 유용함)



app = QApplication([])  # 프로그램 실행
ex = main()
ex.show()
sys.exit(app.exec_())

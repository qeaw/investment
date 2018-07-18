import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QMessageBox,
                             QMainWindow,QAction,qApp,QLabel,QHBoxLayout,QVBoxLayout,
                             QGridLayout,QLCDNumber,QSlider,QTextEdit,QLineEdit,
                             QInputDialog,QFileDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import (QCoreApplication,Qt,QObject,pyqtSignal)
from time import sleep
import tushare as ts
from datetime import datetime, timedelta


# gpdm = [["600604",8,10],["002264",5,100]]
# with open(r"C:\Users\qeaw\Desktop\config.txt","r") as f:
#    r = f.readlines()
# gpdm = eval(r[0])



class jiance(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        with open(r"C:\Users\qeaw\Desktop\config.txt", "r") as f:
            r = f.readlines()
        gpdm = eval(r[0])
        self.textEdit = QTextEdit()
        self.textEdit.setText("default value")
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openfile = QAction(QIcon("open.png"),"open",self)
        openfile.setShortcut("Ctrl+O")
        openfile.setStatusTip("open new file")

        openfile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        filemenu = menubar.addMenu("file")
        filemenu.addAction(openfile)
        n = 0
        # btn_add = QPushButton("添加", self)
        # btn_add.setToolTip("添加条目")
        # btn_add.resize(btn_add.sizeHint())
        # btn_add.move(550, 400)
        # btn_add.clicked.connect(self.showchuangkou)
        #
        # btn_delate = QPushButton("删除", self)
        # btn_delate.setToolTip("删除条目")
        # btn_delate.resize(btn_delate.sizeHint())
        # btn_delate.move(550, 450)

        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle("监测程序")
        self.show()
        while datetime.now().hour < 25:
            result = f"code\tname\tbid\task\t买入价\t卖出价\t买入卖出比\n"
            for i in gpdm:
                r = ts.get_realtime_quotes(i[0])
                liangbi =(float(r.b1_v[0])+float(r.b2_v[0])+float(r.b3_v[0])+float(r.b4_v[0])+float(r.b5_v[0])) / (float(r.a1_v[0])+float(r.a2_v[0])+float(r.a3_v[0])+float(r.a4_v[0])+float(r.a5_v[0]))
                # print(liangbi)
                result += f"{r.code[0]}\t{r.name[0]}\t{r.bid[0]}\t{r.ask[0]}\t{i[1]}\t{i[2]}\t{str(liangbi)}\n"


            self.textEdit.setText(result)
            QApplication.processEvents()


            sleep(1)
        # sys.exit(app.exec_())
    def showchuangkou(self):
        text, ok = QInputDialog.getText(self,"输入条目","输入参数 ([代码，买入价，卖出价])")
        if ok:
            print(text)

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, "open file","/desktop")

        if fname[0]:
            f = open(fname[0],"r")

            with f:
                data = f.read()
                self.textEdit.setText(data)


class xuangu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        with open(r"C:\Users\qeaw\Desktop\config.txt", "r") as f:
            r = f.readlines()
        gpdm = eval(r[0])
        self.textEdit = QTextEdit()
        self.textEdit.setText(str(gpdm))
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openfile = QAction(QIcon("open.png"),"open",self)
        openfile.setShortcut("Ctrl+O")
        openfile.setStatusTip("open new file")

        openfile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        filemenu = menubar.addMenu("file")
        filemenu.addAction(openfile)
        n = 0
        btn_add = QPushButton("添加", self)
        btn_add.setToolTip("添加条目")
        btn_add.resize(btn_add.sizeHint())
        btn_add.move(550, 400)
        btn_add.clicked.connect(self.showtianjia)

        btn_delate = QPushButton("删除", self)
        btn_delate.setToolTip("删除条目")
        btn_delate.resize(btn_delate.sizeHint())
        btn_delate.move(550, 450)
        btn_delate.clicked.connect(self.showshanchu)

        btn_jiance = QPushButton("开始监测", self)
        btn_jiance.setToolTip("点击开始监测")
        btn_jiance.resize(btn_jiance.sizeHint())
        btn_jiance.move(550, 500)
        btn_jiance.clicked.connect(jiance)

        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle("监测程序")
        self.show()


    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, "open file","/desktop")

        if fname[0]:
            f = open(fname[0],"r")

            with f:
                data = f.read()
                self.textEdit.setText(data)

    def showtianjia(self):
        text, ok = QInputDialog.getText(self, "输入条目", "输入参数 ([代码，买入价，卖出价])")
        if ok:

            item = eval(text)

            with open(r"C:\Users\qeaw\Desktop\config.txt","r") as f:
                l = eval(f.readline())
            l.append(item)

            with open(r"C:\Users\qeaw\Desktop\config.txt", "w+") as ff:

                ff.write(str(l))

            self.textEdit.setText(str(l))

    def showshanchu(self):
        text, ok = QInputDialog.getText(self, "输入删除对象", "输入gpdm")
        if ok:

            print(text)

            with open(r"C:\Users\qeaw\Desktop\config.txt","r") as f:
                l = eval(f.readline())
            print(l)
            n = 0
            for i in l:
                print(i)

                print(str(i[0]))
                if str(text) == str(i[0]):
                    print("zhaodao")
                    l.remove(i)
                    n += 1
                    print(l)
                    with open(r"C:\Users\qeaw\Desktop\config.txt", "w+") as ff:
                        ff.write(str(l))
            if n == 0:
                print(f"{gpdm}并不存在")

            self.textEdit.setText(str(l))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = xuangu()
    sys.exit(app.exec_())
#
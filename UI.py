#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pymysql
import pymysql.cursors
import Recomments
from random import randint
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')        # 这个就很厉害了，设置默认编码
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'passwd':'654321',
    'db':'douban_database',     # 选择数据库
    'use_unicode':1,
    'charset':'utf8',
    'cursorclass':pymysql.cursors.DictCursor             # 以字典形式返回,默认是元组
}
con_sql = pymysql.Connect(**config)
cursor = con_sql.cursor()
sql = "select * from system_douban"
cursor.execute(sql)
allinfors = cursor.fetchall()
User = ''     # 推荐

username = ''
LoginSuccessFlag = False
RegisterFlag = False
favorite = None     # 实例对象

class StackWidget(QMainWindow):

    def __init__(self,parent=None):
        super(StackWidget,self).__init__(parent)
        font = QFont(self.tr("宋体"),11)    # 设置显示的字体和字号
        QApplication.setFont(font)
        self.resize(525,350)
        self.setWindowTitle(self.tr("仅供学术交流~"))

        widget = QWidget()
        self.setCentralWidget(widget)

        mainlayout = QHBoxLayout()
        listwidget = QListWidget()
        listwidget.insertItem(0,self.tr("首页"))
        listwidget.insertItem(1,self.tr("个人资料"))
        listwidget.insertItem(2,self.tr("收藏夹"))
        mainlayout.addWidget(listwidget)

        stack = QStackedWidget()
        stack.setFrameStyle(QFrame.Panel | QFrame.Raised)  # 框架风格

        mainpage = MainPage()      # 这里是重点
        basicinfo = BasicInfo()
        global favorite
        favorite = Favorite()

        stack.addWidget(mainpage)
        stack.addWidget(basicinfo)
        stack.addWidget(favorite)

        closePushButton = QPushButton(self.tr("关闭"))
        self.connect(closePushButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(listwidget, SIGNAL("currentRowChanged(int)"), stack, SLOT("setCurrentIndex(int)"))
        buttonlayout = QHBoxLayout()
        buttonlayout.addStretch()
        buttonlayout.addWidget(closePushButton)

        rightlayout = QVBoxLayout()
        rightlayout.setMargin(10)
        rightlayout.setSpacing(6)

        rightlayout.addWidget(stack)
        rightlayout.addLayout(buttonlayout)
        mainlayout.addLayout(rightlayout)

        mainlayout.setStretchFactor(listwidget,1)   # 设置左右框1:5
        mainlayout.setStretchFactor(rightlayout,5)
        widget.setLayout(mainlayout)

class MainPage(QWidget):

    def __init__(self,parent=None):
        super(MainPage,self).__init__(parent)

        mainlayout = QVBoxLayout()  # 主窗口,垂直布局

        startlabel = QLabel(self.tr("豆瓣电影推荐系统"))
        startlabel.setFont(QFont(self.tr("宋体"), 15))
        startlabel.setAlignment(Qt.AlignHCenter)     # 文字水平居中

        handlelayout = QHBoxLayout()
        handlelayout.addStretch()
        self.userlabel = QLabel(self.tr(""))             # 这里应该是 用户名:
        self.loginPushButton = QPushButton(self.tr("登录"))
        self.registerPushButton = QPushButton(self.tr("注册"))
        handlelayout.addWidget(self.userlabel)
        handlelayout.addWidget(self.loginPushButton)
        handlelayout.addWidget(self.registerPushButton)

        searchlayout = QHBoxLayout()
        searchlabel = QLabel()
        searchlabel.setPixmap(QPixmap("C:/Users/asus-pc/Pictures/search.png").scaled(25,25))
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setPlaceholderText(self.tr("输入内容"))      # 设置输入框浮显文字,这个就非常厉害了
        # self.searchLineEdit.backspace()   # 模拟backspace退格键,看不出来。。。
        searchPushButton = QPushButton(self.tr("搜索"))
        searchlayout.addWidget(searchlabel)
        searchlayout.addWidget(self.searchLineEdit)
        searchlayout.addWidget(searchPushButton)

        choicelayout = QHBoxLayout()
        self.movieRadioButton = QRadioButton(self.tr("电影"))
        self.dirRadioButton = QRadioButton(self.tr("导演"))
        self.starRadioButton = QRadioButton(self.tr("演员"))
        self.typeRadioButton = QRadioButton(self.tr("类型"))
        self.areaRadioButton = QRadioButton(self.tr("地区"))
        self.details = QCheckBox(self.tr("详情"))
        # self.dirRadioButton = QCheckBox(self.tr("导演"))       # 复选框
        # self.starRadioButton = QCheckBox(self.tr("演员"))
        # self.typeRadioButton = QCheckBox(self.tr("类型"))
        # self.areaRadioButton = QCheckBox(self.tr("地区"))
        choicelayout.addWidget(self.movieRadioButton)
        choicelayout.addWidget(self.dirRadioButton)
        choicelayout.addWidget(self.starRadioButton)
        choicelayout.addWidget(self.typeRadioButton)
        choicelayout.addWidget(self.areaRadioButton)
        choicelayout.addWidget(self.details)

        self.searchcontent = QTextEdit()    # 输出的内容
        self.searchcontent.setReadOnly(True)

        likelayout = QHBoxLayout()
        self.addPushButton = QPushButton(self.tr("添加至收藏夹"))
        likelayout.addWidget(self.addPushButton)
        likelayout.addStretch()
        self.likePushButton = QPushButton(self.tr("猜我喜欢"))
        likelayout.addWidget(self.likePushButton)

        mainlayout.addWidget(startlabel)
        mainlayout.addLayout(handlelayout)
        mainlayout.addLayout(searchlayout)
        mainlayout.addLayout(choicelayout)
        mainlayout.addWidget(self.searchcontent)
        mainlayout.addLayout(likelayout)

        # 这里想办法解决，，，
        self.connect(self.loginPushButton,SIGNAL("clicked()"),self.Login)   # 有没有方法可以一起写两个的,带参数的。。。
        self.connect(self.registerPushButton, SIGNAL("clicked()"),self.Register)
        self.connect(searchPushButton,SIGNAL("clicked()"),self.search)
        self.connect(self.likePushButton,SIGNAL("clicked()"),self.guessLike)
        self.connect(self.addPushButton,SIGNAL("clicked()"),self.addToFavor)
        self.likePushButton.setEnabled(False)   # 不登录和注册就没有“猜我喜欢”和“添加至收藏夹”这个按钮
        self.likePushButton.setVisible(False)   # 其实加这个就可以了
        self.addPushButton.setVisible(False)

        self.captchvalue = ''
        self.setLayout(mainlayout)

    def Login(self):
        global User
        LoginInput = InputDlg()
        LoginInput.setWindowTitle(self.tr("登录窗口"))
        LoginInput.captchalabel.setVisible(False)
        LoginInput.captchaLineEdit.setVisible(False)
        LoginInput.captchvaluelabel.setVisible(False)
        LoginInput.exec_()       # 运行

        # 运行结束后
        # global LoginSuccessFlag    # 写了就错了
        if LoginSuccessFlag:
            self.userlabel.setText(self.tr("用户名:"))
            self.loginPushButton.setText(self.tr(username))
            self.loginPushButton.setEnabled(False)            # 设置为不可按
            self.registerPushButton.setText(self.tr("退出"))
            self.likePushButton.setEnabled(True)  # 登录和注册就有“猜我喜欢”这个按钮
            self.likePushButton.setVisible(True)
            self.addPushButton.setVisible(True)

            User = Recomments.NewRecommend()  #
            User.load(cursor, username)

    def Register(self):
        global RegisterFlag
        global LoginSuccessFlag
        global User
        content = self.registerPushButton.text()
        if content == self.tr("注册"):
            RegisterFlag = True
            RegisterInput = InputDlg()   # 实例化对话框
            RegisterInput.setWindowTitle(self.tr("注册窗口"))
            RegisterInput.exec_()
            RegisterFlag = False   # 去掉注册标记

            if LoginSuccessFlag:
                self.userlabel.setText(self.tr("用户名:"))
                self.loginPushButton.setText(self.tr(username))
                self.loginPushButton.setEnabled(False)  # 设置为不可按
                self.registerPushButton.setText(self.tr("退出"))
                self.likePushButton.setEnabled(True)  # 登录和注册就有“猜我喜欢”和“添加至收藏夹”这个按钮
                self.likePushButton.setVisible(True)
                self.addPushButton.setVisible(True)
                ## line to mysql...
                # RegisterInput.userLineEdit.text()
                # RegisterInput.passwordLineEdit.text()
                User = Recomments.NewRecommend()
                User.load(cursor,username)
                sql = "alter table moviesforusers add %s int not null default 0"
                cursor.execute(sql % username)
                con_sql.commit()

        elif content == self.tr('退出'):
            LoginSuccessFlag = False
            self.userlabel.setText(self.tr(""))
            self.loginPushButton.setText(self.tr("登录"))
            self.loginPushButton.setEnabled(True)
            self.registerPushButton.setText(self.tr("注册"))
            self.likePushButton.setEnabled(False)  # 不登录和注册就没有“猜我喜欢”和“添加至收藏夹”这个按钮
            self.likePushButton.setVisible(False)
            self.addPushButton.setVisible(False)    # 添加至收藏夹
            User.save(cursor, username, con_sql)
            con_sql.commit()
            User = ''
            self.searchLineEdit.setText("")
            self.movieRadioButton.setChecked(False)
            self.dirRadioButton.setChecked(False)
            self.starRadioButton.setChecked(False)
            self.typeRadioButton.setChecked(False)
            self.areaRadioButton.setChecked(False)
            self.details.setChecked(False)
            self.searchcontent.setText("")

    def search(self):
        # 电影
        if self.movieRadioButton.isChecked():  # 被选中。。。
            if not self.details.isChecked():
                content = ''
                if self.searchLineEdit.text():
                    sql = "select * from system_douban where name like '%%%%%s%%%%'"
                    cursor.execute(sql % str(self.searchLineEdit.text()))
                    res = cursor.fetchall()
                    for rs in res:
                        content += rs['name'] + '\n'
                self.searchcontent.setText(content)
            # 详情，认为看过。。。
            else:
                sql = "select * from system_douban where name='%s'"
                cursor.execute(sql % str(self.searchLineEdit.text()))
                res = cursor.fetchone()              # 字典
                content = ''
                if res:
                    for rs in res:
                        if rs != 'name':
                            content += rs + ':' + '\n' + res[rs] + '\n'
                    if LoginSuccessFlag:    # 如果登录的话，就添加到用户的看过的电影中
                        if res not in User.watched:
                            User.watched.append(res)
                            User.learn([[res['diretor']],res['star'].split(','),res['type'].split(','),res['area'].split('/')])
                            User.save(cursor,username,con_sql)
                            User.load(cursor,username)
                            # add to moviesforusers....
                            # sql = "alter table moviesforusers add %s int not null default 0"
                            # cursor.execute(sql % username)
                            sql = "update moviesforusers set %s=1 where movie='%s'"   # 1表示已经看过
                            cursor.execute(sql % (username,res['name']))
                            con_sql.commit()
                else:
                    content = self.tr("没有找到相关的信息...")
                self.searchcontent.setText(content)
        # 导演
        elif self.dirRadioButton.isChecked():
            if not self.details.isChecked():
                content = ''
                if self.searchLineEdit.text():
                    sql = "select * from system_douban where diretor like '%%%%%s%%%%'"
                    cursor.execute(sql % str(self.searchLineEdit.text()))
                    res = cursor.fetchall()
                    NorepeatList = []
                    for rs in res:
                        if rs['diretor'] not in NorepeatList:
                            content += rs['diretor'] + '\n'
                            NorepeatList.append(rs['diretor'])
                self.searchcontent.setText(content)
            else:
                sql = "select * from system_douban where diretor='%s'"
                cursor.execute(sql % str(self.searchLineEdit.text()))
                res = cursor.fetchall()
                content = ''
                if res:
                    res = sorted(res, key=lambda x: float(x['score']), reverse=True)[:100]  # 输出50部电影
                    N = 1
                    for rs in res:
                        content += str(N) + ':' + rs['name'] + '\n'
                        N += 1
                else:
                    content = self.tr("没有找到相关的信息...")
                self.searchcontent.setText(content)
        # 演员
        elif self.starRadioButton.isChecked():
            content = ''
            res = []
            NorepeatList = []
            if self.searchLineEdit.text():
                for ai in allinfors:
                    starlist = ai['star'].split(',')
                    for sl in starlist:
                        if str(self.searchLineEdit.text()) in sl:
                            if sl not in NorepeatList:
                                content += sl + '\n'
                                NorepeatList.append(sl)
                            if str(self.searchLineEdit.text()) == sl:
                                res.append(ai)
            if not self.details.isChecked():
                self.searchcontent.setText(content)
            else:
                content = ''
                if res:
                    res = sorted(res,key=lambda x: float(x['score']),reverse=True)[:100]
                    N = 1
                    for rs in res:
                        content += str(N) + ':' + rs['name'] + '\n'
                        N += 1
                else:
                    content = self.tr("没有找到相关的信息...")
                self.searchcontent.setText(content)
        # 类型
        elif self.typeRadioButton.isChecked():
            content = ''
            sql = "select * from system_type where movie_type='%s'"
            cursor.execute(sql % str(self.searchLineEdit.text()))
            res = cursor.fetchall()
            if res:
                res = sorted(res, key=lambda x: float(x['score']), reverse=True)[:100]
                N = 1
                for rs in res:
                    content += str(N) + ':' + rs['name'] + '\n'
                    N += 1
            else:
                sql = "select * from system_type"
                cursor.execute(sql)
                res = cursor.fetchall()
                content = self.tr("没有找到相关的信息...\n请输入以下类型...\n")
                typelist = []
                for rs in res:
                    if rs['movie_type'] not in typelist:
                        typelist.append(rs['movie_type'])
                N = 1
                for ll in typelist:
                    content += str(N) + ':' + ll + '\n'
                    N += 1
            self.searchcontent.setText(content)
        # 地区
        elif self.areaRadioButton.isChecked():
            content = ''
            sql = "select * from system_zone where zone_name='%s'"
            cursor.execute(sql % str(self.searchLineEdit.text()))
            res = cursor.fetchall()
            if res:
                res = sorted(res, key=lambda x: float(x['score']), reverse=True)[:100]
                N = 1
                for rs in res:
                    content += str(N) + ':' + rs['name'] + '\n'
                    N += 1
            else:
                sql = "select * from system_zone"
                cursor.execute(sql)
                res = cursor.fetchall()
                content = self.tr("没有找到相关的信息...\n请输入以下类型...\n")
                zonelist = []
                for rs in res:
                    if rs['zone_name'] not in zonelist:
                        zonelist.append(rs['zone_name'])
                N = 1
                for ll in zonelist:
                    content += str(N) + ':' + ll + '\n'
                    N += 1
            self.searchcontent.setText(content)

        else:
            QMessageBox.information(self,self.tr("错误"),self.tr("请选择一个属性！"))

    # 最后一个按钮实现了，，，现在2:40了，，莹仔晚安~~~
    def guessLike(self):
        # link to mysql...
        Like = RecommendForYou()
        # content = ''
        # if User:
        #     rs = User.GetRecommendResult(allinfors)
        #     N = 1
        #     for r in rs:
        #         content += str(N) + ':' + r['name'] + '\n'
        #         N += 1
        # Like.moviecontent.setText(self.tr(content))   # 在这里设置推荐的内容
        Like.exec_()

    def addToFavor(self):
        moviename,ok = QInputDialog.getText(self,self.tr("添加至收藏夹..."),self.tr("输入电影名字："),QLineEdit.Normal)
        if ok and (not moviename.isEmpty()):
            # add to favorite...
            # favorite.LineEdit1.setText(moviename)
            if favorite.LineEditList[9].text() == '':
                for ll in favorite.LineEditList:
                    if ll.text() == moviename:
                        QMessageBox.information(self, self.tr("提醒"), self.tr("已在收藏夹了！"))
                        break
                    if ll.text() == '':
                        ll.setText(moviename)
                        favorite.Favorites.append(moviename)
                        break
            else:
                QMessageBox.information(self,self.tr("错误"),self.tr("收藏夹已满！"))
            pass

    def getVal(self):
        self.captchvalue = str(randint(1000, 9999))
        return self.captchvalue


class BasicInfo(QWidget):

    def __init__(self,parent=None):
        super(BasicInfo,self).__init__(parent)

        uplayout = QGridLayout()  # 使用网格布局
        userlabel = QLabel(self.tr("用户名:"))
        self.userlineedit = QLineEdit(self.tr("莹仔"))
        self.userlineedit.setEnabled(False)           ##
        namelabel = QLabel(self.tr("  姓名:"))
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setEnabled(False)            ##
        sexlabel = QLabel(self.tr("  性别:"))
        self.sexComboBox = QComboBox()
        self.sexComboBox.insertItem(0, self.tr("女"))
        self.sexComboBox.insertItem(1, self.tr("男"))
        self.sexComboBox.insertItem(2, self.tr("保密"))
        self.sexComboBox.setEnabled(False)             ##
        headlabel = QLabel(self.tr("头像:"))
        self.headImglabel = QLabel()
        self.headImglabel.setPixmap(QPixmap("C:/Users/asus-pc/Desktop/yz.jpg").scaled(60, 60))  # 这里要改下图片的路径
        self.changePushButton = QPushButton(self.tr("更改"))
        self.changePushButton.setEnabled(False)       ##
        birthdaylabel = QLabel(self.tr("生日:"))
        self.birthday = QDateTimeEdit()
        self.birthday.setDateTime(QDateTime(1996, 10, 5, 0, 0))   # 初始化
        self.birthday.setDisplayFormat("yyyy/MM/dd")              # 竟然是大写的M   噗噗噗
        self.birthday.setCalendarPopup(True)
        self.birthday.setEnabled(False)          ##

        uplayout.addWidget(userlabel, 0, 0)
        uplayout.addWidget(self.userlineedit, 0, 1)
        uplayout.addWidget(namelabel, 1, 0)
        uplayout.addWidget(self.nameLineEdit, 1, 1)
        uplayout.addWidget(sexlabel, 2, 0)
        uplayout.addWidget(self.sexComboBox, 2, 1)
        uplayout.addWidget(headlabel, 0, 2)
        uplayout.addWidget(self.headImglabel, 0, 3, 2, 2)
        uplayout.addWidget(self.changePushButton, 1, 4)
        uplayout.addWidget(birthdaylabel, 2, 2)
        uplayout.addWidget(self.birthday,2,3)

        personlabel = QLabel(self.tr("个人说明:"))
        self.personTextEdit = QTextEdit()
        self.personTextEdit.setEnabled(False)      ##
        # uplayout.setSpacing(20)
        bottomlayout = QHBoxLayout()
        bottomlayout.addStretch()
        self.amendPushButton = QPushButton(self.tr("修改"))
        bottomlayout.addWidget(self.amendPushButton)

        self.connect(self.changePushButton, SIGNAL("clicked()"), self.changeImg)
        self.connect(self.amendPushButton, SIGNAL("clicked()"), self.info)

        allLayout = QVBoxLayout()
        allLayout.addLayout(uplayout)
        allLayout.addWidget(personlabel)
        allLayout.addWidget(self.personTextEdit)
        allLayout.addLayout(bottomlayout)
        self.setLayout(allLayout)

    def changeImg(self):
        s = QFileDialog.getOpenFileName(self, "Open Picture...", "C:/", "(*.jpg);;(*.png);;(*.jpeg)")
        if s:
            self.headImglabel.setPixmap(QPixmap(self.tr(str(s))).scaled(60, 60))

    def info(self):
        text = self.amendPushButton.text()
        if text == self.tr('修改'):
            self.amendPushButton.setText(self.tr("确定"))
            self.userlineedit.setEnabled(True)
            self.nameLineEdit.setEnabled(True)
            self.sexComboBox.setEnabled(True)
            self.changePushButton.setEnabled(True)
            self.birthday.setEnabled(True)
            self.personTextEdit.setEnabled(True)
        elif text == self.tr("确定"):
            self.amendPushButton.setText(self.tr("修改"))
            self.userlineedit.setEnabled(False)
            self.nameLineEdit.setEnabled(False)
            self.sexComboBox.setEnabled(False)
            self.changePushButton.setEnabled(False)
            self.birthday.setEnabled(False)
            self.personTextEdit.setEnabled(False)


class Favorite(QWidget):

    def __init__(self,parent=None):
        super(Favorite,self).__init__(parent)
        self.Favorites = []  #[u"莹仔",u"我爱你"]

        startlabel = QLabel(self.tr("我收藏的电影"))
        startlabel.setFont(QFont(self.tr("宋体"), 12))
        # startlabel.setAlignment(Qt.AlignHCenter)  # 文字水平居中

        self.checkbox1 = QCheckBox();self.checkbox2 = QCheckBox()
        self.checkbox3 = QCheckBox();self.checkbox4 = QCheckBox()
        self.checkbox5 = QCheckBox();self.checkbox6 = QCheckBox()
        self.checkbox7 = QCheckBox();self.checkbox8 = QCheckBox()
        self.checkbox9 = QCheckBox();self.checkbox10 = QCheckBox()

        self.LineEdit1 = QLineEdit();self.LineEdit2 = QLineEdit()
        self.LineEdit3 = QLineEdit();self.LineEdit4 = QLineEdit()
        self.LineEdit5 = QLineEdit();self.LineEdit6 = QLineEdit()
        self.LineEdit7 = QLineEdit();self.LineEdit8 = QLineEdit()
        self.LineEdit9 = QLineEdit();self.LineEdit10 = QLineEdit()

        self.LineEdit1.setReadOnly(True);self.LineEdit2.setReadOnly(True)
        self.LineEdit3.setReadOnly(True);self.LineEdit4.setReadOnly(True)
        self.LineEdit5.setReadOnly(True);self.LineEdit6.setReadOnly(True)
        self.LineEdit7.setReadOnly(True);self.LineEdit8.setReadOnly(True)
        self.LineEdit9.setReadOnly(True);self.LineEdit10.setReadOnly(True)

        uplayout = QGridLayout()
        uplayout.addWidget(self.checkbox1,0,0);uplayout.addWidget(self.checkbox2,1,0)
        uplayout.addWidget(self.checkbox3,2,0);uplayout.addWidget(self.checkbox4,3,0)
        uplayout.addWidget(self.checkbox5,4,0);uplayout.addWidget(self.checkbox6,5,0)
        uplayout.addWidget(self.checkbox7,6,0);uplayout.addWidget(self.checkbox8,7,0)
        uplayout.addWidget(self.checkbox9,8,0);uplayout.addWidget(self.checkbox10,9,0)
        uplayout.addWidget(self.LineEdit1,0,1);uplayout.addWidget(self.LineEdit2, 1, 1)
        uplayout.addWidget(self.LineEdit3, 2, 1);uplayout.addWidget(self.LineEdit4, 3, 1)
        uplayout.addWidget(self.LineEdit5, 4, 1);uplayout.addWidget(self.LineEdit6, 5, 1)
        uplayout.addWidget(self.LineEdit7, 6, 1);uplayout.addWidget(self.LineEdit8, 7, 1)
        uplayout.addWidget(self.LineEdit9, 8, 1);uplayout.addWidget(self.LineEdit10, 9, 1)
        spacer = QSpacerItem(75, 15)
        uplayout.addItem(spacer, 9, 2)

        bottomlayout = QHBoxLayout()
        self.editPushButton = QPushButton(self.tr("编辑"))
        self.deletePushButton = QPushButton(self.tr("删除"))
        bottomlayout.addWidget(self.editPushButton)
        bottomlayout.addStretch()
        bottomlayout.addWidget(self.deletePushButton)


        mainlayout = QVBoxLayout()
        mainlayout.addWidget(startlabel)
        mainlayout.addLayout(uplayout)
        mainlayout.addLayout(bottomlayout)
        mainlayout.setSpacing(15)

        self.checkbox1.setVisible(False);self.checkbox2.setVisible(False)
        self.checkbox3.setVisible(False);self.checkbox4.setVisible(False)
        self.checkbox5.setVisible(False);self.checkbox6.setVisible(False)
        self.checkbox7.setVisible(False);self.checkbox8.setVisible(False)
        self.checkbox9.setVisible(False);self.checkbox10.setVisible(False)

        # self.LineEdit1.setVisible(False);self.LineEdit2.setVisible(False)
        # self.LineEdit3.setVisible(False);self.LineEdit4.setVisible(False)
        # self.LineEdit5.setVisible(False);self.LineEdit6.setVisible(False)
        # self.LineEdit7.setVisible(False);self.LineEdit8.setVisible(False)
        # self.LineEdit9.setVisible(False);self.LineEdit10.setVisible(False)
        # self.editPushButton.setVisible(False);self.deletePushButton.setVisible(False)
        self.checkboxdict = {
            self.checkbox1: self.LineEdit1,self.checkbox2: self.LineEdit2,
            self.checkbox3: self.LineEdit3,self.checkbox4: self.LineEdit4,
            self.checkbox5: self.LineEdit5,self.checkbox6: self.LineEdit6,
            self.checkbox7: self.LineEdit7,self.checkbox8: self.LineEdit8,
            self.checkbox9: self.LineEdit9,self.checkbox10:self.LineEdit10
        }
        self.LineEditList = [
            self.LineEdit1,self.LineEdit2,
            self.LineEdit3,self.LineEdit4,
            self.LineEdit5,self.LineEdit6,
            self.LineEdit7,self.LineEdit8,
            self.LineEdit9,self.LineEdit10
        ]
        self.Update()

        self.connect(self.editPushButton,SIGNAL("clicked()"),self.modify)
        self.connect(self.deletePushButton,SIGNAL("clicked()"),self.delete)
        self.setLayout(mainlayout)

    def modify(self):
        content = self.editPushButton.text()
        if content == self.tr("编辑"):
            self.editPushButton.setText(self.tr("取消"))
            self.checkbox1.setVisible(True);self.checkbox2.setVisible(True)     # 设置可见
            self.checkbox3.setVisible(True);self.checkbox4.setVisible(True)
            self.checkbox5.setVisible(True);self.checkbox6.setVisible(True)
            self.checkbox7.setVisible(True);self.checkbox8.setVisible(True)
            self.checkbox9.setVisible(True);self.checkbox10.setVisible(True)

        elif content == self.tr("取消"):
            self.editPushButton.setText(self.tr("编辑"))
            self.checkbox1.setVisible(False);self.checkbox2.setVisible(False)     # 设置不可见
            self.checkbox3.setVisible(False);self.checkbox4.setVisible(False)
            self.checkbox5.setVisible(False);self.checkbox6.setVisible(False)
            self.checkbox7.setVisible(False);self.checkbox8.setVisible(False)
            self.checkbox9.setVisible(False);self.checkbox10.setVisible(False)

            self.checkbox1.setChecked(False);self.checkbox2.setChecked(False)      # 把打钩的去掉
            self.checkbox3.setChecked(False);self.checkbox4.setChecked(False)
            self.checkbox5.setChecked(False);self.checkbox6.setChecked(False)
            self.checkbox7.setChecked(False);self.checkbox8.setChecked(False)
            self.checkbox9.setChecked(False);self.checkbox10.setChecked(False)


    def delete(self):

        for cbn in self.checkboxdict:
            if cbn.isChecked():
                if self.checkboxdict[cbn].text() != '':
                    self.Favorites.remove(str(self.checkboxdict[cbn].text()))
                    self.checkboxdict[cbn].setText("")
                cbn.setChecked(False)
        self.update()

    def Update(self):
        for n in range(10):
            if n < len(self.Favorites):
                self.LineEditList[n].setText(self.tr(self.Favorites[n]))
            else:
                self.LineEditList[n].setText("")


class InputDlg(QDialog):

    def __init__(self,parent=None):
        super(InputDlg,self).__init__(parent)

        userlabel = QLabel(self.tr("用户名:"))
        self.userLineEdit = QLineEdit()
        passwordlabel = QLabel(self.tr("  密码:"))
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)    # 设置密码显示模式 setEchoMode
        self.captchalabel = QLabel(self.tr("验证码:"))
        self.captchaLineEdit = QLineEdit()
        self.captchvaluelabel = QLabel()
        self.captch = MainPage().getVal()               # 验证码获取
        self.captchvaluelabel.setText(self.tr(self.captch))

        # 给控件设置颜色
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.blue)
        self.captchvaluelabel.setPalette(pe)

        self.okPushButton = QPushButton("ok")
        cancelPushButton = QPushButton("cancel")

        uplayout = QGridLayout()
        uplayout.addWidget(userlabel,0,0)
        uplayout.addWidget(self.userLineEdit,0,1)
        uplayout.addWidget(passwordlabel,1,0)
        uplayout.addWidget(self.passwordLineEdit,1,1)
        uplayout.addWidget(self.captchalabel,2,0)
        uplayout.addWidget(self.captchaLineEdit,2,1)
        uplayout.addWidget(self.captchvaluelabel,2,2)
        spacer = QSpacerItem(10,40)
        uplayout.addItem(spacer,2,3)

        bottomlayout = QHBoxLayout()
        bottomlayout.addStretch()
        bottomlayout.addWidget(self.okPushButton)
        bottomlayout.addWidget(cancelPushButton)

        mainlayout = QVBoxLayout()
        mainlayout.addLayout(uplayout)
        mainlayout.addLayout(bottomlayout)

        self.connect(cancelPushButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(self.okPushButton,SIGNAL("clicked()"),self.ok)
        mainlayout.setSizeConstraint(QLayout.SetFixedSize)   # 固定大小
        self.setLayout(mainlayout)

    def ok(self):
        global username
        global LoginSuccessFlag
        usercontent = str(self.userLineEdit.text())    # 这里要转成str 不然就是QString了
        passwordcontent = str(self.passwordLineEdit.text())
        captchcontent = str(self.captchaLineEdit.text())

        if usercontent == '':
            content = self.tr("用户名为空！")
            if passwordcontent == '':
                content += self.tr("\n密码为空！")
                # 如果是注册的话
                if RegisterFlag:
                    if captchcontent == '':
                        content += self.tr("\n验证码为空！")
            else:
                content = self.tr("请输入用户名！")
            QMessageBox.information(self,self.tr("错误"),content)
        else:
            sql = "select * from system_LoginOrRegister where username = '%s'"
            cursor.execute(sql % usercontent)
            record = cursor.fetchone()

            # 登录
            if not RegisterFlag:
                if not record:
                    content = self.tr("用户名不存在！")
                    QMessageBox.information(self, self.tr("错误"), content)
                else:
                    if passwordcontent == '':
                        content = self.tr("密码为空！")
                        QMessageBox.information(self, self.tr("错误"), content)
                    else:
                        if record['password'] != passwordcontent:
                            content = self.tr("密码错误！")
                            QMessageBox.information(self, self.tr("错误"), content)
                        else: # 登录成功
                            username = usercontent  # 得到用户名  声明为global 这个真的很厉害
                            LoginSuccessFlag = True
                            self.close()  # 关闭窗口
            # 注册
            else:
                # 用户名已存在。。。
                if record:
                    content = self.tr("用户名已存在！")
                    QMessageBox.information(self, self.tr("错误"), content)
                else:
                    if passwordcontent == '':
                        content = self.tr("密码为空！")
                        if captchcontent == '':
                            content += self.tr("\n验证码为空！")
                        QMessageBox.information(self, self.tr("错误"), content)
                    else:
                        if len(passwordcontent) != 6:
                            content = self.tr("密码应该设置为6位！")
                            QMessageBox.information(self, self.tr("错误"), content)
                        else:
                            if self.captch != captchcontent:
                                if captchcontent == '':
                                    content = self.tr("验证码为空！")
                                else:
                                    content = self.tr("验证码错误！")
                                    self.captch = MainPage().getVal()
                                    self.captchvaluelabel.setText(self.tr(self.captch))  # 更新验证码
                                QMessageBox.information(self, self.tr("错误"), content)
                            else:  # 注册成功
                                sql = "insert into system_LoginOrRegister(username,password,RegisterTime) values('%s','%s','%s')"
                                cursor.execute(sql % (usercontent,passwordcontent,time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))))
                                con_sql.commit()
                                # 存放标签
                                sql = "create table if not exists %s_lables(lable varchar(100),times bigint,save_time bigint," \
                                      "type varchar(100),primary key(lable,times,save_time,type))"
                                cursor.execute(sql % usercontent)
                                con_sql.commit()
                                # 存放看过的电影
                                sql = "create table if not exists %s_watched(name varchar(255),diretor varchar(255)," \
                                      "star varchar(1000),score varchar(100),runtime varchar(100),date varchar(100)," \
                                      "area varchar(255),type varchar(255),url varchar(100)," \
                                      "primary key(name))"
                                cursor.execute(sql % usercontent)
                                con_sql.commit()
                                ###  还有存放个人信息的。。。
                                username = usercontent  # 得到用户名  声明为global 这个真的很厉害
                                LoginSuccessFlag = True
                                self.close()  # 关闭窗口
            con_sql.commit()


class RecommendForYou(QDialog):

    def __init__(self,parent=None):
        super(RecommendForYou,self).__init__(parent)
        self.setWindowTitle(self.tr("仅供学术交流~"))
        self.resize(400,350)

        startlabel = QLabel(self.tr("为你推荐..."))
        startlabel.setFont(QFont(self.tr("宋体"), 15))
        startlabel.setAlignment(Qt.AlignHCenter)  # 文字水平居中

        self.moviecontent = QTextEdit()
        # self.moviecontent.setText("")
        goodsPushButton = QPushButton(self.tr("基于物品推荐"))
        consumerPushButton = QPushButton(self.tr("基于用户推荐"))
        okPushButton = QPushButton("ok")

        middlelayout = QHBoxLayout()
        middlelayout.addWidget(goodsPushButton)
        middlelayout.addStretch()
        middlelayout.addWidget(consumerPushButton)
        bottomlayout = QHBoxLayout()
        bottomlayout.addStretch()
        bottomlayout.addWidget(okPushButton)

        mainlayout = QVBoxLayout()
        mainlayout.addWidget(startlabel)
        mainlayout.addWidget(self.moviecontent)
        mainlayout.addLayout(middlelayout)
        mainlayout.addLayout(bottomlayout)

        self.moviecontent.setReadOnly(True)
        self.connect(okPushButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(goodsPushButton,SIGNAL("clicked()"),self.goods)
        self.connect(consumerPushButton,SIGNAL("clicked()"),self.consumer)
        mainlayout.setSizeConstraint(QLayout.SetFixedSize)     # 固定窗口大小
        self.setLayout(mainlayout)

    def goods(self):
        content = ''
        if User:
            rs = User.GetRecommendResult(allinfors)
            N = 1
            for r in rs:
                content += str(N) + ':' + r['name'] + '\n'
                N += 1
        self.moviecontent.setText(self.tr(content))   # 在这里设置推荐的内容

    def consumer(self):
        sql = "select * from moviesforusers where %s=1"
        cursor.execute(sql % username)
        infors = cursor.fetchall()

        res = dict()
        for fs in infors:
            for key in fs:
                if key != 'movie' and key != username:  # 除掉Movie和当前用户
                    if key in res:
                        res[key] += fs[key]
                    else:
                        res[key] = fs[key]

        res_name = sorted(res,lambda e: res[e],reverse=True)[:5]    # 选出重复次数最多的5个人
        sql = "select movie from moviesforusers where %s=1 and %s=0"
        movie_list = []       #  待推荐的电影
        for rn in res_name:    # rn是用户名
            cursor.execute(sql % (rn,username))
            dictformovie = cursor.fetchall()
            for dm in dictformovie:
                if dm['movie'] not in movie_list:
                    movie_list.append(dm['movie'])
        # 推荐Movie_list中评分最高的10部电影
        sql = "select score from system_douban where name='%s'"
        res = dict()
        for ml in movie_list:
            cursor.execute(sql % ml)
            score = cursor.fetchone().get('score')
            res[ml] = score

        res = sorted(res,key=lambda e: res[e],reverse=True)[:10]
        N = 1
        content = ''
        for rs in res:
            content += str(N) + ':' + rs + '\n'
            N += 1
        self.moviecontent.setText(content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = StackWidget()
    main.show()
    app.exec_()
    cursor.close()
    con_sql.close()


from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap
from ui_captha import Ui_captcha

class CaptchaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_captcha()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowType.Dialog)

        self.one_image = QPixmap("icons/1.png")
        self.one_image = self.one_image.scaled(QSize(150,150))
        self.two_image = QPixmap("icons/2.png")
        self.two_image = self.two_image.scaled(QSize(150,150))
        self.three_image = QPixmap("icons/4.png")
        self.three_image = self.three_image.scaled(QSize(150,150))
        self.fourth_image = QPixmap("icons/3.png")
        self.fourth_image = self.fourth_image.scaled(QSize(150,150))

        if self.one_image.isNull():
            print("Failed to load image: :/icons/1.png")

        self.ui.next_button.clicked.connect(self.nextClicked)
        self.set_i = 1
        self.setImage()
        
        self.curr_try = 1

    def nextClicked(self):
        self.nextSet()
        self.setImage()

    def setImage(self):
        if self.set_i == 0:
            self.ui.one.setPixmap(self.one_image)
            self.ui.two.setPixmap(self.two_image)
            self.ui.three.setPixmap(self.three_image)
            self.ui.fourth.setPixmap(self.fourth_image)
        elif self.set_i == 1:
            self.ui.two.setPixmap(self.one_image)
            self.ui.three.setPixmap(self.two_image)
            self.ui.fourth.setPixmap(self.three_image)
            self.ui.one.setPixmap(self.fourth_image)
        elif self.set_i == 2:
            self.ui.three.setPixmap(self.one_image)
            self.ui.fourth.setPixmap(self.two_image)
            self.ui.one.setPixmap(self.three_image)
            self.ui.two.setPixmap(self.fourth_image)
        elif self.set_i == 3:
            self.ui.fourth.setPixmap(self.one_image)
            self.ui.one.setPixmap(self.two_image)
            self.ui.two.setPixmap(self.three_image)
            self.ui.three.setPixmap(self.fourth_image)

    def nextSet(self):
        self.set_i = (self.set_i + 1) % 4

    def isRight(self):
        if self.set_i == 0:
            return True
        return False

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'captha.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_captcha(object):
    def setupUi(self, captcha):
        if not captcha.objectName():
            captcha.setObjectName(u"captcha")
        captcha.resize(318, 359)
        self.widget = QWidget(captcha)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 301, 341))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.one = QLabel(self.widget)
        self.one.setObjectName(u"one")
        self.one.setMinimumSize(QSize(150, 150))
        self.one.setMaximumSize(QSize(150, 150))
        self.one.setScaledContents(True)

        self.gridLayout.addWidget(self.one, 0, 0, 1, 1)

        self.two = QLabel(self.widget)
        self.two.setObjectName(u"two")
        self.two.setMinimumSize(QSize(150, 150))
        self.two.setMaximumSize(QSize(150, 150))
        self.two.setScaledContents(True)

        self.gridLayout.addWidget(self.two, 0, 1, 1, 1)

        self.fourth = QLabel(self.widget)
        self.fourth.setObjectName(u"fourth")
        self.fourth.setMinimumSize(QSize(150, 150))
        self.fourth.setMaximumSize(QSize(150, 150))
        self.fourth.setScaledContents(True)

        self.gridLayout.addWidget(self.fourth, 1, 0, 1, 1)

        self.three = QLabel(self.widget)
        self.three.setObjectName(u"three")
        self.three.setMinimumSize(QSize(150, 150))
        self.three.setMaximumSize(QSize(150, 150))
        self.three.setScaledContents(True)

        self.gridLayout.addWidget(self.three, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.next_button = QPushButton(self.widget)
        self.next_button.setObjectName(u"next_button")

        self.verticalLayout.addWidget(self.next_button)

        self.buttonBox = QDialogButtonBox(self.widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(captcha)
        self.buttonBox.accepted.connect(captcha.accept)
        self.buttonBox.rejected.connect(captcha.reject)

        QMetaObject.connectSlotsByName(captcha)
    # setupUi

    def retranslateUi(self, captcha):
        captcha.setWindowTitle(QCoreApplication.translate("captcha", u"Dialog", None))
        self.one.setText(QCoreApplication.translate("captcha", u"one", None))
        self.two.setText(QCoreApplication.translate("captcha", u"two", None))
        self.fourth.setText(QCoreApplication.translate("captcha", u"fourth", None))
        self.three.setText(QCoreApplication.translate("captcha", u"three", None))
        self.next_button.setText(QCoreApplication.translate("captcha", u"\u0421\u043b\u0435\u0434\u0443\u044e\u0438\u0449\u0439", None))
    # retranslateUi


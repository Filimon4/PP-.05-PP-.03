# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_customer.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_add_customer(object):
    def setupUi(self, add_customer):
        if not add_customer.objectName():
            add_customer.setObjectName(u"add_customer")
        add_customer.resize(618, 471)
        self.layoutWidget = QWidget(add_customer)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 601, 451))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(self.layoutWidget)
        self.title.setObjectName(u"title")

        self.verticalLayout.addWidget(self.title)

        self.line = QFrame(self.layoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.name = QLineEdit(self.layoutWidget)
        self.name.setObjectName(u"name")

        self.horizontalLayout.addWidget(self.name)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.inn = QLineEdit(self.layoutWidget)
        self.inn.setObjectName(u"inn")

        self.horizontalLayout_2.addWidget(self.inn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.email = QLineEdit(self.layoutWidget)
        self.email.setObjectName(u"email")

        self.horizontalLayout_4.addWidget(self.email)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.phone = QLineEdit(self.layoutWidget)
        self.phone.setObjectName(u"phone")

        self.horizontalLayout_5.addWidget(self.phone)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.address = QLineEdit(self.layoutWidget)
        self.address.setObjectName(u"address")

        self.horizontalLayout_6.addWidget(self.address)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.buyer_combo = QComboBox(self.layoutWidget)
        self.buyer_combo.addItem("")
        self.buyer_combo.addItem("")
        self.buyer_combo.setObjectName(u"buyer_combo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buyer_combo.sizePolicy().hasHeightForWidth())
        self.buyer_combo.setSizePolicy(sizePolicy)
        self.buyer_combo.setEditable(False)

        self.horizontalLayout_7.addWidget(self.buyer_combo)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_9 = QLabel(self.layoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_8.addWidget(self.label_9)

        self.salesman_combo = QComboBox(self.layoutWidget)
        self.salesman_combo.addItem("")
        self.salesman_combo.addItem("")
        self.salesman_combo.setObjectName(u"salesman_combo")
        sizePolicy.setHeightForWidth(self.salesman_combo.sizePolicy().hasHeightForWidth())
        self.salesman_combo.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.salesman_combo)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.line_2 = QFrame(self.layoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(add_customer)
        self.buttonBox.accepted.connect(add_customer.accept)
        self.buttonBox.rejected.connect(add_customer.reject)

        QMetaObject.connectSlotsByName(add_customer)
    # setupUi

    def retranslateUi(self, add_customer):
        add_customer.setWindowTitle(QCoreApplication.translate("add_customer", u"Dialog", None))
        self.title.setText(QCoreApplication.translate("add_customer", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u044f", None))
        self.label.setText(QCoreApplication.translate("add_customer", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.label_2.setText(QCoreApplication.translate("add_customer", u"\u0418\u041d\u041d", None))
        self.label_4.setText(QCoreApplication.translate("add_customer", u"\u041f\u043e\u0447\u0442\u0430", None))
        self.email.setInputMask("")
        self.label_5.setText(QCoreApplication.translate("add_customer", u"\u0422\u0435\u043b\u0435\u0444\u043e\u043d", None))
        self.phone.setInputMask(QCoreApplication.translate("add_customer", u"+9-999-999-99-99", None))
        self.label_6.setText(QCoreApplication.translate("add_customer", u"\u0410\u0434\u0440\u0435\u0441\u0441", None))
        self.label_7.setText(QCoreApplication.translate("add_customer", u"\u041f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u044c", None))
        self.buyer_combo.setItemText(0, QCoreApplication.translate("add_customer", u"\u0414\u0430", None))
        self.buyer_combo.setItemText(1, QCoreApplication.translate("add_customer", u"\u041d\u0435\u0442", None))

        self.buyer_combo.setCurrentText(QCoreApplication.translate("add_customer", u"\u0414\u0430", None))
        self.label_9.setText(QCoreApplication.translate("add_customer", u"\u041f\u0440\u043e\u0434\u0430\u0432\u0435\u0446", None))
        self.salesman_combo.setItemText(0, QCoreApplication.translate("add_customer", u"\u0414\u0430", None))
        self.salesman_combo.setItemText(1, QCoreApplication.translate("add_customer", u"\u041d\u0435\u0442", None))

    # retranslateUi


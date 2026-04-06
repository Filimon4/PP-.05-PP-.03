# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_employee.ui'
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

class Ui_add_employee(object):
    def setupUi(self, add_employee):
        if not add_employee.objectName():
            add_employee.setObjectName(u"add_employee")
        add_employee.resize(618, 471)
        self.layoutWidget = QWidget(add_employee)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 601, 451))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.layoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout.addWidget(self.label_8)

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

        self.first_name = QLineEdit(self.layoutWidget)
        self.first_name.setObjectName(u"first_name")

        self.horizontalLayout.addWidget(self.first_name)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.family_name = QLineEdit(self.layoutWidget)
        self.family_name.setObjectName(u"family_name")

        self.horizontalLayout_2.addWidget(self.family_name)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.last_name = QLineEdit(self.layoutWidget)
        self.last_name.setObjectName(u"last_name")

        self.horizontalLayout_3.addWidget(self.last_name)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

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

        self.position_combo = QComboBox(self.layoutWidget)
        self.position_combo.setObjectName(u"position_combo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.position_combo.sizePolicy().hasHeightForWidth())
        self.position_combo.setSizePolicy(sizePolicy)

        self.horizontalLayout_7.addWidget(self.position_combo)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_10 = QLabel(self.layoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_9.addWidget(self.label_10)

        self.login = QLineEdit(self.layoutWidget)
        self.login.setObjectName(u"login")

        self.horizontalLayout_9.addWidget(self.login)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_11 = QLabel(self.layoutWidget)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_10.addWidget(self.label_11)

        self.password = QLineEdit(self.layoutWidget)
        self.password.setObjectName(u"password")

        self.horizontalLayout_10.addWidget(self.password)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_9 = QLabel(self.layoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_8.addWidget(self.label_9)

        self.blocked_combo = QComboBox(self.layoutWidget)
        self.blocked_combo.addItem("")
        self.blocked_combo.addItem("")
        self.blocked_combo.setObjectName(u"blocked_combo")
        sizePolicy.setHeightForWidth(self.blocked_combo.sizePolicy().hasHeightForWidth())
        self.blocked_combo.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.blocked_combo)


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


        self.retranslateUi(add_employee)
        self.buttonBox.accepted.connect(add_employee.accept)
        self.buttonBox.rejected.connect(add_employee.reject)

        QMetaObject.connectSlotsByName(add_employee)
    # setupUi

    def retranslateUi(self, add_employee):
        add_employee.setWindowTitle(QCoreApplication.translate("add_employee", u"Dialog", None))
        self.label_8.setText(QCoreApplication.translate("add_employee", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0430", None))
        self.label.setText(QCoreApplication.translate("add_employee", u"\u0418\u043c\u044f", None))
        self.label_2.setText(QCoreApplication.translate("add_employee", u"\u0424\u0430\u043c\u0438\u043b\u0438\u044f", None))
        self.label_3.setText(QCoreApplication.translate("add_employee", u"\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.label_4.setText(QCoreApplication.translate("add_employee", u"\u041f\u043e\u0447\u0442\u0430", None))
        self.email.setInputMask("")
        self.label_5.setText(QCoreApplication.translate("add_employee", u"\u0422\u0435\u043b\u0435\u0444\u043e\u043d", None))
        self.phone.setInputMask(QCoreApplication.translate("add_employee", u"+9-999-999-99-99", None))
        self.label_6.setText(QCoreApplication.translate("add_employee", u"\u0410\u0434\u0440\u0435\u0441\u0441", None))
        self.label_7.setText(QCoreApplication.translate("add_employee", u"\u041f\u043e\u0437\u0438\u0446\u0438\u044f", None))
        self.label_10.setText(QCoreApplication.translate("add_employee", u"\u041b\u043e\u0433\u0438\u043d", None))
        self.login.setInputMask("")
        self.label_11.setText(QCoreApplication.translate("add_employee", u"\u041f\u0430\u0440\u043e\u043b\u044c", None))
        self.password.setInputMask("")
        self.label_9.setText(QCoreApplication.translate("add_employee", u"\u0417\u0430\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u0430\u043d", None))
        self.blocked_combo.setItemText(0, QCoreApplication.translate("add_employee", u"\u0414\u0430", None))
        self.blocked_combo.setItemText(1, QCoreApplication.translate("add_employee", u"\u041d\u0435\u0442", None))

    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bill_of_material.ui'
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
    QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_bill_of_material(object):
    def setupUi(self, bill_of_material):
        if not bill_of_material.objectName():
            bill_of_material.setObjectName(u"bill_of_material")
        bill_of_material.resize(420, 160)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(bill_of_material.sizePolicy().hasHeightForWidth())
        bill_of_material.setSizePolicy(sizePolicy)
        bill_of_material.setMinimumSize(QSize(420, 160))
        bill_of_material.setMaximumSize(QSize(420, 160))
        bill_of_material.setAutoFillBackground(False)
        self.layoutWidget = QWidget(bill_of_material)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 401, 144))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.quantity = QLineEdit(self.layoutWidget)
        self.quantity.setObjectName(u"quantity")
        self.quantity.setAutoFillBackground(False)

        self.horizontalLayout_3.addWidget(self.quantity)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.material_combo = QComboBox(self.layoutWidget)
        self.material_combo.setObjectName(u"material_combo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.material_combo.sizePolicy().hasHeightForWidth())
        self.material_combo.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.material_combo)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(bill_of_material)
        self.buttonBox.accepted.connect(bill_of_material.accept)
        self.buttonBox.rejected.connect(bill_of_material.reject)

        QMetaObject.connectSlotsByName(bill_of_material)
    # setupUi

    def retranslateUi(self, bill_of_material):
        bill_of_material.setWindowTitle(QCoreApplication.translate("bill_of_material", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("bill_of_material", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0441\u043f\u0435\u0446\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438", None))
        self.label_4.setText(QCoreApplication.translate("bill_of_material", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.label_2.setText(QCoreApplication.translate("bill_of_material", u"\u041c\u0430\u0442\u0435\u0440\u0438\u0430\u043b", None))
    # retranslateUi


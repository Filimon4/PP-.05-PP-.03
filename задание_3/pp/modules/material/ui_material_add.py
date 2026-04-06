# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'material_add.ui'
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
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_material_add(object):
    def setupUi(self, material_add):
        if not material_add.objectName():
            material_add.setObjectName(u"material_add")
        material_add.resize(420, 160)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(material_add.sizePolicy().hasHeightForWidth())
        material_add.setSizePolicy(sizePolicy)
        material_add.setMinimumSize(QSize(420, 160))
        material_add.setMaximumSize(QSize(420, 160))
        material_add.setAutoFillBackground(False)
        self.layoutWidget = QWidget(material_add)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 401, 144))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.materialName = QLineEdit(self.layoutWidget)
        self.materialName.setObjectName(u"materialName")

        self.horizontalLayout.addWidget(self.materialName)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.materialCost = QLineEdit(self.layoutWidget)
        self.materialCost.setObjectName(u"materialCost")
        self.materialCost.setAutoFillBackground(False)

        self.horizontalLayout_3.addWidget(self.materialCost)

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

        self.materialUnits = QComboBox(self.layoutWidget)
        self.materialUnits.setObjectName(u"materialUnits")

        self.horizontalLayout_2.addWidget(self.materialUnits)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(material_add)
        self.buttonBox.accepted.connect(material_add.accept)
        self.buttonBox.rejected.connect(material_add.reject)

        QMetaObject.connectSlotsByName(material_add)
    # setupUi

    def retranslateUi(self, material_add):
        material_add.setWindowTitle(QCoreApplication.translate("material_add", u"Dialog", None))
        self.label_3.setText(QCoreApplication.translate("material_add", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0430", None))
        self.label.setText(QCoreApplication.translate("material_add", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.label_4.setText(QCoreApplication.translate("material_add", u"\u0426\u0435\u043d\u0430", None))
        self.label_2.setText(QCoreApplication.translate("material_add", u"\u0415\u0434\u0435\u043d\u0438\u0446\u044b \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f", None))
    # retranslateUi


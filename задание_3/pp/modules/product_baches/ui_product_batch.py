# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_product_batch.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDateEdit,
    QDialog, QDialogButtonBox, QFrame, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_add_product_batch(object):
    def setupUi(self, add_product_batch):
        if not add_product_batch.objectName():
            add_product_batch.setObjectName(u"add_product_batch")
        add_product_batch.resize(618, 471)
        self.layoutWidget = QWidget(add_product_batch)
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

        self.product_combo = QComboBox(self.layoutWidget)
        self.product_combo.setObjectName(u"product_combo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.product_combo.sizePolicy().hasHeightForWidth())
        self.product_combo.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.product_combo)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.order_combo = QComboBox(self.layoutWidget)
        self.order_combo.setObjectName(u"order_combo")
        sizePolicy.setHeightForWidth(self.order_combo.sizePolicy().hasHeightForWidth())
        self.order_combo.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.order_combo)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.date = QDateEdit(self.layoutWidget)
        self.date.setObjectName(u"date")
        sizePolicy.setHeightForWidth(self.date.sizePolicy().hasHeightForWidth())
        self.date.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.date)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.quantity = QLineEdit(self.layoutWidget)
        self.quantity.setObjectName(u"quantity")

        self.horizontalLayout_5.addWidget(self.quantity)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

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


        self.retranslateUi(add_product_batch)
        self.buttonBox.accepted.connect(add_product_batch.accept)
        self.buttonBox.rejected.connect(add_product_batch.reject)

        QMetaObject.connectSlotsByName(add_product_batch)
    # setupUi

    def retranslateUi(self, add_product_batch):
        add_product_batch.setWindowTitle(QCoreApplication.translate("add_product_batch", u"Dialog", None))
        self.title.setText(QCoreApplication.translate("add_product_batch", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u044f", None))
        self.label.setText(QCoreApplication.translate("add_product_batch", u"\u041f\u0440\u043e\u0434\u0443\u043a\u0442", None))
        self.label_2.setText(QCoreApplication.translate("add_product_batch", u"\u0417\u0430\u043a\u0430\u0437", None))
        self.label_4.setText(QCoreApplication.translate("add_product_batch", u"\u0412\u0440\u0435\u043c\u044f", None))
        self.label_5.setText(QCoreApplication.translate("add_product_batch", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.quantity.setInputMask("")
    # retranslateUi


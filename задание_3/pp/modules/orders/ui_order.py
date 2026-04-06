# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'order.ui'
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
    QLabel, QListView, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_order(object):
    def setupUi(self, order):
        if not order.objectName():
            order.setObjectName(u"order")
        order.resize(420, 617)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(order.sizePolicy().hasHeightForWidth())
        order.setSizePolicy(sizePolicy)
        order.setMinimumSize(QSize(420, 500))
        order.setMaximumSize(QSize(420, 1200))
        order.setAutoFillBackground(False)
        self.layoutWidget = QWidget(order)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(11, 11, 401, 591))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(self.layoutWidget)
        self.title.setObjectName(u"title")

        self.verticalLayout_2.addWidget(self.title)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.order_customer_combo = QComboBox(self.layoutWidget)
        self.order_customer_combo.setObjectName(u"order_customer_combo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.order_customer_combo.sizePolicy().hasHeightForWidth())
        self.order_customer_combo.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.order_customer_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.order_status_combo = QComboBox(self.layoutWidget)
        self.order_status_combo.setObjectName(u"order_status_combo")
        sizePolicy1.setHeightForWidth(self.order_status_combo.sizePolicy().hasHeightForWidth())
        self.order_status_combo.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.order_status_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.order_manager_combo = QComboBox(self.layoutWidget)
        self.order_manager_combo.setObjectName(u"order_manager_combo")
        sizePolicy1.setHeightForWidth(self.order_manager_combo.sizePolicy().hasHeightForWidth())
        self.order_manager_combo.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.order_manager_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.order_date = QDateEdit(self.layoutWidget)
        self.order_date.setObjectName(u"order_date")
        sizePolicy1.setHeightForWidth(self.order_date.sizePolicy().hasHeightForWidth())
        self.order_date.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.order_date)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.line = QFrame(self.layoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout.addWidget(self.label_6)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.order_item_add = QPushButton(self.layoutWidget)
        self.order_item_add.setObjectName(u"order_item_add")

        self.horizontalLayout_6.addWidget(self.order_item_add)

        self.order_item_change = QPushButton(self.layoutWidget)
        self.order_item_change.setObjectName(u"order_item_change")

        self.horizontalLayout_6.addWidget(self.order_item_change)

        self.order_item_delete = QPushButton(self.layoutWidget)
        self.order_item_delete.setObjectName(u"order_item_delete")

        self.horizontalLayout_6.addWidget(self.order_item_delete)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.order_item_load = QPushButton(self.layoutWidget)
        self.order_item_load.setObjectName(u"order_item_load")

        self.horizontalLayout_6.addWidget(self.order_item_load)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.order_item_list = QListView(self.layoutWidget)
        self.order_item_list.setObjectName(u"order_item_list")

        self.verticalLayout.addWidget(self.order_item_list)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.order_actions = QHBoxLayout()
        self.order_actions.setObjectName(u"order_actions")

        self.verticalLayout_2.addLayout(self.order_actions)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(order)
        self.buttonBox.accepted.connect(order.accept)
        self.buttonBox.rejected.connect(order.reject)

        QMetaObject.connectSlotsByName(order)
    # setupUi

    def retranslateUi(self, order):
        order.setWindowTitle(QCoreApplication.translate("order", u"Dialog", None))
        self.title.setText(QCoreApplication.translate("order", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u0437\u0430\u043a\u0430\u0437\u0430", None))
        self.label.setText(QCoreApplication.translate("order", u"\u0417\u0430\u043a\u0430\u0437\u0447\u0438\u043a", None))
        self.label_3.setText(QCoreApplication.translate("order", u"\u0421\u0442\u0430\u0442\u0443\u0441", None))
        self.label_4.setText(QCoreApplication.translate("order", u"\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440", None))
        self.label_5.setText(QCoreApplication.translate("order", u"\u0414\u0430\u0442\u0430", None))
        self.label_6.setText(QCoreApplication.translate("order", u"\u041f\u043e\u0437\u0438\u0446\u0438\u0438 \u0437\u0430\u043a\u0430\u0437\u0430", None))
        self.order_item_add.setText(QCoreApplication.translate("order", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.order_item_change.setText(QCoreApplication.translate("order", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.order_item_delete.setText(QCoreApplication.translate("order", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.order_item_load.setText(QCoreApplication.translate("order", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
    # retranslateUi


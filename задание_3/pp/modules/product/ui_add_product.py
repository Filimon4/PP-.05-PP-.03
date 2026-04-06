# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_product.ui'
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
    QLineEdit, QListView, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_add_product(object):
    def setupUi(self, add_product):
        if not add_product.objectName():
            add_product.setObjectName(u"add_product")
        add_product.resize(420, 617)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(add_product.sizePolicy().hasHeightForWidth())
        add_product.setSizePolicy(sizePolicy)
        add_product.setMinimumSize(QSize(420, 500))
        add_product.setMaximumSize(QSize(420, 1200))
        add_product.setAutoFillBackground(False)
        self.widget = QWidget(add_product)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(11, 11, 401, 581))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(self.widget)
        self.title.setObjectName(u"title")

        self.verticalLayout_2.addWidget(self.title)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.product_name = QLineEdit(self.widget)
        self.product_name.setObjectName(u"product_name")

        self.horizontalLayout.addWidget(self.product_name)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.product_code = QLineEdit(self.widget)
        self.product_code.setObjectName(u"product_code")

        self.horizontalLayout_4.addWidget(self.product_code)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.product_description = QLineEdit(self.widget)
        self.product_description.setObjectName(u"product_description")
        self.product_description.setAutoFillBackground(False)

        self.horizontalLayout_3.addWidget(self.product_description)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.product_default_price = QLineEdit(self.widget)
        self.product_default_price.setObjectName(u"product_default_price")

        self.horizontalLayout_5.addWidget(self.product_default_price)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.product_unit_combo = QComboBox(self.widget)
        self.product_unit_combo.setObjectName(u"product_unit_combo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.product_unit_combo.sizePolicy().hasHeightForWidth())
        self.product_unit_combo.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.product_unit_combo)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout.addWidget(self.label_6)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.bill_of_material_add = QPushButton(self.widget)
        self.bill_of_material_add.setObjectName(u"bill_of_material_add")

        self.horizontalLayout_6.addWidget(self.bill_of_material_add)

        self.bill_of_material_change = QPushButton(self.widget)
        self.bill_of_material_change.setObjectName(u"bill_of_material_change")

        self.horizontalLayout_6.addWidget(self.bill_of_material_change)

        self.bill_of_material_delete = QPushButton(self.widget)
        self.bill_of_material_delete.setObjectName(u"bill_of_material_delete")

        self.horizontalLayout_6.addWidget(self.bill_of_material_delete)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.bill_of_material_load = QPushButton(self.widget)
        self.bill_of_material_load.setObjectName(u"bill_of_material_load")

        self.horizontalLayout_6.addWidget(self.bill_of_material_load)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.bill_of_material_list = QListView(self.widget)
        self.bill_of_material_list.setObjectName(u"bill_of_material_list")

        self.verticalLayout.addWidget(self.bill_of_material_list)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(self.widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(add_product)
        self.buttonBox.accepted.connect(add_product.accept)
        self.buttonBox.rejected.connect(add_product.reject)

        QMetaObject.connectSlotsByName(add_product)
    # setupUi

    def retranslateUi(self, add_product):
        add_product.setWindowTitle(QCoreApplication.translate("add_product", u"Dialog", None))
        self.title.setText(QCoreApplication.translate("add_product", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430", None))
        self.label.setText(QCoreApplication.translate("add_product", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.label_3.setText(QCoreApplication.translate("add_product", u"\u041a\u043e\u0434 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u0430", None))
        self.label_4.setText(QCoreApplication.translate("add_product", u"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435", None))
        self.label_5.setText(QCoreApplication.translate("add_product", u"\u0411\u0430\u0437\u043e\u0432\u0430\u044f \u0446\u0435\u043d\u0430", None))
        self.label_2.setText(QCoreApplication.translate("add_product", u"\u0415\u0434\u0435\u043d\u0438\u0446\u044b \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f", None))
        self.label_6.setText(QCoreApplication.translate("add_product", u"\u0421\u043f\u0435\u0446\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f", None))
        self.bill_of_material_add.setText(QCoreApplication.translate("add_product", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.bill_of_material_change.setText(QCoreApplication.translate("add_product", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.bill_of_material_delete.setText(QCoreApplication.translate("add_product", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.bill_of_material_load.setText(QCoreApplication.translate("add_product", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
    # retranslateUi


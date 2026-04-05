# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QListView, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1036, 620)
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setEnabled(True)
        self.horizontalLayout = QHBoxLayout(self.central_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttons = QVBoxLayout()
        self.buttons.setSpacing(0)
        self.buttons.setObjectName(u"buttons")
        self.orders_but = QPushButton(self.central_widget)
        self.orders_but.setObjectName(u"orders_but")
        self.orders_but.setCheckable(True)
        self.orders_but.setAutoExclusive(True)

        self.buttons.addWidget(self.orders_but)

        self.employees_but = QPushButton(self.central_widget)
        self.employees_but.setObjectName(u"employees_but")
        self.employees_but.setCheckable(True)
        self.employees_but.setAutoExclusive(True)

        self.buttons.addWidget(self.employees_but)

        self.products_but = QPushButton(self.central_widget)
        self.products_but.setObjectName(u"products_but")
        self.products_but.setCheckable(True)
        self.products_but.setAutoExclusive(True)

        self.buttons.addWidget(self.products_but)

        self.product_batches_but = QPushButton(self.central_widget)
        self.product_batches_but.setObjectName(u"product_batches_but")
        self.product_batches_but.setCheckable(True)
        self.product_batches_but.setAutoExclusive(True)

        self.buttons.addWidget(self.product_batches_but)

        self.customers_but = QPushButton(self.central_widget)
        self.customers_but.setObjectName(u"customers_but")
        self.customers_but.setCheckable(True)
        self.customers_but.setAutoExclusive(True)

        self.buttons.addWidget(self.customers_but)

        self.materials_but = QPushButton(self.central_widget)
        self.materials_but.setObjectName(u"materials_but")
        self.materials_but.setCheckable(True)
        self.materials_but.setAutoExclusive(True)

        self.buttons.addWidget(self.materials_but)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.buttons.addItem(self.verticalSpacer)

        self.exit_but = QPushButton(self.central_widget)
        self.exit_but.setObjectName(u"exit_but")

        self.buttons.addWidget(self.exit_but)


        self.horizontalLayout.addLayout(self.buttons)

        self.menu = QWidget(self.central_widget)
        self.menu.setObjectName(u"menu")
        self.menu.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu.sizePolicy().hasHeightForWidth())
        self.menu.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.menu)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.stackedWidget = QStackedWidget(self.menu)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.orders = QWidget()
        self.orders.setObjectName(u"orders")
        sizePolicy.setHeightForWidth(self.orders.sizePolicy().hasHeightForWidth())
        self.orders.setSizePolicy(sizePolicy)
        self.layoutWidget = QWidget(self.orders)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, -3, 901, 541))
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_5.addWidget(self.label_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.order_add = QPushButton(self.layoutWidget)
        self.order_add.setObjectName(u"order_add")

        self.horizontalLayout_6.addWidget(self.order_add)

        self.order_change = QPushButton(self.layoutWidget)
        self.order_change.setObjectName(u"order_change")

        self.horizontalLayout_6.addWidget(self.order_change)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)

        self.order_load = QPushButton(self.layoutWidget)
        self.order_load.setObjectName(u"order_load")

        self.horizontalLayout_6.addWidget(self.order_load)

        self.order_load_filter_combo = QComboBox(self.layoutWidget)
        self.order_load_filter_combo.addItem("")
        self.order_load_filter_combo.addItem("")
        self.order_load_filter_combo.addItem("")
        self.order_load_filter_combo.setObjectName(u"order_load_filter_combo")

        self.horizontalLayout_6.addWidget(self.order_load_filter_combo)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.order_list = QListView(self.layoutWidget)
        self.order_list.setObjectName(u"order_list")

        self.verticalLayout_5.addWidget(self.order_list)

        self.stackedWidget.addWidget(self.orders)
        self.product_batches = QWidget()
        self.product_batches.setObjectName(u"product_batches")
        self.layoutWidget1 = QWidget(self.product_batches)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 0, 891, 541))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.product_batches_add = QPushButton(self.layoutWidget1)
        self.product_batches_add.setObjectName(u"product_batches_add")

        self.horizontalLayout_4.addWidget(self.product_batches_add)

        self.product_batches_delete = QPushButton(self.layoutWidget1)
        self.product_batches_delete.setObjectName(u"product_batches_delete")

        self.horizontalLayout_4.addWidget(self.product_batches_delete)

        self.product_batches_change = QPushButton(self.layoutWidget1)
        self.product_batches_change.setObjectName(u"product_batches_change")

        self.horizontalLayout_4.addWidget(self.product_batches_change)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.product_batches_load = QPushButton(self.layoutWidget1)
        self.product_batches_load.setObjectName(u"product_batches_load")

        self.horizontalLayout_4.addWidget(self.product_batches_load)

        self.product_batches_load_filter_combo = QComboBox(self.layoutWidget1)
        self.product_batches_load_filter_combo.addItem("")
        self.product_batches_load_filter_combo.addItem("")
        self.product_batches_load_filter_combo.setObjectName(u"product_batches_load_filter_combo")

        self.horizontalLayout_4.addWidget(self.product_batches_load_filter_combo)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.product_batches_list = QListView(self.layoutWidget1)
        self.product_batches_list.setObjectName(u"product_batches_list")

        self.verticalLayout_3.addWidget(self.product_batches_list)

        self.stackedWidget.addWidget(self.product_batches)
        self.customers = QWidget()
        self.customers.setObjectName(u"customers")
        self.layoutWidget2 = QWidget(self.customers)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(0, 0, 891, 541))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget2)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.customer_add = QPushButton(self.layoutWidget2)
        self.customer_add.setObjectName(u"customer_add")

        self.horizontalLayout_3.addWidget(self.customer_add)

        self.customer_delete = QPushButton(self.layoutWidget2)
        self.customer_delete.setObjectName(u"customer_delete")

        self.horizontalLayout_3.addWidget(self.customer_delete)

        self.customer_change = QPushButton(self.layoutWidget2)
        self.customer_change.setObjectName(u"customer_change")

        self.horizontalLayout_3.addWidget(self.customer_change)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.customer_load = QPushButton(self.layoutWidget2)
        self.customer_load.setObjectName(u"customer_load")

        self.horizontalLayout_3.addWidget(self.customer_load)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.customer_list = QListView(self.layoutWidget2)
        self.customer_list.setObjectName(u"customer_list")

        self.verticalLayout_2.addWidget(self.customer_list)

        self.stackedWidget.addWidget(self.customers)
        self.materials = QWidget()
        self.materials.setObjectName(u"materials")
        self.layoutWidget3 = QWidget(self.materials)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(0, 0, 891, 541))
        self.materials_layout = QVBoxLayout(self.layoutWidget3)
        self.materials_layout.setObjectName(u"materials_layout")
        self.materials_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.materials_layout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget3)
        self.label_2.setObjectName(u"label_2")

        self.materials_layout.addWidget(self.label_2)

        self.material_buttons = QHBoxLayout()
        self.material_buttons.setObjectName(u"material_buttons")
        self.material_add = QPushButton(self.layoutWidget3)
        self.material_add.setObjectName(u"material_add")

        self.material_buttons.addWidget(self.material_add)

        self.material_delete = QPushButton(self.layoutWidget3)
        self.material_delete.setObjectName(u"material_delete")

        self.material_buttons.addWidget(self.material_delete)

        self.material_change = QPushButton(self.layoutWidget3)
        self.material_change.setObjectName(u"material_change")

        self.material_buttons.addWidget(self.material_change)

        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.material_buttons.addItem(self.horizontal_spacer)

        self.material_load = QPushButton(self.layoutWidget3)
        self.material_load.setObjectName(u"material_load")

        self.material_buttons.addWidget(self.material_load)


        self.materials_layout.addLayout(self.material_buttons)

        self.material_list = QListView(self.layoutWidget3)
        self.material_list.setObjectName(u"material_list")

        self.materials_layout.addWidget(self.material_list)

        self.stackedWidget.addWidget(self.materials)
        self.bill_of_material = QWidget()
        self.bill_of_material.setObjectName(u"bill_of_material")
        self.bill_of_material.setEnabled(False)
        self.stackedWidget.addWidget(self.bill_of_material)
        self.employee = QWidget()
        self.employee.setObjectName(u"employee")
        self.layoutWidget4 = QWidget(self.employee)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(0, 5, 891, 531))
        self.verticalLayout = QVBoxLayout(self.layoutWidget4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(self.layoutWidget4)
        self.title.setObjectName(u"title")

        self.verticalLayout.addWidget(self.title)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.employee_add = QPushButton(self.layoutWidget4)
        self.employee_add.setObjectName(u"employee_add")

        self.horizontalLayout_2.addWidget(self.employee_add)

        self.employee_delete = QPushButton(self.layoutWidget4)
        self.employee_delete.setObjectName(u"employee_delete")

        self.horizontalLayout_2.addWidget(self.employee_delete)

        self.employee_change = QPushButton(self.layoutWidget4)
        self.employee_change.setObjectName(u"employee_change")

        self.horizontalLayout_2.addWidget(self.employee_change)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.employee_load = QPushButton(self.layoutWidget4)
        self.employee_load.setObjectName(u"employee_load")

        self.horizontalLayout_2.addWidget(self.employee_load)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.employee_list = QListView(self.layoutWidget4)
        self.employee_list.setObjectName(u"employee_list")

        self.verticalLayout.addWidget(self.employee_list)

        self.stackedWidget.addWidget(self.employee)
        self.products = QWidget()
        self.products.setObjectName(u"products")
        self.layoutWidget5 = QWidget(self.products)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(0, 0, 881, 541))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.layoutWidget5)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_4.addWidget(self.label_5)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.product_add = QPushButton(self.layoutWidget5)
        self.product_add.setObjectName(u"product_add")

        self.horizontalLayout_5.addWidget(self.product_add)

        self.product_delete = QPushButton(self.layoutWidget5)
        self.product_delete.setObjectName(u"product_delete")

        self.horizontalLayout_5.addWidget(self.product_delete)

        self.product_change = QPushButton(self.layoutWidget5)
        self.product_change.setObjectName(u"product_change")

        self.horizontalLayout_5.addWidget(self.product_change)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.product_load = QPushButton(self.layoutWidget5)
        self.product_load.setObjectName(u"product_load")

        self.horizontalLayout_5.addWidget(self.product_load)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.product_list = QListView(self.layoutWidget5)
        self.product_list.setObjectName(u"product_list")

        self.verticalLayout_4.addWidget(self.product_list)

        self.stackedWidget.addWidget(self.products)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.menu)

        MainWindow.setCentralWidget(self.central_widget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.orders_but.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043a\u0430\u0437\u044b", None))
        self.employees_but.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0438", None))
        self.products_but.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0434\u0443\u043a\u0442\u044b", None))
        self.product_batches_but.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u044f", None))
        self.customers_but.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u0438", None))
        self.materials_but.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u044b", None))
        self.exit_but.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043a\u0430\u0437\u044b", None))
        self.order_add.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.order_change.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.order_load.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.order_load_filter_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0435", None))
        self.order_load_filter_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"\u0410\u043a\u0442\u0438\u0432\u043d\u044b\u0435 \u0437\u0430\u043a\u0430\u0437\u044b", None))
        self.order_load_filter_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044b\u0435", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u044f", None))
        self.product_batches_add.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.product_batches_delete.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.product_batches_change.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.product_batches_load.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.product_batches_load_filter_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0435", None))
        self.product_batches_load_filter_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"\u041e\u0441\u0442\u0430\u0442\u043a\u0438", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u0438", None))
        self.customer_add.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.customer_delete.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.customer_change.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.customer_load.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u044b", None))
        self.material_add.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.material_delete.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.material_change.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.material_load.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.title.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0438", None))
        self.employee_add.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.employee_delete.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.employee_change.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.employee_load.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0434\u0443\u043a\u0442\u044b", None))
        self.product_add.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.product_delete.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.product_change.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.product_load.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
    # retranslateUi


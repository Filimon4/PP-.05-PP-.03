import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PySide6.QtCore import Qt
from modules.mainwindow.ui_mainwindow import Ui_MainWindow

from psycopg2.extras import RealDictCursor

import shared.resources_rc as resources_rc

from common.db import conn
from psycopg2.extras import RealDictCursor

from modules.customer.customer import CustomerAddDialog, CustomerChangeDialog, CustomerListModel
from modules.employee.employee import EmployeeAddDialog, EmployeeChangeDialog, EmployeeListModel
from modules.material.material import MaterialAddDialog, MaterialChangeDialog, MaterialsListModel
from modules.orders.orders import OrdersAddDialog, OrdersChangeDialog, OrdersListModel
from modules.product.product import ProductAddDialog, ProductChangeDialog, ProductListModel
from modules.auth.auth import AuthDialog
from modules.product_baches.product_baches import ProductBatchAddDialog, ProductBatchChangeDialog, ProductBatchListModel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.orders_but.setChecked(True)
        self.ui.exit_but.clicked.connect(self.exitButtonClicked)

        # menu
        self.ui.customers_but.clicked.connect       (self.customersClicked)
        self.ui.employees_but.clicked.connect       (self.employeeButClicked)
        self.ui.materials_but.clicked.connect       (self.materialButClicked)
        self.ui.orders_but.clicked.connect          (self.ordersButClicked)
        self.ui.product_batches_but.clicked.connect (self.productBatchesButClicked)
        self.ui.products_but.clicked.connect        (self.productsButClicked)

        # order
        self.ui.order_add.clicked.connect       (self.ordersAdd)
        self.ui.order_change.clicked.connect    (self.orderChange)
        self.ui.order_load.clicked.connect      (self.orderLoad)

        # material
        self.ui.material_load.clicked.connect   (self.materialLoad)
        self.ui.material_add.clicked.connect    (self.materialAdd)
        self.ui.material_change.clicked.connect (self.materialChange)
        self.ui.material_delete.clicked.connect (self.materialDelete)

        # employee
        self.ui.employee_load.clicked.connect   (self.employeeLoad)
        self.ui.employee_add.clicked.connect    (self.employeeAdd)
        self.ui.employee_change.clicked.connect (self.employeeChange)
        self.ui.employee_delete.clicked.connect (self.employeeDelete)

        # customer
        self.ui.customer_add.clicked.connect    (self.customerAdd)
        self.ui.customer_change.clicked.connect (self.customerChange)
        self.ui.customer_load.clicked.connect   (self.customerLoad)
        self.ui.customer_delete.clicked.connect (self.customerDelete)

        # product_batches
        self.ui.product_batches_add.clicked.connect     (self.productBatchesAdd)
        self.ui.product_batches_change.clicked.connect  (self.productBatchesChange)
        self.ui.product_batches_load.clicked.connect    (self.productBatchesLoad)
        self.ui.product_batches_delete.clicked.connect  (self.productBatchesDelete)

        # product
        self.ui.product_add.clicked.connect     (self.productAdd)
        self.ui.product_change.clicked.connect  (self.productChange)
        self.ui.product_load.clicked.connect    (self.productLoad)
        self.ui.product_delete.clicked.connect  (self.productDelete)

        self.ui.central_widget.setEnabled(False)
        dialog = AuthDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.role = dialog.user['role_code']
            self.ui.central_widget.setEnabled(True)
        else:
            sys.exit()

        if self.role != 'admin':
            self.ui.employees_but.setEnabled(False)
            self.ui.employees_but.deleteLater()

    def exitButtonClicked(self):
        self.ui.central_widget.setEnabled(False)
        dialog = AuthDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.role = dialog.user['role_code']
            self.ui.central_widget.setEnabled(True)
        else:
            sys.exit()

        if self.role != 'admin':
            self.ui.employees_but.setEnabled(False)
            self.ui.employees_but.deleteLater()

    # region menu
    
    def customersClicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def employeeButClicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def materialButClicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def ordersButClicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def productBatchesButClicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def productsButClicked(self):
        self.ui.stackedWidget.setCurrentIndex(6)
    # endregion

    # region orders

    def orderLoad(self):
        currentFilter = self.ui.order_load_filter_combo.currentText()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
                select
                    o."date",
                    o.id,
                    os.code as status_code,
                    os.title as status_title,
                    c."name" as customer_name,
                    c.buyer as is_buyer,
                    c.salesman as is_salesman,
                    c.email as customer_email,
                    e.email as employee_email,
                    e.phone as employee_phone,
                    CONCAT(e.id, ' ', e.first_name, ' ', e.family_name) AS manager_code
                from orders o
                left join order_statuses os on os.id = o.status_id
                left join customers c on o.customer_id = c.id
                left join employees e on o.manager_id = e.id
            """
            
            params = {}
            
            if currentFilter == "Активные заказы":
                query += " WHERE os.code = 'active'"
            elif currentFilter == "Закрытые":
                query += " WHERE os.code = 'closed'"
            
            query += 'order by id asc '

            cur.execute(query, params)
            orders = cur.fetchall() 

        model = OrdersListModel(orders)
        self.ui.order_list.setModel(model)

    def ordersAdd(self):
        dialog = OrdersAddDialog()
        customers = self.getCustomers()
        dialog.setCustomers(list(map(lambda u: u['customer_name'], list(customers))))
        statuses = self.setStatuses()
        dialog.setStatuses(list(map(lambda u: u['title'], list(statuses))))
        managers = self.getManagers()
        dialog.setMangers(list(map(lambda u: u['manager_code'], list(managers))))

        index = dialog.ui.order_status_combo.findText(list(filter(lambda x: x['code'] == 'active', list(statuses)))[0]['title'])
        if index >= 0:
            dialog.ui.order_status_combo.setCurrentIndex(index)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute("""
                        SELECT c.id
                        FROM customers c
                        WHERE c."name" = %(name)s
                    """, {"name": data['customer_name']})
                                        
                    customerData = cur.fetchone()
                    if customerData is None:
                        raise Exception(f"Заказчик '{data['customer_name']}' не найден")
                    
                    cur.execute("""
                        select
                            os.id
                        from order_statuses os
                        where os.title = %(code)s
                    """, {"code": data['status_title']})
                    statusData = cur.fetchone()
                    if statusData is None:
                        raise Exception(f"Статус '{data['status_title']}' не найден")

                    cur.execute("""
                        select
                            e.id
                        from employees e
                        left join employee_positions ep on ep.id = e.position_id
                        where ep.code = 'SALES_HEAD' and CONCAT(e.id, ' ', e.first_name, ' ', e.family_name) = %(manager_name)s
                    """, {"manager_name": data['manager_code']})

                    managerData = cur.fetchone()
                    if managerData is None:
                        raise Exception(f"Менеджер '{data['status_title']}' не найден")

                    cur.execute("""
                        INSERT INTO orders (date, customer_id, status_id, manager_id)
                        VALUES (%(date)s, %(customer_id)s, %(status_id)s, %(manager_id)s)
                        RETURNING id
                    """, {
                        'date': data['order_date'],
                        'customer_id': customerData['id'],
                        'status_id': statusData['id'],
                        'manager_id': managerData['id']
                    })
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"Error: {e}") # TODO: добавить warning
                    return
            self.orderLoad()
        
    def orderChange(self):
        if not self.ui.order_list.selectionModel():
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return

        selected = self.ui.order_list.selectionModel().selectedIndexes()
        
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.order_list.model().data(selected_index, Qt.UserRole)

        dialog = OrdersChangeDialog(None, item)
        customers = self.getCustomers()
        dialog.setCustomers(list(map(lambda u: u['customer_name'], list(customers))))
        statuses = self.setStatuses()
        dialog.setStatuses(list(map(lambda u: u['title'], list(statuses))))
        managers = self.getManagers()
        dialog.setMangers(list(map(lambda u: u['manager_code'], list(managers))))
        dialog.setDefault()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute("""
                        select
                            c.id,
                            c."name" as customer_name
                        from customers c
                        where c."name" = %(customer_name)s
                    """, {"customer_name": data['customer_name']})
                    
                    customerData = cur.fetchone()
                    if customerData is None:
                        raise Exception(f"Заказчик '{data['customer_name']}' не найден")

                    cur.execute("""
                        select
                            e.id,
                            CONCAT(e.id, ' ', e.first_name, ' ', e.family_name) AS name
                        from employees e
                        left join employee_positions ep on ep.id = e.position_id
                        where ep.code = 'SALES_HEAD' and CONCAT(e.id, ' ', e.first_name, ' ', e.family_name) = %(manager_name)s
                    """, {"manager_name": data['manager_code']})

                    managerData = cur.fetchone()
                    if managerData is None:
                        raise Exception(f"Статус '{data['manager_code']}' не найден")

                    cur.execute("""
                        UPDATE orders 
                        SET date = %(date)s,
                            customer_id = %(customer_id)s,
                            manager_id = %(manager_id)s
                        WHERE id = %(order_id)s
                        RETURNING id
                    """, {
                        'order_id': item['id'],
                        'date': data['order_date'],
                        'customer_id': customerData['id'],
                        'manager_id': managerData['id']
                    })
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"Error: {e}") # TODO: добавить warning
                    return
            self.orderLoad()


    def getOrders(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT o.id, o.date, c.name as customer_name
                FROM orders o
                LEFT JOIN customers c ON c.id = o.customer_id
                left join order_statuses os on o.status_id = os.id
                where os.code = 'active'
                ORDER BY o.id DESC
            """)
            return cur.fetchall()

    # endregion

    # region material

    def materialLoad(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    m.id,
                    m."cost",
                    m."name",
                    uom.code as unit_code
                from materials m
                left join units_of_measures uom on m.unit_of_measure_id = uom.id
                order by id asc
            """)
            materials = cur.fetchall()

        model = MaterialsListModel(materials)
        self.ui.material_list.setModel(model)

    def materialAdd(self):
        dialog = MaterialAddDialog()
        units = self.getUnitOfMeasure()
        dialog.setUnits(list(map(lambda u: u['code'], list(units))))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            cur = conn.cursor()
            try:
                cur.execute("""
                    SELECT
                        m.id
                    FROM units_of_measures m
                    WHERE m.code = %(code)s
                """, {"code": data['unit']})
                
                unitData = cur.fetchone()
                if unitData is None:
                    raise Exception(f"Unit of measure with code '{data['unit']}' not found")
                cur.execute("""
                    INSERT INTO materials (name, cost, unit_of_measure_id)
                    VALUES (%(name)s, %(cost)s, %(unit_id)s)
                """, {
                    "name": data['name'], 
                    "cost": data['cost'], 
                    "unit_id": unitData[0]
                })
                conn.commit()
            except Exception as e:
                conn.rollback()
            finally:
                cur.close()
                self.materialLoad()

    def materialChange(self):
        if not self.ui.material_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected = self.ui.material_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.material_list.model().data(selected_index, Qt.UserRole)

        dialog = MaterialChangeDialog(None, item)
        units = self.getUnitOfMeasure()
        dialog.setUnits(list(map(lambda u: u['code'], list(units))))
        dialog.setDefault()
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT
                        m.id
                    FROM units_of_measures m
                    WHERE m.code = %(code)s
                """, {"code": data['unit']})
                unitData = cur.fetchone()
                if unitData is None:
                    raise Exception(f"Unit of measure with code '{data['unit']}' not found")
                cur.execute("""
                    update materials
                    set name = %(name)s, cost = %(cost)s, unit_of_measure_id = %(unit_id)s
                    where id = %(id)s
                    returning id
                """, {'id': item['id'], 'name': data['name'], 'unit_id': unitData['id'], 'cost': data['cost']})
                cur.fetchone()
                conn.commit()
            self.materialLoad()

    def materialDelete(self):
        if not self.ui.material_list.selectionModel():
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return

        selected = self.ui.material_list.selectionModel().selectedIndexes()
        
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.material_list.model().data(selected_index, Qt.UserRole)
        
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                DELETE FROM materials
                WHERE id = %s
                RETURNING *
            """, (item['id'],))
            
            cur.fetchone()
            conn.commit()
        
        self.materialLoad()

    # endregion

    # region unit_of_measure

    def getUnitOfMeasure(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    uom.id,
                    uom.code
                from units_of_measures uom 
            """)
            unitsOfMeasure = cur.fetchall()

        return unitsOfMeasure

    # endregion

    # region employee_positions

    def getEmployeePositions(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    ep.id,
                    ep.title,
                    ep.code
                from employee_positions ep
            """)
            positions = cur.fetchall()

        return positions

    # endregion

    # region employee

    def employeeLoad(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    e.id,
                    e.address,
                    e.email,
                    e.first_name,
                    e.family_name,
                    e.last_name,
                    e.phone,
                    e.login,
                    e.password,
                    e.blocked,
                    e.failed_attempts,
                    ep.title as position_title
                from employees e
                left join employee_positions ep on ep.id = e.position_id
                order by id asc
            """)
            employee = cur.fetchall()

        model = EmployeeListModel(employee)
        self.ui.employee_list.setModel(model)

    def employeeAdd(self):
        dialog = EmployeeAddDialog()
        units = self.getEmployeePositions()
        dialog.setPositions(list(map(lambda u: u['title'], list(units))))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    select
                        ep.id
                    from employee_positions ep
                    where ep.title = %(title)s
                """, {'title': data['position_title']})
                position = cur.fetchone()

                if not position:
                    raise Exception(f"Position with code '{data['position_title']}' not found")
                cur.execute("""
                    INSERT INTO employees (first_name, family_name, last_name, email, phone, position_id, address, login, password, blocked)
                    VALUES (%(first_name)s, %(family_name)s, %(last_name)s, %(email)s, %(phone)s, %(position_id)s, %(address)s, %(login)s, %(password)s, %(blocked)s)
                """, {
                    'first_name': data['first_name'],
                    'family_name': data['family_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'phone': data['phone'],
                    'position_id': position['id'],
                    'address': data['address'],
                    'login': data['login'],
                    'password': data['password'],
                    'blocked': data['blocked']
                })
                conn.commit()
            self.employeeLoad()

    def employeeChange(self):
        if not self.ui.employee_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected = self.ui.employee_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        selected_index = selected[0]
        item = self.ui.employee_list.model().data(selected_index, Qt.UserRole)

        dialog = EmployeeChangeDialog(None, item)
        units = self.getEmployeePositions()
        dialog.setPositions(list(map(lambda u: u['title'], list(units))))
        dialog.setDefault()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    select
                        ep.id
                    from employee_positions ep
                    where ep.title = %(title)s
                """, {'title': data['position_title']})
                position = cur.fetchone()

                if not position:
                    raise Exception(f"Position with code '{data['position_title']}' not found")
                
                cur.execute("""
                    UPDATE employees
                    SET first_name = %(first_name)s,
                        last_name = %(last_name)s,
                        family_name = %(family_name)s,
                        email = %(email)s,
                        phone = %(phone)s,
                        address = %(address)s,
                        position_id = %(position_id)s,
                        login = %(login)s,
                        password = %(password)s,
                        blocked = %(blocked)s,
                        failed_attempts = %(failed_attempts)s
                    WHERE id = %(id)s
                    RETURNING id
                """, {
                    'id': item['id'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'family_name': data['family_name'],
                    'email': data['email'],
                    'phone': data['phone'],
                    'address': data['address'],
                    'position_id': position['id'],
                    'login': data['login'],
                    'password': data['password'],
                    'blocked': data['blocked'],
                    'failed_attempts': 0 if data['blocked'] == False else item['failed_attempts']
                })
                cur.fetchone()
                conn.commit()
            self.employeeLoad()

    def employeeDelete(self):
        if not self.ui.employee_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected = self.ui.employee_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        selected_index = selected[0]
        item = self.ui.employee_list.model().data(selected_index, Qt.UserRole)

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                DELETE FROM employees
                WHERE id = %s
                RETURNING *
            """, (item['id'],))
            
            cur.fetchone()
            conn.commit()
        
        self.employeeLoad()

    def getManagers(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    e.id,
                    CONCAT(e.id, ' ', e.first_name, ' ', e.family_name) AS manager_code
                from employees e
                left join employee_positions ep on ep.id = e.position_id
                where ep.code = 'SALES_HEAD'
            """)
            return cur.fetchall()

    # endregion

    # region customer

    def getCustomers(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    c.id,
                    c."name" as customer_name
                from customers c
            """)
            customers = cur.fetchall()

        return customers

    def customerLoad(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    id,
                    name,
                    inn,
                    email,
                    phone,
                    address,
                    buyer,
                    salesman
                FROM customers
                ORDER BY id ASC
            """)
            customers = cur.fetchall()

        model = CustomerListModel(customers)
        self.ui.customer_list.setModel(model)

    def customerAdd(self):
        dialog = CustomerAddDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute("""
                        INSERT INTO customers (name, inn, email, phone, address, buyer, salesman)
                        VALUES (%(name)s, %(inn)s, %(email)s, %(phone)s, %(address)s, %(buyer)s, %(salesman)s)
                        RETURNING id
                    """, {
                        'name': data['name'],
                        'inn': data['inn'],
                        'email': data['email'],
                        'phone': data['phone'],
                        'address': data['address'],
                        'buyer': data['buyer'],
                        'salesman': data['salesman']
                    })
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    raise
            self.customerLoad()

    def customerChange(self):
        if not self.ui.customer_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберите элемент")
            return
        
        selected = self.ui.customer_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберите элемент")
            return
        selected_index = selected[0]
        item = self.ui.customer_list.model().data(selected_index, Qt.UserRole)

        dialog = CustomerChangeDialog(None, item)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    UPDATE customers
                    SET name = %(name)s,
                        inn = %(inn)s,
                        email = %(email)s,
                        phone = %(phone)s,
                        address = %(address)s,
                        buyer = %(buyer)s,
                        salesman = %(salesman)s
                    WHERE id = %(id)s
                    RETURNING id
                """, {
                    'id': item['id'],
                    'name': data['name'],
                    'inn': data['inn'],
                    'email': data['email'],
                    'phone': data['phone'],
                    'address': data['address'],
                    'buyer': data['buyer'],
                    'salesman': data['salesman']
                })
                cur.fetchone()
                conn.commit()
            self.customerLoad()

    def customerDelete(self):
        if not self.ui.customer_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберите элемент")
            return
        
        selected = self.ui.customer_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберите элемент")
            return
        selected_index = selected[0]
        item = self.ui.customer_list.model().data(selected_index, Qt.UserRole)

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                DELETE FROM customers
                WHERE id = %s
                RETURNING *
            """, (item['id'],))
            
            cur.fetchone()
            conn.commit()
        
        self.customerLoad()

    # endregion

    # region product_batches

    def productBatchesAdd(self):
        dialog = ProductBatchAddDialog()
        products = self.getProducts()
        product_names = list(map(lambda p: p['name'], products))
        dialog.setProducts(product_names)
        orders = self.getOrders()
        order_numbers = list(map(lambda o: f"Заказ №{o['id']} от {o['date'].strftime('%d.%m.%Y')} - {o['customer_name']}", orders))
        dialog.setOrders(order_numbers)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute("""
                        SELECT id
                        FROM products
                        WHERE name = %(name)s
                    """, {"name": data['product']})
                    product = cur.fetchone()
                    if not product:
                        raise Exception(f"Продукт '{data['product']}' не найден")
                    
                    order_text = data['order']
                    order_id = None
                    for order in self.getOrders():
                        order_display = f"Заказ №{order['id']} от {order['date'].strftime('%d.%m.%Y')} - {order['customer_name']}"
                        if order_display == order_text:
                            order_id = order['id']
                            break
                    
                    if not order_id:
                        raise Exception(f"Заказ '{data['order']}' не был найден")
                    
                    cur.execute("""
                        INSERT INTO product_batches (product_id, order_id, date, quantity)
                        VALUES (%(product_id)s, %(order_id)s, %(date)s, %(quantity)s)
                        RETURNING id
                    """, {
                        'product_id': product['id'],
                        'order_id': order_id,
                        'date': data['date'],
                        'quantity': data['quantity']
                    })
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении: {str(e)}")
                finally:
                    self.productBatchesLoad()

    def productBatchesChange(self):
        if not self.ui.product_batches_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберите элемент")
            return
        
        selected = self.ui.product_batches_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберите элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.product_batches_list.model().data(selected_index, Qt.UserRole)

        dialog = ProductBatchChangeDialog(None, item)
        
        products = self.getProducts()
        product_names = list(map(lambda p: p['name'], products))
        dialog.setProducts(product_names)
        
        orders = self.getOrders()
        order_numbers = list(map(lambda o: f"Заказ №{o['id']} от {o['date'].strftime('%d.%m.%Y')} - {o['customer_name']}", orders))
        dialog.setOrders(order_numbers)

        dialog.setDefault()
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute("""
                        SELECT id
                        FROM products
                        WHERE name = %(name)s
                    """, {"name": data['product']})
                    product = cur.fetchone()
                    if not product:
                        raise Exception(f"Продукт '{data['product']}' не найден")
                    
                    order_text = data['order']
                    order_id = None
                    for order in self.getOrders():
                        order_display = f"Заказ №{order['id']} от {order['date'].strftime('%d.%m.%Y')} - {order['customer_name']}"
                        if order_display == order_text:
                            order_id = order['id']
                            break
                    
                    if not order_id:
                        raise Exception(f"Заказ '{data['order']}' не найдены")
                    
                    cur.execute("""
                        UPDATE product_batches
                        SET product_id = %(product_id)s,
                            order_id = %(order_id)s,
                            date = %(date)s,
                            quantity = %(quantity)s
                        WHERE id = %(id)s
                        RETURNING id
                    """, {
                        'id': item['id'],
                        'product_id': product['id'],
                        'order_id': order_id,
                        'date': data['date'],
                        'quantity': data['quantity']
                    })
                    cur.fetchone()
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении: {str(e)}")
                finally:
                    self.productBatchesLoad()

    def productBatchesLoad(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            currentFilter = self.ui.product_batches_load_filter_combo.currentText()
            
            query = """
                SELECT 
                    pb.id,
                    pb.product_id,
                    pb.order_id,
                    pb.date,
                    pb.quantity,
                    p.name as product_name,
                    o.id as order_number,
                    c.name as customer_name
                FROM product_batches pb
                LEFT JOIN products p ON p.id = pb.product_id
                LEFT JOIN orders o ON o.id = pb.order_id
                LEFT JOIN customers c ON c.id = o.customer_id
            """
            
            if currentFilter == "Остатки":
                query += " WHERE pb.order_id IS NULL"
            
            query += " ORDER BY pb.id ASC"
            
            cur.execute(query)
            batches = cur.fetchall()

        model = ProductBatchListModel(batches)
        self.ui.product_batches_list.setModel(model)
        
    def productBatchesDelete(self):
        if not self.ui.product_batches_list.selectionModel():
            QMessageBox.warning(self, "Ошибка", "Выберите элемент")
            return

        selected = self.ui.product_batches_list.selectionModel().selectedIndexes()
        
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.product_batches_list.model().data(selected_index, Qt.UserRole)
        
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            try:
                cur.execute("""
                    DELETE FROM product_batches
                    WHERE id = %s
                    RETURNING *
                """, (item['id'],))
                
                cur.fetchone()
                conn.commit()
            except Exception as e:
                conn.rollback()
            finally:
                self.productBatchesLoad()

    # endregion

    # region products

    def productAdd(self):
        dialog = ProductAddDialog()
        units = self.getUnitOfMeasure()
        dialog.setUnits(list(map(lambda u: u['code'], list(units))))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute("""
                        SELECT
                            m.id
                        FROM units_of_measures m
                        WHERE m.code = %(code)s
                    """, {"code": data['unit']})
                    
                    unitData = cur.fetchone()
                    if unitData is None:
                        raise Exception(f"Unit of measure with code '{data['unit']}' not found")

                    cur.execute("""
                        INSERT INTO products (name, description, code, unit_of_measure_id, default_price)
                        VALUES (%(name)s, %(description)s, %(code)s, %(unit_of_measure_id)s, %(default_price)s)
                        RETURNING id
                    """, {
                        'name': data['name'],
                        'description': data['description'],
                        'code': data['code'],
                        'unit_of_measure_id': unitData['id'],
                        'default_price': data['default_price']
                    })
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(e) # TODO: добавить warning
                    return
            self.productLoad()

    def productChange(self):
        if not self.ui.product_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected = self.ui.product_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.product_list.model().data(selected_index, Qt.UserRole)

        dialog = ProductChangeDialog(None, item)
        units = self.getUnitOfMeasure()
        dialog.setUnits(list(map(lambda u: u['code'], list(units))))
        dialog.setDefault()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                data = dialog.getData()
                try:
                    cur.execute("""
                        SELECT
                            m.id
                        FROM units_of_measures m
                        WHERE m.code = %(code)s
                    """, {"code": data['unit']})
                    
                    unitData = cur.fetchone()
                    if unitData is None:
                        raise Exception(f"Unit of measure with code '{data['unit']}' not found")

                    cur.execute("""
                        UPDATE products 
                        SET name = %(name)s,
                            description = %(description)s,
                            code = %(code)s,
                            unit_of_measure_id = %(unit_of_measure_id)s,
                            default_price = %(default_price)s
                        WHERE id = %(id)s
                        RETURNING id
                    """, {
                        'id': item['id'],
                        'name': data['name'],
                        'description': data['description'],
                        'code': data['code'],
                        'unit_of_measure_id': unitData['id'],
                        'default_price': data['default_price']
                    })
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(e)
                    return
            self.productLoad()

    def productLoad(self): 
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    p.id,
                    p."name",
                    p.code,
                    p.default_price as default_price,
                    p.description,
                    uom.code as unit_code
                from products p
                left join units_of_measures uom on p.unit_of_measure_id = uom.id
                where p.deleted = false
                order by id asc
            """)
            products = cur.fetchall()

        model = ProductListModel(products)
        self.ui.product_list.setModel(model)

    def productDelete(self):
        if not self.ui.product_list.selectionModel():
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return

        selected = self.ui.product_list.selectionModel().selectedIndexes()
        
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.product_list.model().data(selected_index, Qt.UserRole)

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                update products
                set deleted = true
                WHERE id = %s
                RETURNING id
            """, (item['id'],))
            
            cur.fetchone()
            conn.commit()
        self.productLoad()

    def getProducts(self):
        """Helper method to get all products for combo box"""
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, name
                FROM products
                ORDER BY name ASC
            """)
            return cur.fetchall()

    # endregion

    # region status

    def setStatuses(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    os.id,
                    os.code,
                    os.title
                from order_statuses os 
            """)
            return cur.fetchall()

    # endregion

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

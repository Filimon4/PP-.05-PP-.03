import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QPushButton, QStyledItemDelegate
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QDateTime, QDate, QSize 
from PySide6.QtGui import QIcon, QPixmap
from ui_mainwindow import Ui_MainWindow
from ui_material_add import Ui_material_add
from ui_add_employee import Ui_add_employee
from ui_add_customer import Ui_add_customer
from ui_product_batch import Ui_add_product_batch
from ui_add_product import Ui_add_product
from ui_bill_of_material import Ui_bill_of_material
from ui_order_item import Ui_order_item
from ui_order import Ui_order
from ui_auth import Ui_auth
from ui_captha import Ui_captcha
import psycopg2
from psycopg2.extras import RealDictCursor

import resources_rc

# TODO: Добавить функцию разархивации, deleted = false
# TODO: Добавить разные виды просмотра фильтры для просмотра, combo box на загрузку

# TODO: order_actions добавлять кнопки в зависимости состояния

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="postgres",
    user="postgres",
    password="postgres"
)

# region: orders

class OrdersListModel(QAbstractListModel):
    def __init__(self, orders=None):
        super().__init__()
        self.orders = orders or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.orders)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.orders):
            return None

        product = self.orders[index.row()]

        if role == Qt.DisplayRole:
            return f"{product['id']} | {product['customer_name']} | Покупатель: {'Да' if product['is_buyer'] else 'Нет' } | Продавец: {'Да' if product['is_salesman'] else 'Нет'} | Телефон менеджера: {product['employee_phone']} | Почта менеджера {product['employee_email']}"
        
        if role == Qt.UserRole:
            return product

        return None
    
class OrdersAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_order()
        self.ui.setupUi(self) 
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)

        self.ui.order_item_list.setEnabled(False)
        self.ui.order_item_add.setEnabled(False)
        self.ui.order_item_change.setEnabled(False)
        self.ui.order_item_load.setEnabled(False)
        self.ui.order_item_delete.setEnabled(False)
        self.ui.order_status_combo.setEnabled(False)

        self.ui.order_date.setDate(QDate.currentDate())

    def getData(self):
        date_value = self.ui.order_date.dateTime().toPython() if hasattr(self.ui.order_date, 'dateTime') else self.ui.order_date.dateTime()
        return {
            'customer_name': self.ui.order_customer_combo.currentText(),
            'status_title': self.ui.order_status_combo.currentText(),
            'manager_code': self.ui.order_manager_combo.currentText(),
            'order_date': date_value
        }
    
    def validate(self):
        data = self.getData()

        if self.ui.order_customer_combo.currentIndex() == -1 or not data['customer_name']:
            return False, "Введите заказчика"
        
        if self.ui.order_manager_combo.currentIndex() == -1 or not data['manager_code']:
            return False, "Введите менеджера заказа"
        
        return True, ""
    
    def setCustomers(self, list):
        self.ui.order_customer_combo.clear()
        self.ui.order_customer_combo.addItems(list)

    def setMangers(self, list):
        self.ui.order_manager_combo.clear()
        self.ui.order_manager_combo.addItems(list)

    def setStatuses(self, list):
        self.ui.order_status_combo.clear()
        self.ui.order_status_combo.addItems(list)

    def accept(self):
        is_valid, error_msg = self.validate()
        
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_msg)
            return
        
        super().accept()

class OrdersChangeDialog(OrdersAddDialog):
    def __init__(self, parent=None, order=object):
        super().__init__(parent)
        self.order = order

        self.ui.order_item_list.setEnabled(True)
        self.ui.order_item_add.setEnabled(True)
        self.ui.order_item_change.setEnabled(True)
        self.ui.order_item_load.setEnabled(True)
        self.ui.order_item_delete.setEnabled(True)

        self.ui.order_item_add.clicked.connect      (self.orderItemsAdd)
        self.ui.order_item_change.clicked.connect   (self.orderItemsChange)
        self.ui.order_item_delete.clicked.connect   (self.orderItemsDelete)
        self.ui.order_item_load.clicked.connect     (self.orderItemsLoad)

        self.orderItemsLoad()
        
        if self.order['status_code'] == 'active':
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    select
                        pb.quantity,
                        pb.order_id,
                        pb.product_id
                    from product_batches pb 
                    left join orders o on pb.order_id = o.id
                    left join products p on pb.product_id = p.id
                    where o.id = %(order_id)s
                """, {'order_id': self.order['id']})
                self.batches = cur.fetchall()

            close_button = QPushButton("Отменить")
            self.ui.order_actions.addWidget(close_button)
            close_button.clicked.connect(self.declineOrder)
            
            closed_ids = []

            print(self.orderItems)
            for item in self.orderItems:
                total_batch_quantity = sum(
                    batch['quantity'] for batch in self.batches 
                    if batch['product_id'] == item['product_id']
                )
                
                if total_batch_quantity >= item['quantity']:
                    closed_ids.append(item['id'])

            if len(closed_ids) == len(self.orderItems) and len(self.orderItems) > 0:
                close_button = QPushButton("Закрыть")
                self.ui.order_actions.addWidget(close_button)
                close_button.clicked.connect(self.closeOrder)
    
    def declineOrder(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            try:
                cur.execute("""
                    UPDATE orders 
                    SET status_id = (SELECT id FROM order_statuses WHERE code = 'cancelled')
                    WHERE id = %(order_id)s
                """, {'order_id': self.order['id']})
                conn.commit()
                self.accept()
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Ошибка", f"Ошибка при отмене заказа: {str(e)}")

    def closeOrder(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            try:
                cur.execute("BEGIN")
                
                for item in self.orderItems:
                    batch = list(filter(lambda x: x['product_id'] == item['product_id'], list(self.batches)))[0]
                    remaining_quantity = batch['quantity'] - item['quantity']
                    print(remaining_quantity)

                    if remaining_quantity < 0:
                        raise Exception("Не достаточно товара для закрытия заказа")
                    
                    if remaining_quantity > 0:
                        cur.execute("""
                            INSERT INTO product_batches (product_id, order_id, date, quantity)
                            VALUES (%(product_id)s, NULL, CURRENT_TIMESTAMP, %(remain)s)
                        """, {
                            'product_id': item['product_id'],
                            'remain': remaining_quantity
                        })

                    cur.execute("""
                        INSERT INTO product_batches (product_id, order_id, date, quantity)
                        VALUES (%(product_id)s, %(order_id)s, CURRENT_TIMESTAMP, %(total)s)
                    """, {
                        'order_id': self.order['id'],
                        'product_id': item['product_id'],
                        'total': item['quantity'] * (-1)
                    })

                cur.execute("""
                    UPDATE orders 
                    SET status_id = (SELECT id FROM order_statuses WHERE code = 'closed')
                    WHERE id = %(order_id)s
                """, {'order_id': self.order['id']})
                conn.commit()
                self.accept()
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Ошибка", f"Ошибка при закрытии заказа: {str(e)}")

    # region order_items

    def orderItemsAdd(self):
        dialog = OrderItemsAddDialog()
        products = self.getProducts()
        product_names = list(map(lambda p: p['name'], products))
        dialog.setProducts(product_names)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute("""
                        SELECT id, name
                        FROM products
                        where name = %(name)s
                    """, {"name": data['product_unit']})
                    
                    productData = cur.fetchone()
                    if productData is None:
                        raise Exception(f"Unit of measure with code '{data['unit']}' not found")
                
                    cur.execute("""
                        INSERT INTO order_items (order_id, product_id, quantity, price_at_sale)
                        VALUES (%(order_id)s, %(product_id)s, %(quantity)s, %(price_at_sale)s)
                    """, {
                        "order_id": self.order['id'],
                        "product_id": productData['id'],
                        "quantity": data['quantity'],
                        "price_at_sale": data['price_at_sale']
                    })
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(e)
                finally:
                    cur.close()
                    self.orderItemsLoad()

    def orderItemsChange(self):
        if not self.ui.order_item_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected = self.ui.order_item_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.order_item_list.model().data(selected_index, Qt.UserRole)

        dialog = OrderItemsChangeDialog(None, item)
        products = self.getProducts()
        product_names = list(map(lambda p: p['name'], products))
        dialog.setProducts(product_names)
        dialog.setDefault()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute("""
                        SELECT id, name
                        FROM products
                        where name = %(name)s
                    """, {"name": data['product_unit']})
                    
                    productData = cur.fetchone()
                    if productData is None:
                        raise Exception(f"Unit of measure with code '{data['unit']}' not found")
                
                    cur.execute("""
                        UPDATE order_items 
                        SET product_id = %(product_id)s,
                            quantity = %(quantity)s,
                            price_at_sale = %(price_at_sale)s
                        WHERE id = %(item_id)s AND order_id = %(order_id)s
                        RETURNING id
                    """, {
                        "item_id": item['id'],
                        "order_id": self.order['id'],
                        "product_id": productData['id'],
                        "quantity": int(data['quantity']),
                        "price_at_sale": float(data['price_at_sale'])
                    })
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(e)
                finally:
                    cur.close()
                    self.orderItemsLoad()

    def orderItemsDelete(self):
        if not self.ui.order_item_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected = self.ui.order_item_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.order_item_list.model().data(selected_index, Qt.UserRole)

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                delete from order_items
                where id = %(id)s
                returning id
            """, {'id': item['id']})
            
            cur.fetchone()
            conn.commit()
        self.orderItemsLoad()

    def orderItemsLoad(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    oi.id,
                    oi.price_at_sale as price_at_sale,
                    oi.quantity,
                    p."name" as product_name,
                    p.id as product_id
                from order_items oi
                left join products p on oi.product_id = p.id
                where oi.order_id = %(id)s
                order by id asc
            """, {'id': self.order['id']})
            self.orderItems = cur.fetchall()

        model = OrderItemsListModel(self.orderItems)
        self.ui.order_item_list.setModel(model)

    def getProducts(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, name
                FROM products
                ORDER BY name ASC
            """)
            return cur.fetchall()

    # endregion

    def setDefault(self):
        print(self.order)
        self.ui.order_date.setDate(self.order['date'])

        index = self.ui.order_customer_combo.findText(self.order['customer_name'])
        if index >= 0:
            self.ui.order_customer_combo.setCurrentIndex(index)

        index = self.ui.order_status_combo.findText(self.order['status_title'])
        if index >= 0:
            self.ui.order_status_combo.setCurrentIndex(index)

        index = self.ui.order_manager_combo.findText(self.order['manager_code'])
        if index >= 0:
            self.ui.order_manager_combo.setCurrentIndex(index)

# endregion

# region: material ui

class MaterialsListModel(QAbstractListModel):
    def __init__(self, materials=[]):
        super().__init__()
        self.materials = materials

    def rowCount(self, parent=QModelIndex()):
        return len(self.materials)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.materials):
            return None
        
        material = self.materials[index.row()]

        if role == Qt.DisplayRole:
            return f"{material['id']} | {material['name']} | Цена: {material['cost']} | Ед. изм: {material['unit_code']}"
        
        if role == Qt.UserRole:
            return material
        
        return None

class MaterialAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_material_add()
        self.ui.setupUi(self) 
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
    
    def getData(self):
        return {
            'name': self.ui.materialName.text().strip(),
            'unit': self.ui.materialUnits.currentText(),
            'cost': self.ui.materialCost.text().strip()
        }
    
    def validate(self):
        data = self.getData()

        if not data['name']:
            return False, "Введите название материала"
        
        if self.ui.materialUnits.currentIndex() == -1 or not data['unit']:
            return False, "Выберите единицы измерения"
        
        if not data['cost']:
            return False, "Введите цену материала"

        if not data['cost']:
            return False, "Введите стоимость материала"
        
        try:
            cost = int(data['cost'])
            if cost <= 0:
                return False, "Стоимость должна быть положительным числом"
            data['cost'] = cost
        except ValueError:
            return False, "Стоимость должна быть целым числом"
        
        return True, ""
    
    def setUnits(self, units_list):
        """Set available units in the combo box"""
        self.ui.materialUnits.clear()
        self.ui.materialUnits.addItems(units_list)

    def accept(self):
        is_valid, error_msg = self.validate()
        
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_msg)
            return
        
        super().accept()

class MaterialChangeDialog(MaterialAddDialog):
    def __init__(self, parent=None, material=object):
        super().__init__(parent)
        self.material = material

    def setDefault(self):
        self.ui.materialName.setText(self.material['name'])
        self.ui.materialCost.setText(str(round(self.material['cost'])))

        index = self.ui.materialUnits.findText(self.material['unit_code'])
        if index >= 0:
            self.ui.materialUnits.setCurrentIndex(index)

# endregion 

# region employee ui

class EmployeeListModel(QAbstractListModel):
    def __init__(self, employee=[]):
        super().__init__()
        self.employee = employee

    def rowCount(self, parent=QModelIndex):
        return len(self.employee)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.employee):
            return None
        
        employee = self.employee[index.row()]

        if role == Qt.DisplayRole:
            return f"{employee['id']} | {employee['first_name']} | {employee['last_name']} | Телефон: {employee['phone']} | Почта: {employee['email']}"
        
        if role == Qt.UserRole:
            return employee
        
        return None

class EmployeeAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_add_employee()
        self.ui.setupUi(self) 
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
    
    def getData(self):
        return {
            'first_name': self.ui.first_name.text().strip(),  # string, exist, not null
            'last_name': self.ui.last_name.text().strip(),    # string, exist, not null
            'family_name': self.ui.family_name.text().strip(), # string, exist, not null
            'email': self.ui.email.text().strip(),            # string, not null, should contain @ and domain
            'phone': self.ui.phone.text().strip(),            # string
            'address': self.ui.address.text().strip(),        # string
            'position_title': self.ui.position_combo.currentText(), # string (from combo box)
            'login': self.ui.login.text().strip(),
            'password': self.ui.password.text().strip(),
            'blocked': self.ui.blocked_combo.currentText() == 'Да' if True else False
        }
    
    def validate(self):
        data = self.getData()
        
        if not data['first_name']:
            return False, "Введите имя сотрудника"
        
        if not data['last_name']:
            return False, "Введите фамилию сотрудника"
        
        if not data['family_name']:
            return False, "Введите отчество сотрудника"
        
        if not data['email']:
            return False, "Введите email сотрудника"
        
        if '@' not in data['email']:
            return False, "Email должен содержать символ '@'"
        
        local_part, domain = data['email'].split('@', 1)
        if not domain or '.' not in domain:
            return False, "Email должен содержать домен (например, @example.com)"
        
        if self.ui.position_combo.currentIndex() == -1 or not data['position_title']:
            return False, "Выберите должность сотрудника"
        
        return True, ""
    
    def setPositions(self, positions_list):
        """Set available positions in the combo box"""
        self.ui.position_combo.clear()
        self.ui.position_combo.addItems(positions_list)
    
    def checkLoginUnique(self, login):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    e.id,
                    e.login
                from employees e
                where e.login = %(login)s
            """, {'login': login})
            potentialUser = cur.fetchone()
            if potentialUser:
                QMessageBox.warning(self, "Ошибка", "Этот логин уже занят")
                return False
        return True

    def accept(self):
        data = self.getData()
        is_valid, error_msg = self.validate()

        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_msg)
            return

        if not data['password']:
            QMessageBox.warning(self, "Ошибка", "Поле пароль не может быть пустым")
            return

        if not data['login']:
            QMessageBox.warning(self, "Ошибка", "Поле логин не может быть пустым")
            return
        
        if not self.checkLoginUnique(data['login']):
            return

        super().accept()

class EmployeeChangeDialog(EmployeeAddDialog):
    def __init__(self, parent=None, employee=None):
        super().__init__(parent)
        self.employee = employee
    
    def setDefault(self):
        self.ui.first_name.setText(self.employee['first_name'])
        self.ui.last_name.setText(self.employee['last_name'])
        self.ui.family_name.setText(self.employee['family_name'])
        self.ui.email.setText(self.employee['email'])
        self.ui.phone.setText(self.employee['phone'] if self.employee['phone'] else '')
        self.ui.address.setText(self.employee['address'] if self.employee['address'] else '')
        self.ui.login.setText(self.employee['login'])
        self.ui.password.setText(self.employee['password'])
        
        index = self.ui.blocked_combo.findText('Да' if self.employee['blocked'] == True else 'Нет')
        if index >= 0:
            self.ui.blocked_combo.setCurrentIndex(index)

        index = self.ui.position_combo.findText(self.employee['position_title'])
        if index >= 0:
            self.ui.position_combo.setCurrentIndex(index)

    def checkLoginUnique(self, login):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    e.id,
                    e.login
                from employees e
                where e.login = %(login)s
            """, {'login': login})
            potentialUser = cur.fetchone()
            if potentialUser and potentialUser['id'] != self.employee['id']:
                QMessageBox.warning(self, "Ошибка", "Этот логин уже занят")
                return False
        return True

# endregion

# region customers ui

class CustomerListModel(QAbstractListModel):
    def __init__(self, customers=[]):
        super().__init__()
        self.customers = customers

    def rowCount(self, parent=QModelIndex):
        return len(self.customers)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.customers):
            return None
        
        customer = self.customers[index.row()]

        if role == Qt.DisplayRole:
            buyer_status = "Покупатель" if customer['buyer'] else "Не покупатель"
            salesman_status = "Продавец" if customer['salesman'] else "Не продавец"
            return f"{customer['id']} | {customer['name']} | ИНН: {customer['inn']} | {buyer_status} | {salesman_status}"
        
        if role == Qt.UserRole:
            return customer
        
        return None

class CustomerAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_add_customer()
        self.ui.setupUi(self) 
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
    
    def getData(self):
        return {
            'name': self.ui.name.text().strip(),
            'inn': self.ui.inn.text().strip(),
            'email': self.ui.email.text().strip(),
            'phone': self.ui.phone.text().strip(),
            'address': self.ui.address.text().strip(),
            'buyer': self.ui.buyer_combo.currentText() == "Да",
            'salesman': self.ui.salesman_combo.currentText() == "Да"
        }
    
    def validate(self):
        data = self.getData()
        
        if not data['name']:
            return False, "Введите название организации"
        
        if not data['inn']:
            return False, "Введите ИНН"
        
        if len(data['inn']) != 10 and len(data['inn']) != 12:
            return False, "ИНН должен содержать 10 или 12 цифр"
        
        if not data['inn'].isdigit():
            return False, "ИНН должен содержать только цифры"
        
        if data['email'] and '@' not in data['email']:
            return False, "Email должен содержать символ '@'"
        
        if data['email']:
            local_part, domain = data['email'].split('@', 1)
            if not domain or '.' not in domain:
                return False, "Email должен содержать домен (например, @example.com)"
        
        return True, ""
    
    def accept(self):
        is_valid, error_msg = self.validate()
        
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_msg)
            return
        
        super().accept()

class CustomerChangeDialog(CustomerAddDialog):
    def __init__(self, parent=None, customer=None):
        super().__init__(parent)
        self.customer = customer
        self.setDefault()
    
    def setDefault(self):
        self.ui.name.setText(self.customer['name'] if self.customer['name'] else '')
        self.ui.inn.setText(self.customer['inn'] if self.customer['inn'] else '')
        self.ui.email.setText(self.customer['email'] if self.customer['email'] else '')
        self.ui.phone.setText(self.customer['phone'] if self.customer['phone'] else '')
        self.ui.address.setText(self.customer['address'] if self.customer['address'] else '')
        
        self.ui.buyer_combo.setCurrentText("Да" if self.customer['buyer'] else "Нет")
        self.ui.salesman_combo.setCurrentText("Да" if self.customer['salesman'] else "Нет")

# endregion

# region product_baches ui

class ProductBatchListModel(QAbstractListModel):
    def __init__(self, batches=[]):
        super().__init__()
        self.batches = batches

    def rowCount(self, parent=QModelIndex):
        return len(self.batches)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.batches):
            return None
        
        batch = self.batches[index.row()]

        if role == Qt.DisplayRole:
            date_str = batch['date'].strftime("%d.%m.%Y %H:%M") if batch['date'] else "Нет даты"
            return f"{batch['id']} | {batch['product_name']} | {batch['order_number']} | {date_str} | Количество: {batch['quantity']}"
        
        if role == Qt.UserRole:
            return batch
        
        return None

class ProductBatchAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_add_product_batch()
        self.ui.setupUi(self) 
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.ui.date.setDate(QDate.currentDate())
    
    def getData(self):
        date_value = self.ui.date.dateTime().toPython() if hasattr(self.ui.date, 'dateTime') else self.ui.date.dateTime()
        return {
            'product': self.ui.product_combo.currentText(),
            'order': self.ui.order_combo.currentText(),
            'date': date_value,
            'quantity': self.ui.quantity.text()
        }
    
    def validate(self):
        data = self.getData()
        
        if not data['product'] or self.ui.product_combo.currentIndex() == -1:
            return False, "Выберите продукт"
        
        if not data['order'] or self.ui.order_combo.currentIndex() == -1:
            return False, "Выберите заказ"
        
        if not data['date']:
            return False, "Выберите дату"
        
        if int(data['quantity']) <= 0:
            return False, "Количество должно быть больше 0"
        
        return True, ""
    
    def setProducts(self, products_list):
        """Set available products in the combo box"""
        self.ui.product_combo.clear()
        self.ui.product_combo.addItems(products_list)
    
    def setOrders(self, orders_list):
        """Set available orders in the combo box"""
        self.ui.order_combo.clear()
        self.ui.order_combo.addItems(orders_list)
    
    def accept(self):
        is_valid, error_msg = self.validate()
        
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_msg)
            return
        
        super().accept()

class ProductBatchChangeDialog(ProductBatchAddDialog):
    def __init__(self, parent=None, batch=None):
        super().__init__(parent)
        self.batch = batch
    
    def setDefault(self):
        index = self.ui.product_combo.findText(self.batch['product_name'])
        if index >= 0:
            self.ui.product_combo.setCurrentIndex(index)
        
        index = self.ui.order_combo.findText(
            f"Заказ №{self.batch['order_number']} от {self.batch['date'].strftime('%d.%m.%Y')} - {self.batch['customer_name']}"
        )
        if index >= 0:
            self.ui.order_combo.setCurrentIndex(index)
        
        if self.batch['date']:
            self.ui.date.setDateTime(QDateTime.fromString(self.batch['date'].strftime("%Y-%m-%d %H:%M:%S"), "yyyy-MM-dd hh:mm:ss"))
        
        self.ui.quantity.setText(str(round(self.batch['quantity'])))


# endregion

# region product ui

class ProductListModel(QAbstractListModel):
    def __init__(self, products=[]):
        super().__init__()
        self.products = products

    def rowCount(self, parent=QModelIndex()):
        return len(self.products)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.products):
            return None
        
        product = self.products[index.row()]

        if role == Qt.DisplayRole:
            return f"{product['id']} | {product['name']} | Цена: {product['default_price']} | Ед. изм: {product['unit_code']}"
        
        if role == Qt.UserRole:
            return product
        
        return None

class ProductAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_add_product()
        self.ui.setupUi(self) 
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)

        self.ui.bill_of_material_list.setEnabled(False)
        self.ui.bill_of_material_load.setEnabled(False)
        self.ui.bill_of_material_add.setEnabled(False)
        self.ui.bill_of_material_delete.setEnabled(False)
        self.ui.bill_of_material_change.setEnabled(False)

    def getData(self):
        return {
            'name': self.ui.product_name.text().strip(),
            'unit': self.ui.product_unit_combo.currentText(),
            'code': self.ui.product_code.text().strip(),
            'description': self.ui.product_description.text().strip(),
            'default_price': self.ui.product_default_price.text().strip()
        }
    
    def validate(self):
        data = self.getData()

        if not data['name']:
            return False, "Введите название продукта"
        
        if self.ui.product_unit_combo.currentIndex() == -1 or not data['unit']:
            return False, "Выберите единицы измерения"
        
        if not data['code']:
            return False, "Введите код"

        if not data['default_price']:
            return False, "Введите базовую цену"

        try:
            default_price = int(data['default_price'])
            if default_price <= 0:
                return False, "Базовую цену должна быть положительным числом"
            data['default_price'] = default_price
        except ValueError:
            return False, "Базовую цену должна быть целым числом"
        
        return True, ""
    
    def setUnits(self, list):
        """Set available units in the combo box"""
        self.ui.product_unit_combo.clear()
        self.ui.product_unit_combo.addItems(list)

    def accept(self):
        is_valid, error_msg = self.validate()
        
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_msg)
            return
        
        super().accept()

class ProductChangeDialog(ProductAddDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product

        self.ui.bill_of_material_list.setEnabled(True)
        self.ui.bill_of_material_load.setEnabled(True)
        self.ui.bill_of_material_add.setEnabled(True)
        self.ui.bill_of_material_delete.setEnabled(True)
        self.ui.bill_of_material_change.setEnabled(True)
    
        self.ui.bill_of_material_load.clicked.connect(self.billOfMaterialLoad)
        self.ui.bill_of_material_add.clicked.connect(self.billOfMaterialAdd)
        self.ui.bill_of_material_delete.clicked.connect(self.billOfMaterialDelete)
        self.ui.bill_of_material_change.clicked.connect(self.billOfMaterialChange)
    
    # region bill_of_material

    def getMaterials(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    m.id,
                    m.name,
                    uom.code as material_unit_code
                from materials m
                left join units_of_measures uom on uom.id = m.unit_of_measure_id
            """)
            materials = cur.fetchall()

        return materials

    def billOfMaterialAdd(self):
        dialog = BillOfMaterialAddDialog()
        units = self.getMaterials()
        dialog.setMaterials(list(map(lambda u: u['name'], list(units))))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute("""
                        SELECT
                            m.id
                        FROM materials m
                        WHERE m.name = %(name)s
                    """, {"name": data['material_name']})
                    
                    materialData = cur.fetchone()
                    if materialData is None:
                        raise Exception(f"Unit of measure with code '{data['unit']}' not found")
                
                    cur.execute("""
                        INSERT INTO bill_of_material (product_id, material_id, quantity)
                        VALUES (%(product_id)s, %(material_id)s, %(quantity)s)
                    """, {
                        "product_id": self.product['id'],
                        "material_id": materialData['id'],
                        "quantity": float(data['quantity'])
                    })
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(e)
                finally:
                    cur.close()
                    self.billOfMaterialLoad()

    def billOfMaterialDelete(self):
        if not self.ui.bill_of_material_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected = self.ui.bill_of_material_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.bill_of_material_list.model().data(selected_index, Qt.UserRole)

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                update bill_of_material
                set deleted = true
                WHERE id = %s
                RETURNING id
            """, (item['id'],))
            
            cur.fetchone()
            conn.commit()
        self.billOfMaterialLoad()

    def billOfMaterialChange(self):
        if not self.ui.bill_of_material_list.selectionModel(): 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected = self.ui.bill_of_material_list.selectionModel().selectedIndexes()
        
        if not selected: 
            QMessageBox.warning(self, "Ошибка", "Выберете элемент")
            return
        
        selected_index = selected[0]
        item = self.ui.bill_of_material_list.model().data(selected_index, Qt.UserRole)

        dialog = BillOfMaterialChangeDialog(None, item)
        units = self.getMaterials()
        dialog.setMaterials(list(map(lambda u: u['name'], list(units))))
        dialog.setDefault()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.getData()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT
                        m.id
                    FROM materials m
                    WHERE m.name = %(name)s
                """, {"name": data['material_name']})
                
                materialData = cur.fetchone()
                if materialData is None:
                    raise Exception(f"Unit of measure with code '{data['unit']}' not found")
                
                cur.execute("""
                    UPDATE bill_of_material
                    SET material_id = %(material_id)s, 
                        quantity = %(quantity)s
                    WHERE id = %(id)s
                    RETURNING id
                """, {
                    'id': item['id'], 
                    'material_id': materialData['id'], 
                    'quantity': float(data['quantity'])
                })
                cur.fetchone()
                conn.commit()
            self.billOfMaterialLoad()

    def billOfMaterialLoad(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    bom2.id,
                    bom2.quantity,
                    m."name" as material_name,
                    uom.code as material_unit_code
                from bill_of_material bom2
                left join materials m on bom2.material_id = m.id
                left join units_of_measures uom on m.unit_of_measure_id = uom.id
                where bom2.product_id = %(product_id)s and bom2.deleted = false
            """, {'product_id': self.product['id']})
            bilOfMaterials = cur.fetchall()

        model = BillOfMaterialListModel(bilOfMaterials)
        self.ui.bill_of_material_list.setModel(model)

    # endregion

    def setDefault(self):
        self.ui.product_name.setText(self.product['name'])
        self.ui.product_description.setText(self.product['description'])
        self.ui.product_code.setText(self.product['code'])
        self.ui.product_default_price.setText(str(round(self.product['default_price'])))
        
        index = self.ui.product_unit_combo.findText(self.product['unit_code'])
        if index >= 0:
            self.ui.product_unit_combo.setCurrentIndex(index)

# endregion

# region bill_of_material ui

class BillOfMaterialListModel(QAbstractListModel):
    def __init__(self, billOfMaterials=[]):
        super().__init__()
        self.billOfMaterials = billOfMaterials

    def rowCount(self, parent=QModelIndex()):
        return len(self.billOfMaterials)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.billOfMaterials):
            return None
        
        billOfMaterial = self.billOfMaterials[index.row()]

        if role == Qt.DisplayRole:
            return f"{billOfMaterial['id']} | Кол-во: {billOfMaterial['quantity']} | Материал: {billOfMaterial['material_name']} | Ед. изм: {billOfMaterial['material_unit_code']}"
        
        if role == Qt.UserRole:
            return billOfMaterial
        
        return None

class BillOfMaterialAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_bill_of_material()
        self.ui.setupUi(self) 
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
    
    def getData(self):
        return {
            'quantity': self.ui.quantity.text().strip(),
            'material_name': self.ui.material_combo.currentText(),
        }
    
    def validate(self):
        data = self.getData()

        if self.ui.material_combo.currentIndex() == -1 or not data['material_name']:
            return False, "Выберите единицы измерения"
        
        if not data['quantity']:
            return False, "Введите кол-во материала"

        try:
            quantity = float(data['quantity'])
            if quantity <= 0:
                return False, "Количество должно быть положительным числом"
            data['quantity'] = quantity
        except ValueError:
            return False, "Стоимость должна быть целым числом"
        
        return True, ""
    
    def setMaterials(self, list):
        """Set available units in the combo box"""
        self.ui.material_combo.clear()
        self.ui.material_combo.addItems(list)

    def accept(self):
        is_valid, error_msg = self.validate()
        
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_msg)
            return
        
        super().accept()

class BillOfMaterialChangeDialog(BillOfMaterialAddDialog):
    def __init__(self, parent=None, billOfMaterial=object):
        super().__init__(parent)
        self.billOfMaterial = billOfMaterial

    def setDefault(self):
        self.ui.quantity.setText(str(self.billOfMaterial['quantity']))

        index = self.ui.material_combo.findText(self.billOfMaterial['material_name'])
        if index >= 0:
            self.ui.material_combo.setCurrentIndex(index)

# endregion

# region order_items ui

class OrderItemsListModel(QAbstractListModel):
    def __init__(self, orderItems=[]):
        super().__init__()
        self.orderItems = orderItems

    def rowCount(self, parent=QModelIndex()):
        return len(self.orderItems)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.orderItems):
            return None
        
        orderItem = self.orderItems[index.row()]

        if role == Qt.DisplayRole:
            return f"{orderItem['id']} | Кол-во: {orderItem['quantity']} | Продукт: {orderItem['product_name']} | Цена: {orderItem['price_at_sale']}"
        
        if role == Qt.UserRole:
            return orderItem
        
        return None

class OrderItemsAddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_order_item()
        self.ui.setupUi(self) 
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
    
    def getData(self):
        return {
            'quantity': self.ui.quantity.text().strip(),
            'price_at_sale': self.ui.price_at_sale.text().strip(),
            'product_unit': self.ui.product_combo.currentText()
        }
    
    def validate(self):
        data = self.getData()

        if self.ui.product_combo.currentIndex() == -1 or not data['product_unit']:
            return False, "Выберите единицы измерения"
        
        try:
            quantity = int(data['quantity'])
            if quantity <= 0:
                return False, "Количество должно быть положительным числом"
            data['quantity'] = quantity
        except ValueError:
            return False, "Кол-во должна быть целым числом"

        try:
            price_at_sale = float(data['price_at_sale'])
            if price_at_sale <= 0:
                return False, "Количество должно быть положительным числом"
            data['price_at_sale'] = price_at_sale
        except ValueError:
            return False, "Стоимость должна быть целым числом"
        
        return True, ""
    
    def setProducts(self, list):
        """Set available units in the combo box"""
        self.ui.product_combo.clear()
        self.ui.product_combo.addItems(list)

    def accept(self):
        is_valid, error_msg = self.validate()
        
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", error_msg)
            return
        
        super().accept()

class OrderItemsChangeDialog(OrderItemsAddDialog):
    def __init__(self, parent=None, orderItem=object):
        super().__init__(parent)
        self.orderItem = orderItem

    def setDefault(self):
        self.ui.quantity.setText(str(self.orderItem['quantity']))
        self.ui.price_at_sale.setText(str(self.orderItem['price_at_sale']))

        index = self.ui.product_combo.findText(self.orderItem['product_name'])
        if index >= 0:
            self.ui.product_combo.setCurrentIndex(index)

# endregion

# region auth

class CaptchaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_captcha()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowType.Dialog)

        self.one_image = QPixmap("icons/1.png")
        self.one_image = self.one_image.scaled(QSize(150,150))
        self.two_image = QPixmap("icons/2.png")
        self.two_image = self.two_image.scaled(QSize(150,150))
        self.three_image = QPixmap("icons/4.png")
        self.three_image = self.three_image.scaled(QSize(150,150))
        self.fourth_image = QPixmap("icons/3.png")
        self.fourth_image = self.fourth_image.scaled(QSize(150,150))

        if self.one_image.isNull():
            print("Failed to load image: :/icons/1.png")

        self.ui.next_button.clicked.connect(self.nextClicked)
        self.set_i = 1
        self.setImage()
        
        self.curr_try = 1

    def nextClicked(self):
        self.nextSet()
        self.setImage()

    def setImage(self):
        if self.set_i == 0:
            self.ui.one.setPixmap(self.one_image)
            self.ui.two.setPixmap(self.two_image)
            self.ui.three.setPixmap(self.three_image)
            self.ui.fourth.setPixmap(self.fourth_image)
        elif self.set_i == 1:
            self.ui.two.setPixmap(self.one_image)
            self.ui.three.setPixmap(self.two_image)
            self.ui.fourth.setPixmap(self.three_image)
            self.ui.one.setPixmap(self.fourth_image)
        elif self.set_i == 2:
            self.ui.three.setPixmap(self.one_image)
            self.ui.fourth.setPixmap(self.two_image)
            self.ui.one.setPixmap(self.three_image)
            self.ui.two.setPixmap(self.fourth_image)
        elif self.set_i == 3:
            self.ui.fourth.setPixmap(self.one_image)
            self.ui.one.setPixmap(self.two_image)
            self.ui.two.setPixmap(self.three_image)
            self.ui.three.setPixmap(self.fourth_image)

    def nextSet(self):
        self.set_i = (self.set_i + 1) % 4

    def isRight(self):
        if self.set_i == 0:
            return True
        return False

class AuthDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_auth()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Dialog)

        self.ui.login_button.clicked.connect(self.loginClicked)

    def loginClicked(self):
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()

        if not login:
            QMessageBox.warning(self, "Ошибка", "Поле логин пустое")
            return
        
        if not password:
            QMessageBox.warning(self, "Ошибка", "Поле пароль пустое")
            return

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                select
                    e.id,
                    e.login,
                    e.password,
                    e.blocked,
                    er.code as role_code
                from employees e
                left join employee_roles er on er.id = e.role_id
                where e.login = %(login)s and e.password = %(password)s
            """, {'login': login, 'password': password})
            self.user = cur.fetchone()

        if self.user is None:
            QMessageBox.warning(self, "Ошибка", "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные")
            return
        
        if self.user['blocked'] == True:
            QMessageBox.warning(self, "Ошибка", "Вы заблокированы. Обратитесь к администратору")
            return
        
        captcha = CaptchaDialog()
        if captcha.exec() == QDialog.DialogCode.Accepted:
            isRight = captcha.isRight()
            if not isRight:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        select
                            e.failed_attempts
                        from employees e
                        where e.id = %(id)s
                    """, {'id': self.user['id']})
                    attempts = cur.fetchone()
                
                attempts['failed_attempts'] += 1

                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        update employees
                        set failed_attempts = %(attempts)s
                        where id = %(id)s
                    """, {'id': self.user['id'], 'attempts': attempts['failed_attempts']})
                    conn.commit()

                if attempts['failed_attempts'] >= 3:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute("""
                            update employees
                            set blocked = true
                            where id = %(id)s
                        """, {'id': self.user['id']})
                        conn.commit()
                    QMessageBox.warning(self, "Ошибка", "Вы заблокированы. Обратитесь к администратору")
                    return
                else:
                    QMessageBox.warning(self, "Ошибка", "Капча не пройдена, повторите попытку")
                    return
            else:
                QMessageBox.information(self, "Инфо", "Вы успешно авторизовались")
        else:
            QMessageBox.warning(self, "Ошибка", "Повторите ввод каптчи")
            return

        super().accept()

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

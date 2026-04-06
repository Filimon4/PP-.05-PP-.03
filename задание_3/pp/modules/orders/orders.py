from PySide6.QtWidgets import QDialog, QMessageBox, QPushButton
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QDate 
from modules.orders.ui_order import Ui_order
from common.db import conn
from psycopg2.extras import RealDictCursor
from modules.order_items.order_items import OrderItemsAddDialog, OrderItemsChangeDialog, OrderItemsListModel

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

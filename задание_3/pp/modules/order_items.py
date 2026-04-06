
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from ui_order_item import Ui_order_item

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

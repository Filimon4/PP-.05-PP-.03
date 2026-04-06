from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QDateTime, QDate 
from PySide6.QtGui import QPixmap
from modules.product_baches.ui_product_batch import Ui_add_product_batch
from common.messageBox import MessageBox

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
        self.setWindowIcon(QPixmap('icons/house-with-window.png'))
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
            MessageBox.warning(self, "Ошибка", error_msg)
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


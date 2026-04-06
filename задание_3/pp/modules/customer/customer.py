from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtGui import QPixmap
from modules.customer.ui_add_customer import Ui_add_customer
from common.messageBox import MessageBox

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
        self.setWindowIcon(QPixmap('icons/house-with-window.png'))
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
            MessageBox.warning(self, "Ошибка", error_msg)
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

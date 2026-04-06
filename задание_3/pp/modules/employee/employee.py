from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from modules.employee.ui_add_employee import Ui_add_employee
from common.db import conn
from psycopg2.extras import RealDictCursor

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

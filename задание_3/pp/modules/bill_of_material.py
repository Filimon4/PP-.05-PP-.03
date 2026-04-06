from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex 
from ui_bill_of_material import Ui_bill_of_material

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

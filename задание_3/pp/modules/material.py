from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from ui_material_add import Ui_material_add

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

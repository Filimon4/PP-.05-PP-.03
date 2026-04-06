from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex, QDateTime, QDate, QSize 
from ui_add_product import Ui_add_product
from common.db import conn
from psycopg2.extras import RealDictCursor
from modules.bill_of_material import BillOfMaterialAddDialog, BillOfMaterialChangeDialog, BillOfMaterialListModel

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

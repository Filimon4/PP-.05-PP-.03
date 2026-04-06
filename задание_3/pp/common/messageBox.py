from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap, QIcon

class MessageBox(QMessageBox):
    @staticmethod
    def information(parent, title, text):
        msg = QMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setWindowIcon(QPixmap('icons/info.png'))
        
        return msg.exec()
    
    @staticmethod
    def warning(parent, title, text):
        msg = QMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setWindowIcon(QPixmap('icons/warning.png'))
        
        return msg.exec()
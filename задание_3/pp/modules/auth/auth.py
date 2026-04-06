from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt 
from ui_auth import Ui_auth
from common.db import conn
from psycopg2.extras import RealDictCursor
from auth.captcha import CaptchaDialog

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

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from modules.auth.ui_auth import Ui_auth
from common.db import conn
from psycopg2.extras import RealDictCursor
from modules.auth.capcha.captcha import CaptchaDialog
from common.messageBox import MessageBox

class AuthDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QPixmap("icons/house-with-window.png"))

        self.ui = Ui_auth()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Dialog)

        self.ui.login_button.clicked.connect(self.loginClicked)

    def loginClicked(self):
        login = self.ui.login_input.text()
        password = self.ui.password_input.text()

        if not login:
            MessageBox.warning(self, "Ошибка", "Поле логин пустое")
            return
        
        if not password:
            MessageBox.warning(self, "Ошибка", "Поле пароль пустое")
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
                where e.login = %(login)s
            """, {'login': login})
            self.user = cur.fetchone()

        if self.user['password'] != password:
            MessageBox.warning(self, "Ошибка", "Вы ввели неверный пароль. Пожалуйста проверьте ещё раз введенные данные")
            attempts = self.incFailedAttempts()
            if attempts >= 3:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        update employees
                        set blocked = true
                        where id = %(id)s
                    """, {'id': self.user['id']})
                    conn.commit()
                MessageBox.warning(self, "Ошибка", "Вы заблокированы. Обратитесь к администратору")
            return
        
        if self.user['blocked'] == True:
            MessageBox.warning(self, "Ошибка", "Вы заблокированы. Обратитесь к администратору")
            return
        
        captcha = CaptchaDialog()
        if captcha.exec() == QDialog.DialogCode.Accepted:
            isRight = captcha.isRight()
            if not isRight:
                attempts = self.incFailedAttempts()
                if attempts >= 3:
                    with conn.cursor(cursor_factory=RealDictCursor) as cur:
                        cur.execute("""
                            update employees
                            set blocked = true
                            where id = %(id)s
                        """, {'id': self.user['id']})
                        conn.commit()
                    MessageBox.warning(self, "Ошибка", "Вы заблокированы. Обратитесь к администратору")
                    return
                else:
                    MessageBox.warning(self, "Ошибка", "Капча не пройдена, повторите попытку")
                    return
            else:
                MessageBox.information(self, "Инфо", "Вы успешно авторизовались")
        else:
            MessageBox.warning(self, "Ошибка", "Повторите ввод каптчи")
            return

        self.resetFailedAttempts()

        super().accept()

    def incFailedAttempts(self):
        print(self.user)

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
        
        return attempts['failed_attempts']

    def resetFailedAttempts(self):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                update employees
                set failed_attempts = 0
                where id = %(id)s
            """, {'id': self.user['id']})
            conn.commit()

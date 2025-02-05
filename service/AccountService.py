from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from dao.AccountDao import AccountDao

'''
класс sevice отвечает за работу с dao и данными account
'''
class AccountService:
    
    def __init__(self, dao: AccountDao):
        super().__init__()
        self.dao = dao

    def login(self, email: str, password: str):
        account = self.dao.select_account_by_email(email)
        if account and check_password_hash(account[0][9], password):
            return account[0]
        return None
    
    def registration(self, firstname, lastname, email, phone, birth, password_hash, new_avatar_filename):
        dict  = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "phone": phone,
            "birth": birth,
            "date_reg": datetime.date.today(),
            "role_id": 1,
            "password": password_hash,
            "avatar": new_avatar_filename
        }
        return self.dao.insert(dict)
    
    def exists(self, email: str):
        return self.dao.exists_account_by_email(email)
    
    def get_account_by_id(self, id: str):
        return self.dao.select_account_by_id(id)
    
    def update_account(self, id, firstname, lastname, email, phone, birth, password_hash, avatar_filename):
        account_data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "phone": phone,
            "birth": birth,
            "password": password_hash,
            "avatar": avatar_filename
        }
        self.dao.update_account_by_id(account_data,id)
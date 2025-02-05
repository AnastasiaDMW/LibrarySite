from dao.CommonDao import CommonDao
from database.LibraryDatabase import LibraryDatabase

'''
класс dao отвечающий за таблицу account в базе данных
'''
class AccountDao(CommonDao):
    
    def __init__(self, db: LibraryDatabase):
        super().__init__(db)
    
    def _get_table_name(self):
        return 'account'
        
    def exists_account_by_email(self, email: str):
        return self._exists(f"email = '{email}'")
    
    def select_account_by_email(self, email: str):
        return self._select_all(f"email = '{email}'")
    
    def select_account_by_id(self, id: str):
        account: list = self._select_all(f"id = '{id}'")
        if len(account) > 0:
            return account[0]
        return None
    
    def update_account_by_id(self, data: dict, id: str):
        self._update(data, f"id = {id}")
        
    def update_account_by_id(self, data: dict, id: str):
        self._update(data, f"id = {id}")
        
from dao.HistoryOfIssuanceDao import HistoryOfIssuanceDao
import datetime

'''
класс sevice отвечает за работу с dao и данными history_of_issuance
'''
class HistoryOfIssuanceService:
    
    def __init__(self, dao: HistoryOfIssuanceDao):
        super().__init__()
        self.dao = dao
        
    def exists_in_history(self, book_id: str, account_id: str):
        return self.dao.exists_in_history(book_id, account_id)
    
    def add_history_issuence(self, account_id: str, book_id: str):
        history_issuence_data = {
            "account_id": account_id,
            "book_id": book_id,
            "start_date": datetime.date.today(),
            "is_read": False
        }
        self.dao.insert(history_issuence_data)
        
    def get_history_issuence_by_account_id(self, account_id: str):
        return self.dao.select_history_issuence_by_account_id(account_id)
    
    def get_count_history_issuence(self, account_id: str):
        return self.dao.count_history_issuence(account_id)
    
    def get_history_request_by_book_ids(self, book_ids: str, account_id: str, per_page: str, page: str):
        return self.dao.select_history_issuance_by_books_ids_by_account_id(book_ids, account_id, per_page, page)
    
    def update_history_issuence_is_read(self, account_id: str, book_id: str, is_read: str):
        history_issuence = {
            "is_read": is_read
        }
        self.dao.update_history_issuence_is_read_by_account_id_by_book_id(history_issuence, account_id, book_id)
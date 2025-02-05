from dao.HistoryRequestDao import HistoryRequestDao

'''
класс sevice отвечает за работу с dao и данными history_request
'''
class HistoryRequestService:
    
    def __init__(self, dao: HistoryRequestDao):
        super().__init__()
        self.dao = dao
        
    def exists(self, book_id: str, account_id: str):
        return self.dao.exists_by_book_id_and_account_id(book_id, account_id)
    
    def get_history_request_by_book_ids(self, chapter_id: str, per_page: str, page: str):
        return self.dao.select_history_request_by_books_ids(chapter_id, per_page, page)
    
    def get_count_history_request_by_book_ids(self, chapter_id: str):
        return self.dao.select_count_request_by_books_ids(chapter_id)
    
    def delete_history_request_by_history_request_id(self, history_request_id: str):
        self.dao.delete_history_request(history_request_id)
            
    def add_history_request(self, book_id: str, account_id: str):
        history_request_data = {
            "book_id": book_id,
            "account_id": account_id
        }
        self.dao.insert(history_request_data)
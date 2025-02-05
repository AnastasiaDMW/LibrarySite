from dao.CommonDao import CommonDao
from database.LibraryDatabase import LibraryDatabase

'''
класс dao отвечающий за таблицу history_request в базе данных
'''
class HistoryRequestDao(CommonDao):
    
    def __init__(self, db: LibraryDatabase):
        super().__init__(db)
        self.select_with_join = '''
            SELECT a.id, a.firstname, a.lastname, a.email, b.id, b.title, b.author, hr.id 
            FROM history_request hr 
            JOIN book b ON hr.book_id = b.id 
            JOIN account a ON hr.account_id = a.id 
            WHERE b.chapter_id = %s
            LIMIT %s OFFSET %s
        '''
        self.select_count_with_join = '''
            SELECT count(*) 
            FROM history_request hr 
            JOIN book b ON hr.book_id = b.id 
            JOIN account a ON hr.account_id = a.id 
            WHERE b.chapter_id = %s
        '''
        
    def _get_table_name(self):
        return 'history_request'
        
    def exists_by_book_id_and_account_id(self, book_id: str, account_id: str):
        return self._exists(f"book_id = {book_id} AND account_id = {account_id}")
    
    def select_history_request_by_books_ids(self, chapter_id: str, per_page: str, page: str):
        offset = (page - 1) * per_page
        return self._execute_request_all(self.select_with_join % (chapter_id, per_page, offset))
    
    def select_count_request_by_books_ids(self, chapter_id: str):
        return self._execute_request_all(self.select_count_with_join % (chapter_id))[0][0]
    
    def delete_history_request(self, history_request_id: str):
        self._delete(f"id = {history_request_id}")
from dao.CommonDao import CommonDao
from database.LibraryDatabase import LibraryDatabase

'''
класс dao отвечающий за таблицу history_of_issuance в базе данных
'''
class HistoryOfIssuanceDao(CommonDao):
    
    def __init__(self, db: LibraryDatabase):
        super().__init__(db)
        self.count_history_issuence_with_where_template = 'SELECT COUNT(*) FROM %s WHERE %s'
        self.select_with_join = '''
            SELECT hoi.id, hoi.start_date, hoi.is_read, c.title, b.* FROM history_of_issuance hoi 
            JOIN book b ON b.id = hoi.book_id
            JOIN chapter c ON b.chapter_id = c.id 
            WHERE hoi.book_id IN (%s) AND hoi.account_id = %s
            LIMIT %s OFFSET %s
        '''
        
    def _get_table_name(self):
        return 'history_of_issuance'
        
    def exists_in_history(self, book_id: str, account_id: str):
        return self._exists(f"account_id = {account_id} and book_id = {book_id}")
    
    def select_all_by_title(self, title: str, per_page: str, page: str):
        return self._select_with_pageable(f"LOWER(title) LIKE '%{title.lower()}%'", per_page, page)
    
    def count_history_issuence(self, account_id: str):
        res = self._execute_request_all(self.count_history_issuence_with_where_template % (self._get_table_name(), f"account_id = {account_id}"))[0][0]
        return int(res)
    
    def select_history_issuence_by_account_id(self, account_id: str):
        return self._select_all(f"account_id = {account_id}")
    
    def select_history_issuance_by_books_ids_by_account_id(self, book_ids: str, account_id:str, per_page: str, page: str):
        offset = (page - 1) * per_page
        return self._execute_request_all(self.select_with_join % (book_ids, account_id, per_page, offset))
    
    def update_history_issuence_is_read_by_account_id_by_book_id(self, data, account_id, book_id):
        self._update(data, f"account_id = {account_id} AND book_id = {book_id}")
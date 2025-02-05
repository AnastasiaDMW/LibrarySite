import abc

from database.LibraryDatabase import LibraryDatabase

'''
Абстрактный класс dao для выноса общей логики работы с базой данных
'''
class CommonDao(abc.ABC):
    
    def __init__(self, db: LibraryDatabase):
        super().__init__()
        self.db = db
        self.insert_template = 'INSERT INTO %s (%s) VALUES (%s)'
        self.update_template = 'UPDATE %s SET %s WHERE %s'
        self.delete_template = 'DELETE FROM %s WHERE %s'
        self.select_template = 'SELECT * FROM %s WHERE %s'
        self.exists_template = '''
            SELECT EXISTS (
                SELECT 1
                FROM %s 
                WHERE %s
            )
        '''
        self.select_with_pageable_template = 'SELECT * FROM %s WHERE %s LIMIT %s OFFSET %s'        
    
    @abc.abstractmethod
    def _get_table_name(self): pass 
    
    def insert(self, data: dict):
        title_param = ""
        value_param = ""
        for key, value in data.items():
            title_param += f"{key},"
            value_param += f"'{value}',"
            
        title_param = title_param.rstrip(',')
        value_param = value_param.rstrip(',')

        return self._execute_request(self.insert_template % (self._get_table_name(), title_param, value_param))
    
    def _update(self, data: dict, condition: str):
        set_param = ""
        for key, value in data.items():
            set_param += f"{key} = '{value}',"
        
        set_param = set_param.rstrip(',')
        return self._execute_request(self.update_template % (self._get_table_name(), set_param, condition))
    
    def _delete(self, condition: str):
        self._execute_request(self.delete_template % (self._get_table_name(), condition))

    def _select_all(self, condition: str):
        return self._execute_request_all(self.select_template % (self._get_table_name(), condition))
    
    def _select_with_pageable(self, condition: str, per_page: str, page:str):
        offset = (page - 1) * per_page
        return self._execute_request_all(self.select_with_pageable_template % (self._get_table_name(), condition, per_page, offset))
    
    def _exists(self, condition: str):
        return self._execute_request_one(self.exists_template % (self._get_table_name(), condition))
    
    def _execute_request_all(self, request):
        conn = self.db.get_db_connection()
        cur = conn.cursor()
        cur.execute(request)
        items = cur.fetchall()
        cur.close()
        conn.close()
        return items
    
    def _execute_request(self, request):
        conn = self.db.get_db_connection()
        cur = conn.cursor()
        cur.execute(request)
        conn.commit()
        cur.close()
        conn.close()
        
    def _execute_request_one(self, request):
        conn = self.db.get_db_connection()
        cur = conn.cursor()
        cur.execute(request)
        items = cur.fetchone()
        cur.close()
        conn.close()
        return items[0]
    

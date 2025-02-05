from dao.CommonDao import CommonDao
from database.LibraryDatabase import LibraryDatabase

'''
класс dao отвечающий за таблицу chapter в базе данных
'''
class ChapterDao(CommonDao):
    
    def __init__(self, db: LibraryDatabase):
        super().__init__(db)
        
    def _get_table_name(self):
        return 'chapter'
    
    def select_librarian_chapter(self, librarian_id: str):
        chapter: list = self._select_all(f"account_id = {librarian_id}")
        if len(chapter) > 0:
            return chapter[0]
        return None
    
    def select_by_id(self, chapter_id: str):
        chapter: list = self._select_all(f"id = {chapter_id}")
        if len(chapter) > 0:
            return chapter[0]
        return None
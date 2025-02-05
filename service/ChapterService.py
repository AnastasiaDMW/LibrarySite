from dao.ChapterDao import ChapterDao

'''
класс sevice отвечает за работу с dao и данными chapter
'''
class ChapterService:
    
    def __init__(self, dao: ChapterDao):
        super().__init__()
        self.dao = dao
        
    def get_librarian_chapter(self, librarian_id: str):
        return self.dao.select_librarian_chapter(librarian_id)
    
    def get_chapter_by_id(self, chapter_id: str):
        return self.dao.select_by_id(chapter_id)
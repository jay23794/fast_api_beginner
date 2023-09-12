def noteEntity(item) -> dict:
    return {
        "id":str(item['_id']),
        "title":str(item['title']),
        "desc":str(item['desc']),
        "important":str(item['important']),
    }

def notesEntity(items) -> list:
    return [noteEntity(item) for item in items]
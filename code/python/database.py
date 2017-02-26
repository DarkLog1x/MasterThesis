import tinydb


def PrintList(instanceID, type,  data):
    db = tinydb.TinyDB('./db.json')
    instanceSearch = tinydb.Query()
    if db.search(instanceSearch.id == instanceID):
        db.update({type: data}, instanceSearch.id == instanceID)
    else:
        db.insert({'id': instanceID, type: data})

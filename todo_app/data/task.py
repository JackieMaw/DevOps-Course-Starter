#TODO - how do I make this class JSON Serializable so that I can store it in Session?
class task():

    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status
class ChatClient:
    def __init__(self, conn, name, _id):
        self.conn = conn
        self.name = name
        self._id = _id

    def get_conn(self):
        return self.conn

    def get_name(self):
        return self.name

    def get_id(self):
        return self._id

    def set_conn(self, conn):
        self.conn = conn

    def set_name(self, name):
        self.name = name

    def set_id(self, _id):
        self._id = _id

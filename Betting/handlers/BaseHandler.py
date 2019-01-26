class BaseHandler(dict):
    def __init__(self, date, info):
        self.date = date
        super().__init__(info)


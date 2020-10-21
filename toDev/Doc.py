from toDev.Dev_client import Dev_client


class Doc(Dev_client):
    def __init__(self, conf, data_base, __doc_id):
        Dev_client.__init__(self, conf, data_base)
        self.__doc_id = __doc_id

    def get_document(self):
        return self.get_element("docs", self.__doc_id)

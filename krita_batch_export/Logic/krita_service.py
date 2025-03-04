from krita import *

class KritaService:
    def __init__(self):
        pass

    @staticmethod
    def get_all_open_documents():
        """Returns a list of all currently open documents in Krita"""
        return Krita.instance().documents()


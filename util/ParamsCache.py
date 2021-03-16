import json

class  ParamsCache:
    
    __instance = None
    params = {}
    is_doodle = True
    is_pictionay = False

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if ParamsCache.__instance == None:
            ParamsCache()
        return ParamsCache.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if ParamsCache.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            with open('./util/params.json', 'rb') as f:
                self.params = json.load(f)
            ParamsCache.__instance = self
    
    def getParams(self):
        return self.params
    
    def getUrl(self):
        return f"{self.params['server']}{self.params['service']}"

    def getLocalUrl(self):
        return f"{self.params['server_local']}{self.params['service']}"
    
    def getIsDoodle(self):
        return self.is_doodle

    def getIsPictionary(self):
        return self.is_pictionay

    def setCurrentPage(self, is_doodle, is_pictionay):
        self.is_doodle = is_doodle
        self.is_pictionay = is_pictionay
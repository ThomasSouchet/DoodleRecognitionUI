import json

class  ParamsCache:
    
    __instance = None
    params = {}
    
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

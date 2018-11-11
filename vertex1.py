GlobalID = 0

class Vertex:
    
    def __init__(self):
        self.__ID = 0
        self.__xcoor = 0
        self.__ycoor = 0
        self.__street = None
        self.intersection_streets = []
        
    def create_ID(self):
        self.__ID = GlobalID + 1
        global GlobalID
        GlobalID = self.__ID
        return
    
    def set_ID(self, new_ID):
        self.__ID = new_ID
        return
    
    def get_ID(self):
        return self.__ID
    
    def set_xcoor(self, new_xcoor):
        self.__xcoor = new_xcoor
        return
    
    def set_ycoor(self, new_ycoor):
        self.__ycoor = new_ycoor
        return
        
    def set_street(self, new_street):
        self.__street = new_street
        return
    
    def get_xcoor(self):
        return self.__xcoor
    
    def get_ycoor(self):
        return self.__ycoor
    
    def get_street(self):
        return self.__street


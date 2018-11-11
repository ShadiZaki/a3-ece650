from vertex1 import Vertex

class Edge:
    
    def __init__(self):
        self.__vertex1 = Vertex()
        self.__vertex2 = Vertex()
        self.__street = None
    
    def set_vertex1(self, new_vertex1):
        self.__vertex1 = new_vertex1
        return
    
    def set_vertex2(self, new_vertex2):
        self.__vertex2 = new_vertex2
        return
    
    def set_street(self, new_street):
        self.__street = new_street
        return
    
    def get_vertex1(self):
        return self.__vertex1
    
    def get_vertex2(self):
        return self.__vertex2
    
    def get_street(self):
        return self.__street
import sys
from vertex1 import Vertex
from edge1 import Edge
    
class Graph:
    
    intersections = []
    def __init__(self):
        self.__vertex_list = []
        self.__edges_list = []
        self.__updated_edges_list = []
        self.__updated_vertex_list = []
    
    def __intersect (self, edge1, edge2):
        x1 = float(edge1.get_vertex1().get_xcoor())
        y1 = float(edge1.get_vertex1().get_ycoor())
        x2 = float(edge1.get_vertex2().get_xcoor())
        y2 = float(edge1.get_vertex2().get_ycoor())
        
        x3 = float(edge2.get_vertex1().get_xcoor())
        y3 = float(edge2.get_vertex1().get_ycoor())
        x4 = float(edge2.get_vertex2().get_xcoor())
        y4 = float(edge2.get_vertex2().get_ycoor())

        den = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
        ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
        
        if(den != 0):
            xcoor =  xnum / den
            ycoor = ynum / den
            if(not (xcoor >= min(x1,x2) and xcoor <= max(x1,x2) and xcoor >= min(x3,x4) and xcoor <= max(x3,x4) 
               and ycoor >= min(y1,y2) and ycoor <= max(y1,y2) and ycoor >= min(y3,y4) and ycoor <= max(y3,y4))):
                return "No intersection"
        else:
            return "No intersection"
        
        intersection = Vertex()
        intersection.create_ID()
        intersection.set_xcoor(xcoor)
        intersection.set_ycoor(ycoor)
        intersection.intersection_streets.append(edge1.get_street())
        intersection.intersection_streets.append(edge2.get_street())
                
        for i in self.intersections:
            if(i.get_xcoor() == intersection.get_xcoor() and i.get_ycoor() == intersection.get_ycoor()):
                intersection.set_ID(i.get_ID())
            
        return intersection
    
    def __overlapping(self, edge1, edge2):
        x1 = float(edge1.get_vertex1().get_xcoor())
        y1 = float(edge1.get_vertex1().get_ycoor())
        x2 = float(edge1.get_vertex2().get_xcoor())
        y2 = float(edge1.get_vertex2().get_ycoor())
        
        x3 = float(edge2.get_vertex1().get_xcoor())
        y3 = float(edge2.get_vertex1().get_ycoor())
        x4 = float(edge2.get_vertex2().get_xcoor())
        y4 = float(edge2.get_vertex2().get_ycoor())
        
        num_edge1 = y2 - y1
        den_edge1 = x2 - x1
        
        num_edge2 = y4 - y3
        den_edge2 = x4 - x3
        
        if(den_edge1 != 0):
            slope_edge1 = float(num_edge1 / den_edge1)
            yint_edge1 = float(y1 - slope_edge1*x1)
            
        else:
            slope_edge1 = None
            yint_edge1 = None
        
        if(den_edge2 != 0):
            slope_edge2 = float(num_edge2 / den_edge2)
            yint_edge2 = float(y3 - slope_edge2*x3)
        else:
            slope_edge2 = None
            yint_edge2 = None
        
        if(slope_edge1 != None and slope_edge2 != None and yint_edge1 != None and yint_edge2 != None) :       
            if(round(slope_edge1, 3) == round(slope_edge2, 3) and round(yint_edge1, 3) == round(yint_edge2, 3)):
                return True
            else:
                return False
        else:
            if(slope_edge1 == None and slope_edge2 == None and yint_edge1 == None and yint_edge2 == None):
                return True
            else:
                return False
        
    def __rem_edge_duplicates(self):
        i = 0
        while i < len(self.__updated_edges_list)-1:
            j = i + 1
            while j < len(self.__updated_edges_list):
                if(self.__updated_edges_list[i].get_vertex1().get_ID() == self.__updated_edges_list[j].get_vertex1().get_ID() 
                   and self.__updated_edges_list[i].get_vertex2().get_ID() == self.__updated_edges_list[j].get_vertex2().get_ID()):
                    self.__updated_edges_list.pop(j)
                    i = 0
                elif(self.__updated_edges_list[i].get_vertex1().get_ID() == self.__updated_edges_list[j].get_vertex2().get_ID()
                   and self.__updated_edges_list[i].get_vertex2().get_ID() == self.__updated_edges_list[j].get_vertex1().get_ID()):
                    self.__updated_edges_list.pop(j)
                    i = 0
                j += 1
            i += 1
        
        i = 0
        while i < len(self.__updated_edges_list):
            if(self.__updated_edges_list[i].get_vertex1().get_ID() == self.__updated_edges_list[i].get_vertex2().get_ID()):
                self.__updated_edges_list.pop(i)
                i = 0
            i += 1
        return
    
    def __rem_vertex_duplicates(self):
        i = 0
        while i < len(self.__updated_vertex_list)-1:
            j = i + 1
            while j < len(self.__updated_vertex_list):
                if(self.__updated_vertex_list[i].get_ID() == self.__updated_vertex_list[j].get_ID()):
                    self.__updated_vertex_list.pop(j)
                    i = 0
                j += 1
            i += 1            
        return
    
    def __rem_unneeded_vertex(self):
        temp_vertex_list = []
        for i in self.__updated_vertex_list:
            for j in self.__updated_edges_list:
                if(i.get_ID() == j.get_vertex1().get_ID() or i.get_ID() == j.get_vertex2().get_ID()):
                    temp_vertex_list.append(i)
                    break
        self.__updated_vertex_list[:] = []
        for i in temp_vertex_list:
            self.__updated_vertex_list.append(i)
        return
    
    def __rem_joined_edges(self):
        to_pop = [] 
        i = 0
        while i < len(self.__updated_edges_list)-1:
            j = i + 1
            while j < len(self.__updated_edges_list):
                if(self.__updated_edges_list[i].get_vertex1().get_ID() == self.__updated_edges_list[j].get_vertex2().get_ID()):
                    for k in range(0, len(self.__updated_edges_list)):
                        if(self.__updated_edges_list[k].get_vertex1().get_ID() == self.__updated_edges_list[i].get_vertex2().get_ID() 
                           and self.__updated_edges_list[k].get_vertex2().get_ID() == self.__updated_edges_list[j].get_vertex1().get_ID()):
                            to_pop.append(k)
                        elif(self.__updated_edges_list[k].get_vertex1().get_ID() == self.__updated_edges_list[j].get_vertex1().get_ID() 
                           and self.__updated_edges_list[k].get_vertex2().get_ID() == self.__updated_edges_list[i].get_vertex2().get_ID()):
                            to_pop.append(k)
                elif(self.__updated_edges_list[i].get_vertex2().get_ID() == self.__updated_edges_list[j].get_vertex1().get_ID()):
                    for k in range(0, len(self.__updated_edges_list)):
                        if(self.__updated_edges_list[k].get_vertex1().get_ID() == self.__updated_edges_list[i].get_vertex1().get_ID() 
                           and self.__updated_edges_list[k].get_vertex2().get_ID() == self.__updated_edges_list[j].get_vertex2().get_ID()):
                            to_pop.append(k)
                        elif(self.__updated_edges_list[k].get_vertex1().get_ID() == self.__updated_edges_list[j].get_vertex2().get_ID() 
                           and self.__updated_edges_list[k].get_vertex2().get_ID() == self.__updated_edges_list[i].get_vertex1().get_ID()):
                            to_pop.append(k)
                j += 1
            i += 1
        
        x = 0
        while x < len(to_pop):
            y = 0
            while y < len(self.__updated_edges_list):
                if(y == to_pop[x]):
                    self.__updated_edges_list.pop(y)
                y += 1
            x += 1
        return
    
    def __fix_edges(self):
        to_pop = []
        temp_edges = []
        i = 0
        while i < len(self.__updated_edges_list)-1:
            j = i + 1
            while j < len(self.__updated_edges_list):
                if(not self.__overlapping(self.__updated_edges_list[i], self.__updated_edges_list[j])):
                    temp_edges.append(self.__updated_edges_list[i])
                    temp_edges.append(self.__updated_edges_list[j])
                else:
                    x3 = float(self.__updated_edges_list[j].get_vertex1().get_xcoor())
                    x4 = float(self.__updated_edges_list[j].get_vertex2().get_xcoor())
                    y3 = float(self.__updated_edges_list[j].get_vertex1().get_ycoor())
                    y4 = float(self.__updated_edges_list[j].get_vertex2().get_ycoor())
                    
                    x1 = float(self.__updated_edges_list[i].get_vertex1().get_xcoor())
                    x2 = float(self.__updated_edges_list[i].get_vertex2().get_xcoor())
                    y1 = float(self.__updated_edges_list[i].get_vertex1().get_ycoor())
                    y2 = float(self.__updated_edges_list[i].get_vertex2().get_ycoor())
                    
                    if(min(x3, x4) <= x1 <= max(x3,x4) and not (min(y3, y4) <= y1 <= max(y3, y4))
                       and min(x3, x4) <= x2 <= max(x3,x4) and min(y3, y4) < y2 < max(y3, y4)):
                        edge = Edge()
                        edge.set_street(self.__updated_edges_list[i].get_street())
                        edge.set_vertex1(self.__updated_edges_list[i].get_vertex2())
                        edge.set_vertex2(self.__updated_edges_list[j].get_vertex1())
                        temp_edges.append(edge)

                        edge1_to_pop = Edge()
                        edge1_to_pop.set_vertex1(self.__updated_edges_list[i].get_vertex1())
                        edge1_to_pop.set_vertex2(self.__updated_edges_list[i].get_vertex2())
                        to_pop.append(edge1_to_pop)
                        edge2_to_pop = Edge()
                        edge2_to_pop.set_vertex1(self.__updated_edges_list[j].get_vertex1())
                        edge2_to_pop.set_vertex2(self.__updated_edges_list[j].get_vertex2())
                        to_pop.append(edge2_to_pop)
                        
                    elif(min(x1, x2) <= x3 <= max(x1,x2) and not (min(y1, y2) <= y3 <= max(y1, y2))
                       and min(x1, x2) <= x4 <= max(x1,x2) and min(y1, y2) < y4 < max(y1, y2)):
                        edge = Edge()
                        edge.set_street(self.__updated_edges_list[i].get_street())
                        edge.set_vertex1(self.__updated_edges_list[i].get_vertex1())
                        edge.set_vertex2(self.__updated_edges_list[j].get_vertex2())
                        temp_edges.append(edge)

                        edge1_to_pop = Edge()
                        edge1_to_pop.set_vertex1(self.__updated_edges_list[i].get_vertex1())
                        edge1_to_pop.set_vertex2(self.__updated_edges_list[i].get_vertex2())
                        to_pop.append(edge1_to_pop)
                        edge2_to_pop = Edge()
                        edge2_to_pop.set_vertex1(self.__updated_edges_list[j].get_vertex1())
                        edge2_to_pop.set_vertex2(self.__updated_edges_list[j].get_vertex2())
                        to_pop.append(edge2_to_pop)
                    
                    elif(min(x1, x2) < x3 < max(x1, x2) and min(y1, y2) <= y3 <= max(y1, y2) 
                         and not(min(x1,x2) <= x4 <= max(x1,x2)) and min(y1, y2) <= y4 <= max(y1, y2)):
                        edge = Edge()
                        edge.set_street(self.__updated_edges_list[i].get_street())
                        edge.set_vertex1(self.__updated_edges_list[j].get_vertex1())
                        edge.set_vertex2(self.__updated_edges_list[i].get_vertex2())
                        temp_edges.append(edge)

                        edge1_to_pop = Edge()
                        edge1_to_pop.set_vertex1(self.__updated_edges_list[i].get_vertex1())
                        edge1_to_pop.set_vertex2(self.__updated_edges_list[i].get_vertex2())
                        to_pop.append(edge1_to_pop)
                        edge2_to_pop = Edge()
                        edge2_to_pop.set_vertex1(self.__updated_edges_list[j].get_vertex1())
                        edge2_to_pop.set_vertex2(self.__updated_edges_list[j].get_vertex2())
                        to_pop.append(edge2_to_pop)
                        
                    elif(min(x3, x4) < x1 < max(x3, x4) and min(y3, y4) <= y1 <= max(y3, y4) 
                         and not(min(x3, x4) <= x2 <= max(x3, x4)) and min(y3, y4) <= y2 <= max(y3, y4)):
                        edge = Edge()
                        edge.set_street(self.__updated_edges_list[i].get_street())
                        edge.set_vertex1(self.__updated_edges_list[i].get_vertex1())
                        edge.set_vertex2(self.__updated_edges_list[j].get_vertex2())
                        temp_edges.append(edge)

                        edge1_to_pop = Edge()
                        edge1_to_pop.set_vertex1(self.__updated_edges_list[i].get_vertex1())
                        edge1_to_pop.set_vertex2(self.__updated_edges_list[i].get_vertex2())
                        to_pop.append(edge1_to_pop)
                        edge2_to_pop = Edge()
                        edge2_to_pop.set_vertex1(self.__updated_edges_list[j].get_vertex1())
                        edge2_to_pop.set_vertex2(self.__updated_edges_list[j].get_vertex2())
                        to_pop.append(edge2_to_pop)
                                            
                    elif(min(x1, x2) < x3 < max(x1, x2) and min(y1, y2) < y3 < max(y1, y2) 
                         and not(min(x1,x2) <= x4 <= max(x1,x2)) and not(min(y1, y2) <= y4 <= max(y1, y2))):
                        edge = Edge()
                        edge.set_street(self.__updated_edges_list[i].get_street())
                        edge.set_vertex1(self.__updated_edges_list[j].get_vertex1())
                        edge.set_vertex2(self.__updated_edges_list[i].get_vertex2())
                        temp_edges.append(edge)

                        edge1_to_pop = Edge()
                        edge1_to_pop.set_vertex1(self.__updated_edges_list[i].get_vertex1())
                        edge1_to_pop.set_vertex2(self.__updated_edges_list[i].get_vertex2())
                        to_pop.append(edge1_to_pop)
                        edge2_to_pop = Edge()
                        edge2_to_pop.set_vertex1(self.__updated_edges_list[j].get_vertex1())
                        edge2_to_pop.set_vertex2(self.__updated_edges_list[j].get_vertex2())
                        to_pop.append(edge2_to_pop)
                    
                    elif(min(x3, x4) < x1 < max(x3, x4) and min(y3, y4) < y1 < max(y3, y4) 
                         and not(min(x3, x4) <= x2 <= max(x3, x4)) and not(min(y3, y4) <= y2 <= max(y3, y4))):
                        edge = Edge()
                        edge.set_street(self.__updated_edges_list[i].get_street())
                        edge.set_vertex1(self.__updated_edges_list[i].get_vertex1())
                        edge.set_vertex2(self.__updated_edges_list[j].get_vertex2())
                        temp_edges.append(edge)

                        edge1_to_pop = Edge()
                        edge1_to_pop.set_vertex1(self.__updated_edges_list[i].get_vertex1())
                        edge1_to_pop.set_vertex2(self.__updated_edges_list[i].get_vertex2())
                        to_pop.append(edge1_to_pop)
                        edge2_to_pop = Edge()
                        edge2_to_pop.set_vertex1(self.__updated_edges_list[j].get_vertex1())
                        edge2_to_pop.set_vertex2(self.__updated_edges_list[j].get_vertex2())
                        to_pop.append(edge2_to_pop)
                    
                j += 1
            i += 1
        self.__updated_edges_list[:] = []
        for item in temp_edges:
            self.__updated_edges_list.append(item)
        
        self.__rem_edge_duplicates()
        
        k = 0
        while k < len(to_pop):
            l = 0
            while l < len(self.__updated_edges_list):
                if(to_pop[k].get_vertex1().get_ID() == self.__updated_edges_list[l].get_vertex1().get_ID() 
                   and to_pop[k].get_vertex2().get_ID() == self.__updated_edges_list[l].get_vertex2().get_ID()):
                    self.__updated_edges_list.pop(l)
                l += 1
            k += 1
        return
    
    def __generate_graph(self):
        self.__updated_vertex_list[:] = []
        self.__updated_edges_list[:] = []
        for item in self.__vertex_list:
            self.__updated_vertex_list.append(item)
        
        i = 0
        while i < len(self.__edges_list)-1:
            j = i + 1
            while j < len(self.__edges_list):
                if (self.__edges_list[i].get_street() != self.__edges_list[j].get_street()):
                    intersection = self.__intersect(self.__edges_list[i], self.__edges_list[j])
                    if (intersection != "No intersection"):
                        self.__updated_vertex_list.append(intersection)
                        self.intersections.append(intersection)
                        if(len(self.__updated_vertex_list) > 20):
                            break

                        edge1 = Edge()
                        edge1.set_street(self.__edges_list[i].get_street())
                        edge1.set_vertex1(self.__edges_list[i].get_vertex1())
                        edge1.set_vertex2(intersection)
                            
                        edge2 = Edge()
                        edge2.set_street(self.__edges_list[i].get_street())
                        edge2.set_vertex1(intersection)
                        edge2.set_vertex2(self.__edges_list[i].get_vertex2())
                            
                        edge3 = Edge()
                        edge3.set_street(self.__edges_list[j].get_street())
                        edge3.set_vertex1(self.__edges_list[j].get_vertex1())
                        edge3.set_vertex2(intersection)
                            
                        edge4 = Edge()
                        edge4.set_street(self.__edges_list[j].get_street())
                        edge4.set_vertex1(intersection)
                        edge4.set_vertex2(self.__edges_list[j].get_vertex2())
                            
                        self.__updated_edges_list.append(edge1)
                        self.__updated_edges_list.append(edge2)
                        self.__updated_edges_list.append(edge3)
                        self.__updated_edges_list.append(edge4)
                j += 1
                if(len(self.__updated_vertex_list) > 20):
                    break
            i += 1
        if(len(self.__updated_vertex_list) > 20):
            self.__updated_vertex_list[:] = []
            return

        self.__rem_edge_duplicates()
        self.__rem_vertex_duplicates()
        self.__rem_unneeded_vertex()
        self.__fix_edges()
        self.__rem_joined_edges()
        return

    def add_street(self, street_name, coor):
        contained = False
        for i in self.__vertex_list:
            if(street_name == i.get_street()):
                contained = True
                break
        
        if(not contained):
            length = len(coor)/2
            templen = len(self.__vertex_list)
        
            for i in range(0,length):
                new_ver = Vertex()
                new_ver.create_ID()
                new_ver.set_street(street_name)
                new_ver.set_xcoor(coor[2*i])
                new_ver.set_ycoor(coor[2*i+1])
                self.__vertex_list.append(new_ver)
            
            for i in range(0, length - 1):
                new_edge = Edge()
                new_edge.set_street(street_name)
                j = i + templen
                new_edge.set_vertex1(self.__vertex_list[j])
                new_edge.set_vertex2(self.__vertex_list[j+1])
                self.__edges_list.append(new_edge)
        else:
            sys.stderr.write("Error: street has already been added \n")

        return

    def remove_street(self,street_name):
        contained = False
        for i in self.__vertex_list:
            if(street_name == i.get_street()):
                contained = True
                break
            
        if(contained):
            self.__vertex_list[:] = [i for i in self.__vertex_list if i.get_street() != street_name]
            self.__edges_list[:] = [i for i in self.__edges_list if i.get_street() != street_name]
        else:
            sys.stderr.write("Error: street does not exist \n")
        
        return

    def change_street(self, street_name, coor):
        self.remove_street(street_name)
        self.add_street(street_name, coor)
        return
    
    def __format_edges(self):
        formatted_edge_list = []
        for i in range(0, len(self.__updated_edges_list)):
            for j in range(0, len(self.__updated_vertex_list)):
                if(self.__updated_edges_list[i].get_vertex1().get_ID() == self.__updated_vertex_list[j].get_ID()):
                    new_vertex1 = Vertex()
                    new_vertex1.set_ID(j)
                    break
            for j in range(0, len(self.__updated_vertex_list)):
                if(self.__updated_edges_list[i].get_vertex2().get_ID() == self.__updated_vertex_list[j].get_ID()):
                    new_vertex2 = Vertex()
                    new_vertex2.set_ID(j)
                    break
            formatted_edge = Edge()
            formatted_edge.set_vertex1(new_vertex1)
            formatted_edge.set_vertex2(new_vertex2)
            formatted_edge_list.append(formatted_edge)
        return formatted_edge_list
                

    def output_graph(self):
        self.__generate_graph()
        if(len(self.__updated_vertex_list) != 0):
            formatted_edge_list = self.__format_edges()
        else:
            formatted_edge_list = []
        V_string = "V " + str(len(self.__updated_vertex_list)) +"\n"
        E_param = ""
        for i in range(0, len(formatted_edge_list)):
            E_param = E_param + "<" + str(formatted_edge_list[i].get_vertex1().get_ID()) + "," + str(formatted_edge_list[i].get_vertex2().get_ID()) + ">"
            if(i != len(formatted_edge_list)-1):
                E_param = E_param + ","
        E_string = "E {" + E_param + "}\n"
        sys.stdout.write(V_string)
        sys.stdout.write(E_string)
        sys.stdout.flush();
#         sys.stdout.write("V = { \n")
#         for i in self.__updated_vertex_list:
#             sys.stdout.write(str(i.get_ID()) + ":" + " (" + "%g" % round(float(i.get_xcoor()),2) + "," + "%g" % round(float(i.get_ycoor()),2) + ") \n")
#         sys.stdout.write("} \n")
#          
#         sys.stdout.write("E = { \n")
#         for i in self.__updated_edges_list:
#             sys.stdout.write("<" + str(i.get_vertex1().get_ID()) + "," + str(i.get_vertex2().get_ID()) + ">, \n")
#         sys.stdout.write("} \n")
        return

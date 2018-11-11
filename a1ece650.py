#! /usr/bin/python
import sys
from parser import Parser
from graph1 import Graph

parse = Parser()
GGraph = Graph()

def main():
    while(True):
        data = parse.read_and_parse()
        if(data != None):
            if((type(data) is str) and data == "g"):
                GGraph.output_graph()
            else:
                if(data[0] == "a"):
                    GGraph.add_street(data[1], data[2])
                elif(data[0] == "c"):
                    GGraph.change_street(data[1], data[2])
                elif(data[0] == "r"):
                    GGraph.remove_street(data[1])
                else:
                    sys.stderr.write("Error: invalid command \n")

if __name__ == '__main__': main()
    
    
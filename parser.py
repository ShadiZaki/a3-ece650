import re
import sys

class Parser:
    
    def __init__(self):
        pass
    
    def read_and_parse(self):
        try:
            Input = sys.stdin.readline()

            Input = Input.lstrip()
            pattern = re.compile(r'[-+]?[0-9]*\.?[0-9]+')
            coor = pattern.findall(Input)
            coor_len = len(coor)
            invalid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', 
                             '-', '_', '+', '=', '/', '{', '}', '|', ':', ';', '"', '\\', '>', '<', '?', '.', '`', '~']

            paranthesis_count = 0
            for i in Input:
                if(i == "(" or i == ")"):
                    paranthesis_count += 1
            if(paranthesis_count > coor_len):
                sys.stderr.write("Error: invalid command \n")
                return None
            elif(paranthesis_count < coor_len):
                sys.stderr.write("Error: invalid command \n")
                return None
        
            if(paranthesis_count == 2 and coor_len == 2):
                sys.stderr.write("Error: invalid command \n")
                return None
        
            if(coor_len % 2 != 0):
                sys.stderr.write("Error: invalid command \n")
                return None
        
            for i in coor:
                if("." in i):
                    sys.stderr.write("Error: invalid coordinates \n")
                    return None
        
            command = Input[0]
            
            if(command != "a" and command != "c" and command != "r" and command != "g"):
                sys.stderr.write("Error: invalid command \n")
                return None
            else:
                Input_list = Input[1:]
                if(command != "g"):
                    Input_list1 = Input_list.split(' ', 1)
                    if(Input_list1[0] != ''):
                        sys.stderr.write("Error: invalid command \n")
                        return None
                    else:
                        if(len(Input_list1) > 1):
                            Input_list2 = Input_list1[1].split('"', 2)
                            if(len(Input_list2) > 2):
                                if(command == "r" and Input_list2[2] != '\n'):
                                    sys.stderr.write("Error: invalid command \n")
                                    return None
                                if(command == "a" and Input_list2[2] == '\n'):
                                    sys.stderr.write("Error: no coordinates found \n")
                                    return None
                                if(command == "c" and Input_list2[2] == '\n'):
                                    sys.stderr.write("Error: no coordinates found \n")
                                    return None
                            else:
                                sys.stderr.write("Error: invalid command \n")
                                return None
                            for char in invalid_chars:
                                if(char in Input_list2[1]):
                                    sys.stderr.write("Error: invalid street name \n")
                                    return None
                        else:
                            sys.stderr.write("Error: invalid command \n")
                            return None
                elif(command == "g" and Input_list.strip()):
                    sys.stderr.write("Error: invalid command \n")
                    return None
        
            if(command == "a" or command == "c"):
                data = [command, Input_list2[1].upper(), coor]
            elif(command == "r"):
                data = [command, Input_list2[1].upper()]
            elif(command == "g"):
                data = command
        except:
            data = None
            sys.stderr.write("Error: no input was read \n")
        return data
        

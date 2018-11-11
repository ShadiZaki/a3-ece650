#include "parser.hpp"
#include "edge.hpp"
#include "graph.hpp"
using namespace std;

int main(int argc, const char * argv[])
{
    int vertex_count = 0;   //number of vertices
    vector<Edge> edge_list; //vector to store edges
    string command = "    ";
    bool v_specified = false;   //determines if the number of vertices has been specified
    bool e_specified = false;   //determines if the edges have been specified
    
    do{
        Parser parser;  //parser instance
        pair<string, vector<int>> parser_result;    //result of parser (command, parameters)
        vector<int> parameters;     //input parameters
        
        parser_result = parser.read_and_parse();    //read and parse input
        command = parser_result.first;  //splitting parser result into command and parameters
        parameters = parser_result.second;
        
        
        if(command == "V" || command == "v")    //check if command is a vertex number specification
        {
            if(parameters.size() == 1)  //check if there is only one parameter (vertex count)
            {
                vertex_count = parameters[0];
                v_specified = true;
                e_specified = false;
            }
        }
        else if(command == "E" || command == "e")   //check if command is an edges specification
        {
            if(v_specified && !e_specified) //check if the number of vertices has been specified and if the edges were not
            {
                if(parameters.size() % 2 == 0)  //check if the number of parameters is even (because edges are specified as vertex pairs)
                {
                    bool valid_edges = true;    //determines if edge specification is valid
                    
                    for(int i = 0; i < parameters.size(); i+=2)
                    {
                        int vertex1 = parameters[i];
                        int vertex2 = parameters[i+1];
                        if(vertex1 < 0 || vertex1 >= vertex_count || vertex2 < 0 || vertex2 >= vertex_count || vertex1 == vertex2) //check if the vertices are not within range or equal to each other
                        {
                            valid_edges = false;
                            break;
                        }
                    }
                    
                    edge_list.clear();  //clear previous edges
                    
                    if(valid_edges) //check if edges are valid
                    {
                        for(int i = 0; i < parameters.size(); i+=2) //push every edge into the edges vector
                        {
                            int vertex1 = parameters[i];
                            int vertex2 = parameters[i+1];
                            Edge new_edge(vertex1, vertex2);
                            edge_list.push_back(new_edge);
                        }
                        e_specified = true;
                        
                        string v_string = "V " + to_string(vertex_count);   // modification for assignment 3
                        string e_string = "E {";
                        for(int i = 0; i < edge_list.size(); i++)
                        {
                            e_string = e_string + "<" + to_string(edge_list[i].get_vertex1()) + "," + to_string(edge_list[i].get_vertex2()) + ">";
                            if(i != edge_list.size()-1)
                            {
                                e_string = e_string + ",";
                            }
                        }
                        e_string = e_string + "}";
                        cout<<v_string<<endl;
                        cout<<e_string<<endl;   // modification ends here
                    }
                    else    //invalid edges
                    {
                        cerr<<"Error: invalid edges"<<endl;
                    }
                }
            }
            else if(!v_specified && !e_specified)   //number of vertices was not specified
            {
                cerr<<"Error: number of vertices was not specified"<<endl;
            }
            else if(v_specified && e_specified) //edges were already specified
            {
                cerr<<"Error: edges were already specified"<<endl;
            }
        }
        else if(command == "S" || command == "s")   //check if command is shortest-path
        {
            if(v_specified && e_specified)  //check if both the number of vertices and the edges were specified
            {
                if(parameters.size() == 2)  //check if there are only two parameters (source and destination)
                {
                    int source = parameters[0];
                    int destination = parameters[1];
                    if(source >= 0 && source < vertex_count && destination >= 0 && destination < vertex_count && source != destination) //check if source and destination are within range and not equal to each other
                    {
                        Graph graph(vertex_count, edge_list);
                        vector<int> shortest_path = graph.bfs_traversal(source, destination);   //traverse the graph and find the shortest path
                        
                        if(shortest_path.size() == 0)   //check if no path was found
                        {
                            cerr<<"Error: No path was found"<<endl;
                        }
                        else
                        {
                            for(int i = 0; i < shortest_path.size(); i++)   //print out the shortest path
                            {
                                cout<<shortest_path[i];
                                if(i != shortest_path.size()-1)
                                {
                                    cout<<"-";
                                }
                            }
                            cout<<endl;
                        }
                    }
                    else if(source < 0 || source >= vertex_count)   //source is out of range
                    {
                        cerr<<"Error: source is out of range"<<endl;
                    }
                    else if(destination < 0 || destination >= vertex_count) //destination is out of range
                    {
                        cerr<<"Error: destination is out of range"<<endl;
                    }
                    else    //anything else is invalid
                    {
                        cerr<<"Error: invalid command"<<endl;
                    }
                }
            }
            else if(v_specified && !e_specified)    //edges were not specified
            {
                cerr<<"Error: edges were not specified"<<endl;
            }
            else if(!v_specified && !e_specified)   //no graph was specified
            {
                cerr<<"Error: no graph specification found"<<endl;
            }
        }
    }while(true);
    return 0;
}

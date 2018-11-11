#include "graph.hpp"

int Graph::min_distance_index(vector<int> distances)  //function for finding the minimum distance in a given vector of distances
{
    int min = 0;
    for(int i = 0; i < distances.size(); i++)
    {
        if(distances[i] <= distances[min])
        {
            min = i;
        }
    }
    return min;
}

vector<int> Graph::find_shortest_path(pair<vector<int>, vector<int>> traversal_result) //function to find the shortest path from source to destination given a traversal (from source to destination)
{
    vector<int> traversal = traversal_result.first; //traversal from source to destination
    vector<int> previous = traversal_result.second; //previous vertex during traversal(for each vertex encountered)
    
    vector<int> shortest_path;  //representation of a shortest path (in reverse)
    vector<int> final_shortest_path; //final representation of a shortest path
    
    
    int prev = previous[previous.size()-1];
    
    int ind = 1;
    while(!adjacency_matrix[traversal[traversal.size()-1]][prev]) //compute destination's previous vertex
    {
        prev = previous[previous.size()-1-ind];
        ind++;
    }
    
    shortest_path.push_back(prev);
    int traversal_size = int(traversal.size());
    
    while(prev != -1) //tracing path backwards from destination to source using a given traversal from source to destination
    {
        for(int i = traversal_size-1; i >= 0; i--)
        {
            if(traversal[i] == prev)
            {
                prev = previous[i];
                shortest_path.push_back(prev);
                break;
            }
        }
    }
    
    for(int i = int(shortest_path.size())-2; i >= 0; i--) //reversal of shortest path for better representation
    {
        final_shortest_path.push_back(shortest_path[i]);
    }
    final_shortest_path.push_back(traversal[traversal_size-1]);
    
    return final_shortest_path; //return shortest path
}

void Graph::populate_adjacency_matrix() //function to populate adjacency matrix
{
    for(int i = 0; i < edge_list.size(); i++)
    {
        adjacency_matrix[edge_list[i].get_vertex1()][edge_list[i].get_vertex2()] = true;
        adjacency_matrix[edge_list[i].get_vertex2()][edge_list[i].get_vertex1()] = true;
    }
}

Graph::Graph(int new_vertex_count, vector<Edge> new_edge_list) //constructor
{
    this->vertex_count = new_vertex_count;
    this->edge_list = new_edge_list;
    vector<vector<bool>> new_adjacency_matrix(new_vertex_count, vector<bool>(new_vertex_count, false));
    this->adjacency_matrix = new_adjacency_matrix;
    populate_adjacency_matrix();
}

vector<int> Graph::bfs_traversal(int source, int destination)  //function performing bfs traversal of given graph from source to destination
{
    queue<int> Q;   //queue for traversal
    vector<bool> visited;   //boolean vector for checking if a given vertex has been visited before
    vector<int> traversal;  //traversal of complete graph (starting from source)
    vector<int> previous;   //previouse vertex during traversal (for each vertex encountered)
    
    for(int i = 0; i < vertex_count; i++)  //initializing all vertices to not visited
    {
        visited.push_back(false);
    }
    
    Q.push(source); //push first vertex(source) to queue
    visited[source] = true; //set first vertex(source) as visited
    previous.push_back(-1); //source has no predecessor
    
    while(!Q.empty())   //perform traversal of complete graph starting from source
    {
        source = Q.front();
        Q.pop();
        traversal.push_back(source);
        
        for(int i = 0; i < vertex_count; i++)
        {
            if(adjacency_matrix[source][i] && !visited[i])
            {
                Q.push(i);
                visited[i] = true;
                previous.push_back(source);
            }
        }
    }
    
    if(!visited[destination]) //check if destination was never reached
    {
        vector<int> no_path;
        return no_path;
    }
    
    vector<int> new_traversal; //sub-traversal from source to destination only
    vector<int> new_previous;   //previous vector for sub-traversal
    
    int path_count = 0;
    for(int i = 0; i < traversal.size(); i++)   //compute number of possible paths from source to destination
    {
        if(traversal[i] == destination)
        {
            path_count++;
        }
    }
    vector<int> *paths = new vector<int>[path_count]; //array of possible paths
    
    int count = 0;
    while(find(traversal.begin(), traversal.end(), destination) != traversal.end()) //keep performing traversals from source to destination for all possible paths
    {
        for(int i = 0; i < traversal.size(); i++)
        {
            new_traversal.push_back(traversal[i]);
            new_previous.push_back(previous[i]);
            if(traversal[i] == destination)
            {
                traversal[i] = -1;
                break;
            }
        }
        
        pair<vector<int>, vector<int>> bfs_result = {new_traversal, new_previous};
        vector<int> path = find_shortest_path(bfs_result);
        paths[count] = path;
        count++;
    }
    
    vector<int> distances;
    for(int i = 0; i < path_count; i++) //store distances of all possible paths
    {
        distances.push_back(int(paths[i].size()));
    }
    
    int min_index = min_distance_index(distances); //find index of shortest path
    vector<int> min_path = paths[min_index];
    delete [] paths;
    return min_path;    //return shortest of all possible paths
}




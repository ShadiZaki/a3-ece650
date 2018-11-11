#ifndef graph_hpp
#define graph_hpp

#include <vector>
#include <queue>
#include <algorithm>
#include "edge.hpp"
using namespace std;

class Graph
{
private:
    int vertex_count;   //number of vertices in graph
    vector<Edge> edge_list; //edges in graph
    vector<vector<bool>> adjacency_matrix;  //adjacency matrix
    
    int min_distance_index(vector<int> distances);  //function for finding the minimum distance in a given vector of distances
    vector<int> find_shortest_path(pair<vector<int>, vector<int>> traversal_result); //function to find the shortest path from source to destination given a traversal (from source to destination)
    void populate_adjacency_matrix();   //function to populate adjacency matrix
public:
    Graph(int new_vertex_count, vector<Edge> new_edge_list); //constructor
    vector<int> bfs_traversal(int source, int destination);  //function performing bfs traversal of given graph from source to destination
};

#endif

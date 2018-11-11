#include <stdio.h>
#include "unistd.h"
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
using namespace std;

class rgen
{
private:
    int s = 10;
    int n = 5;
    int l = 5;
    int c = 20;
    
    
    string generate_string()
    {
        string generated_string = "          ";
        char alphanumeric[] = {
            'A','B','C','D','E','F',
            'G','H','I','J','K',
            'L','M','N','O','P',
            'Q','R','S','T','U',
            'V','W','X','Y','Z',
            'a','b','c','d','e','f',
            'g','h','i','j','k',
            'l','m','n','o','p',
            'q','r','s','t','u',
            'v','w','x','y','z'};
        
        ifstream urandom("/dev/urandom");
        if (urandom.fail())
        {
            cerr << "Error: cannot open /dev/urandom"<<endl;
        }
        
        for(int i = 0; i < 10; i++)
        {
            int generated_int;
            urandom.read((char*)&generated_int, sizeof(int));
            if(generated_int < 0)
            {
                generated_int = -generated_int;
            }
            generated_string[i] = alphanumeric[generated_int % 52];
        }
        
        urandom.close();
        return generated_string;
    }
    
    pair<int, int> generate_coor()
    {
        pair<int, int> generated_coor;
        int vertex1;
        int vertex2;
        
        ifstream urandom("/dev/urandom");
        if (urandom.fail())
        {
            cerr << "Error: cannot open /dev/urandom"<<endl;
        }
        
        urandom.read((char*)&vertex1, sizeof(int));
        urandom.read((char*)&vertex2, sizeof(int));
        
        vertex1 = vertex1 % (c+1);
        vertex2 = vertex2 % (c+1);
        
        urandom.close();
        
        generated_coor = {vertex1, vertex2};
        return generated_coor;
    }
    
    bool overlapping(int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4)
    {
        int num_edge1 = y2 - y1;
        int den_edge1 = x2 - x1;
        
        int num_edge2 = y4 - y3;
        int den_edge2 = x4 - x3;
        
        int slope_edge1;
        int yint_edge1;
        int slope_edge2;
        int yint_edge2;
        
        if(den_edge1 != 0)
        {
            slope_edge1 = float(num_edge1 / den_edge1);
            yint_edge1 = float(y1 - slope_edge1*x1);
        }
        else
        {
            slope_edge1 = -999999;
            yint_edge1 = -999999;
        }
        
        if(den_edge2 != 0)
        {
            slope_edge2 = float(num_edge2 / den_edge2);
            yint_edge2 = float(y3 - slope_edge2*x3);
        }
        else
        {
            slope_edge2 = -999999;
            yint_edge2 = -999999;
        }
        
        if(slope_edge1 != -999999 && slope_edge2 != -999999 && yint_edge1 != -999999 && yint_edge2 != -999999)
        {
            if(((abs(slope_edge1-slope_edge2)) < 0.001) && ((abs(yint_edge1-yint_edge2)) < 0.001))
            {
                if(x4 >= min(x1, x2) && x4 <= max(x1, x2) && y4 >= min(y1, y2) && y4 <= max(y1, y2))
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                return false;
            }
        }
        else
        {
            if(slope_edge1 == -999999 && slope_edge2 == -999999 && yint_edge1 == -999999 && yint_edge2 == -999999)
            {
                if(x4 >= min(x1, x2) && x4 <= max(x1, x2) && y4 >= min(y1, y2) && y4 <= max(y1, y2))
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                return false;
            }
        }
    }
    
    bool intersect(int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4)
    {
        double den = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4));
        double xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4));
        double ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4);
        if(den != 0)
        {
           double xcoor =  xnum / den;
           double ycoor = ynum / den;
            if(!(xcoor >= min(x1,x2) && xcoor <= max(x1,x2) && xcoor >= min(x3,x4) && xcoor <= max(x3,x4)
                && ycoor >= min(y1,y2) && ycoor <= max(y1,y2) && ycoor >= min(y3,y4) && ycoor <= max(y3,y4)))
            {
                return false;
            }
        }
        else
        {
            return false;
        }
        return true;
    }
    
    bool check_streets(vector<pair<int, int>> *all_coor, int street_number)
    {
        for(int i = 0; i < street_number; i++)
        {
            for(int j = 0; j < all_coor[i].size()-1; j++)
            {
                for (int k = j + 1; k < all_coor[i].size(); k++)
                {
                    if(all_coor[i].at(j).first == all_coor[i].at(k).first && all_coor[i].at(j).second == all_coor[i].at(k).second)
                    {
                        return false;
                    }
                }
            }
        }
        
        for(int i = 0; i < street_number; i++)
        {
            vector<pair<pair<int, int>, pair<int, int>>> edges;
            for(int j = 0; j < (all_coor[i].size())-1; j++)
            {
                pair<int, int> coor1 = {all_coor[i].at(j).first, all_coor[i].at(j).second};
                pair<int, int> coor2 = {all_coor[i].at(j+1).first, all_coor[i].at(j+1).second};
                pair<pair<int, int>, pair<int, int>> edge = {coor1, coor2};
                edges.push_back(edge);
            }
            
            if(edges.size() > 1)
            {
            
                for(int j = 0; j < edges.size()-1; j++)
                {
                    for(int k = j+1; k < edges.size(); k++)
                    {
                        int x1 = edges.at(j).first.first;
                        int y1 = edges.at(j).first.second;
                        int x2 = edges.at(j).second.first;
                        int y2 = edges.at(j).second.second;
                    
                        int x3 = edges.at(k).first.first;
                        int y3 = edges.at(k).first.second;
                        int x4 = edges.at(k).second.first;
                        int y4 = edges.at(k).second.second;
                        
                        bool inter = false;
                        if(k != j+1)
                        {
                            inter = intersect(x1, y1, x2, y2, x3, y3, x4, y4);
                        }
                        
                        if(inter || overlapping(x1, y1, x2, y2, x3, y3, x4, y4))
                        {
                            return false;
                        }
                    }
                }
            }
        }
        
        vector<pair<pair<int, int>, pair<int, int>>> edges;
        for(int i = 0; i < street_number; i++)
        {
            for(int j = 0; j < (all_coor[i].size())-1; j++)
            {
                pair<int, int> coor1 = {all_coor[i].at(j).first, all_coor[i].at(j).second};
                pair<int, int> coor2 = {all_coor[i].at(j+1).first, all_coor[i].at(j+1).second};
                pair<pair<int, int>, pair<int, int>> edge = {coor1, coor2};
                edges.push_back(edge);
            }
        }
        
        for(int i = 0; i < edges.size()-1; i++)
        {
            for(int j = i+1; j < edges.size(); j++)
            {
                int x1 = edges.at(i).first.first;
                int y1 = edges.at(i).first.second;
                int x2 = edges.at(i).second.first;
                int y2 = edges.at(i).second.second;
                
                int x3 = edges.at(j).first.first;
                int y3 = edges.at(j).first.second;
                int x4 = edges.at(j).second.first;
                int y4 = edges.at(j).second.second;
                
                if(overlapping(x1, y1, x2, y2, x3, y3, x4, y4))
                {
                    return false;
                }
            }
        }
        return true;
    }
    
    void remove_streets(vector<string> streets)
    {
        string r_street;
        for(int i = 0; i < streets.size(); i++)
        {
            r_street = "r \"" + streets.at(i) + "\"";
            cout<<r_street<<endl;
        }
    }
    
public:
    rgen(int argc, char *argv[])
    {
        if(argc != 1)
        {
            for(int i = 0; i < argc; i++)
            {
                if(strcmp(argv[i], "-s") == 0)
                {
                    this->s = atoi(argv[i+1]);
                    break;
                }
            }
            
            for(int i = 0; i < argc; i++)
            {
                if(strcmp(argv[i], "-n") == 0)
                {
                    this->n = atoi(argv[i+1]);
                    break;
                }
            }
            
            for(int i = 0; i < argc; i++)
            {
                if(strcmp(argv[i], "-l") == 0)
                {
                    this->l = atoi(argv[i+1]);
                    break;
                }
            }
            
            for(int i = 0; i < argc; i++)
            {
                if(strcmp(argv[i], "-c") == 0)
                {
                    this->c = atoi(argv[i+1]);
                    break;
                }
            }
        }
    }
    
    void generate_streets()
    {
        if(s < 2 || n < 1 || l < 5 || c < 1)
        {
            cerr<<"Error: invalid arguments"<<endl;
            exit(0);
        }
        else
        {
            bool first_iter = true;
            bool flag = false;
            int wait_seconds = 0;
            int street_number;
            ifstream urandom("/dev/urandom");
            if (urandom.fail())
            {
                cerr << "Error: cannot open /dev/urandom"<<endl;
            }
            vector<string> street_names;
            int attempt_count = 0;
            
            while(true)
            {
                if(!first_iter && flag)
                {
                    sleep(wait_seconds);
                    remove_streets(street_names);
                    street_names.clear();
                }
                urandom.read((char*)&wait_seconds, sizeof(int));
                wait_seconds = wait_seconds % (l+1);
                if(wait_seconds < 5)
                {
                    wait_seconds = 5;
                }
                
                urandom.read((char*)&street_number, sizeof(int));
                
                street_number = street_number % (s+1);
                
                if(street_number < 2)
                {
                    street_number = 2;
                }
                
                string name;
                string street;
                string graph = "g";
                vector<string> add_streets;
                vector<pair<int, int>> *all_coor = new vector<pair<int, int>>[street_number];
                for(int i = 0; i < street_number; i++)
                {
                    int segment_number;
                    urandom.read((char*)&segment_number, sizeof(int));
                    segment_number = segment_number % (n+1);
                    if(segment_number < 1)
                    {
                        segment_number = 1;
                    }
                    
                    vector<pair<int, int>> street_coor;
                    vector<string> coordinates;
                    string final_coordinates = "";
                    street_names.push_back(generate_string());
                    name = "a \"" + street_names.at(street_names.size()-1) + "\" ";
                    for(int j = 0; j < segment_number+1; j++)
                    {
                        pair<int, int> coor = generate_coor();
                        street_coor.push_back(coor);
                        coordinates.push_back("(" + to_string(coor.first) + "," + to_string(coor.second) + ") ");
                    }
                    
                    for(int j = 0; j < coordinates.size(); j++)
                    {
                        final_coordinates = final_coordinates + coordinates.at(j);
                    }
                    street = name + final_coordinates;
                    all_coor[i] = street_coor;
                    add_streets.push_back(street);
                }
                
                flag = check_streets(all_coor, street_number);
                
                if(flag)
                {
                    for(int i = 0; i < add_streets.size(); i++)
                    {
                        cout<<add_streets.at(i)<<endl;
                    }
                
                    cout<<graph<<endl;
                    attempt_count = 0;
                    first_iter = false;
                }
                else
                {
                    attempt_count++;
                    street_names.clear();
                }
                
                if(attempt_count > 25)
                {
                    cerr<<"Error: failed to generate valid input for 25 simultaneous attempts"<<endl;
                    exit(0);
                }
            }
        }
    }
};

int main(int argc, char * argv[])
{
    rgen generator(argc, argv);
    generator.generate_streets();
    return 0;
}
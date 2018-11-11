#include <iostream>
#include <sys/types.h>
#include <sys/wait.h>
#include <string>
#include <signal.h>
#include <unistd.h>
using namespace std;

int main(int argc, char * argv[])
{
    char *args[10];
    for(int i = 0; i < argc; i++)
    {
        args[i] = argv[i];
    }
    argv[9] = NULL;
    
    int pipe1[2];
    int pipe2[2];
    
    pid_t children[4];
    
    pipe(pipe1);
    pipe(pipe2);
    
    children[0] = fork();
    
    if(children[0] == (pid_t) 0)
    {
        dup2(pipe1[1], STDOUT_FILENO);
        close(pipe1[1]);
        close(pipe1[0]);
        close(pipe2[1]);
        close(pipe2[0]);
        execv("./rgen", args);
    }
    
    children[1] = fork();
    
    if(children[1] == (pid_t) 0)
    {
        dup2(pipe1[0], STDIN_FILENO);
        dup2(pipe2[1], STDOUT_FILENO);
        close(pipe1[1]);
        close(pipe1[0]);
        close(pipe2[1]);
        close(pipe2[0]);
        execv("a1ece650.py", nullptr);
    }
    
    children[2] = fork();
    
    if(children[2] == (pid_t) 0)
    {
        dup2(pipe2[0], STDIN_FILENO);
        close(pipe1[1]);
        close(pipe1[0]);
        close(pipe2[1]);
        close(pipe2[0]);
        execv("./a2-ece650", nullptr);
    }
    
    children[3] = fork();
    
    if(children[3] == (pid_t) 0)
    {
        dup2(pipe2[1], STDOUT_FILENO);
        close(pipe1[1]);
        close(pipe1[0]);
        string input;
        while(true)
        {
            getline(cin, input);
            if(cin.eof())
            {
                for(int i = 0; i < 4; i++)
                {
                    kill(children[i], SIGKILL);
                }
                break;
            }
            else
            {
                cout<<input<<endl;
            }
        }
    }
    
    
    int status[4];
    for(int i = 0; i < 4; i++)
    {
        waitpid(children[i], &status[i], 0);
    }
    
    return 0;
}

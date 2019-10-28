#include <sys/types.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>

unsigned int read_str(char *msg, unsigned int size) {
    char el;
    ssize_t rbytes;
    ssize_t nbytes = 0;
    while (nbytes < size){
        rbytes = read(0, &msg[nbytes], 1);
        if (rbytes == -1){
            if (errno == EAGAIN || errno == EINTR){
                continue;
            }
            return -1;
        }
        if (rbytes == 0){
            break;
        }
        if (msg[nbytes] == '\n') {msg[nbytes] = '\x00'; break;}  
        nbytes += rbytes;
    }
}

void update_name(char *name, unsigned int size)
{
    printf("new name: ");
    read_str(name, sizeof(name));
    printf("name is updated\n");
}

void quit(char * name)
{
    printf("Bye %s\n", name);
    exit(1);
}

char *get_name(){
    char name[0x20];
    printf("Input your name --> ");
    gets(name);
}

int main()
{
    char surname[0x10];
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    char *name;
    char cmd[0x10];
    name = get_name();
    printf("Hi %s, nice to meet you!!!\n", name);
    while(1){
        printf("What do you want to do??\n");
        printf("--> ");
        read_str(cmd, sizeof(cmd));
        if (!(strcmp(cmd, "u"))){
            name = get_name();
        } else if (!(strcmp(cmd, "q"))){
            quit(name);
        } else {
            printf("wrong command!!\n");
        }
    }
}
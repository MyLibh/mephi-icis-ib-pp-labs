#include <sys/types.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>

static const char a[] =
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";

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

void show_msg()
{
    puts("  /$$$$$$                                        /$$   /$$                            /$$                                 ");
    puts(" /$$__  $$                                      | $$  | $$                           | $$                                 ");
    puts("| $$ \\ $$  /$$$$$$   /$$$$$$  /$$$$$$$        /$$$$$$| $$$$$$$   /$$$$$$        /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$    ");
    puts("| $$  | $$ /$$__  $$ /$$__  $$| $$__  $$      |_  $$_/| $$__  $$ /$$__  $$      /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$   ");
    puts("| $$  | $$| $$ \\ $$| $$$$$$$$| $$\\ $$       | $$    | $$  \\ $$| $$$$$$$$     | $$  | $$| $$ \\ $$| $$ \\ $$| $$ \\__/  ");
    puts("| $$  | $$| $$  | $$| $$_____/| $$  | $$      | $$ /$$| $$  | $$| $$_____/      | $$  | $$| $$  | $$| $$  | $$| $$        ");
    puts("|  $$$$$$/| $$$$$$$/|  $$$$$$$| $$  | $$      |  $$$$/| $$  | $$|  $$$$$$$      |  $$$$$$$|  $$$$$$/|  $$$$$$/| $$        ");
    puts(" \\______/ | $$____/  \\_______/|__/  |__/    \\___/  |__/  |__/\\_______/     \\_______/\\______/ \\______/ |__/         ");
    puts("          | $$                                                                                                            ");
    puts("          | $$                                                                                                            ");
    puts("          |__/                                                                                                            ");
}

void success()
{
    puts("door is unlocked!");
}

int main()
{
    char buffer[0x20];
    char key[0x20];
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    for (int i = 0; i < sizeof(key) - 1; ++i) { // fixed by adding - 1
        key[i] = a[rand() % (sizeof(a) - 1)];
    }
    show_msg();
    while (1){
        printf("give me the key --> ");
        read_str(buffer, sizeof(buffer));
        if (strcmp(buffer, key)){
            printf("this is wrong: %s\n", buffer);
        } else {
            success();
        }
    }
}
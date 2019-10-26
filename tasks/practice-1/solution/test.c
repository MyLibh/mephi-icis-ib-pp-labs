#include <stdio.h>

int func()
{
    int p = 0x353535;

    return p;
}

int main()
{
    func();

    int arr[] = {0, 1, 2};
    int arr2[2] = {2, 1};

    int a = 0xFFFFFFFF;
    unsigned b = 0;

    short c = 0;
    unsigned short d = 0;

    long e = 0;
    unsigned long f = 0;

    long long g = 0;
    unsigned long long h = 0;


    signed char i = 0;
    unsigned char j = 0;

    float k = 0.f;
    double l = 0;
    long double m = 0;

    return 0;
}
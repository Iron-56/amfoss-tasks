#include <stdio.h>
#include <string.h>

int main()
{
    FILE* fi = fopen("input.txt", "r");
    fseek(fi, 0L, SEEK_END);
    const int size = ftell(fi);
    fseek(fi, 0L, SEEK_SET);
    
    char data[size];
    
    FILE* fo = fopen("output.txt", "w");
    
    //reads line by line
    while(fgets(data, size, fi))
    {
        int length = strlen(data);
        for(int i=0; i<length; ++i) fputc(data[i], fo);
    }
    
    fclose(fi);
    fclose(fo);
    
    return 0;
}
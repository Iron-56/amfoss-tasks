
#include <stdio.h>
#include <math.h>
#include <string.h>

void replicate(char ch, int num, FILE* f)
{
	for(int i=0; i<num; ++i)
	{
		fputc(ch, f);
	}
}

int main()
{
    FILE* fi = fopen("input.txt", "r");
    fseek(fi, 0L, SEEK_END);
    const int size = ftell(fi);
    fseek(fi, 0L, SEEK_SET);
    
    char data[size];
    
    FILE* fo = fopen("output.txt", "w");
    
    //reads a single line
    fgets(data, size+1, fi);
    
	int n;
	sscanf(data, "%d", &n);
	int counter = n%2;
	printf("%d\n", n);

	for(int i =0; i<n; ++i)
	{
		if(counter == 0)
		{
			counter += 2;
			continue;
		}

		int half = floor((n-counter)/2);
		replicate(' ', half, fo);
		replicate('*', counter, fo);
		replicate(' ', half, fo);
		fputc('\n', fo);

		if(i < floor(n/2))
		{
			counter += 2;
		} else {
			counter -= 2;
		}
	}
	
	fclose(fi);
    fclose(fo);

	return 0;
}
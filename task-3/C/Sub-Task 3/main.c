
#include <stdio.h>
#include <math.h>

void replicate(char ch, int num)
{
	for(int i=0; i<num; ++i)
	{
		printf("%c", ch);
	}
}

int main()
{
	int n;
	printf("Enter rows: ");
	scanf("%d", &n);
	int counter = n%2;

	for(int i =0; i<n; ++i)
	{
		if(counter == 0)
		{
			counter += 2;
			continue;
		}

		int half = floor((n-counter)/2);
		replicate(' ', half);
		replicate('*', counter);
		replicate(' ', half);
		printf("\n");

		if(i < floor(n/2))
		{
			counter += 2;
		} else {
			counter -= 2;
		}
	}

	return 0;
}
#include <stdio.h>

int main(int argc, char *argv[])
{
	int i;
	printf("#nr parameter\n");
	for (i=0; i<argc; i++) 
		printf("%3d %s\n", i, argv[i]);
	return 0;
}

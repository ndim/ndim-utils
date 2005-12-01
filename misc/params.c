#include <stdio.h>

int main(int argc, char *argv[], char *env[])
{
	int i;
	
	printf("#nr environment variable\n");
	for (i=0; env[i] != NULL; i++) 
		printf("%3d %s\n", i, env[i]);
	
	printf("#nr parameter\n");
	for (i=0; i<argc; i++) 
		printf("%3d %s\n", i, argv[i]);
	
	return 0;
}

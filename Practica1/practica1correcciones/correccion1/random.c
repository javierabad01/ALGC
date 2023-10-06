#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){//generates random vectors
	float random;
	srand(time(0));
	char filename[20];
	int N;
	scanf("%s",filename);
	scanf("%d",&N);
	
	FILE* file;
	file=fopen(filename,"w");

	for(int i=0;i<N;i++){
		fprintf(file,"%f\t%f\n",(float) rand(),(float) rand());
	}	

	fclose(file);
	return 0;
}

//TRABAJO
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include <sys/resource.h>




typedef struct Punto{//punto en un plano 2D
	double x;
	double y;
	double tam; //tamaño del punto (su norma)
}punto;

typedef struct Lista{//lista de pares hi-lo
	double hi;
	double lo;
	struct Lista* next;//si es NULL es el ultimo
}lista;

void swap(punto* a, punto* b){//intercambia dos puntos
	punto tmp=*a;
	*a=*b;
	*b=tmp;
	return;
}

double d(punto a, punto b){//calculo la distancia entre 2 puntos
	return(sqrt(pow(a.x-b.x,2)+pow(a.y-b.y,2)));
}

void tamf(punto* puntos, int n, punto ref){//calcula el tamaño de cada elemento del array de puntos como su distancia el punto de referencia
	for(int i=0;i<n;i++){
		puntos[i].tam=d(puntos[i],ref);
	}
}

void insert(punto* puntos,int n){//ordena un array de n puntos con respecto a su tamaño
	for(int i=1;i<n;i++){
		punto insert=puntos[i];
		int j=i-1;
		while(j>=0&&puntos[j].tam>insert.tam){
			puntos[j+1]=puntos[j];
			j--;
		}
		puntos[j+1]=insert;
	}
}


int partition(punto* puntos, int lo, int hi){//en quicksort devuelve el pivote del subvector que va desde lo hasta hi, dejando a su derecha los elementos mayores a el y a su izquierda los menores
	double pivot=puntos[hi].tam;

	int i=lo-1;//indice del pivot temporal

	for(int j=lo;j<hi;j++){
		if(puntos[j].tam<=pivot){
			i++;
			swap(puntos+i,puntos+j);
		}
	}
	i++;	
	swap(puntos+i,puntos+hi);
	return(i);//return indice del pivot
}

void quicksort(punto* puntos, int lo, int hi){//ordena desde puntos[lo] hasta puntos[hi] del array de puntos (si lo=0 y hi=length(puntos) ordena el array completamente)
	if(lo<hi && lo>=0){
		//obtener pivote
		int pivot=partition(puntos,lo,hi);
		
		//ordenar a ambos lados del pivote
		quicksort(puntos,lo,pivot-1);
		quicksort(puntos,pivot+1,hi);
	}
	return;	
}



void quicksort1(punto* puntos, int lo, int hi,int c){//quicksort del metodo 1
	if(lo<hi && lo>=0){
		if(hi-lo>=c){//quicksort usual
			//obtener pivote
			int pivot=partition(puntos,lo,hi);
		
			//ordenar a ambos lados del pivote
			quicksort1(puntos,lo,pivot-1,c);
			quicksort1(puntos,pivot+1,hi,c);
		}else{//insertion sort
			insert(puntos+lo,hi-lo+1);	
		}
	}
	return;	
}


void quicksort2(punto* puntos, int lo, int hi,lista* head, lista* tail){//quicksort del metodo 2. step es el tamaño de los subarray
	if(lo<hi && lo>=0){
		//obtener pivote
		int pivot=partition(puntos,lo,hi);
		//añadir par a la lisa
		lista* nodo=(lista*)malloc(sizeof(lista));
		nodo->hi=hi;
		nodo->lo=pivot+1;
		if(head!=NULL){
			tail->next=nodo;
		}else{
			head=nodo;
			tail=nodo;
		}
		//recursion
		quicksort2(puntos,lo,pivot-1,head,nodo);
		//iteracion
		while(head!=NULL){//mientras quede algun par lohi
			if(head->lo<head->hi && head->lo>=0){
				//obtener pivote
				pivot=partition(puntos,head->lo,head->hi);
				//añadir par a la lista
				nodo=(lista*)malloc(sizeof(lista));
				nodo->hi=pivot-1;
				nodo->lo=head->lo;
				tail->next=nodo;
				tail=nodo;
				//añadir par a la lista
				nodo=(lista*)malloc(sizeof(lista));
				nodo->hi=head->hi;
				nodo->lo=pivot+1;
				nodo->next=NULL;
				tail->next=nodo;
				tail=nodo;
			}
			nodo=head;
			head=nodo->next;
			free(nodo);
		}
	}
	return;	
}


int main(){
	punto ref;
	ref.x=0;ref.y=0;	
	char filename[10];
	int N;

	scanf("%s",filename);
	scanf("%d",&N);
	punto puntos[N];
		
	FILE* file=fopen(filename,"r");
	for(int i=0;i<N;i++){
		fscanf(file,"%lf\t%lf",&(puntos[i].x),&(puntos[i].y));
	}
	fclose(file);
	

	tamf(puntos,N,ref);	
	
	int who=RUSAGE_SELF;
	struct rusage usage;

	quicksort2(puntos,0,N-1,(lista*)NULL,(lista*)NULL);
	//quicksort1(puntos,0,N-1,100);
	//quicksort(puntos,0,N-1);

	getrusage(who,&usage);
	printf("%ld.%06ld s\t%ld Kbytes\n",usage.ru_stime.tv_sec,usage.ru_stime.tv_usec,usage.ru_maxrss);

	return 0;
}

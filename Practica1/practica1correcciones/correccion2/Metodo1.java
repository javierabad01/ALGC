public class Metodo1 {
	
	public static void main(String[] args) {
		Punto origen=new Punto(0,0);
		double tiempo[]=new double[500];
		int n=50000;
		
		//Calculo el tiempo con tamaños de c de 0 a 100 para n=50000
		for(int i=0;i<100;i++) {
			Punto p[]=new Punto[n];
			
			//creo los puntos
			for(int j=0;j<n;j++){
				p[j]=new Punto();
			}
			
			long inicio=System.currentTimeMillis();
			p=quicksort(origen,p,0,p.length-1,i);
			long fin=System.currentTimeMillis();
			tiempo[i]=(double)(fin-inicio)/1000;
			System.out.println(i+"\t"+(double)(fin-inicio)/1000);
		}
		
	}
	
	//Algoritmo quicksort
	public static Punto[] quicksort(Punto origen,Punto[] puntos,int inicio, int fin, int c) {
		if(inicio>=fin) {
			return puntos;
		}
		
		if(fin-inicio<=c) {
			return(insercionDirecta(origen,puntos,inicio,fin));
		}
		
		int p=particion(origen,puntos,inicio,fin);
		puntos=quicksort(origen,puntos, inicio, p - 1,c);
		puntos=quicksort(origen,puntos, p + 1, fin,c);
		return puntos;
	}
	
	//Divide los puntos en menores o mayores a un punto pivot colocando los menores al inicio del
	//array y los mayores al final, y colocando este punto donde se encuentran 
	public static int particion(Punto origen, Punto[] puntos,int inicio,int fin) {
		Punto pivot=puntos[fin];
		int i=inicio;
		for(int j=inicio;j<fin;j++) {
			if(puntos[j].getDistancia(origen)<=pivot.getDistancia(origen)) {
				Punto temp=puntos[i];
				puntos[i]=puntos[j];
				puntos[j]=temp;
				i++;
			}
		}
		
		puntos[fin]=puntos[i];
		puntos[i]=pivot;
		return i;
		
	}
	
	//Algoritmo de insercion directa
	public static Punto[] insercionDirecta(Punto origen,Punto[] puntos, int inicio, int fin) {
		for(int i=inicio+1;i<=fin;i++) {
			Punto x=puntos[i];
			int j=i-1;
			while(j>=0 && puntos[j].getDistancia(origen)>x.getDistancia(origen)) {
				puntos[j+1]=puntos[j];
				j=j-1;
			}
			puntos[j+1]=x;
		}
		return puntos;
	}
}

import java.util.Stack;

public class Metodo2 {
	public static void main(String[] args) {
		Punto origen=new Punto(0,0);
		double tiempo[]=new double[100];
		
		//Calculo el tiempo con tamaños de array de 50000 a 5000000
		for(int i=50000;i<=5000000;i=i+50000) {
			Punto p[]=new Punto[i];
			
			//creo los puntos
			for(int j=0;j<i;j++){
				p[j]=new Punto();
			}
			
			long inicio=System.currentTimeMillis();
			p=quicksort(origen,p,0,p.length-1);
			long fin=System.currentTimeMillis();
			tiempo[(i/50000)-1]=(double)(fin-inicio)/1000;
			System.out.println(i+"\t"+(double)(fin-inicio)/1000);
		}
	}
	
	//Algoritmo quicksort
	public static Punto[] quicksort(Punto origen,Punto[] puntos,int inicio, int fin) {
		if(inicio>=fin) {
			return puntos;
		}
		
		int p=particion(origen,puntos,inicio,fin);
		puntos=quicksort(origen,puntos, inicio, p - 1);
		
		//Ordenamos iterativamente
		
		Stack<Integer> pila = new Stack<>();
		if(fin>p+1) {
			pila.push(p+1);
			pila.push(fin);
		}
		while(!pila.isEmpty()) {
			fin=pila.pop();
			inicio=pila.pop();
			p=particion(origen,puntos,inicio,fin);
			if(inicio<p-1) {
				pila.push(inicio);
				pila.push(p-1);
			}
			if(fin>p+1) {
				pila.push(p+1);
				pila.push(fin);
			}
		}
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
}

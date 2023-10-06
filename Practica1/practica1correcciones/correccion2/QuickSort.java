public class QuickSort {
	
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
			
			Punto p2[]=new Punto[i];
			long inicio=System.currentTimeMillis();
			p2=quicksort(origen,p,0,p.length-1);
			long fin=System.currentTimeMillis();
			tiempo[(i/50000)-1]=(double)(fin-inicio)/1000;
			System.out.println(i+"\t"+(double)(fin-inicio)/1000);
		}
		
	}
	
	public static Punto[] quicksort(Punto origen,Punto[] puntos,int inicio, int fin) {
		if(inicio>=fin) {
			return puntos;
		}
		
		int p=particion(origen,puntos,inicio,fin);
		puntos=quicksort(origen,puntos, inicio, p - 1);
		puntos=quicksort(origen,puntos, p + 1, fin);
		return puntos;
	}
	
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
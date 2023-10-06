public class Insercion {

	public static void main(String[] args) {
		
		
		Punto origen=new Punto(0,0);
		double tiempo[]=new double[100];
		
		//Calculo el tiempo desde tamaño 500 a 50000
		for(int i=500;i<=50000;i=i+500) {
			Punto p[]=new Punto[i];
			
			//creo los puntos
			for(int j=0;j<i;j++){
				p[j]=new Punto();
			}
			
			long inicio=System.currentTimeMillis();
			p=insercion(origen,p);
			long fin=System.currentTimeMillis();
			tiempo[(i/500)-1]=(double)(fin-inicio)/1000;
			System.out.println(i+"\t"+(double)(fin-inicio)/1000);
		}
	
	}
	
	public static Punto[] insercion(Punto origen,Punto[] puntos) {
		for(int i=1;i<puntos.length;i++) {
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

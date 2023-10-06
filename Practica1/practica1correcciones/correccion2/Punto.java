public class Punto {
	double x;
	double y;
	
	public Punto() {
		this.x=Math.random()*10;
		this.y=Math.random()*10;
	}
	
	public Punto(double x, double y) {
		this.x=x;
		this.y=y;
	}
	
	public double getx() {
		return this.x;
	}
	
	public double gety() {
		return this.y;
	}
	
	public double getDistancia(Punto p) {
		return(Math.sqrt((getx()-p.getx())*(getx()-p.getx())+(gety()-p.gety())*(gety()-p.gety())));
	}
}

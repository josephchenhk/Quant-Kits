package com.virtualsports.pmatrix;

public class ProbMatrix {
	
	public double[][] getProbMatrix(double alphaH, double betaH, double alphaA, double betaA,
			double gamma, double[] lambda, double[] mu, double[] rho, double[] xi, int hg, int ag){
		
		double[][] pMatrix = new double[10][10];
		
		System.out.println("Home:"+alphaH+","+betaH+","+gamma);
		System.out.println("Away:"+alphaA+","+betaA);
		System.out.println("Lambda:"+lambda);
		System.out.println("Mu:"+mu);
		System.out.println("rho:"+rho);
		System.out.println("xi:"+xi);
		System.out.println("hg vs ag:"+hg+" vs "+ag);
		
		pMatrix[hg][ag] = 1;
		
		return pMatrix;
	}
}

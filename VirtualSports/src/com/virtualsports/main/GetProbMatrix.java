package com.virtualsports.main;

import java.util.ArrayList;
import java.util.HashMap;
import com.virtualsports.data.SQLConnector;
import com.virtualsports.data.GetParams;
import com.virtualsports.pmatrix.ProbMatrix;

public class GetProbMatrix {
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub		
		System.out.println("Get the probability matrix for a specified match.");
		
		int league_id = 36;
		int homeTeam_id = 348;
		int awayTeam_id = 24;
		int hg = 2;
		int ag = 1;
		double t = 35.0;
		ArrayList<HashMap<String,Object>> homeTeamParams;
		ArrayList<HashMap<String,Object>> awayTeamParams;
		ArrayList<HashMap<String,Object>> leagueParams;
		
		GetParams getParams = new GetParams();
		leagueParams = getParams.getLeagueParams(league_id);
        homeTeamParams = getParams.getTeamParams(league_id, homeTeam_id);
        awayTeamParams = getParams.getTeamParams(league_id, awayTeam_id);	
        
        System.out.println(leagueParams);
        System.out.println(homeTeamParams);
        System.out.println(awayTeamParams);
        
        getParams.close();
        
        
		double alphaH = Double.valueOf(homeTeamParams.get(0).get("alpha").toString());
		double alphaA = Double.valueOf(awayTeamParams.get(0).get("alpha").toString());
		double betaH = Double.valueOf(homeTeamParams.get(0).get("beta").toString());		
		double betaA = Double.valueOf(awayTeamParams.get(0).get("beta").toString());
		double gamma = Double.valueOf(leagueParams.get(0).get("gamma").toString());
		
		String lambdaStr = leagueParams.get(0).get("lambda").toString();
		lambdaStr = lambdaStr.substring(1, lambdaStr.length()-1);
		String[] lambdaStrList = lambdaStr.split(",");
		double[] lambda = new double[lambdaStrList.length];
		for (int i=0; i<lambdaStrList.length; i++){
			lambda[i] = Double.parseDouble(lambdaStrList[i]);
		}
		
		String muStr = leagueParams.get(0).get("mu").toString();
		muStr = muStr.substring(1, muStr.length()-1);
		String[] muStrList = muStr.split(",");
		double[] mu = new double[muStrList.length];
		for (int i=0; i<muStrList.length; i++){
			mu[i] = Double.parseDouble(muStrList[i]);
		}
		
		String rhoStr = leagueParams.get(0).get("rho").toString();
		rhoStr = rhoStr.substring(1, rhoStr.length()-1);
		String[] rhoStrList = rhoStr.split(",");
		double[] rho = new double[rhoStrList.length];
		for (int i=0; i<rhoStrList.length; i++){
			rho[i] = Double.parseDouble(rhoStrList[i]);
		}
		
		String xiStr = leagueParams.get(0).get("xi").toString();
		xiStr = xiStr.substring(1, xiStr.length()-1);
		String[] xiStrList = xiStr.split(",");
		double[] xi = new double[xiStrList.length];
		for (int i=0; i<xiStrList.length; i++){
			xi[i] = Double.parseDouble(xiStrList[i]);
		}
		
		/*
		for (int i=0; i<6; i++){
			System.out.print(lambda[i]+",");
		}
		System.out.println();
		for (int i=0; i<6; i++){
			System.out.print(mu[i]+",");
		}
		System.out.println();
		for (int i=0; i<2; i++){
			System.out.print(rho[i]+",");
		}
		System.out.println();
		for (int i=0; i<2; i++){
			System.out.print(xi[i]+",");
		}
		*/
		
		ProbMatrix pm = new ProbMatrix();
		double[][] pMatrix;
		pMatrix = pm.getProbMatrix(alphaH, betaH, alphaA, betaA, gamma, lambda, mu, rho, xi, hg, ag);
		
		
		System.out.println();
	}


}

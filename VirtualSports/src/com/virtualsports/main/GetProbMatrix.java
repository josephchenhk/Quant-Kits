package com.virtualsports.main;

import java.util.ArrayList;
import java.util.HashMap;
import com.virtualsports.data.SQLConnector;
import com.virtualsports.data.GetParams;

public class GetProbMatrix {
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub		
		System.out.println("Get the probability matrix for a specified match.");
		
		int league_id = 36;
		int homeTeam_id = 348;
		int awayTeam_id = 24;
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
		
	}


}

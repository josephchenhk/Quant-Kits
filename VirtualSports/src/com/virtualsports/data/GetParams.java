package com.virtualsports.data;

import java.util.ArrayList;
import java.util.HashMap;

public class GetParams {
	
	SQLConnector sql = new SQLConnector();
	
	public void close(){
		sql.close();
	}
		
	public ArrayList<HashMap<String,Object>> getTeamParams(int league_id, int team_id){
		String query = ("SELECT * FROM inplay_team_params " +
				        "WHERE league_id = " + String.valueOf(league_id) + " " +
		                "AND team_id = " + String.valueOf(team_id) 
		                );
		ArrayList<HashMap<String,Object>> team_params;
		team_params = sql.rawQuery(query);
		//System.out.println(team_params);
		return team_params;
	}
	
	public ArrayList<HashMap<String,Object>> getLeagueParams(int league_id){
		String query = ("SELECT * FROM inplay_league_params " +
		                "WHERE league_id = " + String.valueOf(league_id)
		                );
		ArrayList<HashMap<String,Object>> league_params;
		league_params = sql.rawQuery(query);
		//System.out.println(league_params);
		return league_params;
	}
}

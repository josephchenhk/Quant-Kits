package com.virtualsports.main;

import java.sql.Connection;
import com.virtualsports.data.SQLConnector;

public class GetProbMatrix {

	public static void main(String[] args) {
		// TODO Auto-generated method stub		
		System.out.println("Get the probability matrix for a specified match.");
		
		SQLConnector sql = new SQLConnector();
		
		String query = ("select * from `order` " +
		                "where updated_timestamp>'2017-03-22' " +
		                "limit 4");
		sql.select(query);
	}

}

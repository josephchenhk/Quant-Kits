package com.virtualsports.data;

import java.util.ArrayList;
import java.util.HashMap;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSetMetaData;

public class SQLConnector {
	private Connection con;
	
	public SQLConnector(){
		try {
	        Connection con = null; 
	        Class.forName("com.mysql.jdbc.Driver").newInstance(); //MYSQL Driver
	        String _Address = "172.20.2.177";
	        String _Port = "3306";
	        String _Database = "football_bet_exp1";
	        String _User = "football2";
	        String _Password = "f00tba11";
	        String _url = "jdbc:mysql://" + _Address + ":" + _Port + "/" + _Database;  // "jdbc:mysql://172.20.2.177:3306/football_bet_exp1"
	        con = DriverManager.getConnection(_url, _User, _Password); // Connect to MYSQL
	        this.con = con;
	        System.out.print("Connect to MySQL successfully!\n");	        	
	    } catch (Exception e) {
	        System.out.print("MYSQL ERROR:" + e.getMessage());
	        this.con = null;
	    }		
	}
	
	public void close(){	
		try {
			this.con.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/*
	public ArrayList<Object> select(String query){

		ArrayList<Object> res_list = new ArrayList<Object>();
		
        try {
        	Statement stmt;
            ResultSet res;
			stmt = this.con.createStatement();
	        res = stmt.executeQuery(query);
	        while(res.next()){
	        	String a = res.getString(1);
	        	int b = res.getInt(2);
	        	System.out.println(a + ", " + b);
	        	res_list.add(a);
	        }
	        return res_list;
		} catch (SQLException e) {
			System.out.print("MYSQL ERROR:" + e.getMessage());
			return null;
		}

	}
	*/
	
	
	//query a full sql command
	public ArrayList<HashMap<String,Object>> rawQuery(String fullCommand) {
		
		try {		
			//create statement
			Statement stm = null;
			stm = this.con.createStatement();
			
			//query
			ResultSet result = null;
			boolean returningRows = stm.execute(fullCommand);
			if (returningRows)
				result = stm.getResultSet();
			else
				return new ArrayList<HashMap<String,Object>>();
			
			//get metadata
			ResultSetMetaData meta = null;
			meta = result.getMetaData();
			
			//get column names
			int colCount = meta.getColumnCount();
			ArrayList<String> cols = new ArrayList<String>();
			for (int index=1; index<=colCount; index++){
				cols.add(meta.getColumnName(index));
			}
			
			//fetch out rows
			ArrayList<HashMap<String,Object>> rows = new ArrayList<HashMap<String,Object>>();
			
			while (result.next()) {
				HashMap<String,Object> row = new HashMap<String,Object>();
				for (String colName:cols) {
					Object val = result.getObject(colName);
			    row.put(colName,val);
			  }
			  rows.add(row);
			}
			
			//close statement
			stm.close();
			
			//pass back rows
			return rows;
		} catch (Exception ex) {
			System.out.print(ex.getMessage());
			return new ArrayList<HashMap<String,Object>>();
		}
	}//raw_query
       
}

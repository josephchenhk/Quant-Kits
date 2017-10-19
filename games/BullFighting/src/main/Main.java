package main;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.List;

import game.BullFighting;
import game.Config;
import game.PayTable;

public class Main {

	public static void main(String[] args) throws FileNotFoundException{
		System.out.println("<<<<<<<< Bull Fighting >>>>>>>");
		long tic = System.currentTimeMillis();
		BullFighting bf = new BullFighting();
		bf.play();
		//System.out.println(bf.account);
		long toc = System.currentTimeMillis();
		System.out.println("Elapsed time: " + ((toc-tic)/1000) + " seconds.");
		
		PrintWriter pw = new PrintWriter(new File("results/bull_fighting.csv"));
		StringBuilder sb = new StringBuilder();
		sb.append(",");
		sb.append("Odds,");
		sb.append("Placement,");
		sb.append("Payment,");
		sb.append("RTP\n");
		pw.write(sb.toString());
        
		for (int i=0; i<Config.sim_choices.size(); i++){
			String choice = Config.sim_choices.get(i);
			List<Double> acc = bf.account.getAccount(choice);
			double RTP = acc.get(1)/acc.get(0);
			double odd = PayTable.getOdd(choice) - 1;
			
			System.out.println(choice + ": " + acc + " RTP: " + RTP);
			
			StringBuilder sb1 = new StringBuilder();
			sb1.append(choice);
			sb1.append(",");
			sb1.append(odd);
			sb1.append(",");
			sb1.append(acc.get(0));
			sb1.append(",");
			sb1.append(acc.get(1));
			sb1.append(",");
			sb1.append(RTP);
			sb1.append("\n");
			pw.write(sb1.toString());
		}
		pw.close();
	}

}

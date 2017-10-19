package main;

import java.util.List;

import game.BullFighting;
import game.Config;

public class Main {

	public static void main(String[] args) {
		System.out.println("<<<<<<<< Bull Fighting >>>>>>>");
		long tic = System.currentTimeMillis();
		BullFighting bf = new BullFighting();
		bf.play();
		//System.out.println(bf.account);
		long toc = System.currentTimeMillis();
		System.out.println("Elapsed time: " + (toc-tic) + " seconds.");
		
		for (int i=0; i<Config.sim_choices.size(); i++){
			String choice = Config.sim_choices.get(i);
			List<Double> acc = bf.account.getAccount(choice);
			double RTP = acc.get(1)/acc.get(0);
			System.out.println(choice + ": " + acc + " RTP: " + RTP);
		}
	}

}

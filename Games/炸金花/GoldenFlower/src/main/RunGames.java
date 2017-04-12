package main;

import java.util.ArrayList;
import game.TenThousandGame;

public class RunGames {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Õ¨½ð»¨£ºÈfÈËˆö");
		TenThousandGame game1 = new TenThousandGame();
		/*for (int i=0; i<52; i++){
			System.out.println(game1.deck.get(i));
		}*/		
		System.out.println(game1.deck);
		
		/*
		ArrayList<Integer> banker = game1.BankerDrawCards();
		System.out.println(banker);
		*/
	}

}

package game;

import java.util.Random;
import java.util.ArrayList;
import java.util.Arrays;
import utility.ShuffleList;
import rules.GoldenFlower;
import utility.Combo;



public class TenThousandGame {
	
	public ArrayList<Integer> deck;

	public TenThousandGame(){
		GoldenFlower flower = new GoldenFlower();
		
		ArrayList<Integer> banker = flower.BankerDrawCards();		
		ArrayList<Integer> player1 = flower.Player1DrawCards();		
		ArrayList<Integer> player2 = flower.Player2DrawCards();		
		ArrayList<Integer> player3 = flower.Player3DrawCards();		
		ArrayList<Integer> player4 = flower.Player4DrawCards();
		
		Combo result = flower.Compare(banker, player1);
		System.out.println(result.type+","+result.winner);
	}
	
}


package game;

import java.util.Random;
import java.util.ArrayList;
import utility.ShuffleList;



public class TenThousandGame {
	
	public ArrayList<Integer> deck;

	public TenThousandGame(){
		int NUM_CARDS = 52;
		// Initialization
		int[] deck = new int[NUM_CARDS];
		for (int i=1; i<=NUM_CARDS; i++){
			deck[i-1] = i;
		}
		// Shuffle
		//ShuffleList shuffle = new ShuffleList();
		//shuffle.shuffleArray(deck);
		ShuffleList.shuffleArray(deck);		
		ArrayList<Integer> shuffle_deck = new ArrayList<Integer>();
		for (int i=0; i<NUM_CARDS; i++){
			shuffle_deck.add(deck[i]);
		}
		
		this.deck = shuffle_deck;
		
		ArrayList<Integer> banker = BankerDrawCards();		
		ArrayList<Integer> player1 = Player1DrawCards();		
		ArrayList<Integer> player2 = Player2DrawCards();		
		ArrayList<Integer> player3 = Player3DrawCards();		
		ArrayList<Integer> player4 = Player4DrawCards();
				
		System.out.println("Banker:"+banker);
		for (int i=0; i<3; i++){
			Card card = Num2Card(banker.get(i));
			System.out.print("("+card.rank+","+card.suit+"); ");
		}
		System.out.println();
		System.out.println("Player1:"+player1);
		System.out.println("Player2:"+player2);
		System.out.println("Player3:"+player3);
		System.out.println("Player4:"+player4);
		
		
		
		Combo result = Compare(banker, player1);
		System.out.println(result.type+","+result.winner);
	}
	
	public ArrayList<Integer> BankerDrawCards(){
		ArrayList<Integer> banker = new ArrayList<Integer>();
		int start = 0;
		for (int i=start; i<start+3; i++ ){
			banker.add(this.deck.get(i));
		}
		return banker;
	}
	
	public ArrayList<Integer> Player1DrawCards(){
		ArrayList<Integer> banker = new ArrayList<Integer>();
		int start = 3;
		for (int i=start; i<start+3; i++ ){
			banker.add(this.deck.get(i));
		}
		return banker;
	}
	
	public ArrayList<Integer> Player2DrawCards(){
		ArrayList<Integer> banker = new ArrayList<Integer>();
		int start = 6;
		for (int i=start; i<start+3; i++ ){
			banker.add(this.deck.get(i));
		}
		return banker;
	}
	
	public ArrayList<Integer> Player3DrawCards(){
		ArrayList<Integer> banker = new ArrayList<Integer>();
		int start = 9;
		for (int i=start; i<start+3; i++ ){
			banker.add(this.deck.get(i));
		}
		return banker;
	}
	
	public ArrayList<Integer> Player4DrawCards(){
		ArrayList<Integer> banker = new ArrayList<Integer>();
		int start = 12;
		for (int i=start; i<start+3; i++ ){
			banker.add(this.deck.get(i));
		}
		return banker;
	}
	
	
	private static class Combo {
		String type; // scatter,pair,straight, flush, straightFlush, leopard, leopardKiller
	    int winner; // 1 means banker wins; 2 means player wins
	}
	
	private static class Card {
		String suit; // spade, heart, club, diamond
	    int rank; // 1,2,3,4,5,6,7,8,9,10,11,12,13
	}
	
	public Card Num2Card(int a){
		/* input an integer from 1 to 52, output the corresponding suit&rank */
		Card card = new Card();
		int suitNum = a%4;
		if(suitNum==0){
			card.suit = "diamond";
			card.rank = a/4;
		}else if(suitNum==1){
			card.suit = "spade";
			card.rank = a/4 + 1;
		}else if(suitNum==2){
			card.suit = "heart";
			card.rank = a/4 + 1;
		}else if(suitNum==3){
			card.suit = "club";
			card.rank = a/4 + 1;
		}
		return card;
	}
	
	public Combo Compare(ArrayList<Integer> banker, ArrayList<Integer> player){
		
		ArrayList<Card> bankerCard = new ArrayList<Card>();
		ArrayList<Card> playerCard = new ArrayList<Card>();
		for (int i=0; i<3; i++){
			Card card = Num2Card(banker.get(i));
			bankerCard.add(card);
		}
		for (int i=0; i<3; i++){
			Card card = Num2Card(player.get(i));
			playerCard.add(card);
		}
		
		for (int i=0; i<3; i++){
			Card bcard = bankerCard.get(i);
			Card pcard = playerCard.get(i);
			System.out.print(bcard.rank + "," + bcard.suit);
			System.out.print(" | ");
			System.out.print(pcard.rank + "," + pcard.suit);
			System.out.println();
		} 
		
		Combo result = new Combo();
		result.type = "scatter";
		result.winner = 1;
		return result;
	}
}

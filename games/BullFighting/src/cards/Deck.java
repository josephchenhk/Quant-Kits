package cards;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class Deck{
	public int n;
	public int m;
	public Map<Integer, Card> deck;
	
	/**
	 * This Deck class allows for more than one deck.
	 * @param num_deck The number of deck used in a game.
	 */
	public Deck(int num_deck){
		Map<Integer,Card> deck = new HashMap<Integer,Card>();
		for(int j=0; j<num_deck; j++){
			for(int i=1; i<=52; i++){
				//System.out.print("("+i+")");
				n = i/4;
				m = i%4;				
				if(m!=0){
					//System.out.println("["+(n+1)+","+m+"]");
					Card card = new Card(n+1, m);
					deck.put(i+j*52, card);
				}
				else{
					//System.out.println("["+n+","+(m+4)+"]");
					Card card = new Card(n, m+4);
				    deck.put(i+j*52, card);
				}
			}
		}		
		this.deck = deck;
	} 
	
	/**
	 * This method randomly draws a card from the deck. The deck will automatically remove the drawed card.
	 * @return The draw card.
	 */
	public Card Draw(){
		Random rand = new Random();
		int rand_idx = rand.nextInt(deck.keySet().size());
		int rand_num = (Integer) deck.keySet().toArray()[rand_idx];
		Card card = deck.get(rand_num);
		deck.remove(rand_num);
		return card;
	}
	
} 



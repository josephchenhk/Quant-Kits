package game;

import java.util.ArrayList;
import java.util.List;

import cards.Card;
import cards.Deck;



public class BullFighting {
	public Deck deck;
	public Card card;
	public List<Card> red;
	public List<Card> blue;
	public BettingAccount account;
	
	public BullFighting(){
		init();
	}
	
	public void new_game(){
		this.deck = new Deck(Config.num_deck);
		this.red = new ArrayList<Card>();
		this.blue = new ArrayList<Card>();
	}
	
	public void init(){
		this.account = new BettingAccount();
	}
	
	public void play(){
		for(int i=0; i<Config.num_sim; i++){
			new_game();	
			
			// First, each party gets a revealed card
			card = deck.Draw();
	        red.add(card);
	        card = deck.Draw();
	        blue.add(card);
	        System.out.println(red.get(0) + "  " + blue.get(0));
	        
	        // Second, place bets
	        for(int j=0; j<Config.sim_choices.size(); j++){
	        	String choice = Config.sim_choices.get(j);
	        	account.place_bet(choice, Config.min_stake);
	        }
	        System.out.println(account);
	        // 
		}
	}

}

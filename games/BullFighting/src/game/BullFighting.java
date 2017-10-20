package game;

import java.util.ArrayList;
import java.util.Arrays;
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
	
	public void newGame(){
		this.deck = new Deck(Config.num_deck);
		this.red = new ArrayList<Card>();
		this.blue = new ArrayList<Card>();
	}
	
	public void init(){
		this.account = new BettingAccount();
	}
	
	public void play(){
		int count_double_bb = 0;
		for(int i=0; i<Config.num_sim; i++){
			newGame();	
			
			// First, each party gets a revealed card
			card = deck.Draw();
	        red.add(card);
	        card = deck.Draw();
	        blue.add(card);
	        /*System.out.print("Red: "+red.get(0) + "  Blue: "+blue.get(0));*/
	        
	        // Second, place bets
	        for(int j=0; j<Config.sim_choices.size(); j++){
	        	String choice = Config.sim_choices.get(j);
	        	account.placeBet(choice, Config.min_stake);
	        }
	        /*System.out.println(account);*/
	        
	        // Third, each party gets THREE more revealed cards
	        for (int j=0; j<3; j++){
	        	card = deck.Draw();
		        red.add(card);
		        card = deck.Draw();
		        blue.add(card);
	        }
	        /*
	        for (int j=0; j<4; j++){
	        	System.out.println("Red: "+red.get(j) + "  Blue: "+blue.get(j));
	        }*/
	        
	        // Fourth, each team leader chooses another card
	        card = deck.Draw();
	        red.add(card);
	        card = deck.Draw();
	        blue.add(card);
	        /*
	        for (int j=0; j<5; j++){
	        	System.out.println("Red: "+red.get(j) + "  Blue: "+blue.get(j));
	        }*/
	        //System.out.println(deck.deck.size());
	        
	        // Fifth, check hand cards
	        String red_hand = CheckHands.check(red);
	        String blue_hand = CheckHands.check(blue);
	        //System.out.println(red_hand + " vs " + blue_hand);
	        
	        // Sixth, check choices hit
	        List<String> choices_hit = new ArrayList<String>();
	        int red_score = CheckHands.handScore(red_hand);
	        int blue_score = CheckHands.handScore(blue_hand);
	        if (red_score > blue_score){
	        	choices_hit.add("Red Win");
	        }else if (red_score < blue_score){
	        	choices_hit.add("Blue Win");
	        }else{
	        	choices_hit.add("Tie");
	        }
	        if (red_hand=="Bull Bull" && blue_hand=="Bull Bull"){
	        	choices_hit.add("Double Bull Bull");
	        	count_double_bb += 1;
	        }
	        List<String> either_choice = Arrays.asList("No Bull", "Bull 1", "Bull 2", "Bull 3", "Bull 4",
	        		"Bull 5", "Bull 6", "Bull 7", "Bull 8", "Bull 9", "Bull Bull", 
	        		"Silver Bull - Gold Bull - Bomb - Five Little Bull");
	        for (String ch: either_choice){
	        	if (ch.contains(red_hand) || ch.contains(blue_hand)){
		        	choices_hit.add(ch);
		        }
	        }      
	        //System.out.println(choices_hit);
	        
	        // Seventh, check pay table and update payments
	        for(int j=0; j<Config.sim_choices.size(); j++){
	        	String choice = Config.sim_choices.get(j);
	        	if (choices_hit.contains(choice)){
	        		double payment = PayTable.getOdd(choice);
	        		account.updateReturn(choice, payment);
	        	}        		
	        }
	        
	        //System.out.println(account);
		}
		System.out.println("Count double bull bull: " + count_double_bb);
	}

}

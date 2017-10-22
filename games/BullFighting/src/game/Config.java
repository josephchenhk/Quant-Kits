package game;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public interface Config {
	int num_sim = 100; //200000000;      // Number of simulations
	int num_player = 1;	
	int num_deck = 1;              // Number of decks
	double total_stake = 0.0;
	double total_return = 0.0;
	double min_stake = 1.0;            // Stake at each game
	
	/*
	List<String> choices = Arrays.asList("No Bull", "Bull 1", "Bull 2", "Bull 3", "Bull 4", "Bull 5",
			"Bull 6", "Bull 7", "Bull 8", "Bull 9", "Bull Bull", "Double Bull Bull", "Silver Bull",
			"Gold Bull", "Bomb", "Five Little Bull", "Red Win", "Blue Win", "Tie");
	
	List<String> sim_choices = Arrays.asList("No Bull", "Bull 1", "Bull 2", "Bull 3", "Bull 4", "Bull 5",
			"Bull 6", "Bull 7", "Bull 8", "Bull 9", "Bull Bull", "Double Bull Bull", "Silver Bull",
			"Gold Bull", "Bomb", "Five Little Bull", "Red Win", "Blue Win", "Tie");
	*/
	
	List<String> choices = Arrays.asList("No Bull", "Bull 1", "Bull 2", "Bull 3", "Bull 4", "Bull 5",
			"Bull 6", "Bull 7", "Bull 8", "Bull 9", "Bull Bull", "Double Bull Bull", 
			"Silver Bull - Gold Bull - Bomb - Five Little Bull", 
			"Red Win", "Blue Win", "Tie");
	
	List<String> sim_choices = Arrays.asList("No Bull", "Bull 1", "Bull 2", "Bull 3", "Bull 4", "Bull 5",
			"Bull 6", "Bull 7", "Bull 8", "Bull 9", "Bull Bull", "Double Bull Bull", 
			"Silver Bull - Gold Bull - Bomb - Five Little Bull", 
			"Red Win", "Blue Win", "Tie");
}

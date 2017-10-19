package game;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class BettingAccount {
	/*
	List<Double> no_bull          = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bull_1           = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bull_2           = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bull_3           = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bull_4           = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bull_5           = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bull_6           = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bull_7           = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bull_8           = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bull_9           = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bull_bull        = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> double_bull_bull = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> silver_bull      = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> gold_bull        = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> bomb             = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> five_little_bull = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> red_win          = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> blue_win         = new ArrayList<>(Arrays.asList(0.0, 0.0));
	List<Double> tie              = new ArrayList<>(Arrays.asList(0.0, 0.0));
	*/
	
	public Map<String, List<Double>> account;
	
	public BettingAccount(){
		account = new HashMap<String, List<Double>>();
		for (int i=0; i<Config.choices.size(); i++){
			String choice = Config.choices.get(i);
			List<Double> init_acc = new ArrayList<>(Arrays.asList(0.0, 0.0));
			account.put(choice, init_acc);
		}
	}
	
	public void place_bet(String choice, double bet){
		account.put(choice, Arrays.asList(account.get(choice).get(0)+bet, account.get(choice).get(1)));
	}
	
	public void update_return(String choice, double payment){
		account.put(choice, Arrays.asList(account.get(choice).get(0), account.get(choice).get(1)+payment));
	}
	
	public String toString(){
		String output = "";
		for (Map.Entry<String, List<Double>> pair : account.entrySet()) {
		    output += pair.getKey() + ": " + pair.getValue() + "\n";
		}
		return output;
	}
	
	public List<Double> getAccount(String choice){
		return account.get(choice);
	}
}

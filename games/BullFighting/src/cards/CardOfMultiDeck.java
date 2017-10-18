package cards;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class CardOfMultiDeck{
	int n;
	int m;
	Map<Integer,List<Integer>> card;
	
	public CardOfMultiDeck(int num_deck){
		Map<Integer,List<Integer>> card = new HashMap<Integer,List<Integer>>();
		for(int j=0; j<num_deck; j++){
			for(int i=1; i<=52; i++){
				//System.out.print("("+i+")");
				n = i/4;
				m = i%4;
				
				if(m!=0){
					//System.out.println("["+(n+1)+","+m+"]");
					List<Integer> list = new ArrayList<Integer>();
					list.add(n+1);
					list.add(m);
					card.put(i+j*52, list);
				}
				else{
					//System.out.println("["+n+","+(m+4)+"]");
					List<Integer> list = new ArrayList<Integer>();
					list.add(n);
					list.add(m+4);
					card.put(i+j*52, list);
				}
			}
		}
		
		this.card = card;
	} 
	
	public int Pop(Map<Integer,List<Integer>> card){
		
		Random rand = new Random();
		//System.out.print(card.keySet().size());
		int rand_idx = rand.nextInt(card.keySet().size());
		//System.out.println(rand_idx);
		int rand_num = (Integer) card.keySet().toArray()[rand_idx];
		//System.out.println(rand_num);

		//card.remove(rand_num); 
		return rand_num;
	}
	
	
} 


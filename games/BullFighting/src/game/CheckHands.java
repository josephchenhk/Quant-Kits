package game;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import cards.Card;
import utils.Combination;

public class CheckHands {

	/**
	 * Check the results of hand.
	 * @param hand Current hand with 5 cards
	 * @return The hand type
	 */
	public static String check(List<Card> hand){
		int rank1 = hand.get(0).rank;
		int rank2 = hand.get(1).rank;
		int rank3 = hand.get(2).rank;
		int rank4 = hand.get(3).rank;
		int rank5 = hand.get(4).rank;
		
		if (isFiveLittleBull(rank1, rank2, rank3, rank4, rank5)){
			return "Five Little Bull";
		}else if (isBomb(rank1, rank2, rank3, rank4, rank5)){
			return "Bomb";
		}else if (isGoldBull(rank1, rank2, rank3, rank4, rank5)){
			return "Gold Bull";
		}else if (isSilverBull(rank1, rank2, rank3, rank4, rank5)){
			return "Silver Bull";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==10){
			return "Bull Bull";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==9){
			return "Bull 9";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==8){
			return "Bull 8";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==7){
			return "Bull 7";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==6){
			return "Bull 6";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==5){
			return "Bull 5";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==4){
			return "Bull 4";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==3){
			return "Bull 3";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==2){
			return "Bull 2";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==1){
			return "Bull 1";
		}else if (isBullX(rank1 ,rank2, rank3, rank4, rank5)==0){
			return "No Bull";
		}
		
		return "Error!";
	}
	
	/**
	 * Check whether hand is Five Little Bull
	 * @param rank1
	 * @param rank2
	 * @param rank3
	 * @param rank4
	 * @param rank5
	 * @return true/false
	 */
	public static boolean isFiveLittleBull(int rank1, int rank2, int rank3, int rank4, int rank5){
		int sum_rank = rank1 + rank2 + rank3 + rank4 + rank5;
		if (rank1<5 && rank2<5 && rank3<5 && rank4<5 && rank5<5 && sum_rank<10){
			return true;
		}
		return false;		
	}
	
	/**
	 * Check whether hand is Bomb
	 * @param rank1
	 * @param rank2
	 * @param rank3
	 * @param rank4
	 * @param rank5
	 * @return true/false
	 */
	public static boolean isBomb(int rank1, int rank2, int rank3, int rank4, int rank5){
		int[] rank_array = {rank1, rank2, rank3, rank4, rank5};
		//Arrays.sort(rank_array);
		Set<Integer> rank_set = new HashSet<Integer>();
		rank_set.add(rank1);
		rank_set.add(rank2);
		rank_set.add(rank3);
		rank_set.add(rank4);
		rank_set.add(rank5);
		//System.out.println(rank_array[0] +","+ rank_array[1] +","+ rank_array[2] +","+ rank_array[3] +","+ rank_array[4]);
		List<List<Integer>> rank_occurance = new ArrayList<List<Integer>>();
		for (int rank: rank_set){
			int count = 0;
			for (int i=0; i<rank_array.length; i++){
				if (rank_array[i]==rank){
					count += 1;
				}
			}
			List<Integer> occur = Arrays.asList(rank, count);
			rank_occurance.add(occur);
		}
		/*
		for (int i=0; i<rank_occurance.size(); i++){
			System.out.println(rank_occurance.get(i));
		}*/
		
		if (rank_occurance.size()==1){ // This should never happen for one deck.
			return true;
		}else if (rank_occurance.size()==2){
			if (rank_occurance.get(0).get(1)>=4 || rank_occurance.get(1).get(1)>=4){
				return true;
			}
		}
		return false;
			
	}
	
	/**
	 * Check whether hand is Gold Bull
	 * @param rank1
	 * @param rank2
	 * @param rank3
	 * @param rank4
	 * @param rank5
	 * @return true/false
	 */
	public static boolean isGoldBull(int rank1, int rank2, int rank3, int rank4, int rank5){
		if (rank1>10 && rank2>10 && rank3>10 && rank4>10 && rank5>10){
			return true;
		}
		return false;
		
	}
	
	/**
	 * Check whether hand is Silver Bull
	 * @param rank1
	 * @param rank2
	 * @param rank3
	 * @param rank4
	 * @param rank5
	 * @return true/false
	 */
	public static boolean isSilverBull(int rank1, int rank2, int rank3, int rank4, int rank5){
		if (rank1>=10 && rank2>=10 && rank3>=10 && rank4>=10 && rank5>=10){
			if (!isGoldBull(rank1, rank2, rank3, rank4, rank5)){
				return true;
			}
		}
		return false;
	}
	
	/**
	 * Method to determine Bull X
	 * @param rank1
	 * @param rank2
	 * @param rank3
	 * @param rank4
	 * @param rank5
	 * @return Bull `X`, int from 0 to 10 (0 means no bull, while 10 means bull bull)
	 */
	public static int isBullX(int rank1, int rank2, int rank3, int rank4, int rank5){
		List<Integer> bull_x = new ArrayList<Integer>();
		List<Integer> rank_array = Arrays.asList(rank1, rank2, rank3, rank4, rank5);
		List<List<Integer>> comb3 = Combination.combinations(rank_array, 3);
		for (List<Integer> c3: comb3){
			List<Integer> c2 = new ArrayList<Integer>(rank_array);
			for (int i=0; i<c3.size(); i++){
				c2.remove(c3.get(i));
			}
			//System.out.println(c3 + "; " + c2);
			int sum_c3 = rankToNum(c3.get(0)) + rankToNum(c3.get(1)) + rankToNum(c3.get(2));
			int sum_c2 = rankToNum(c2.get(0)) + rankToNum(c2.get(1));
			if (sum_c3%10==0 && sum_c2%10==0){
				bull_x.add(10);
			}else if (sum_c3%10==0){
				bull_x.add(sum_c2%10);
			}else{
				bull_x.add(0);
			}
		}
		Collections.sort(bull_x);
		Collections.reverse(bull_x);
		return bull_x.get(0);
	}
	
	
	/**
	 * Another method to determine Bull X
	 * @param rank1
	 * @param rank2
	 * @param rank3
	 * @param rank4
	 * @param rank5
	 * @return Bull `X`, int from 0 to 10 (0 means no bull, while 10 means bull bull)
	 */
	/*public static int isBullX(int rank1, int rank2, int rank3, int rank4, int rank5){
		List<Integer> rank_array = Arrays.asList(rank1, rank2, rank3, rank4, rank5);
		int c1,c2,c3,c4,c5;
		for (int i=0; i<rank_array.size(); i++){
		    for (int j=i+1; j<rank_array.size(); j++){
		    	for (int k=j+1; k<rank_array.size(); k++){
		    		c1 = rank_array.get(i);
		    		c2 = rank_array.get(j);
		    		c3 = rank_array.get(k);
		    		
		    		c1 = Math.min(c1, 10);
		    		c2 = Math.min(c2, 10);
		    		c3 = Math.min(c3, 10);

		    		if((c1+c2+c3)%10==0){    			
		    			ArrayList<Integer> list_index = new ArrayList<Integer>(Arrays.asList(0,1,2,3,4));	    			
		    			list_index.remove(k);
		    			list_index.remove(j);
		    			list_index.remove(i);
		 
		    			c4 = rank_array.get(list_index.get(0));
		    			c5 = rank_array.get(list_index.get(1));
		    			
		    			c4 = Math.min(c4, 10);
			    		c5 = Math.min(c5, 10);
			    		
		    			if((c4+c5)%10==0){
		    				return 10;
		    			}else if((c4+c5)%10==9){
		    				return 9;
		    			}else if((c4+c5)%10==8){
		    				return 8;
		    			}else if((c4+c5)%10==7){
		    				return 7;
		    			}else if((c4+c5)%10==6){
		    				return 6;
		    			}else if((c4+c5)%10==5){
		    				return 5;
		    			}else if((c4+c5)%10==4){
		    				return 4;
		    			}else if((c4+c5)%10==3){
		    				return 3;
		    			}else if((c4+c5)%10==2){
		    				return 2;
		    			}else if((c4+c5)%10==1){
		    				return 1;
		    			}
		    		}
		    	}
		    }
		}
	    return 0;
	}*/

	/**
	 * Rank J/Q/K are treated as 10.
	 * @param rank
	 * @return min(rank,10)
	 */
	public static int rankToNum(int rank){
		if (rank>10){
			return 10;
		}else{
			return rank;
		}
	}
	
	/**
	 * The hand score.
	 * @param hand The hand result such as "Bull 1" or "Silver Bull"
	 * @return The score of the hand, in range of 0 to 14
	 */
	public static int handScore(String hand){
		if (hand=="No Bull"){
			return 0;
		}else if (hand=="Bull 1"){
			return 1;
		}else if (hand=="Bull 2"){
			return 2;
		}else if (hand=="Bull 3"){
			return 3;
		}else if (hand=="Bull 4"){
			return 4;
		}else if (hand=="Bull 5"){
			return 5;
		}else if (hand=="Bull 6"){
			return 6;
		}else if (hand=="Bull 7"){
			return 7;
		}else if (hand=="Bull 8"){
			return 8;
		}else if (hand=="Bull 9"){
			return 9;
		}else if (hand=="Bull Bull"){
			return 10;
		}else if (hand=="Silver Bull"){
			return 11;
		}else if (hand=="Gold Bull"){
			return 12;
		}else if (hand=="Bomb"){
			return 13;
		}else if (hand=="Five Little Bull"){
			return 14;
		}else{
			System.out.println("Input hand invalid: non-existing category.");
			return -1;
		}
	}
}

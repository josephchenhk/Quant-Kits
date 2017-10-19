package game;

public class PayTable {
	
	public static double getOdd(String hand){
		
		if (hand=="No Bull"){
			return 0.7 + 1.0;
		}else if (hand=="Bull 1"){
			return 5.0 + 1.0;
		}else if (hand=="Bull 2"){
			return 5.0 + 1.0;
		}else if (hand=="Bull 3"){
			return 5.0 + 1.0;
		}else if (hand=="Bull 4"){
			return 5.0 + 1.0;
		}else if (hand=="Bull 5"){
			return 5.0 + 1.0;
		}else if (hand=="Bull 6"){
			return 5.0 + 1.0;
		}else if (hand=="Bull 7"){
			return 5.0 + 1.0;
		}else if (hand=="Bull 8"){
			return 5.0 + 1.0;
		}else if (hand=="Bull 9"){
			return 5.0 + 1.0;
		}else if (hand=="Bull Bull"){
			return 5.0 + 1.0;
		}else if (hand=="Double Bull Bull"){
			return 100.0 + 1.0;
		}else if (hand=="Silver Bull"){
			return 200.0 + 1.0;
		}else if (hand=="Gold Bull"){
			return 200.0 + 1.0;
		}else if (hand=="Bomb"){
			return 200.0 + 1.0;
		}else if (hand=="Five Little Bull"){
			return 200.0 + 1.0;
		}else if (hand=="Red Win"){
			return 1.0 + 1.0;
		}else if (hand=="Blue Win"){
			return 1.0 + 1.0;
		}else if (hand=="Tie"){
			return 5.0 + 1.0;
		}else{
			System.out.println("[PayTable] Input hand invalid: non-existing category");
			return -1;
		}
		
	}
	
	

}

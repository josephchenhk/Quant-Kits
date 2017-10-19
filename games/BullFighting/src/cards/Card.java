package cards;

public class Card {
	public int rank;
	public int suit;
	
	public Card(int rank, int suit){
		this.rank = rank;
		this.suit = suit;
	}
	
	public String toString(){
		return "[Rank: " + rank + ", " + "Suit: " + suit + "]";
	}

}

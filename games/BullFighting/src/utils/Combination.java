package utils;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Combination {
	
	public static List<List<Integer>> combinations(List<Integer> groupSize, int k) {

	    List<List<Integer>> allCombos = new ArrayList<List<Integer>> ();
	    // base cases for recursion
	    if (k == 0) {
	        // There is only one combination of size 0, the empty team.
	        allCombos.add(new ArrayList<Integer>());
	        return allCombos;
	    }
	    if (k > groupSize.size()) {
	        // There can be no teams with size larger than the group size,
	        // so return allCombos without putting any teams in it.
	        return allCombos;
	    }

	    // Create a copy of the group with one item removed.
	    List<Integer> groupWithoutX = new ArrayList<Integer> (groupSize);
	    Integer x = groupWithoutX.remove(groupWithoutX.size()-1);

	    List<List<Integer>> combosWithoutX = combinations(groupWithoutX, k);
	    List<List<Integer>> combosWithX = combinations(groupWithoutX, k-1);
	    for (List<Integer> combo : combosWithX) {
	        combo.add(x);
	    }
	    allCombos.addAll(combosWithoutX);
	    allCombos.addAll(combosWithX);
	    return allCombos;
	}
		


}

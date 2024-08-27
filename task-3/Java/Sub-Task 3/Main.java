
import java.util.Scanner;


public class Main
{
    public static String repeat(String s, int n)
    {
        return new String(new char[n]).replace("\0", s);
    }
    
	public static void main(String[] args) {
	    
	    Scanner sc = new Scanner(System.in);
		System.out.println("Enter rows: ");
		
		int n = sc.nextInt();
        int counter = n%2;
        
        for (int i = 0; i < n; i++) {
        	if(counter == 0)
        	{
        		counter += 2;
        		continue;
        	}
        	
        	String stars = repeat("*", counter);
        	String spaces = repeat(" ", (int) (n-counter)/2);
        
        	if(i < (int) n/2) {
        		counter += 2;
        	} else {
        		counter -= 2;
        	}
        	
        	System.out.println(spaces+stars+spaces);
        }
	}
}
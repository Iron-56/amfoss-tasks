
import java.io.BufferedWriter;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class Main
{
    public static String repeat(String s, int n)
    {
        return new String(new char[n]).replace("\0", s);
    }
    
	public static void main(String[] args)
	{
	    int n = 0;
	    String pattern = "";
	    
	    try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
            n = Integer.parseInt(br.readLine());
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        int counter = n%2;
        
        for (int i = 0; i < n; i++)
		{
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
        	
        	pattern += spaces+stars+spaces+"\n";
        	
        }
        
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt"))) {
            writer.write(pattern);
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
	}
}
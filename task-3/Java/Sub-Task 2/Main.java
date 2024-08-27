
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class Main {
	public static void main(String[] args) throws IOException {
		File fi = new File("input.txt");
			
		Scanner scanner = new Scanner(fi);
		FileWriter writer = new FileWriter("output.txt");

		while (scanner.hasNextLine())
		{
			String data = scanner.nextLine()+"\n";
			writer.write(data);
		}
			
		scanner.close();
		writer.close();
	}
}

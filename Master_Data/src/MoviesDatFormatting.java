import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;


public class MoviesDatFormatting {
	File fInput=null;
	public static void main(String args[]) throws IOException
	{
		HashMap<Integer, Integer> hm = new HashMap<Integer,Integer>();
		FileReader fr=new FileReader(new File("/home/aneesh/aneesh_clodflix/total_movies_data.dat"));
		BufferedReader br =new BufferedReader(fr);
		String newLine;
		while((newLine=br.readLine())!=null)
		{
			//Some Movie are having empty fields instead having a dummy value '/N'
			newLine=newLine.replaceAll("		", "	/N	");
			StringTokenizer st=new StringTokenizer(newLine,"	");
			int count=st.countTokens();
			if(hm.containsKey(count))
			{
				hm.put(count, hm.get(count) + 1);
			}
			else
			{
				hm.put(count, 1);
			}	
		}
		for (Map.Entry<Integer, Integer> entry : hm.entrySet()) {
		    System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
		}
	}
	
	
	

}

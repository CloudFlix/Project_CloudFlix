import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.ObjectInputStream.GetField;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;


public class MovieDirectorsData {
	File fInput=null;
	 static int val=0;

	public static  HashMap<String, String> getDirectors() throws IOException
	{
		HashMap<String, String> hm = new HashMap<String,String>();
		FileReader fr=new FileReader(new File("/home/aneesh/aneesh_clodflix/movie_directors.dat"));
		BufferedReader br =new BufferedReader(fr);
		String newLine;
		while((newLine=br.readLine())!=null)
		{
			StringTokenizer st=new StringTokenizer(newLine,"	");
			int count=st.countTokens();
			String MovieId=st.nextToken().trim();
			st.nextToken();

				String DirectorName=st.nextToken().trim();

				if(hm.containsKey(MovieId))
				{
					hm.put(MovieId, hm.get(MovieId) +"::"+ DirectorName);
				}
				else
				{
					hm.put(MovieId, DirectorName);
				}	
			}

		

	for (Map.Entry<String, String> entry : hm.entrySet()) {
		//System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
		val++;	
	}
	
	System.out.println(val);
	return hm;
}
	
}

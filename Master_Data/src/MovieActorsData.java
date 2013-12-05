import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;


public class MovieActorsData {
	File fInput=null;
	 static int val=0;

	public  static HashMap<String, String> getActors() throws IOException
	{
		HashMap<String, String> hm = new HashMap<String,String>();
		FileReader fr=new FileReader(new File("/home/aneesh/aneesh_clodflix/movie_actors.dat"));
		BufferedReader br =new BufferedReader(fr);
		String newLine;
		while((newLine=br.readLine())!=null)
		{
			//Some actors are having empty fields instead having a dummy value '/N'
			newLine=newLine.replaceAll("		", "	/N	");
			StringTokenizer st=new StringTokenizer(newLine,"	");
			int count=st.countTokens();
			String MovieId=st.nextToken().trim();
			if(!st.nextToken().equalsIgnoreCase("not_applicable"))
			{

				String ActorName=st.nextToken().trim();

				if(hm.containsKey(MovieId))
				{
					hm.put(MovieId, hm.get(MovieId) +"::"+ ActorName);
				}
				else
				{
					hm.put(MovieId, ActorName);
				}	
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

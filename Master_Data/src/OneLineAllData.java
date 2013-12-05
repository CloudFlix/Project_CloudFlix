import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;


public class OneLineAllData {
	File fInput=null;
	static File file=null;
	static FileWriter fw=null;
	public static void main(String args[]) throws IOException
	{
		file=new File("/home/aneesh/aneesh_clodflix/total_movies_data.dat");
		fw=new FileWriter(file,true);
		HashMap<String,String> Actors =new HashMap<String,String>();
		HashMap<String,String> Directors =new HashMap<String,String>();
		Actors=MovieActorsData.getActors();
		Directors=MovieDirectorsData.getDirectors();
		FileReader fr=new FileReader(new File("/home/aneesh/aneesh_clodflix/movies.dat"));
		BufferedReader br =new BufferedReader(fr);
		String newLine=br.readLine();
		newLine=newLine.concat("	Actors	Directors");
		fw.write(newLine);
		fw.write("\n");
		while((newLine=br.readLine())!=null)
		{
			fw.write(newLine);
			StringTokenizer st=new StringTokenizer(newLine,"	");
			String MovieID = st.nextToken().trim();	
			if(Actors.containsKey(MovieID))
			{
				fw.write("	");
				fw.write(Actors.get(MovieID));
			}
			else
			{
				fw.write("	");
				fw.write("\\N");
			}
			if(Directors.containsKey(MovieID))
			{
				fw.write("	");
				fw.write(Directors.get(MovieID));
			}
			else
			{
				fw.write("	");
				fw.write("\\N");
			}	
			fw.write("\n");
			
		}
		fw.close();
	}




}

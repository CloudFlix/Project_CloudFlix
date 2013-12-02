import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
/*
 * Class to format ratings data & generate separate files, each containing 30 movies highly rated by
 * each user 
 */

public class ReviewFilesGen {

	void GenOutput(String folderpath)
	{
		try{
			BufferedReader br=new BufferedReader(new FileReader(folderpath));
			String line=br.readLine();
			while(line!=null)
			{
				StringBuilder sb=new StringBuilder();
				String parts[]=line.split("\t");
				String uid=parts[0];
				String recos=parts[1].substring(1,parts[1].length()-1);
				Pattern pattern=Pattern.compile("\\,(.*?):"); 
				Matcher matcher = pattern.matcher(recos);
				/*Split each line to get movie ids 
				 * Each line corresponds to each user
				*/
				while (matcher.find())
				{
					sb.append(matcher.group(1) + "\n");
				}
				pattern=Pattern.compile("^(.*?):");
				matcher = pattern.matcher(recos);
				if (matcher.find())
				{
					sb.append(matcher.group(1) + "\n");
				}
				try{
					String recoData=sb.toString();
					PrintWriter pw=new PrintWriter("userRatings/collabReco_" + uid + ".dat");
					pw.println(recoData);
					pw.close();
				}catch(Exception e)
				{
					
				}
				line=br.readLine();
			}
		}
		catch(Exception e)
		{
			
		}
		
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
			ReviewFilesGen gs=new ReviewFilesGen();
			gs.GenOutput("part-r-00000");
	}

}

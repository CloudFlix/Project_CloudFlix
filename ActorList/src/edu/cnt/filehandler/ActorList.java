package edu.cnt.filehandler;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ActorList 
{
static File file = new File("./output/newFile.txt");  
static PrintWriter writer ;
	public static void main(String args[])
	{
		try{
			// Open the file that is the first 
			// command line parameter
			FileInputStream fstream = new FileInputStream("./input/actors.list");
		  //  fout= new FileOutputStream(new File("./output/newFile.txt"));
		    writer= new PrintWriter(file);
		    // Get the object of DataInputStream
			DataInputStream in = new DataInputStream(fstream);
			BufferedReader br = new BufferedReader(new InputStreamReader(in));
			String strLine;
			//Read File Line By Line
			StringBuffer str1=new StringBuffer();
			while ((strLine = br.readLine()) != null)   {
				// Print the content on the console
				//System.out.println (strLine);
				if(!strLine.isEmpty())
					str1.append(strLine);
				else
				{   

					if(!str1.equals(null))
						someFunction(str1);  
					str1.delete(0, str1.length());
				}
			}
			//Close the input stream
			in.close();
		}catch (Exception e){//Catch exception if any
			System.err.println("Error: " + e.getMessage());
		}
	}

	private static  void someFunction(StringBuffer str1) throws IOException {
		System.out.println("=---------------------=");
		String str=str1.toString();
		str=str.replaceAll("			","		").replaceAll("		","	");
		String[] pairs=str.split("	");
		StringBuffer finalString=new StringBuffer();
		doSomeMore(finalString,pairs);
		//		System.exit(0);
		// TODO Auto-generated method stub
	}

	private static  void doSomeMore(StringBuffer finalString,String[] pairs) throws IOException {
		// TODO Auto-generated method stub
		//Sure that actor is printed only if it has some movies
		String Actor=pairs[0].trim();

		for(int i=1;i<pairs.length;i++)
		{
			String temp=pairs[i];
			String pattern="\\(([0-9]{4})\\)";
			temp=temp.trim();

			int retVal;
			if(!(temp.indexOf("\"")==0))
			{
				retVal=printMatches(temp,pattern);
				System.out.println(retVal);

				if(retVal!=-1)
					finalString.append("::"+temp.substring(0,retVal).trim());
			}

		}

		if(!finalString.toString().isEmpty())
		{
			writer.println(Actor.concat(finalString.toString()));

		}
	}


	public static int printMatches(String text, String regex) {
		Pattern pattern = Pattern.compile(regex);
		Matcher matcher = pattern.matcher(text);
		// Check all occurrences
		while (matcher.find()) {
			//System.out.println(" Found: " + matcher.group());
			return matcher.start();
		}
		return -1;
	}

}

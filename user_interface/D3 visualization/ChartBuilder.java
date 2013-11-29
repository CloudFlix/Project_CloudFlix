import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeMap;
import java.util.TreeSet;


class MovieInfo{
	int yearRange;
	String name;
	int numRecos;
}

public class ChartBuilder {

	static HashMap<String,Integer> movieCount=new HashMap<String,Integer>();
	static HashMap<Integer,String> movieIdPair=new HashMap<Integer,String>();
	static HashMap<String,Integer> movieYearPair=new HashMap<String,Integer>();
	static LinkedHashMap<String,Integer> sortedByCount=new LinkedHashMap<String,Integer>();
	static LinkedList ll[]=new LinkedList[10];
	
	void BuildMovieCount(String folderpath) throws FileNotFoundException
	{
		File folder = new File(folderpath);
		File[] listOfFiles = folder.listFiles();

		//for all files in folder
		for (File file : listOfFiles) 
		{
		    if (file.isFile()) 
		    {
		    	BufferedReader br=new BufferedReader(new FileReader(folderpath + file.getName()));
		    	 try
		    	 {
		    	   String line = br.readLine();
		    	   while (line != null)
		    	   {
		    		   String parts[]=line.split("\t");
		    		    Integer movieid=Integer.parseInt(parts[0]);
		    		  //  System.out.println(movieid);
		    		    String moviename=movieIdPair.get(movieid);
		    		   // System.out.println(moviename);
		    		    if(!movieCount.containsKey(moviename))
		    		    {
		    		    	//System.out.println(moviename);
		    		    	movieCount.put(moviename,1);
		    		    }
		    		    else
		    		    {
		    		    	Integer currCount=movieCount.get(moviename);
		    		    	//System.out.println(currCount + "----" + moviename);
		    		    	currCount+=1;
		    		    	movieCount.put(moviename, currCount);
		    		    }   
		    	        line = br.readLine();
		    	    }
		    	    
		    	  } 
		    	  catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					} 
		    }
		}
		sortedByCount=sortHashMapByValuesD(movieCount);
		
		//BuildJson1(5);
	}
	
	void BuildMovieIdPairs(String movieDataPath)
	{
		try
		{
		BufferedReader br=new BufferedReader(new FileReader(movieDataPath));
        br.readLine();
		String line=br.readLine();
		while(line!=null)
		{
			String parts[]=line.split("\t");
			movieIdPair.put(Integer.parseInt(parts[0]),parts[1]);
			movieYearPair.put(parts[1], Integer.parseInt(parts[5]));
			//System.out.println(parts[0] + "-----------" + parts[1]);
			line=br.readLine();
		}
		}
		catch(IOException e)
		{
			
		}
	}
	static LinkedHashMap sortHashMapByValuesD(HashMap passedMap) {
		   java.util.List mapKeys = new ArrayList(passedMap.keySet());
		   java.util.List mapValues = new ArrayList(passedMap.values());
		   Collections.sort(mapValues,Collections.reverseOrder());
		 //  Collections.sort(mapKeys);

		   LinkedHashMap sortedMap = new LinkedHashMap();

		   Iterator valueIt = mapValues.iterator();
		   while (valueIt.hasNext()) {
		       Object val = valueIt.next();
		       Iterator keyIt = mapKeys.iterator();

		       while (keyIt.hasNext()) {
		           Object key = keyIt.next();
		           String comp1 = passedMap.get(key).toString();
		           String comp2 = val.toString();

		           if (comp1.equals(comp2)){
		               passedMap.remove(key);
		               mapKeys.remove(key);
		               sortedMap.put((String)key, (Integer)val);
		               break;
		           }

		       }

		   }
		   return sortedMap;
		}
	static void SetMatrix(int topN)
	{
		Iterator it = sortedByCount.entrySet().iterator();
		for(int i=0;i<10;i++)
		{
			ll[i]=new LinkedList();
		}
	    while (it.hasNext() && topN>0 ) {
	        Map.Entry pairs = (Map.Entry)it.next();
	        String movieName=(String)pairs.getKey();
	        Integer movieCount=(Integer)pairs.getValue();
	       // System.out.println(pairs.getKey() + " = " + pairs.getValue());
	        //it.remove();
	        if(movieName!=null)
	        {	
	        Integer year=movieYearPair.get(movieName);
	        MovieInfo m=new MovieInfo();
	        m.name=movieName;
        	m.numRecos=movieCount;
        	
	        if(year<1960)
	        {
	        	m.yearRange=1900;
	        	ll[0].add(m);
	        }
	        else if(year>=1960 && year<1970)
	        {
	        	m.yearRange=1960;
	        	ll[1].add(m);
	        }
	        else if(year>=1970 && year<1980)
	        {
	        	m.yearRange=1970;
	        	ll[2].add(m);
	        }
	        else if(year>=1980 && year<1990)
	        {
	        	m.yearRange=1980;
	        	ll[3].add(m);
	        }
	        else if(year>=1990 && year<2000)
	        {
	        	m.yearRange=1990;
	        	ll[4].add(m);
	        }
	        else if(year>=2000 && year<2010)
	        {
	        	m.yearRange=2000;
	        	ll[5].add(m);
	        }
	        else if(year>=2010)
	        {
	        	m.yearRange=2010;
	        	ll[6].add(m);
	        }
	        } 	
	        topN--;
	    }
	}
	
   /* static void WriteJson()
	{
		//MovieInfo x1=(MovieInfo)ll[4].getFirst();
		//System.out.println(x1.yearRange);
		//System.out.println(x1);
		StringBuilder sb=new StringBuilder();
		sb.append("{");
		sb.append("\n" + "\"name\":\"flare\",");
		sb.append("\n" + "\"children\":[");
		for(int i=0;i<ll.length;i++)
		{
			if(ll[i].size()!=0)
			{
			sb.append("\n{");
				
			MovieInfo currrange=(MovieInfo)ll[i].get(0);
			sb.append("\n" + "\"name\":\"" + currrange.yearRange +"\",");
			sb.append("\n" + "\"children\":[");
			int j=0;
			MovieInfo x1;
		    for(j=0;j<ll[i].size()-1;j++)
			{
		    	x1=(MovieInfo)ll[i].get(j);
		    	sb.append("\n{" + "\"name\":\"" + x1.name +"\",\"size\":" + x1.numRecos + "},");
			}
		    x1=(MovieInfo)ll[i].get(j);
		    sb.append("\n{" + "\"name\":\"" + x1.name +"\",\"size\":" + x1.numRecos + "}");
		    sb.append("\n]},");	
			}
		}
		sb.replace(sb.length()-1,sb.length()," ");
		sb.append("\n]}");
		String Json=sb.toString();
		try{
			PrintWriter pw=new PrintWriter("Flare.json");
			pw.println(Json);
			pw.close();
		}catch(Exception e)
		{
			
		}
	}*/
	static void writeHtml(int topNmovies)
	{
		StringBuilder sb=new StringBuilder();
		sb.append("<html><head>");
		sb.append("\n<title> Top " + topNmovies + " recommended movies</title>" );
	    sb.append("\n<script type=\"text/javascript\" src=\"http://d3js.org/d3.v2.js\"></script>");
	    sb.append("\n<script type=\"text/javascript\" src=\"http://www.treesheets.org/hotlink/cts.js\"></script>");
	    sb.append("\n<script type=\"text/cts\" src=\"http://people.csail.mit.edu/eob/cts/widgets/bubblechart.cts\"></script>");
	    sb.append("\n</head>\n<body>\n<div class=\"bubblechart\">\n<ul class=\"bubblechains\">");
	    for(int i=0;i<ll.length;i++)
	    {
	    	if(ll[i].size()!=0)
			{
			sb.append("\n<li>");
			MovieInfo currrange=(MovieInfo)ll[i].get(0);
			sb.append("\n<span>" + currrange.yearRange + "</span>");	
			sb.append("\n<table>");
			int j=0;
			MovieInfo x1;
		    for(j=0;j<ll[i].size();j++)
			{
		    	x1=(MovieInfo)ll[i].get(j);
		    	sb.append("\n<tr><td>" + x1.name +"</td><td>" + x1.numRecos + "</td></tr>");
			}
		    sb.append("\n</table>\n</li>");	
			}
	    }
	    sb.append("</ul></div></body></html>");
	    String htmlData=sb.toString();
		try{
			PrintWriter pw=new PrintWriter("RecoAdmin.html");
			pw.println(htmlData);
			pw.close();
		}catch(Exception e)
		{
			
		}
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		//args[0]:top n movies
		//args[1]:path of recom files
		//args[2]:path to movie list
		if(args.length!=3)
			System.out.println("Invalid number of arguments");
		else
		{	
		ChartBuilder js=new ChartBuilder();
		js.BuildMovieIdPairs(args[2]);
		try {
			js.BuildMovieCount(args[1]);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	
		SetMatrix(Integer.parseInt(args[0]));
		writeHtml(Integer.parseInt(args[0]));
		}
		//WriteJson();
	}
   
}


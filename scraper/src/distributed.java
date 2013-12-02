

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.Iterator;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;

import com.gargoylesoftware.htmlunit.FailingHttpStatusCodeException;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.html.HtmlPage;
//class that contains map and reduce
public class distributed {

	public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {


		//map function makes (key,value) of (word,occurence) 
		public void map(LongWritable key, Text value, OutputCollector<Text, Text> output, Reporter reporter) throws IOException {
			String imdb_id="";
			Text link_localID = new Text();
			String link = "http://www.imdb.com/title/tt/reviews?start=0";
			String localID = "";
			String line = value.toString();
			StringTokenizer tokenizer = new StringTokenizer(line,"::");


			if(tokenizer.hasMoreTokens()) 
				localID = tokenizer.nextToken().toString();



			if(tokenizer.hasMoreTokens()){
				imdb_id = tokenizer.nextToken();
				//System.out.println(imdb_id);
			}
			link = link.replaceAll("/tt/", "/tt"+imdb_id+"/");
			link_localID.set(link+"::"+localID);
			//System.out.println(link_localID);	                

			output.collect(new Text(localID), new Text(link));	        

		}
	}

	public static class Reduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {
		public void reduce(Text key, Iterator<Text> values, OutputCollector<Text, Text> output, Reporter reporter) throws IOException {
			String link;
			String localID = key.toString();
			String reviews = "";

			if(values.hasNext())
			{
				//String link_localID[]=values.next().toString().split("::");
				link = values.next().toString();

				int cnt = 0;
				
				//System.out.println(link_localID);

				final WebClient webClient = new WebClient();
				webClient.getOptions().setJavaScriptEnabled(false);
				while(cnt < 50) {	    //cnt<10 will fetch 10 reviews
					System.out.println(link);
					
					try {
						HtmlPage page = webClient.getPage(link);
						String page2 = page.asXml();
						//System.out.println(page2);
						//Pattern pattern = Pattern.compile("Author:.*?<p>\\s*(.*)\\s*?</p>");
						Pattern pattern = Pattern.compile("Author:.*?</div>.*?<p>(.*?)</p>", Pattern.DOTALL);    		
						Matcher matcher = pattern.matcher(page2);
						int i = 1;
						while (matcher.find()) {
							//System.out.printf("Review: %d\n", i);
							//System.out.print("Start index: " + matcher.start());
							//System.out.print(" End index: " + matcher.end() + " ");
							String temp = matcher.group(1);
							//System.out.println(temp);
							temp =temp.replaceAll("<p>.*?This review may contain spoilers.*?</p>", "");
							temp =temp.replaceAll("\\s*<.*?>\\s*", " ");
							temp =temp.replaceAll("\\n", " ");
							temp =temp.replaceAll("[^A-Za-z0-9 _\\.,:;\\!\"\'/$\\-\\(\\)&]", "");
							temp =temp.replaceAll("\\s+", " ");
							temp =temp.replaceAll("^\\s+", "");
							temp =temp.replaceAll("\\s+$", "");
							//System.out.println(temp);

							if(cnt == 0 && i == 1)
								reviews += temp;
							else
								reviews += "||"+temp;

							i++;
						}

					} catch (final FailingHttpStatusCodeException e) {
						System.out.println("One");
						e.printStackTrace();
					} catch (final MalformedURLException e) {
						System.out.println("Two");
						e.printStackTrace();
					} catch (final IOException e) {
						System.out.println("Three");
						e.printStackTrace();
					} catch (final Exception e) {
						System.out.println("Four");
						e.printStackTrace();
					}
					//System.out.println("Finished");


					//final String pageAsXml = page.asXml();
					//Assert.assertTrue(pageAsXml.contains("<body class=\"composite\">"));

					//final String pageAsText = page.asText();
					//Assert.assertTrue(pageAsText.contains("Support for the HTTP and HTTPS protocols"));

					
					cnt += 10;
					link = link.replaceAll("\\?start=.*?$", "\\?start="+cnt);
					//http://www.imdb.com/title/tt0405159/reviews?start=0
				}
				webClient.closeAllWindows();
				output.collect(new Text(localID), new Text(reviews));
			}
		}
	}

	public static void main(String[] args) throws Exception {
		JobConf conf = new JobConf(distributed.class);
		conf.setJobName("Distributed_Scraping");
		conf.setJarByClass(distributed.class);
		//Set io types
		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(Text.class);

		conf.setMapperClass(Map.class);
		conf.setReducerClass(Reduce.class);

		conf.setInputFormat(TextInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);

		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));

		//Start MapReduce
		JobClient.runJob(conf);
	}
}

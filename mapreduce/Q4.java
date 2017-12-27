package edu.gatech.cse6242; 

import java.io. * ; 
import java.lang. * ; 
import org.apache.hadoop.fs.Path; 
import org.apache.hadoop.conf.Configuration; 
import org.apache.hadoop.io. * ; 
import org.apache.hadoop.mapreduce. * ; 
import org.apache.hadoop.util. * ; 
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat; 
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat; 
// import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
// import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import java.io.IOException; 

public class Q4 {

  public static class M1
       extends Mapper < Object, Text, Text, IntWritable >  {
    public void map(Object key, Text val, Context con
                    )throws IOException, InterruptedException {
      String line = val.toString();
      if (! line.isEmpty()) {
        String[] parts = line.split("\t"); 
        if (parts.length == 2) {
          con.write(new Text(parts[0]), new IntWritable(1)); 
          con.write(new Text(parts[1]), new IntWritable(-1)); 
        }
      }
    }
  }

  public static class R1
       extends Reducer < Text, IntWritable, Text, IntWritable >  {
    public void reduce(Text key, Iterable < IntWritable > values, 
                       Context con)throws IOException, InterruptedException {
      int sum = 0; 
      for (IntWritable val:values) {
          sum += val.get(); 
      }
      con.write(key, new IntWritable(sum)); 
    }
  }

  public static class M2
       extends Mapper < LongWritable, Text, Text, IntWritable >  {
    public void map(LongWritable key, Text val, Context con)throws IOException, InterruptedException {
      String line = val.toString(); 
      if (line != null &&  ! line.isEmpty()) {
        String[] parts = line.split("\t"); 
        if (parts.length == 2) {
        	con.write(new Text(parts[1]), new IntWritable(1)); 
        }
      }
    }
  }

  public static void main(String[] args)throws Exception {
    Configuration conf = new Configuration(); 
    Job job1 = Job.getInstance(conf, "Q4"); 
    job1.setJarByClass(Q4.class); 
    job1.setMapperClass(M1.class); 
    job1.setCombinerClass(R1.class); 
    job1.setReducerClass(R1.class); 
    job1.setOutputKeyClass(Text.class); 
    job1.setOutputValueClass(IntWritable.class); 
    //FileInputFormat.addInputPath(job1, new Path(args[0]));
    //FileOutputFormat.setOutputPath(job1, new Path("out1"));
    // job1.setInputFormatClass(TextInputFormat.class);
    // job1.setOutputFormatClass(TextOutputFormat.class);
    FileInputFormat.addInputPath(job1, new Path(args[0])); 
    FileOutputFormat.setOutputPath(job1, new Path("tempoutputampr3")); 

    /*if (!job1.waitForCompletion(true)) {
      System.exit(1);
    }*/
    job1.waitForCompletion(true); 

    Job job2 = Job.getInstance(conf, "degree"); 
    job2.setJarByClass(Q4.class); 
    job2.setMapperClass(M2.class); 
    job2.setCombinerClass(R1.class); 
    job2.setReducerClass(R1.class); 
    job2.setOutputKeyClass(Text.class); 
    job2.setOutputValueClass(IntWritable.class); 
    //
    // /* TODO: Needs to be implemented */
    //
    // job2.setInputFormatClass(TextInputFormat.class);
    // job2.setOutputFormatClass(TextOutputFormat.class);
    FileInputFormat.addInputPath(job2, new Path("tempoutputampr3")); 
    FileOutputFormat.setOutputPath(job2, new Path(args[1])); 
    System.exit(job2.waitForCompletion(true)?0:1); 

  }
}

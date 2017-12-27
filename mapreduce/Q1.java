

import java.lang.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import java.io.IOException;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q1 {

  public static class TokenizerMapper
       extends Mapper<Object, Text, Text, IntWritable>{

    public void map(Object key, Text val, Context con
                    ) throws IOException, InterruptedException {
      int min = 0;
      String line = val.toString();
      String[] parts = line.split("\t");
      min = Integer.parseInt(parts[2]);
      con.write(new Text(parts[1]), new IntWritable(min));
    }
  }

  public static class IntMinReducer
       extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable res = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values,
                       Context con
                       ) throws IOException, InterruptedException {
      int min = Integer.MAX_VALUE;
      for (IntWritable val : values) {
        if(min > val.get()) {
          min= val.get();
        }
      }
      res.set(min);
      con.write(key, res);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1");
    job.setJarByClass(Q1.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntMinReducer.class);
    job.setReducerClass(IntMinReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}

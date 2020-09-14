import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
//import org.apache.hadoop.mapred.FileOutputFormat;
//import org.apache.hadoop.mapreduce.Mapper.Context;

public class Merge {
    public static class Map extends Mapper<Object,Text,Text, IntWritable> {
        private static Text text=new Text();
        private final IntWritable one =new IntWritable(1);

        public void map(Object key,Text value,Context context) throws IOException, InterruptedException{
            String line = value.toString();
            String[] arr = line.split(" ");
            String usr = arr[1];
            //text=value;
            context.write(new Text(usr), one);

        }

    }
    public static class Reduce extends Reducer<Text,IntWritable,Text,IntWritable>{
        private IntWritable result=new IntWritable();

        public void reduce(Text key, Iterable <IntWritable>values, Context context) throws IOException, InterruptedException{
            int count = 0;
            for(IntWritable val : values) {
                count += val.get();
            }
            result.set(count);
            context.write(key, result);
        }
    }
    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException{
        Configuration conf=new Configuration();
        conf.set("fs.defaultFS","hdfs://localhost:9000");
        String[] otherArgs=new String[]{"/usr/hadoop/input","/usr/hadoop/Input2"};
        if(otherArgs.length!=2){
            System.err.println("Usage:Merge and duplicate removal<in><out>");
            System.exit(2);
        }
        Job job=Job.getInstance(conf,"Merge and duplicate removal");
        job.setJarByClass(Merge.class);
        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job,new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job,new Path(otherArgs[1]));
        System.exit(job.waitForCompletion(true)?0:1);
    }
}
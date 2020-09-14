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

public class blacklist {

    public static class Mmap extends Mapper<Object,Text,Text, IntWritable> {
        private static Text text=new Text();
        private final IntWritable one =new IntWritable(1);

        public void map(Object key,Text value,Context context) throws IOException, InterruptedException{
            String line = value.toString();
            String[] arr = line.split(" ");
            String usr = arr[1];
            String[] data = arr[0].split("-");
            String[] time = data[3].split(":");
            int hashtime = Integer.parseInt(time[2]) + Integer.parseInt(time[1]) * 60 + Integer.parseInt(time[0]) * 3600 + Integer.parseInt(data[2]) * 24 * 3600 + Integer.parseInt(data[1]) * 30 * 24 * 3600;
            text = value;
            one.set(hashtime);
            context.write(new Text(usr), one);

        }

    }
    public static class Rreduce extends Reducer<Text,IntWritable,Text,IntWritable>{
        private IntWritable result=new IntWritable();
        public static final int base = 10;

        public void reduce(Text key, Iterable <IntWritable>values, Context context) throws IOException, InterruptedException{
            int count = 0;
            int now = 0;
            int last = 0;
            for(IntWritable val : values) {
                now = val.get();
                /**
                 * the method to define black list
                 */
                if((now - last) <= base && last != 0) {
                    count++;
                }
                else {
                    if(count >= 20) {
                        count -= 10;
                    }
                    else {
                        count = 0;
                    }
                }
                last = now;
            }
            if(count >= 30) {
                context.write(key, new IntWritable(count));  // blacklist & he's criminal times
            }
        }
    }
    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException{
        Configuration conf=new Configuration();
        conf.set("fs.defaultFS","hdfs://localhost:9000");
        String[] otherArgs=new String[]{"/usr/hadoop/input","/usr/hadoop/out2"};
        if(otherArgs.length!=2){
            System.err.println("Usage:Merge and duplicate removal<in><out>");
            System.exit(2);
        }
        Job job=Job.getInstance(conf,"Merge and duplicate removal");
        job.setJarByClass(blacklist.class);
        job.setMapperClass(Mmap.class);
        job.setReducerClass(Rreduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job,new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job,new Path(otherArgs[1]));
        System.exit(job.waitForCompletion(true)?0:1);
    }
}
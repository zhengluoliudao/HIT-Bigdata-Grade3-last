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
import java.util.Comparator;
import java.util.StringTokenizer;
import java.util.TreeMap;
import java.util.regex.Pattern;

public class Logs {

    public static class myMap extends Mapper<Object, Text, IntWritable,Text> {
        IntWritable outkey = new IntWritable();
        Text outvalue = new Text();
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            StringTokenizer str = new StringTokenizer(value.toString());
            while(str.hasMoreTokens()){
                String element = str.nextToken();
                if(Pattern.matches("\\d+", element)) {
                    outkey.set(-Integer.parseInt(element));
                }
                else {
                    outvalue.set(element);
                }
            }
            context.write(outkey,outvalue);
        }
    }

    public static class myReduce extends Reducer<IntWritable,Text,Text,IntWritable> {
        public static final int k = 20;  // top k
        public int count = 0;

        private static TreeMap<Integer, String> m = new TreeMap<Integer, String>(new Comparator<Integer>(){
            public int compare(Integer o1, Integer o2) {
                return o2.compareTo(o1);
            }
        });

        public void reduce(IntWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException{
            for(Text text : values) {
                int num = key.get();
                key.set(-num);
                if(count < k) {
                    context.write(text, key);
                    count++;
                }
                m.put(new Integer(key.get()), text.toString());
                if(m.size() > k) {
                   m.remove(m.lastKey());
                }
            }
        }
    }

    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException{
        Configuration conf=new Configuration();
        conf.set("fs.defaultFS","hdfs://localhost:9000");
        String[] otherArgs=new String[]{"/usr/hadoop/Input2","/usr/hadoop/out"}; //the path in hadoop of input & output
        if(otherArgs.length!=2){
            System.err.println("Usage:Merge and duplicate removal<in><out>");
            System.exit(2);
        }
        Job job=Job.getInstance(conf,"Merge and duplicate removal");
        job.setJarByClass(Logs.class);

        job.setMapperClass(myMap.class);
        job.setReducerClass(myReduce.class);

        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(Text.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job,new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job,new Path(otherArgs[1]));
        System.exit(job.waitForCompletion(true)?0:1);
    }
}

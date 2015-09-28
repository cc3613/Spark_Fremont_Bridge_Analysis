# Spark_Fremont_Bridge_Analysis
Simple project integrating Spark into data analysis

Since this project is more about integrating Spark, the Spark environment has to be set correctly.

I used <a href='https://github.com/minrk/findspark'>Findspark plugin</a> to find the config for importing Spark, then write

    findspark.init(spark_home)
    
where `spark_home` is the path to spark directory.

After that, the Spark environment can be set by:

    conf=SparkConf().setMaster('local').setAppName('Fremont Bridge Bike Analysis')
    sc=SparkContext(conf=conf)
    
of course we need to `from pyspark import SparkConf, SparkContext` first

The rest is pretty straightforward. Use `sc.TextFile` to get the data from the csv file, then use `take` to put them into lists. One thing to note is that I'm using lists to avoid further RDD actions to simply get some results, and I'm way more familiar with lists and dicts than RDDs. This project can be modified in the future to apply more RDD functions.

After running the code, <a href='http://imgur.com/AlMdzN0'>this figure should be produced</a>, and analysis can be made from there. I know there's a lot of imporvement to be made, but this is a start for further use of Spark.


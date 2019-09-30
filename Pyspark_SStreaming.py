##pyspark --jars spark-sql-kafka-0-10_2.11-2.4.0.jar,kafka-clients-1.1.0.jar
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import re
rg= r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] \"(\S+) (\S+) (\S+)\" (\d{3}) (\d+) (\S+) \"(.*?)\"'
##https://regex101.com/r/x20Rmi/1 

KAFKA_TOPIC_NAME_CONS = "phdata_project"
KAFKA_BOOTSTRAP_SERVERS_CONS = 'localhost:9092'

spark = SparkSession \
        .builder \
        .appName("PySpark Structured Streaming with Kafka Demo").getOrCreate()


df = spark \
         .readStream \
         .format("kafka") \
         .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_CONS) \
         .option("subscribe", KAFKA_TOPIC_NAME_CONS) \
         .option("startingOffsets", "latest") \
         .load()


df1 = df.selectExpr("CAST(value AS STRING)")

bm = df1.select(regexp_extract("value",rg,1).alias('ip'),regexp_extract("value",rg,2).alias('clientIdentd'),regexp_extract("value",rg,3).alias('userId'),
from_unixtime(unix_timestamp(regexp_extract("value",rg,4).substr(1, 20), 'dd/MMM/yyyy:HH:mm:ss'), 'yyyy-MM-dd:HH:mm:ss').alias('dateTime')\
,regexp_extract("value",rg,5).alias('method'),regexp_extract("value",rg,6).alias('endpoint'),regexp_extract("value",rg,7).alias('protocol'),regexp_extract("value",rg,8).alias('responseCode')\
,regexp_extract("value",rg,9).alias('contentSize'),regexp_extract("value",rg,10).alias('Referer'),regexp_extract("value",rg,11).alias('UserAgent'))


final=bm.select('ip','dateTime',unix_timestamp(col("dateTime"), 'yyyy-MM-dd:HH:mm:ss').cast("timestamp").alias('time'))\
.withWatermark('time','2 seconds').groupBy('ip','time').agg(count('ip').alias('count')).filter(column('count')>5)
op_stream = final \
         .writeStream \
         .trigger(processingTime='10 seconds') \
         .outputMode("update") \
         .option("truncate", "false")\
         .format("console") \
         .start()

op_stream_f = final \
         .writeStream \
         .trigger(processingTime='10 seconds') \
         .format("csv")\
         .option("path", "/Users/bhavya0609/Downloads/ph_data/") \
         .option("checkpointLocation", "/Users/bhavya0609/Downloads/ph_data_checkpoint/")\
         .outputMode("append")\
         .start()
         
op_stream_f.awaitTermination()
sc.stop()

# DDOS_Detection_ApacheAccessLog
DDOS_Detection_ApacheAccesLog
The Objective of this project was to read a file from local disk via apache flume and write to a message system to Kafka. Spark Streaming application that reads data from the message system and detects whether the attacker is part of the DDOS attack and once an attacker is found, the ip-address should be written to a results directory which could be used for further processing.
Prerequisite
1.	kafka_2.11-0.10.0.1
Link: https://kafka.apache.org/downloads
2.	Python 3.7.3
Link: https://www.python.org/ftp/python/3.7.3/
3.	spark-2.4.4-bin-hadoop2.7
Link: https://spark.apache.org/downloads.html
4.	Flume_1.9.0
Link: https://flume.apache.org/download.html  
Installation
1.	Kafka
•	Download and install kafka using the following link https://kafka.apache.org/quickstart 
•	Unzip the kakfa file contents tar -xzf kafka_2.11-0.10.0.1.tgz 


2.	Flume
After downloading the Apache flume should be created a configuration file in the folder flume/1.9.0/libexec/conf/ "flume-sample.conf"

1.Agent Name:
a1.sources = r1
a1.sinks = sample 
a1.channels = sample-channel
2.Source configuration:
a1.sources.r1.type = exec
a1.sources.r1.command = tail -f /Users/folder/Downloads/ProjectDeveloperapache-access-log.txt
a1.sources.r1.logStdErr = true
3.Sink type
a1.sinks.sample.type = logger
4.Buffers events in memory to channel
a1.channels.sample-channel.type = memory
a1.channels.sample-channel.capacity = 1000
a1.channels.sample-channel.transactionCapacity = 100
5. Bind the source and sink to the channel
a1.sources.r1.channels.selector.type = replicating
a1.sources.r1.channels = sample-channel
6.Related settings Kafka, topic, and host channel where it set the source
a1.sinks.sample.type = org.apache.flume.sink.kafka.KafkaSink
a1.sinks.sample.topic = phdata_project
a1.sinks.sample.brokerList = 127.0.0.1:9092
a1.sinks.sample.requiredAcks = 1
a1.sinks.sample.batchSize = 20
a1.sinks.sample.channel = sample-channel


3.	Apache Spark

Download a pre-built version of Apache Spark2.4.4  from https://spark.apache.org/downloads.html

Execution Steps:
1.	START Zookepper ->  bin/zookeeper-server-start.sh config/zookeeper.properties&
2.	START Kafka Server -> bin/kafka-server-start.sh config/server.properties&
3.	CREATE TOPIC - bin/kafka-topics.sh --zookeeper 127.0.0.1:2181 --create --replication-factor 1 --partitions 1 --topic phdata_project
4.	START CONSUMER -> bin/kafka-console-consumer.sh --zookeeper 127.0.0.1:2181 --topic phdata_project --from-beginning
5.	Submit Spark Streaming Job

spark-submit --jars spark-sql-kafka-0-10_2.11-2.4.0.jar,kafka-clients-1.1.0.jar Pyspark_SStreaming.py

6.	START Flume--> sh bin/flume-ng agent --conf conf --conf-file libexec/conf/flume-sample.conf  -Dflume.root.logger=DEBUG,console --name a1 -Xmx512m -Xms256m

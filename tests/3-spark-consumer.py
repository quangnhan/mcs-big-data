from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("KafkaConsumerPrint") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "automotive-logs") \
    .option("startingOffsets", "latest") \
    .load()
    
# Convert binary Kafka value to string and display along with headers
query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)").writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination(5)
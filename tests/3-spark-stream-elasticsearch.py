from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Spark Session
spark = SparkSession.builder \
    .appName("KafkaToElasticsearch") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,"
                                    "org.elasticsearch:elasticsearch-spark-30_2.12:8.6.2") \
    .config("es.nodes", "localhost") \
    .config("es.port", "9200") \
    .getOrCreate()

# Define schema
schema = StructType([
    StructField("vehicle_id", StringType()),
    StructField("timestamp", DoubleType()),
    StructField("speed", DoubleType()),
    StructField("engine_temp", DoubleType()),
    StructField("location", StructType([
        StructField("lat", DoubleType()),
        StructField("lon", DoubleType())
    ]))
])

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "automotive-logs") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON
parsed = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("data"))
flattened = parsed.select(
    col("data.vehicle_id"),
    col("data.timestamp"),
    col("data.speed"),
    col("data.engine_temp"),
    col("data.location.lat").alias("lat"),
    col("data.location.lon").alias("lon")
)

# Write to Elasticsearch
query = flattened.writeStream \
    .outputMode("append") \
    .format("es") \
    .option("checkpointLocation", "/tmp/spark-checkpoint") \
    .option("es.resource", "automotive-logs/_doc") \
    .start()

query.awaitTermination()

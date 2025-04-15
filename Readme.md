1. Start/stop system
- docker-compose up -d
- docker-compose down

2. Test systems
- kafka-ui: http://localhost:8082/ 
- spark: http://localhost:8080/
- elasticsearch: http://localhost:9200/
- kibana: http://localhost:5601/

3. Submit spark job
- spark-submit --master spark://localhost:7077 --conf spark.jars.packages=org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 ./tests/3-spark-consumer.py

- spark-submit --master spark://localhost:7077 --conf spark.jars.packages=org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.elasticsearch:elasticsearch-spark-30_2.12:8.6.2 ./tests/3-spark-stream-elasticsearch.py
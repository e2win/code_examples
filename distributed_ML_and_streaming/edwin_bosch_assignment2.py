# Databricks notebook source
# Edwin Bosch
# make directory and moving files
# dbutils.fs.mkdirs("FileStore/tables/assignment2") 
# dbutils.fs.mv("FileStore/tables/Maternal_Health_Risk_Data_Set.csv", "FileStore/tables/assignment2/Maternal_Health_Risk_Data_Set.csv")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Machine Learning Model

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# COMMAND ----------

maternalSchema = StructType( \
[StructField("Age", FloatType(), False),
 StructField("SystolicBP", FloatType(), False),
 StructField("DiastolicBP", FloatType(), False),
 StructField("BS", FloatType(), False),
 StructField("BodyTemp", FloatType(), False),
 StructField("HeartRate", FloatType(), False),
 StructField("RiskLevel", StringType(), False)
])

# COMMAND ----------

mr_data = spark.read.format("csv").option("header", True).schema(maternalSchema).load("/FileStore/tables/assignment2/Maternal_Health_Risk_Data_Set.csv")
mr_data.show()

# COMMAND ----------

riskIndexer = StringIndexer(inputCol="RiskLevel", outputCol="label")
assembler = VectorAssembler(inputCols=["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"], outputCol="features")
rf = RandomForestClassifier(numTrees=500, maxDepth=14, seed=45)

# COMMAND ----------

train, test = mr_data.randomSplit([0.7, 0.3], seed=12)
print("Training data length: ", train.count())
print("Testing data length: ", test.count())

# COMMAND ----------

p = Pipeline(stages=[riskIndexer, assembler, rf])
model = p.fit(train)
out = model.transform(train)
print("Testing the forest on training data:\n")
out.select("label", "probability", "prediction").show()

# COMMAND ----------

evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction")
accuracy = evaluator.evaluate(out)
print("Results on the training data:")
print("Accuracy = %s" % (accuracy))

# save the model for use in streaming
model.write().overwrite().save("/FileStore/tables/assignment2/model")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Streaming Section

# COMMAND ----------

# create the files for streaming 
# test = test.repartition(25)
# test.write.format("csv").option("header", True).save("/FileStore/tables/assignment2/maternal_health_data_stream/")

# COMMAND ----------

pipeline_model = PipelineModel.load("/FileStore/tables/assignment2/model")

# Read streaming data from directory
streamingDF = spark.readStream.option("header", "true").option("maxFilesPerTrigger", 1).schema(maternalSchema).csv("/FileStore/tables/assignment2/maternal_health_data_stream/")

output = pipeline_model.transform(streamingDF)

# Select the relevant columns and start writing the output stream to a memory sink
results = output.select("label", "probability", "prediction")
query = results.writeStream \
    .outputMode("append") \
    .format("memory") \
    .queryName("maternal_risk_prediction") \
    .trigger(processingTime="5 seconds") \
    .start()


# COMMAND ----------

# Query the results from memory sink
print("Current length of stream file: ", spark.sql("SELECT * FROM maternal_risk_prediction").count())
print("Last 20 values read in: ")
spark.sql("SELECT * FROM maternal_risk_prediction").tail(20)
# show some final results
spark.sql("SELECT label, prediction FROM maternal_risk_prediction").show()

# COMMAND ----------

evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction")
accuracy = evaluator.evaluate(spark.table("maternal_risk_prediction"))
print("Results on the testing data:")
print("Accuracy = %s" % (accuracy))

# COMMAND ----------



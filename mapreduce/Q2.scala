package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._

object Q2 {

	case class Graph(Source: Int, Target: Int, Weight: Int)

	def main(args: Array[String]) {
    	val sc = new SparkContext(new SparkConf().setAppName("Q2"))
		val sqlContext = new SQLContext(sc)
		import sqlContext.implicits._

    	// read the file
    	val file = sc.textFile("hdfs://localhost:8020" + args(0))
		val graphDf = file.map(line => line.split("\t")).map(p => Graph(p(0).toInt, p(1).toInt, p(2).toInt)).toDF()

		val weightfilter = graphDf.filter(graphDf("Weight") >= 5)
		val o = weightfilter.groupBy(weightfilter("Source")).agg(sum("Weight").alias("OutWeight"))
		val i = weightfilter.groupBy(weightfilter("Target")).agg(sum("Weight").alias("InWeight"))

		val jdf = o.join(i, $"Source" === $"Target", "full_outer")
		.select(when(col("Source").isNull, col("Target")).otherwise(col("Source")).alias("NodeID"), o("OutWeight"), i("InWeight"))
		.withColumn("Degree", when(col("InWeight").isNull, lit(0)).otherwise(col("InWeight")) - when(col("OutWeight").isNull, lit(0)).otherwise(col("OutWeight")))
		.select("NodeID","Degree")
		//final.show()
		val output=jdf.map(r => r.mkString("\t"))
		output.saveAsTextFile("hdfs://localhost:8020" + args(1))
		
  	}
}

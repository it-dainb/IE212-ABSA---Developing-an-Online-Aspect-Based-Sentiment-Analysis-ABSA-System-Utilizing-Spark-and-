from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
import pyspark.sql.functions as F
from preprocess import udf_tokenize

class NERExtractor(Transformer, HasInputCol, HasOutputCol, DefaultParamsReadable, DefaultParamsWritable):
    def __init__(self, inputCol="example", outputCol="sa_ner", **kwargs):
        self.inputCol = inputCol
        self.outputCol = outputCol
        self.kwargs = kwargs
        self.result_col = "result"

    def _transform(self, result):
        result = result.select(
            F.col("cmtid"),
            F.col("text"),
            F.explode(F.arrays_zip("entity.result", "entity.metadata", "entity.begin", "entity.end")).alias("cols"),
        ).select(
            F.col("cmtid"),
            F.col("text"),
            F.col("cols.begin").alias("begin").cast("int"),
            F.col("cols.end").alias("end").cast("int"),
            F.expr("cols['result']").alias("keyword"),
            F.expr("cols['metadata']['entity']").alias("label"),
        )
        
        result = result.withColumn(
            "text",
            udf_tokenize(F.col("text"))
        ).withColumn(
            "keyword",
            udf_tokenize(F.col("keyword"))
        )

        result = result.withColumn(
            self.outputCol,
            F.concat("text", F.lit(" : "), "keyword")
        )

        result = result.select(
            F.col("cmtid"),
            "text",
            "begin",
            "end",
            "label",
            self.outputCol
        )

        return result

class SA_NERExtractor(Transformer, HasInputCol, HasOutputCol, DefaultParamsReadable, DefaultParamsWritable):
    def __init__(self, inputCol="example", outputCol="sa_ner", **kwargs):
        self.inputCol = inputCol
        self.outputCol = outputCol
        self.kwargs = kwargs
        self.result_col = "result"

    def _transform(self, result):
        result = result.select(
            F.col("cmtid"),
            "text",
            "begin",
            "end",
            "label",
            "class.result"
        )

        result = result.withColumn(
            "label",
            F.concat("label", F.lit("#"), F.expr("result[0]"))
        )

        return result

class Cleaner(Transformer, HasInputCol, HasOutputCol, DefaultParamsReadable, DefaultParamsWritable):
    def __init__(self, inputCol="example", outputCol="example", **kwargs):
        self.inputCol = inputCol
        self.outputCol = outputCol
        self.kwargs = kwargs
        self.result_col = "result"

    def _transform(self, result):
        result = result.select(
            F.col("cmtid"),
            "text",  
            F.expr("class['result'][0]").alias("sentiment"), 
            "begin",
            "end",
            "label"
        )

        return result
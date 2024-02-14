from pyspark.ml import Pipeline
from sparknlp.annotator import Tokenizer, NerConverter
from sparknlp.base import DocumentAssembler
from models import NER_model, SA_model
from transform import NERExtractor, SA_NERExtractor, Cleaner

document_assembler = DocumentAssembler() \
    .setInputCol('text') \
    .setOutputCol('document')

tokenizer = Tokenizer() \
    .setInputCols(['document']) \
    .setOutputCol('token')

converter = NerConverter() \
    .setInputCols(["document", "token", "ner"]) \
    .setOutputCol("entity")

ner_extracter = NERExtractor(inputCol = "entity")

sa_ner_document_assembler = DocumentAssembler() \
    .setInputCol('sa_ner') \
    .setOutputCol('document')

sa_ner_extracter = SA_NERExtractor()

cleaner = Cleaner()

pipeline = Pipeline(stages=[
    document_assembler,
    tokenizer,
    NER_model,
    converter,
    ner_extracter,
    sa_ner_document_assembler,
    tokenizer,
    SA_model,
    sa_ner_extracter,
    document_assembler,
    tokenizer,
    SA_model,
    cleaner
])
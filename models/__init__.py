from sparknlp.annotator import RoBertaForSequenceClassification, BertForTokenClassification
from dotenv import load_dotenv
load_dotenv()

import os

SA_model = RoBertaForSequenceClassification.load('file:///' + os.getenv('ROOT_PATH') + '/models/SA/')\
    .setMaxSentenceLength(256)\
    .setInputCols(["document",'token'])\
    .setOutputCol("class")

NER_model = BertForTokenClassification.load('file:///' + os.getenv('ROOT_PATH') + '/models/NER/')\
    .setMaxSentenceLength(256)\
    .setInputCols(["document",'token'])\
    .setOutputCol("ner")
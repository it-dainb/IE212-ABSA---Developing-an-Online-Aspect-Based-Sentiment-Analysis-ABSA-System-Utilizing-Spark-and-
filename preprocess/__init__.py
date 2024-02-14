from pyspark.sql.functions import udf
import regex as re
from pyvi import ViTokenizer

def remove_punc(text):
        text = text.lower()
        text = re.sub(r'[^\w\d\sàáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]|\_', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

udf_clean = udf(lambda x: remove_punc(x))
udf_tokenize = udf(lambda x: ViTokenizer.tokenize(x))
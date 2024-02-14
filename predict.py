from models import sa_model, ner_model
import regex as re

def absa(text, ner_text, sa_text):
    
    id2label = {
        0: 'NEGATIVE',
        1: 'NEUTRAL',
        2: 'POSITIVE'
    }
    

    ner, _ = ner_model.predict([ner_text])

    pred = {}
    span = []
    for i in ner[0]:
        w = list(i.keys())[0]
        tag = list(i.values())[0].split("-")[-1]

        if span == []:
            span.append(tag)
        
        if tag == "O":
            if len(span) > 1:
                # print("#", span)
                pred[span[0]].append(" ".join(span[1:]))
            
            span = []
            continue
        
        if tag != span[0] or ("B-" in list(i.values())[0] and len(span) > 1):
            # print("#", span)
            
            pred[span[0]].append(" ".join(span[1:]))
            span = [tag]
            
        if tag not in pred:
            pred[tag] = []
        
        span.append(w)

    labels = []
    for k, spans in pred.items():
        for span in spans:
            find = re.search(span, ner_text)

            sa_ner_text = sa_text[find.start(): find.end()] + ' : ' + sa_text
            sa, _ = sa_model.predict(sa_ner_text)

            labels.append([find.start(), find.end(), f"{k}#{id2label[sa[0]]}"])

    sa, _ = sa_model.predict(sa_text)
    
    return {
        "text": text,
        "labels": labels,
        "sentiment": id2label[sa[0]]
    }

if __name__ == '__main__':
    from preprocess import preprocess_ner, preprocess_sa
    
    text = 'Sạc thì kh biết khi nào đầy sạc mãi sài có chút xí ms mua về nghe êm càg ngày càng nhỏ chịu thật'
    
    absa(
        text,
        preprocess_ner(text),
        preprocess_sa(text)
    )
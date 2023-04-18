from transformers import AutoModelForTokenClassification, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM, AutoTokenizer, AutoConfig, pipeline

import os
import json
nlpmodels_dir = os.path.join("NLPModels")

# İlk olarak model ve tokenizer'ları yükleyin
config_ner = AutoConfig.from_pretrained(nlpmodels_dir+r"/NER-MODEL/config.json")
model_ner = AutoModelForTokenClassification.from_pretrained(nlpmodels_dir+r"/NER-MODEL/pytorch_model.bin",config=config_ner)
tokenizer_ner= AutoTokenizer.from_pretrained(nlpmodels_dir+r"/NER-MODEL")

config_sentiment = AutoConfig.from_pretrained(nlpmodels_dir+r"/SENTIMENT-MODEL/config.json")
model_sentiment = AutoModelForSequenceClassification.from_pretrained(nlpmodels_dir+r"/SENTIMENT-MODEL/sentiment_model.bin", config=config_sentiment)
tokenizer_sentiment = AutoTokenizer.from_pretrained(nlpmodels_dir+r"/SENTIMENT-MODEL")

config_summarize = AutoConfig.from_pretrained(nlpmodels_dir+r"/SUMMARIZE-MODEL/config.json")
model_summarize = AutoModelForSeq2SeqLM.from_pretrained(nlpmodels_dir+r"/SUMMARIZE-MODEL/summarize_model.bin", config=config_summarize)
tokenizer_summarize = AutoTokenizer.from_pretrained(nlpmodels_dir+r"/SUMMARIZE-MODEL")

config_subject = AutoConfig.from_pretrained(nlpmodels_dir+r"/SUBJECT-MODEL/config.json")
model_subject = AutoModelForSequenceClassification.from_pretrained(nlpmodels_dir+r"/SUBJECT-MODEL/subject_model.bin", config=config_subject)
tokenizer_subject = AutoTokenizer.from_pretrained(nlpmodels_dir+r"/SUBJECT-MODEL")

def create_pipeline():

    ner_pipeline = pipeline(
        task='ner',
        model=model_ner,
        tokenizer=tokenizer_ner,
        framework='pt',
        aggregation_strategy='first'
        #device=device # GPU kullanmak isterseniz 0 yerine -1 yazın
    )

    sentiment_pipeline = pipeline(
        task='text-classification',
        model=model_sentiment,
        tokenizer=tokenizer_sentiment,
        framework='pt',
        #device=device # GPU kullanmak isterseniz 0 yerine -1 yazın
    )

    summarize_pipeline = pipeline(
        task='summarization',
        model=model_summarize,
        tokenizer=tokenizer_summarize,
        framework='pt',
        #device=device # GPU kullanmak isterseniz 0 yerine -1 yazın
    )

    subject_pipeline = pipeline(
        task='text-classification',
        model=model_subject,
        tokenizer=tokenizer_subject,
        framework='pt',
        #device=device # GPU kullanmak isterseniz 0 yerine -1 yazın
    )

    return ner_pipeline, sentiment_pipeline, summarize_pipeline, subject_pipeline


def predict(text):

    text = text.replace('\n', ' ')

    ner_pipeline, sentiment_pipeline, summarize_pipeline, subject_pipeline = create_pipeline() 

    ner_result = ner_pipeline(text)
    entities = []
    for i in range(len(ner_result)):
        entity_result = {
            "entity_group": ner_result[i]['entity_group'],
            "score": float(ner_result[i]['score']),
            "word": ner_result[i]['word'],
            "start": ner_result[i]['start'],
            "end": ner_result[i]['end']
        }
        entities.append(entity_result)

    sentiment_result = sentiment_pipeline(text)
    sentiment = {
    "sentiment" : sentiment_result[0]['label'],
    "score": sentiment_result[0]['score']
    }

    summarize_result = summarize_pipeline(text)
    summarize = {
        "summary": summarize_result[0]['summary_text']
    }

    subject_result = subject_pipeline(text)
    subject = {
    "subject":subject_result[0]['label'],
    "score":subject_result[0]['score']
    }

    ensemble_result = {
        'ner': entities,
        'sentiment': sentiment,
        'summarize': summarize,
        'subject': subject
    }

    return ensemble_result


#Model preprocess libraries

#import torch
#from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer


#Model File Path 
#config = AutoConfig.from_pretrained(BertAPI.settings.MODEL_CONFIG_PATH)
#tokenizer = AutoTokenizer.from_pretrained(BertAPI.settings.MODEL_TOKENIZER_PATH, config=config)
#model = AutoModelForSequenceClassification.from_pretrained(BertAPI.settings.MODEL_PATH, config=config)

#URL-DECODER
def decode_url(text):

    replaced_characters = {'\u011f':'ğ',
                           '\u011e':'ı',
                           '\u0130':'İ',
                           '\u00f6':'ö',
                           '\u00d6':'Ö',
                           '\u00fc':'ü',
                           '\u00dc':'Ü',
                           '\u015f':'ş',
                           '\u015e':'Ş',
                           '\u00e7':'ç',
                           '\u00c7':'Ç'}
                          
    for key in replaced_characters.keys():
        if key in text:
            text = text.replace(key, replaced_characters[key])
    return text

def predict(input):

    """
    inputs = tokenizer(input, return_tensors="pt")

    outputs = model(**inputs)
    _, predicted = torch.max(outputs.logits, dim=1)

    if(predicted.item()==1):
        return "Positive"
    else:
        return "Negative"
    """
    print("sa")




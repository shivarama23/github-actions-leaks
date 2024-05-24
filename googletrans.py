# code to translate input sentence from english to HIndi using OpenAI gpt3.5 model
#
# import the necessary libraries

import os
import openai
import pandas as pd
from tqdm import tqdm
from openai import OpenAI
from google.cloud import translate_v2 as translate

tqdm.pandas()

'''
# set the OpenAI API key
openai.api_key = 'sk-zfw8smjtR5FmoKvIk0T3BlbkFJtRU3snB5NxlirySzpkcR'

# define the function to translate the input sentence
def translate_to_hindi(input_sentence):
    # use the OpenAI gpt3.5 model to translate the input sentence
    
    client = OpenAI(
        api_key='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',
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a translational assistant, skilled in translating between English and Hindi. If the english sentense is not well formed, please correct it and then translate it to Hindi. Translate every sentence to hindi."},
        {"role": "user", "content": input_sentence}
    ]
    )

    # print(completion.choices[0].message)
    return completion.choices[0].message.content

# get the input sentence from the user
input_sentence = 'Hi.My names Ahdieh.I m from a small city in Iran.My father had a heart attack on sunday as doctor said cpr condition.after 40 minuts he came back to life. now he isnot conscious.he is in ICU.his doctor said his conscious rate is 5.what do you think about his condition?If it is needed I can send you his cardiograf and blood test and the drugs they are using for him in ICU.Kindly tell me can we carry him to a better hospital in Tehran(It takes 4 hours to reach there)?'

# translate the input sentence to Hindi
translated_sentence = translate_to_hindi(input_sentence)

# print the translated sentence
print("The translated sentence is:", translated_sentence)
'''

# translate text from english to hindi using google translate api
debug = False
error_count = 0
def translate_text(text: str) -> dict:
    """Translates text into the target language. i.e. hindi

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    target = 'hi'

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    try:
        result = translate_client.translate(text, target_language=target)
    except Exception as e:
        print(e)
        return ''
    
    if debug:
        print("Text: {}".format(result["input"]))
        print("Translation: {}".format(result["translatedText"]))
        print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result["translatedText"]


# read the excel file
df = pd.read_excel('error_rows.xlsx')

# df = df.head(2)
# apply the translate_text function to the Human_Text and AI_Text columns
df['Human_hindi'] = df['Human_Text'].progress_apply(translate_text)
df['AI_hindi'] = df['AI_Text'].progress_apply(translate_text)

# save the output to a new excel file
df.to_excel('OpenHathi_blog_error_rows_hindi.xlsx', index=False)
print("The translated sentences are saved to OpenHathi_blog_error_rows_hindi.xlsx file")
import re, html, urllib, csv, json
from pythainlp.util import normalize
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


#################### API ####################

app = FastAPI()

class Item(BaseModel):
    text: str

@app.get("/summarize")
def get_request():
    text = "GET method is not allowed. Use POST method instead. Request body must be {text: <input-text>}"
    return text

@app.post("/summarize")
def summarize_text(item: Item):
    
    received_text = item.text
    text = preprocess_text(received_text) # clean and solve abbreviation
    summarized_text = generate_text(text)
    
    try:
        response = {
            "success": True,
            "summarize_text": summarized_text
        }
        return json.dumps(response, ensure_ascii=False)
    except:
        return json.dumps({"success":False})

#################### FUNTIONS FOR PREPROCESSING ####################

def clean_text (text):
  """
  Cleans a string of text by removing URLs, normalizing repeated characters, shrinking white spaces and removing default messages.

  Args:
      text (str): The input string to clean.

  Returns:
      str: The cleaned string, with URLs removed, repeated characters normalized,
      and extra white space removed.

  Example:
      text = "ลูกหนี้  จะะได้รับข้อเเสนอปรับปรุงโครงสร้างหนี้ที่ผ่อนปรนเป็นพิเศษ http://www.thairath.com"
      clean_text(text)
      "ลูกหนี้ จะได้รับข้อเสนอปรับปรุงโครงสร้างหนี้ที่ผ่อนปรนเป็นพิเศษ"
  """
  text = normalize(text).strip() # normalize Thai vowels using Pythai library
  
  ## clean text ##
  text = re.sub(r'ํา','ำ', text) # o + า -> ำ
  text = re.sub('\(ภาพจาก.*\)|>>.*<<', '', text) # remove default msg. e.g. '(ภาพจาก....)', '>> อ่านเรื่องย่อนิยายทุกเรื่อง คลิกที่นี่ <<', '>> คลิกอ่านเรื่องย่อมงกุฎดอกหญ้า <<'
  text = html.unescape(urllib.parse.unquote(text)) # unescape: unicode, unquote: escaped URL
  text = re.sub(r'https?.+?(?:\s|$)', '', text) # remove URL link
  text = re.sub(r'(.)\1{2,}', r'\1', text) # remove repeated more than 3 characters ##
  text = re.sub(r'[\"\'\?\!]', '', text)
  text = re.sub(r'[ \u00a0\xa0\u3000\u2002-\u200a]+', ' ', text) # shrink whitespaces e.g. good  boy -> good boy
  text = re.sub(r'[\r\u200b\ufeff]+|\?', '', text) # remove non-breaking space and ?

  return text.strip()

### dict for abbreviation
with open('data/abbrev.csv') as f:
    ABB_NAME_DICT = dict(csv.reader(f)) # {abb: full word}

def solve_abbrev (text):
    """
    This function is to solve the abbrevations appeared in text, for example, พล.ต.ต. --> พลตำรวจตรี
    """
    for abb, word in ABB_NAME_DICT.items():
        text = text.replace(abb, word)
    
    return text
    
def preprocess_text(text):
    text = clean_text(text)
    text = solve_abbrev(text)
    return text

#################### LOAD MODEL AND PREDICT ####################

MODEL_PATH = "model"

# Specify the name of the pre-trained tokenizer to download
tokenizer_name = "google/mt5-small"

# Download and save the tokenizer to the same directory as the fine-tuned model
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
tokenizer.save_pretrained(MODEL_PATH)

# load model
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# function for generate summarized text
def generate_text(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    summary_ids = model.generate(input_ids)
    summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary_text 
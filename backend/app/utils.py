import re
from datetime import datetime
import pdfplumber
from PIL import Image
import pytesseract
import os
from datetime import date

def extract_text_from_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_image(path: str) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img, lang="spa")

def parse_spanish_date(s: str) -> date:
    month_map = {
        'ene':'01', 'feb':'02', 'mar':'03', 'abr':'04',
        'may':'05', 'jun':'06', 'jul':'07', 'ago':'08',
        'sep':'09', 'oct':'10', 'nov':'11', 'dic':'12',
    }
    dd, m_str, yyyy = s.split('-')
    mm = month_map[m_str.lower()]
    return date(int(yyyy), int(mm), int(dd))

def extract_info_movistar_tv(text: str) -> dict:
    # Price
    filter = "TOTALAPAGAR"
    pos_filter = text.find(filter)
    pos_monto = text.find("$",pos_filter)
    price_str = text[pos_monto+2:pos_monto+8]
    price_int = int(price_str.replace(".",""))
    
    # Service
    service = "PLAN : "
    index_service = text.find(service)
    pos_service_full = text.find(")", index_service)
    service = text[index_service:pos_service_full+1]
    
    texto = "FechadeVencimiento"
    i = text.find(texto)
    date_pos = text.find("-",i)
    date_pos_final = date_pos+9
    expiration_date = text[i:date_pos_final].split(" ")[1]
    expiration_date_formated = parse_spanish_date(expiration_date)

    return {"servicio": service, "monto": price_int, "fecha": expiration_date_formated, "empresa": "MOVISTAR HOGAR"}
    

def filter_company(text: str) -> str:
    if "Plan Movistar TV" in text:
        return "Movistar Hogar"
    return ""
    

def parse_boleta(text: str) -> dict:
    company = filter_company(text)
    
    if company == "Movistar Hogar":
        return extract_info_movistar_tv(text)
        
    return {}

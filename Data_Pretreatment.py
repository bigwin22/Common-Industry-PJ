import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 데이터 전처리
# Preprocessing data
# 데이터를 가져온 후, 데이터를 전처리한다.

# data.json 불러오기
# Load data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
with open('H to K.json', 'r', encoding='utf-8') as f:
    Htok = json.load(f)
with open('K to H.json', 'r', encoding='utf-8') as f:
    Ktoh = json.load(f)

pre_Processed_data = {}
Processed_data = {}

#쓸모없는 데이터 삭제
for country in data.keys():
    pre_Processed_data[country] = {}
    for dcid_name in data[country].keys():
        pre_Processed_data[country][Ktoh[dcid_name]] = data[country][dcid_name]["sourceSeries"][0]["val"]

#데이터 정렬
for country in pre_Processed_data.keys():
    Processed_data[country] = {}
    for indicator in pre_Processed_data[country].keys():
        keys = list(pre_Processed_data[country][indicator].keys())
        keys.sort()

        Processed_data[country][indicator] = {}
        for key in keys:
            Processed_data[country][indicator][key] = pre_Processed_data[country][indicator][key]
with open('Processed_data.json', 'w', encoding='utf-8') as f:
    json.dump(Processed_data, f, indent=4, ensure_ascii=False)


#엑셀화(데이터 프레임화)
#Excelization (DataFrame)
df = {}
for country in Processed_data.keys():
    df[country] = pd.DataFrame(Processed_data[country])
    df[country].to_excel(f'{country}.xlsx')

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


#엑셀화(데이터 프레임화)(각각으로 하나씩)
#Excelization (DataFrame) (one for each)
df = pd.DataFrame(Processed_data["country/KOR"])
df.to_excel('KOR.xlsx')
df = pd.DataFrame(Processed_data["country/JPN"])
df.to_excel('JPN.xlsx')

#엑셀화(데이터 프레임화)(한꺼번에)
#Excelization (DataFrame) (at once)
df = pd.DataFrame(Processed_data["country/KOR"])
df2 = pd.DataFrame(Processed_data["country/JPN"])
with pd.ExcelWriter('comparison.xlsx') as writer:
    df.to_excel(writer, sheet_name='KOR')
    df2.to_excel(writer, sheet_name='JPN')

#그래프화(이미지도 저장)
#Graphing
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 5
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.unicode_minus'] = False
for indicator in Processed_data["country/KOR"].keys():
    plt.plot(Processed_data["country/KOR"][indicator].keys(), Processed_data["country/KOR"][indicator].values(), label='KOR')
    plt.plot(Processed_data["country/JPN"][indicator].keys(), Processed_data["country/JPN"][indicator].values(), label='JPN')
    plt.title(indicator)
    plt.xlabel('년도')
    plt.ylabel('값')
    plt.legend()
    plt.savefig(f'./images/{indicator}.png')
    #plt 초기화
    plt.clf()




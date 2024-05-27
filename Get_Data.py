# 프로젝트: 공일 프로젝트
# 방식: datacommons_pandas 라이브러리를 사용하여 데이터를 가져온다.
# 목적: 한국 및 일본의 데이터 비교를 통한 유사성의 타당성 검증

from ETC import *

import datacommons_pandas as dc
import pandas as pd
import matplotlib.pyplot as plt
import json

#comparison.json 열고 안에 있는 value들 가져오기
# Open 'comparison.json' and get the data inside
with open('comparison.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract the dcids
country = ['country/KOR', 'country/JPN'] #국가
dcids = []#불러올 데이터
Atom = []#데이터 이름
indicators_HtoK = {}
indicators_KtoH = {}
for category in data.values():
    for subcategory in category.values():
        for dcid in subcategory.values():
            dcids.append(dcid)
        for atom in subcategory.keys():
            Atom.append(atom)
for i in range(len(dcids)):
    indicators_HtoK[Atom[i]] = dcids[i]
    indicators_KtoH[dcids[i]] = Atom[i]
json.dump(indicators_HtoK, open('H to K.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
json.dump(indicators_KtoH, open('K to H.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

# exit()

# 데이터 가져오기
duplicated_data = {}
data = dc.get_stat_all(country, dcids)#데이터 가져오기
for dcid_name in data["country/KOR"].keys():
    if len(data["country/KOR"][dcid_name]["sourceSeries"]) == 2:
        del_input = input(f"{dcid_name}의 데이터가 중복되었습니다. 어떤 데이터를 삭제할까요? (1: {data['country/KOR'][dcid_name]['sourceSeries'][0]['measurementMethod']}, 2: {data['country/KOR'][dcid_name]['sourceSeries'][1]['measurementMethod']})")
        if del_input == "1":
            del data["country/KOR"][dcid_name]["sourceSeries"][0]
            del data["country/JPN"][dcid_name]["sourceSeries"][0]
        elif del_input == "2":
            del data["country/KOR"][dcid_name]["sourceSeries"][1]
            del data["country/JPN"][dcid_name]["sourceSeries"][1]
# 데이터 json 파일로 저장
with open('raw_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)


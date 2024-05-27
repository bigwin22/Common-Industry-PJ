# 프로젝트: 공일 프로젝트
# 방식: datacommons_pandas 라이브러리를 사용하여 데이터를 가져온다.
# 목적: 한국 및 일본의 데이터 비교를 통한 유사성의 타당성 검증



import datacommons_pandas as dc
import pandas as pd
import matplotlib.pyplot as plt
import json

# Open 'comparison.json' and get the data inside
with open('comparison.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract the dcids
dcids = []
for category in data.values():
    for subcategory in category.values():
        for dcid in subcategory.values():
            dcids.append(dcid)



# Get the data from Data Commons(TETS CODE)
data = dc.get_stat_all(['country/KOR', 'country/JPN'],dcids)





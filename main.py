# 프로젝트: 공일 프로젝트
# 방식: datacommons_pandas 라이브러리를 사용하여 데이터를 가져온다.
# 목적: 한국 및 일본의 데이터 비교를 통한 유사성의 타당성 검증

# 비교할 데이터 : GDP 성장률, 주식 시장 시가총액(GDP 대비 %), 국내 기업 시가총액(GDP 대비 %), 인구 증가율, 출산율, 부동산, 금리
# ValueData Dcid List : sdg/NY_GDP_MKTP_KD_ZG, worldBank/GFDD_DM_01, worldBank/CM_MKT_LCAP_GD_ZS, GrowthRate_Count_Person, FertilityRate_Person_Female,  


import datacommons_pandas as dc
import pandas as pd
import matplotlib.pyplot as plt

# Get the data for the KOR
gdp_growth = dc.build_time_series_dataframe(['country/KOR', 'country/JPN'], "sdg/NY_GDP_MKTP_KD_ZG")
stock_capitalization = dc.build_time_series_dataframe(['country/KOR', 'country/JPN'], "worldBank/GFDD_DM_01")
# print(dc.get_stat_all(["country/KOR"], ["sdg/NY_GDP_MKTP_KD_ZG", ]))
#export the data to a csv file
stock_capitalization.to_csv('KOR_GDP.csv')


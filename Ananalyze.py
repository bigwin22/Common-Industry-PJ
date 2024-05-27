import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# JSON 파일 로드
with open('K to H.json', 'r', encoding='utf-8') as f:
    KtoH = json.load(f)
with open('Processed_data_verified.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# JSON 데이터를 DataFrame으로 변환 및 전처리
def preprocess_data(country_data, mapping):
    processed_data = {}
    for indicator_key, values in country_data.items():
        indicator_name = mapping.get(indicator_key, indicator_key)
        processed_data[indicator_name] = {int(year): value for year, value in values.items()}
    return processed_data

# 한국 데이터 처리
kor_data = preprocess_data(data['country/KOR'], KtoH)

# 일본 데이터 처리
jpn_data = preprocess_data(data['country/JPN'], KtoH)

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.unicode_minus'] = False

# ARIMA 모델을 사용하여 일본의 미래 값을 예측하고 한국의 현재 데이터와의 상관관계 계산
def predict_and_correlate(jpn_data, kor_data):
    correlation_results = {}
    for indicator, jpn_values in jpn_data.items():
        # ARIMA 모델을 학습하고 예측
        model = ARIMA(np.array(list(jpn_values.values())), order=(5,1,0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=len(kor_data[indicator]))
        
        # 예측값과 한국의 현재 데이터 간의 상관관계 계산
        kor_values = kor_data.get(indicator, {})
        if kor_values:
            correlation = np.corrcoef(list(kor_values.values()), forecast[:len(kor_values)])[0, 1]
            correlation_results[indicator] = correlation
            print(f'{indicator}의 상관계수: {correlation}')
        else:
            print(f'{indicator}의 한국 데이터를 찾을 수 없습니다.')
    
    return correlation_results

correlation_results = predict_and_correlate(jpn_data, kor_data)

# 상관관계 시각화
plt.barh(list(correlation_results.keys()), list(correlation_results.values()))
plt.xlabel('상관관계')
plt.ylabel('지표')
plt.title('한국과 일본의 예측된 미래 데이터와의 상관관계')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

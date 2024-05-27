import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# JSON 파일 로드
with open('K to H.json', 'r', encoding='utf-8') as f:
    KtoH = json.load(f)
with open('Processed_data.json', 'r', encoding='utf-8') as f:
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

# 각 지표에 대해 연도별 데이터를 DataFrame으로 변환 및 0인 값 처리
def create_indicator_df(kor_data, jpn_data):
    indicators = list(kor_data.keys())
    combined_data = {indicator: {'Year': [], 'KOR': [], 'JPN': []} for indicator in indicators}
    
    for indicator in indicators:
        years = sorted(set(kor_data[indicator].keys()).union(set(jpn_data[indicator].keys())))
        kor_values = [kor_data[indicator].get(year, 0) for year in years]
        jpn_values = [jpn_data[indicator].get(year, 0) for year in years]

        # 0이 아닌 첫 번째 값의 인덱스 찾기
        first_nonzero_index_kor = next((i for i, value in enumerate(kor_values) if value != 0), len(kor_values))
        first_nonzero_index_jpn = next((i for i, value in enumerate(jpn_values) if value != 0), len(jpn_values))
        first_nonzero_index = max(first_nonzero_index_kor, first_nonzero_index_jpn)

        # 뒤쪽에서 0이 아닌 마지막 값의 인덱스 찾기
        last_nonzero_index_kor = next((i for i, value in enumerate(reversed(kor_values)) if value != 0), len(kor_values))
        last_nonzero_index_jpn = next((i for i, value in enumerate(reversed(jpn_values)) if value != 0), len(jpn_values))
        last_nonzero_index = max(last_nonzero_index_kor, last_nonzero_index_jpn)

        # 0이 아닌 값부터 데이터 저장, 마지막 0 제거
        if last_nonzero_index != 0:
            combined_data[indicator]['Year'] = years[first_nonzero_index:len(years) - last_nonzero_index]
            combined_data[indicator]['KOR'] = kor_values[first_nonzero_index:len(kor_values) - last_nonzero_index]
            combined_data[indicator]['JPN'] = jpn_values[first_nonzero_index:len(jpn_values) - last_nonzero_index]
        else:
            combined_data[indicator]['Year'] = years[first_nonzero_index:]
            combined_data[indicator]['KOR'] = kor_values[first_nonzero_index:]
            combined_data[indicator]['JPN'] = jpn_values[first_nonzero_index:]
    
    return combined_data

combined_data = create_indicator_df(kor_data, jpn_data)

# 상관계수 계산 및 출력
correlation_results = {}

for indicator, data in combined_data.items():
    df = pd.DataFrame(data)
    if not df['KOR'].empty and not df['JPN'].empty:
        correlation = np.corrcoef(df['KOR'], df['JPN'])[0, 1]
        correlation_results[indicator] = correlation
        print(f'{indicator}의 상관계수: {correlation}')
    else:
        print(f'{indicator}의 상관계수를 계산할 수 없습니다 (데이터가 부족함).')

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.unicode_minus'] = False
# 상관계수 시각화
plt.barh(list(correlation_results.keys()), list(correlation_results.values()))
plt.xlabel('상관계수')
plt.title('각 지표별 한국과 일본의 상관계수')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

import json
import pandas as pd
import matplotlib.pyplot as plt

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

        for i in range(first_nonzero_index, len(kor_values) - last_nonzero_index):
            if kor_values[i] == 0:
                kor_values[i] = None        
                first_nonzero_index = i
            if jpn_values[i] == 0:
                jpn_values[i] = None
                first_nonzero_index = i


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

#json 파일로 저장
#{'country/KOR':{indicator:{year:value}}형식으로 저장
json_data = {}
for country in ['KOR', 'JPN']:
    json_data[f'country/{country}'] ={}
    for indicator, values in combined_data.items():
        json_data[f'country/{country}'][indicator] = {year: value for year, value in zip(values['Year'], values[country])}
with open('Processed_data_verified.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

# 그래프 그리기 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.unicode_minus'] = False

# 각 지표에 대해 그래프 생성 및 저장
for indicator, data in combined_data.items():
    df = pd.DataFrame(data)
    # df를 excel로 저장
    df.to_excel(f'./excel/{indicator}.xlsx')
    
    plt.plot(df['Year'], df['KOR'], label='KOR')
    plt.plot(df['Year'], df['JPN'], label='JPN')
    plt.title(f'{indicator} 비교')
    plt.xlabel('년도')
    plt.ylabel('값')
    plt.legend()
    plt.xticks(rotation=45)  # X축 틱 설정
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=20))  # 틱의 최대 개수 설정
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(f'./images/{indicator}.png')
    plt.clf()

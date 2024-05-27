import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# 데이터 로드 (실제 데이터 파일 경로로 대체)
# df = pd.read_csv('population_growth.csv')

# 예제 데이터 (실제 데이터를 사용하려면 위의 read_csv 부분을 사용)
data = {
    'Year': [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010],
    'Korea_Growth_Rate': [1.1, 1.05, 1.02, 1.03, 1.01, 0.98, 0.95, 0.9, 0.85, 0.8, 0.75],
    'Japan_Growth_Rate': [0.5, 0.48, 0.46, 0.44, 0.42, 0.4, 0.38, 0.36, 0.34, 0.32, 0.3]
}

df = pd.DataFrame(data)

# 데이터 시각화
plt.plot(df['Year'], df['Korea_Growth_Rate'], label='Korea')
plt.plot(df['Year'], df['Japan_Growth_Rate'], label='Japan')
plt.xlabel('Year')
plt.ylabel('Growth Rate')
plt.title('Population Growth Rate Comparison')
plt.legend()
plt.show()

# 상관 분석
correlation = np.corrcoef(df['Korea_Growth_Rate'], df['Japan_Growth_Rate'])[0, 1]
print(f"상관계수: {correlation}")

# 시계열 분석 및 예측
korea_growth = df['Korea_Growth_Rate']

# ARIMA 모델 피팅 (p, d, q 값은 적절히 조정)
model = ARIMA(korea_growth, order=(1, 1, 1))
model_fit = model.fit()

# 향후 10년 예측
forecast_steps = 10
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)
years_forecast = range(df['Year'].iloc[-1] + 1, df['Year'].iloc[-1] + forecast_steps + 1)

# 예측 결과 시각화
plt.plot(df['Year'], df['Korea_Growth_Rate'], label='Korea Actual')
plt.plot(years_forecast, forecast, label='Korea Forecast', linestyle='--')
plt.xlabel('Year')
plt.ylabel('Growth Rate')
plt.title('Korea Population Growth Rate Forecast')
plt.legend()
plt.show()

# 예측된 성장률과 일본의 과거 성장률 비교
japan_past_years = df['Year'][-forecast_steps:]
japan_past_growth = df['Japan_Growth_Rate'][-forecast_steps:]

plt.plot(years_forecast, forecast, label='Korea Forecast')
plt.plot(japan_past_years, japan_past_growth, label='Japan Past', linestyle='--')
plt.xlabel('Year')
plt.ylabel('Growth Rate')
plt.title('Korea Future vs Japan Past Growth Rate')
plt.legend()
plt.show()

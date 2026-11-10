import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

print(f"正在拉取回测数据: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")

# 修复：改用 Ticker().history() 可以避免多层表头导致的报错
spy = yf.Ticker('SPY')
df = spy.history(start=start_date, end=end_date)

df['Daily_Return'] = df['Close'].pct_change()
df = df.dropna()

results = []
for index, row in df.iterrows():
    # 修复：强制将取出来的值转换为单一的浮点数 (float)
    daily_return = float(row['Daily_Return'])
    mock_prediction = 1 if daily_return < 0 else -1 
    
    results.append({
        'Date': index.strftime('%Y-%m-%d'),
        'Close': float(row['Close']),
        'Actual_Return': daily_return,
        'MiroFish_Prediction': mock_prediction 
    })

result_df = pd.DataFrame(results)
result_df['Next_Day_Actual_Return'] = result_df['Actual_Return'].shift(-1)
result_df = result_df.dropna()

result_df['Is_Correct'] = (result_df['MiroFish_Prediction'] * result_df['Next_Day_Actual_Return'] > 0)
accuracy = result_df['Is_Correct'].mean()

print(f"回测完成！过去一年模型准确率 (Accuracy): {accuracy:.2%}")

os.makedirs('output', exist_ok=True)
result_df.to_csv('output/backtest_report.csv', index=False)
print("回测报告已保存至 output/backtest_report.csv")

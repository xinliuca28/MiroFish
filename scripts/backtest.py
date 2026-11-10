import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

# 1. 定义时间窗口（过去一年）
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

print(f"正在拉取回测数据: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")

# 2. 获取大盘历史数据
# 这里以 SPY(标普500 ETF) 代表大盘基准
data = yf.download('SPY', start=start_date, end=end_date)
df = pd.DataFrame(data)
df['Daily_Return'] = df['Close'].pct_change()
df = df.dropna()

# 3. 模拟 MiroFish 回测主循环
results = []
for index, row in df.iterrows():
    # 提取当日特征喂给模型（此处可接入你实际的 MiroFish 预测逻辑）
    # 模拟：如果当日跌，模型预测明日反弹（仅作示例，需替换为真实逻辑）
    mock_prediction = 1 if row['Daily_Return'] < 0 else -1 
    
    results.append({
        'Date': index.strftime('%Y-%m-%d'),
        'Close': row['Close'],
        'Actual_Return': row['Daily_Return'],
        'MiroFish_Prediction': mock_prediction 
    })

# 4. 生成回测结果 DataFrame
result_df = pd.DataFrame(results)

# 计算次日真实涨跌，用来和预测对比 (T日预测对比T+1日实际涨跌)
result_df['Next_Day_Actual_Return'] = result_df['Actual_Return'].shift(-1)
result_df = result_df.dropna()

# 计算准确率 (预测方向与实际次日方向一致)
result_df['Is_Correct'] = (result_df['MiroFish_Prediction'] * result_df['Next_Day_Actual_Return'] > 0)
accuracy = result_df['Is_Correct'].mean()

print(f"回测完成！过去一年模型准确率 (Accuracy): {accuracy:.2%}")

# 5. 保存回测报告
os.makedirs('output', exist_ok=True)
result_df.to_csv('output/backtest_report.csv', index=False)
print("回测报告已保存至 output/backtest_report.csv")

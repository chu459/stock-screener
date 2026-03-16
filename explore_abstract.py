import akshare as ak
import pandas as pd

df = ak.stock_financial_abstract(symbol="000001")
print("DataFrame shape:", df.shape)
print("\nFirst 20 columns:", df.columns.tolist()[:20])
print("\nRows where '指标' contains '净资产收益率':")
roe_rows = df[df['指标'].str.contains('净资产收益率', na=False)]
print(roe_rows[['指标', '20250930', '20240630', '20230331']].head())
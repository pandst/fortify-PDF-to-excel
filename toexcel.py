import pandas as pd

# 讀取JSON檔案
with open('result.json', 'r') as json_file:
    data = pd.read_json(json_file)

# 將DataFrame保存為Excel
data.to_excel('output.xlsx', index=False)

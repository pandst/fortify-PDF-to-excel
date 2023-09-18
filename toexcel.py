import pandas as pd

# 讀取JSON檔案
with open('result1.json', 'r') as json_file:
    data = pd.read_json(json_file)
with open('result2.json', 'r') as json_file:
    data2 = pd.read_json(json_file)
# 將DataFrame保存為Excel
data.to_excel('OWASP.xlsx', index=False)
data2.to_excel('DW.xlsx', index=False)
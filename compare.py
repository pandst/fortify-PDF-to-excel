import json

import json

def compare_json(file1, file2):
    with open(file1, "r", encoding="utf-8") as f:
        data1 = json.load(f)
    with open(file2, "r", encoding="utf-8") as f:
        data2 = json.load(f)
    
    for dict2 in data2:
        keys2 = set(dict2.keys())
        keys2.discard("Package")
        
        for dict1 in data1:
            keys1 = set(dict1.keys())
            keys1.discard("Package")
            keys1.discard("page")

            if not keys1.issubset(keys2):
                continue

            
            if keys1.issubset(keys2):
                if all(dict1.get(k) == dict2.get(k) for k in keys1):
                    dict2["same"] = "OWASP10"
                    break  # 已經找到匹配的，所以跳出內部循環


    # 將修改後的 data2 寫回到 file2
    with open(file2, "w", encoding="utf-8") as f:
        json.dump(data2, f, ensure_ascii=False)

compare_json("result1.json", "result2.json")
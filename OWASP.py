import json
from collections import defaultdict
import re  # 導入正則表達式模塊
from os import path


def generate_result_json():
    with open("all_table.json", "r", encoding="utf-8") as f:
        original_data = json.load(f)

    unique_results = defaultdict(list)
    results = []
    current_result = {}
    all_positions = []
    all_packages = []
    current_package = None
    current_danger = None
    current_method = None
    danger_keywords = ["Critical", "High", "Medium", "Low"]

    for page, content in original_data.items():
        for cell in content:
            current_result["page"] = page

            if "Package" in cell:
                current_package = cell
                current_result["Package"] = current_package
                all_packages.append(current_package)

            elif "Remediation Effort(Hrs): " in cell:
                current_method = re.sub(
                    r"Remediation Effort\(Hrs\): \d+(\.\d+)?", "", cell)

            elif re.search(r':\d+$', cell):
                if not cell.startswith("Sink:"):
                    position, line = cell.rsplit(":", 1)
                    # 使用.strip()來去除多餘的空格
                    position = position.replace(" ", "")
                    current_result["position"] = position.strip()
                    all_positions.append(position.strip())
                    if current_method:
                        line += f" ({current_method.strip()})"
                    current_result["line"] = line.strip()  # 使用.strip()來去除多餘的空格

            elif cell in danger_keywords:
                current_danger = cell

            current_result["danger"] = current_danger

            if all(key in current_result for key in ["page", "Package", "position", "line", "danger"]):
                key = (current_result["Package"], current_result["position"],
                       current_result["line"], current_result["danger"])
                unique_results[key].append(current_result["page"])
                current_result = {"page": page, "Package": current_package,
                                  "danger": current_danger, "method": current_method}

        current_result = {}
        current_package = None
        current_danger = None
        current_method = None
    common_prefix_position = path.commonprefix(all_positions)
    common_prefix_package = path.commonprefix(all_packages)
    for (package, position, line, danger), pages in unique_results.items():
        combined_result = {
            "page": ",".join(set(pages)),
            "Package": package.replace(common_prefix_package, ''),
            "position": position.replace(common_prefix_position, ''),
            "line": line,
            "danger": danger
        }

        results.append(combined_result)

    with open("result1.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


generate_result_json()

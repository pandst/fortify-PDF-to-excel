import json
from collections import defaultdict
from os import path


def generate_result_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        original_data = json.load(f)

    unique_results = defaultdict(list)  # To store unique line values
    page_results = defaultdict(list)    # To store unique page values
    results = []  # Final result list
    current_result = {}
    fill_danger_next = False
    current_package = None
    all_positions = []
    all_packages = []
    for page, content in original_data.items():
        for cell in content:
            current_result["page"] = page

            if "Package" in cell:
                current_package = cell
                current_result["Package"] = current_package.strip()
                all_packages.append(current_package.strip())
            elif ", line" in cell:
                position, line = cell.split(", ", 1)
                line = line.replace("line ", "")  # 移除 "line "
                position = position.replace(" ", "")
                current_result["position"] = position.strip()
                all_positions.append(position.strip())
                current_result["line"] = line
                fill_danger_next = True

            elif fill_danger_next:
                current_result["danger"] = cell
                fill_danger_next = False

                if all(key in current_result for key in ["page", "Package", "position", "line", "danger"]):
                    key = (current_result["Package"], current_result["position"],
                           current_result["line"], current_result["danger"])
                    unique_results[key].append(current_result["page"])
                    page_results[key].append(current_result["page"])
                    current_result = {"page": page, "Package": current_package}

        current_result = {}
        current_package = None
    common_prefix_position = path.commonprefix(all_positions)
    print("common_prefix_position")
    print(common_prefix_position)
    common_prefix_package = path.commonprefix(all_packages)
    print("common_prefix_package")
    print(common_prefix_package)
    # Combine similar entries
    for (package, position, line, danger), pages in unique_results.items():
        combined_result = {
            "page": ",".join(set(pages)),
            "Package": package.replace(common_prefix_package, ''),
            "position": position.replace(common_prefix_position, ''),
            "line": line,
            "danger": danger
        }
        results.append(combined_result)

    with open("result2.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


# 使用範例：
file_path = "all_table.json"
generate_result_json(file_path)

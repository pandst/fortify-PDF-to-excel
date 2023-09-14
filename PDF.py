import pdfplumber
import os
import json

def filter_empty_rows_and_columns(table):
    return [
        [cell.replace("\n", " ") if cell else cell for cell in row if cell not in [None, ""]]
        for row in table if any(cell not in [None, ""] for cell in row)
    ]

def extract_tables_from_pdf(pdf_file_name):
    current_directory = os.getcwd()
    pdf_file_path = os.path.join(current_directory, pdf_file_name)
    
    extracted_tables_by_page = {}
    
    with pdfplumber.open(pdf_file_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            filtered_tables = [filter_empty_rows_and_columns(table) for table in tables if any(cell not in [None, ""] for row in table for cell in row)]
            
            # 降維：將多個表格的內容合併到一個大列表中
            flattened_tables = [cell for table in filtered_tables for row in table for cell in row]
            
            if flattened_tables:  # 只添加有內容的頁面
                extracted_tables_by_page[f'Page {page_num + 1}'] = flattened_tables
    
    # 當所有頁面都被處理後，儲存所有表格到一個 JSON 文件
    with open("all_table.json", "w", encoding='utf-8') as f:
        json.dump(extracted_tables_by_page, f, ensure_ascii=False, indent=4)

# PDF 文件名，請根據您的需求來修改這個部分
pdf_file_name = 'data/XR API/G9_NF17027-2_898109_20230912_161654355928_JS_OWASP.pdf'

# 執行函數
extract_tables_from_pdf(pdf_file_name)

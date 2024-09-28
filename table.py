import pdfplumber
import delete
import pandas as pd

def getTables(path):
    
    delete.delTable('Tables/')

    with pdfplumber.open(path) as pdf:
        for page_num in range(34, len(pdf.pages)): 
            page = pdf.pages[page_num]
            tables = page.extract_tables()
            for i, table in enumerate(tables):
                if len(table[0]) <= 1:
                    continue
                elif page_num not in [40,41]:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df.to_csv(f"Tables/table_{page_num+1}_{i}.csv", index=False)
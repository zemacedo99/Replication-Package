import pandas as pd

def create_query_from_csv(csv_path):
    # Read the CSV
    df = pd.read_csv(csv_path)
    
    # Group by 'Category' and join terms with ' OR '
    query_groups = df.groupby('Category')['Term'].apply(lambda x: f"({') OR ('.join(x)})").tolist()
    
    # Join groups with ' AND '
    query = ' AND '.join(query_groups)
    
    return query

# Assuming 'terms.csv' is your file
query = create_query_from_csv('C:\Users\jamacedo\OneDrive - CRITICAL SOFTWARE, S.A\Documents\FEUP\Thesis\Git\terms.csv')
print(query)

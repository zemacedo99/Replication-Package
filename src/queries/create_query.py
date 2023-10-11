import pandas as pd
import os

def create_query_from_csv(filename):

    script_directory = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_directory, filename)
    
    # Read the CSV
    df = pd.read_csv(csv_path)

    # Ensure 'Term' is of string type
    df['Term'] = df['Term'].astype(str)
    
    # Group by 'Category' and join terms with ' OR '
    query_groups = df.groupby('Category')['Term'].apply(lambda x: f"({' OR '.join(x)})").tolist()
    
    # Join groups with ' AND '
    query = ' AND '.join(query_groups)

    return query

def write_query_to_py_file(query):
    py_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "query.py")
    with open(py_file_path, 'w') as f:
        f.write(f'SCOPUS_QUERY = "{query}"\n')
        f.write(f'IEEE_QUERY = "{query}"\n')
        f.write(f'ENGINEERING_VILLAGE_QUERY = "{query}"\n')

# Assuming 'query_terms.csv' is your file
query = create_query_from_csv("query_terms.csv")

# Write the generated query to query.py
write_query_to_py_file(query)

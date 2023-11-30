import pandas as pd
import os

def create_query_from_csv(filename):

    script_directory = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_directory, filename)
    
    # Read the CSV
    df = pd.read_csv(csv_path)

    # Ensure 'Term' is of string type
    df['Term'] = df['Term'].astype(str)

    # Separate 'ToRemove' category
    to_remove_df = df[df['Category'] == 'ToRemove']
    other_df = df[df['Category'] != 'ToRemove']

    # Format 'ToRemove' terms
    to_remove_query = ' '.join(['AND NOT "{}"'.format(item) for item in to_remove_df['Term']])
    to_remove_query_ev = ' '.join(['NOT "{}"'.format(item) for item in to_remove_df['Term']])  # For ENGINEERING_VILLAGE_QUERY

    # Group other terms by 'Category' and join with ' OR '
    query_groups = other_df.groupby('Category')['Term'].apply(
        lambda x: '({})'.format(' OR '.join(['"{}"'.format(item) for item in x]))
    ).tolist()

    # Combine all queries
    combined_query = ' AND '.join(query_groups)
    query = "{} {}".format(combined_query, to_remove_query).strip()
    query_ev = "{} {}".format(combined_query, to_remove_query_ev).strip()  # For ENGINEERING_VILLAGE_QUERY

    return query, query_ev

def write_query_to_py_file(query, query_ev):
    py_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "query.py")
    with open(py_file_path, 'w') as f:
        f.write('QUERY = \'{}\'\n'.format(query))
        f.write('SCOPUS_QUERY = \'{}\'\n'.format(query))
        f.write('IEEE_QUERY = \'{}\'\n'.format(query))
        f.write('ENGINEERING_VILLAGE_QUERY = \'{}\'\n'.format(query_ev))  # Different format for ENGINEERING_VILLAGE_QUERY
        f.write('SCIENCE_DIRECT_QUERY = \'{}\'\n'.format(query))
        f.write('HAL_OPEN_SCIENCE_QUERY = \'{}\'\n'.format(query))
        f.write('ACM_DIGITAL_LIBRARY_QUERY = \'{}\'\n'.format(query))
        f.write('SPRINGER_NATURE_QUERY = \'{}\'\n'.format(query))

# Assuming 'query_terms.csv' is your file
query, query_ev = create_query_from_csv("query_terms.csv")
print("Standard Query:", query)
print("Engineering Village Query:", query_ev)

# Write the generated query to query.py
write_query_to_py_file(query, query_ev)

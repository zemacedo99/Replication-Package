import pandas as pd

def process_and_save_results(scopus_df, ieee_df):
    """
    Combines data from Scopus and IEEE, creates two CSVs: 
    one for unique results and another for repeated results.
    
    Parameters:
    - scopus_df (DataFrame): Results from Scopus
    - ieee_df (DataFrame): Results from IEEE

    Returns:
    None
    """

    # Combine the DataFrames
    all_results_df = pd.concat([scopus_df, ieee_df], ignore_index=True, sort=False)

    # Find duplicated rows based on 'Title' (or another relevant column)
    duplicate_titles = all_results_df[all_results_df.duplicated(subset='Title', keep=False)].copy()

    # Annotate the duplicates with their source
    def annotate_source(row):
        sources = []
        if row in scopus_df['Title'].values:
            sources.append("Scopus")
        if row in ieee_df['Title'].values:
            sources.append("IEEE")
        return ', '.join(sources)

    duplicate_titles['Source'] = duplicate_titles['Title'].apply(annotate_source)


    # Save the duplicates to a CSV
    duplicate_titles.to_csv("repeated.csv", index=False)

    # Drop duplicates from the all_results_df
    all_results_df.drop_duplicates(subset='Title', inplace=True)

    # Save the results to CSV
    all_results_df.to_csv("all_results.csv", index=False)

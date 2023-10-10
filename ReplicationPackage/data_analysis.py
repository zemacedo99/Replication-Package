import pandas as pd

def process_and_save_results(scopus_results, ieee_results, engineering_village_results):
    """
    Combines data from Scopus, IEEE, and Engineering Village, creates two CSVs: 
    one for unique results and another for repeated results.
    
    Parameters:
    - scopus_results (List): Results from Scopus
    - ieee_results (List): Results from IEEE
    - engineering_village_results (List): Results from Engineering Village

    Returns:
    None
    """

    scopus_df = pd.DataFrame(scopus_results)
    ieee_df = pd.DataFrame(ieee_results)
    engineering_village_df = pd.DataFrame(engineering_village_results)
    
    # Mark the source of each row in the original dataframes
    scopus_df['Source'] = 'Scopus'
    ieee_df['Source'] = 'IEEE'
    engineering_village_df['Source'] = 'Engineering Village'
    
    # Combine the DataFrames
    all_results_df = pd.concat([scopus_df, ieee_df, engineering_village_df], ignore_index=True, sort=False)

    # Group by Title and aggregate the sources
    source_agg = all_results_df.groupby('Title')['Source'].apply(lambda x: ', '.join(x)).reset_index()

    # Merge this aggregated source with the original dataframe
    all_results_df = all_results_df.drop('Source', axis=1).merge(source_agg, on='Title', how='left')

    # Extract rows which are duplicated in Title
    duplicated_df = all_results_df[all_results_df.duplicated(subset='Title', keep=False)].drop_duplicates(subset='Title', keep='first')

    # Save the duplicates to a CSV
    duplicated_df.to_csv("repeated.csv", index=False)

    # Drop duplicates from the all_results_df to only keep the first occurrence
    unique_results_df = all_results_df.drop_duplicates(subset='Title', keep='first')

    # Save the unique results to CSV
    unique_results_df.to_csv("all_results.csv", index=False)
    
    # Save individual database results to CSV
    scopus_df.to_csv("scopus_results.csv", index=False)
    ieee_df.to_csv("ieee_results.csv", index=False)


# after agile manidest 
import pandas as pd
import pandas as pd

def process_and_save_results(scopus_results, ieee_results, engineering_village_results):
    """
    Combines data from Scopus and IEEE, creates two CSVs: 
    one for unique results and another for repeated results.
    
    Parameters:
    - scopus_results (List): Results from Scopus
    - ieee_results (List): Results from IEEE

    Returns:
    None
    """

    scopus_df = pd.DataFrame(scopus_results)
    scopus_df.to_csv("scopus_results.csv", index=False)
    ieee_df = pd.DataFrame(ieee_results)
    ieee_df.to_csv("ieee_results.csv", index=False)
    engineering_village_df = pd.DataFrame(engineering_village_results)
    engineering_village_df.to_csv("engineering_village_results.csv", index=False)

    # Mark the source of each row in the original dataframes
    scopus_df['Source'] = 'Scopus'
    ieee_df['Source'] = 'IEEE'
    engineering_village_df['Source'] = 'Engineering Village'
    
    # Combine the DataFrames
    all_results_df = pd.concat([scopus_df, ieee_df,engineering_village_df], ignore_index=True, sort=False)

    # Extract rows which are duplicated in Title
    duplicated_df = all_results_df[all_results_df.duplicated(subset='Title', keep='first')]

    # Save the duplicates to a CSV
    duplicated_df.to_csv("repeated.csv", index=False)

    # Drop duplicates from the all_results_df to only keep the first occurrence
    unique_results_df = all_results_df.drop_duplicates(subset='Title', keep='first')

    # Save the unique results to CSV
    unique_results_df.to_csv("all_results.csv", index=False)

# after agile manidest 
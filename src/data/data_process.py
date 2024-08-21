import pandas as pd
import os
import sys
from langdetect import detect, LangDetectException
from data.data_validation import validate_results
root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_directory)
from utils import data_to_pdf

def is_english(text):
    # Check if the text is a string and not NaN
    if not isinstance(text, str) or pd.isna(text):
        return False

    # If the text is very short, it might be erroneously detected as non-English
    if len(text.split()) <= 3:  # Threshold for short text, adjust as needed
        return True

    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False


def remove_non_english_rows(df, col1, col2):
    def row_is_non_english(row):
        return not (is_english(row[col1]) or is_english(row[col2]))

    # Identify non-English rows
    non_english_rows = df[df.apply(row_is_non_english, axis=1)]

    # Save these rows to a CSV file
    non_english_rows.to_csv("data_results/non_english.csv", index=False)

    # Keep rows where at least one column is in English
    return df[~df.apply(row_is_non_english, axis=1)]

def filter_venues(df, exclude_venues_file):
    """
    Filters out rows from a DataFrame based on a list of venues to exclude provided in a text file.

    :param df: Pandas DataFrame to filter.
    :param exclude_venues_file: Path to the text file containing venues to exclude (one per line).
    """
    # Read the list of venues to exclude from the text file
    with open(exclude_venues_file, 'r', encoding='utf-8') as file:
        exclude_venues = [line.strip() for line in file]

    # Filter out the rows with the venues to be excluded
    filtered_df = df[~df['Venue'].isin(exclude_venues)]

    return filtered_df

def filter_after_agile_manifesto_date(df):
    """
    Removes rows from the DataFrame where the Publication Year is before 2001.

    Parameters:
    - df (DataFrame): DataFrame containing article or paper details

    Returns:
    - DataFrame: Filtered DataFrame
    """

    # Drop rows where 'Publication Year' is NaN (if any)
    df = df.dropna(subset=['Publication Year'])

    # Ensure 'Publication Year' is of type int
    try:
        df.loc[:, 'Publication Year'] = df['Publication Year'].astype(int)
    except ValueError:
        print("There are values in 'Publication Year' that cannot be converted to integers.")
        return df  

    # Filter rows where Publication Year is 2001 or later
    return df[df['Publication Year'] >= 2001]

def process_and_save_result(result, data_base, folder_name):
    """
    Transforms data into a DataFrame, marks the source of each row, and saves to CSV.

    Parameters:
    - result (List): Raw data.
    - data_base (str): The name of the database/source.

    Returns:
    - DataFrame: Processed DataFrame.
    """
    
    df = pd.DataFrame(result)
    df['Source'] = data_base
    
    # Make filename safe (replace spaces with underscores, etc.) and create the full path
    filename = os.path.join(folder_name, data_base.replace(" ", "_").lower() + ".csv")
    
    df.to_csv(filename, index=False)
    return df


def process_and_save_results(scopus_results, ieee_results, engineering_village_results, science_direct_results, hal_open_science_results, acm_digital_library_results, springer_nature_results, folder_name="data_results"):
    """
    Combines data from Scopus, IEEE, and Engineering Village, creates two CSVs: 
    one for unique results and another for repeated results.
    
    Parameters:
    - scopus_results (List): Results from Scopus
    - ieee_results (List): Results from IEEE
    - engineering_village_results (List): Results from Engineering Village
    - science_direct_results (List): Results from Science Direct

    Returns:
    None
    """

    # Ensure the folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    scopus_df = process_and_save_result(scopus_results, "Scopus",folder_name)
    ieee_df = process_and_save_result(ieee_results, "IEEE",folder_name)
    engineering_village_df = process_and_save_result(engineering_village_results, "Engineering Village",folder_name)
    science_direct_df = process_and_save_result(science_direct_results, "Science Direct",folder_name)
    hal_open_science_results_df = process_and_save_result(hal_open_science_results, "Hal Open Science",folder_name)
    acm_digital_library_results_df = process_and_save_result(acm_digital_library_results, "ACM Digital Library",folder_name)
    springer_nature_results_df = process_and_save_result(springer_nature_results, "Springer Nature",folder_name)

    # Combine the DataFrames
    all_results_df = pd.concat([scopus_df, ieee_df, engineering_village_df,science_direct_df, hal_open_science_results_df,acm_digital_library_results_df,springer_nature_results_df], ignore_index=True, sort=False)

    # Create the processed title
    all_results_df['ProcessedTitle'] = all_results_df['Title'].str.lower().str.replace(r'[!@#$%^&*()_+\-=[\]\{};:\'",.<>?/~`|\\]+', '', regex=True)

    # Create the processed Venue
    all_results_df['ProcessedVenue'] = all_results_df['Venue'].str.lower().str.replace(r'[!@#$%^&*()_+\-=[\]\{};:\'",.<>?/~`|\\]+', '', regex=True)

    # Save all results to a CSV
    all_results_df.to_csv(os.path.join(folder_name,"all_results.csv"), index=False)

    # Group by Title and aggregate the sources
    source_agg = all_results_df.groupby('ProcessedTitle')['Source'].apply(lambda x: ', '.join(x)).reset_index()

    # Merge this aggregated source with the original dataframe
    all_results_df = all_results_df.drop('Source', axis=1).merge(source_agg, on='ProcessedTitle', how='left')

    # Drop duplicates from the all_results_df to only keep the first occurrence
    unique_results_df = all_results_df.drop_duplicates(subset='ProcessedTitle', keep='first')

    # Process unique_results_df using the filter_after_agile_manifesto_date function
    unique_results_df = filter_after_agile_manifesto_date(unique_results_df)

    unique_results_df = remove_non_english_rows(unique_results_df, 'ProcessedTitle', 'ProcessedVenue')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    exclude_venues_txt = os.path.normpath(os.path.join(current_dir, 'venues_to_exclude.txt')) # Path to your text file with venues
     
    unique_results_df = filter_venues(unique_results_df, exclude_venues_txt)

    # unique_results_df['Venue'] = unique_results_df['Venue'].str.lower().str.replace(r'[!@#$%^&*()_+\-=[\]\{};:\'",.<>?/~`|\\]+', '', regex=True)
    # data_to_pdf(unique_results_df, 'Venue')

    # Save the unique results to CSV
    unique_results_df.to_csv(os.path.normpath(os.path.join(folder_name,"unique_results.csv")), index=False)

    # Drop duplicates using the processed title
    duplicated_df = all_results_df[all_results_df.duplicated(subset='ProcessedTitle', keep=False)].drop_duplicates(subset='ProcessedTitle', keep='first')

    # Save the duplicates to a CSV
    duplicated_df.to_csv(os.path.join(folder_name,"repeated.csv"), index=False)

    validate_results()

if __name__ == "__main__":

    print(os.getcwd())
    scopus_results = pd.read_csv('data_results/scopus.csv')
    ieee_results = pd.read_csv('data_results/ieee.csv')
    engineering_village_results = pd.read_csv('data_results/engineering_village.csv')
    science_direct_results = pd.read_csv('data_results/science_direct.csv')
    hal_open_science_results = pd.read_csv('data_results/hal_open_science.csv')
    acm_digital_library_results = pd.read_csv('data_results/acm_digital_library.csv')
    springer_nature_results = pd.read_csv('data_results/springer_nature.csv')

    process_and_save_results(scopus_results, ieee_results, engineering_village_results, science_direct_results,hal_open_science_results,acm_digital_library_results,springer_nature_results)


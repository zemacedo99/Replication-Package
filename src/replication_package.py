from search.scienceDirect_search import extract_science_direct_information, search_science_direct
from search.scopus_search import search_scopus, scopus_extract_information 
from search.ieee_search import search_ieee, extract_ieee_information
from search.inspec_search import search_engineering_village, engineering_village_extract_information
from data.data_process import process_and_save_results
from queries.query import ENGINEERING_VILLAGE_QUERY, IEEE_QUERY, SCIENCE_DIRECT_QUERY, SCOPUS_QUERY
try:
    from config import ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, IEEE_API_KEY
except ImportError:
    raise ImportError("config.py not found. Please set up your API key as instructed in README.md")

if __name__ == "__main__":
    
    scopus_results = []
    ieee_results = []
    engineering_village_results = []
    science_direct_results =[]

    # Initialize flag variables to control the loop
    scopus_more_data = True
    ieee_more_data = True
    engineering_village_more_data = True
    science_direct_more_data = True
    
    start_index = 0
    PAGE_SIZE = 25

    while ((scopus_more_data or ieee_more_data or engineering_village_more_data or science_direct_more_data) and start_index < 100):
        print(f"\nFetching results starting from index {start_index}...")

        # Scopus search
        if scopus_more_data:
            print("Querying Scopus...")
            scopus_data = search_scopus(SCOPUS_QUERY, ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, start=start_index, count=PAGE_SIZE)
            if scopus_data:
                scopus_info = scopus_extract_information({"search-results": {"entry": scopus_data}})
                scopus_results.extend(scopus_info)
                print(f"Fetched {len(scopus_info)} results from Scopus.")
            else:
                print("No more results from Scopus.")
                scopus_more_data = False

        # IEEE Xplore search
        if ieee_more_data:
            print("Querying IEEE Xplore...")
            ieee_data = search_ieee(IEEE_QUERY, IEEE_API_KEY, start_record=start_index + 1, max_records=PAGE_SIZE)  # IEEE uses 1-indexing
            if ieee_data and 'articles' in ieee_data and ieee_data['articles']:
                ieee_info = extract_ieee_information(ieee_data)
                ieee_results.extend(ieee_info)
                print(f"Fetched {len(ieee_info)} results from IEEE Xplore.")
            else:
                print("No more results from IEEE Xplore.")
                ieee_more_data = False

        # Engineering Village search
        if engineering_village_more_data:
            print("Querying Engineering Village...")
            engineering_village_data = search_engineering_village(ENGINEERING_VILLAGE_QUERY, ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, start=start_index, count=PAGE_SIZE)
            if engineering_village_data:
                engineering_village_info = engineering_village_extract_information(engineering_village_data)
                engineering_village_results.extend(engineering_village_info)
                print(f"Fetched {len(engineering_village_info)} results from Engineering Village.")
            else:
                print("No more results from Engineering Village.")
                engineering_village_more_data = False

        # Engineering Village search
        if science_direct_more_data:
            print("Querying Science Direct...")
            science_direct_data = search_science_direct(SCIENCE_DIRECT_QUERY, ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, start=start_index, count=PAGE_SIZE)
            if science_direct_data:
                science_direct_info = extract_science_direct_information(science_direct_data)
                science_direct_results.extend(science_direct_info)
                print(f"Fetched {len(science_direct_info)} results from Science Direct.")
            else:
                print("No more results from Engineering Village.")
                science_direct_more_data = False

        start_index += PAGE_SIZE


    process_and_save_results(scopus_results, ieee_results, engineering_village_results, science_direct_results)



# TODO: Analyzing the data
# TODO: Filtering results by year, journal, etc.
# TODO: Processing and analyzing the retrieved data further, create chards and graphs
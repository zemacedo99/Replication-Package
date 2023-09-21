import pandas as pd
# import json
from  scopus_script import search_scopus, scopus_extract_information 
from ieee_search import search_ieee, extract_ieee_information


if __name__ == "__main__":
    # TODO: when providing this script, make this an input for the user
    SCOPUS_API_KEY = "c803f556d065be19b3905ccee12adbfa" 
    IEEE_API_KEY = "vcahw7f4hxwxrv8kdapvyhnv"

    # TODO: create the query by collection the terms from a csv
    # QUERY = "(agile OR agility OR xp OR ”extreme W/0 programming” OR scrum OR kanban OR scrumban OR safescrum OR agilesafe OR ”agile W/0 safe”) AND (safety OR ”safety W/0 systems” OR safetycritical OR ”safety W/0 critical” OR ”safety-critical W/0 systems” OR ”safety W/0 critical W/0 systems” OR ”high W/0 integrity” OR ”high W/0 integrity W/0 systems” OR his OR ”safety W/0 integrity”) AND (aerospace OR avionic OR avionics OR aviation OR aeronautic OR aeronautics OR aeronautical) OR (”ARP W/0 4761” OR arp4761 OR ”ARP W/0 4754” OR arp4754 OR do-178 OR do-178b OR DO 178C OR do178 OR do178b OR do178c OR do-331 OR do331)"  
    SCOPUS_QUERY = "docops"
    IEEE_QUERY = "machinelearning"
    
    scopus_results = []
    ieee_results = []
    start_index = 0
    PAGE_SIZE = 25
    
    # Initialize flag variables to control the loop
    scopus_more_data = True
    ieee_more_data = True

    while scopus_more_data or ieee_more_data:
        print(f"Fetching results starting from index {start_index}...")

        # Scopus search
        if scopus_more_data:
            print("Querying Scopus...")
            scopus_data = search_scopus(SCOPUS_QUERY, SCOPUS_API_KEY, start=start_index, count=PAGE_SIZE)
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

        start_index += PAGE_SIZE

    scopus_df = pd.DataFrame(scopus_results)
    scopus_df.to_csv("scopus_results.csv", index=False)
    ieee_df = pd.DataFrame(ieee_results)
    ieee_df.to_csv("ieee_results.csv", index=False)
    print("Results saved csv")
    # TODO: group the unique ones from all search engines


# TODO: Analyzing the data
# TODO: Filtering results by year, journal, etc.
# TODO: Processing and analyzing the retrieved data further, create chards and graphs
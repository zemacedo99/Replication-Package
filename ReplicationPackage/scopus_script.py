import requests
import pandas as pd

# TODO: Rate Limits and Pagination
# The Scopus API has rate limits. 
# Ensure that the script doesn't send requests too quickly to avoid getting temporarily blocked. 
# The script below fetches a set number of results (default 25). 
# If the search yields more results, there is a need to implement pagination to retrieve all.

def search_scopus(query, api_key,start=0, count=25):
    base_url = "https://api.elsevier.com/content/search/scopus"
    
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key
    }
    
    params = {
        "query": query,
        "count": count,
        "start": start
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data['search-results'].get('entry', [])  # Return empty list if 'entry' doesn't exist
    else:
        response.raise_for_status()

def extract_information(data):
    extracted = []
    
    for item in data['search-results']['entry']:
        title = item['dc:title']
        
        # Correctly extract the publication year
        cover_date = item.get('prism:coverDate')
        if cover_date and isinstance(cover_date, str):
            publication_year = cover_date.split('-')[0]
        else:
            publication_year = None
        
        journal = item['prism:publicationName']
        
        authors = []
        if 'author' in item:
            for author in item['author']:
                authors.append(author['authname'])
        
        extracted.append({
            'Title': title,
            'Publication Year': publication_year,
            'Journal': journal,
            'Authors': ', '.join(authors)
        })
    
    return extracted


if __name__ == "__main__":
    # TODO: when providing this script, make this an input for the user
    API_KEY = "c803f556d065be19b3905ccee12adbfa" 

    # TODO: create the query by collection the terms from a csv
    # query = "(agile OR agility OR xp OR ”extreme W/0 programming” OR scrum OR kanban OR scrumban OR safescrum OR agilesafe OR ”agile W/0 safe”) AND (safety OR ”safety W/0 systems” OR safetycritical OR ”safety W/0 critical” OR ”safety-critical W/0 systems” OR ”safety W/0 critical W/0 systems” OR ”high W/0 integrity” OR ”high W/0 integrity W/0 systems” OR his OR ”safety W/0 integrity”) AND (aerospace OR avionic OR avionics OR aviation OR aeronautic OR aeronautics OR aeronautical) OR (”ARP W/0 4761” OR arp4761 OR ”ARP W/0 4754” OR arp4754 OR do-178 OR do-178b OR DO 178C OR do178 OR do178b OR do178c OR do-331 OR do331)"  
    QUERY = "docops"

    
    # TODO: Analyzing and Parsing the Results
    # Modify the script to extract more details as per the requirements.
    # The Scopus API returns a lot more information, such as authors, journal name, publication year, etc.
    # The script below prints only the titles of the articles returned by the search for now.
    # results = search_scopus(query, API_KEY)
    # for item in results['search-results']['entry']:
    #     print(item['dc:title'])
    
    all_results = []
    start_index = 0
    PAGE_SIZE = 25
    TOTAL_RESULTS = 250  # Adjust if needed
    
    while start_index < TOTAL_RESULTS:
        print(f"Fetching results starting from index {start_index}...")
        entries = search_scopus(QUERY, API_KEY, start=start_index, count=PAGE_SIZE)
        
        if not entries:  # Break the loop if there are no more entries.
            break

        all_results.extend(extract_information({"search-results": {"entry": entries}}))
        start_index += PAGE_SIZE
        
    df = pd.DataFrame(all_results)
    df.to_csv("scopus_results.csv", index=False)
    print("Results saved to scopus_results.csv")


# TODO: Saving results to a CSV or database.
# TODO: Filtering results by year, journal, etc.
# TODO: Processing and analyzing the retrieved data further, create chards and graphs
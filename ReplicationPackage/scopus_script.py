import requests

# TODO: Rate Limits and Pagination
# The Scopus API has rate limits. 
# Ensure that the script doesn't send requests too quickly to avoid getting temporarily blocked. 
# The script below fetches a set number of results (default 25). 
# If the search yields more results, there is a need to implement pagination to retrieve all.

def search_scopus(query, api_key, count=25):
    base_url = "https://api.elsevier.com/content/search/scopus"
    
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key
    }
    
    params = {
        "query": query,
        "count": count,
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


if __name__ == "__main__":
    # TODO: when providing this script, make this an input for the user
    API_KEY = "c803f556d065be19b3905ccee12adbfa" 

    # TODO: create the query by collection the terms from a csv
    # query = "(agile OR agility OR xp OR ”extreme W/0 programming” OR scrum OR kanban OR scrumban OR safescrum OR agilesafe OR ”agile W/0 safe”) AND (safety OR ”safety W/0 systems” OR safetycritical OR ”safety W/0 critical” OR ”safety-critical W/0 systems” OR ”safety W/0 critical W/0 systems” OR ”high W/0 integrity” OR ”high W/0 integrity W/0 systems” OR his OR ”safety W/0 integrity”) AND (aerospace OR avionic OR avionics OR aviation OR aeronautic OR aeronautics OR aeronautical) OR (”ARP W/0 4761” OR arp4761 OR ”ARP W/0 4754” OR arp4754 OR do-178 OR do-178b OR DO 178C OR do178 OR do178b OR do178c OR do-331 OR do331)"  
    query = "docops"

    # TODO: Analyzing and Parsing the Results
    # Modify the script to extract more details as per the requirements.
    # The Scopus API returns a lot more information, such as authors, journal name, publication year, etc.
    # The script below prints only the titles of the articles returned by the search for now.
    results = search_scopus(query, API_KEY)
    for item in results['search-results']['entry']:
        print(item['dc:title'])



# TODO: Saving results to a CSV or database.
# TODO: Filtering results by year, journal, etc.
# TODO: Processing and analyzing the retrieved data further, create chards and graphs
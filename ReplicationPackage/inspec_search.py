import requests

def search_engineering_village(query, api_key, inst_token, start=0, count=25):

    url = "https://api.elsevier.com/content/ev/results"
    
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key,
        "X-ELS-Insttoken" : inst_token
    }

    params = {
        "database": "i",          
        "query": query,
        "offset": start,
        "pageSize": count,
    }
  
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


# Parsing the search results
# If need modify the script to extract more details as per the requirements.
# The Engineering Village API returns a lot more information https://dev.elsevier.com/tecdoc_ev_request.html
def engineering_village_extract_information(data):
    page_results = data.get('PAGE', {}).get('PAGE-RESULTS', {})
    page_entries = page_results.get('PAGE-ENTRY', [])
    
    extracted = []
    
    for entry in page_entries:
        ei_document = entry.get('EI-DOCUMENT', {})
        doc_properties = ei_document.get('DOCUMENTPROPERTIES', {})
        
        title = doc_properties.get('TI')
        publication_year = doc_properties.get('YR')
        venue = doc_properties.get('SO')
        
        aus = ei_document.get('AUS', {})
        authors = aus.get('AU', [])
        author_names = ', '.join([author.get('NAME', '') for author in authors])
        
        extracted.append({
            'Title': title,
            'Publication Year': publication_year,
            'Venue': venue,
            'Authors': author_names
        })
    
    return extracted

# if __name__ == "__main__":
#     ELSEVIER_API_KEY = "c803f556d065be19b3905ccee12adbfa" 
#     ELSEVIER_INST_TOKEN = "35634be89c56c9527b9c35034e7b9cab"
#     query = "agile" 
        
#     start_index = 0
#     PAGE_SIZE = 25
#     results = search_engineering_village(query, ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, start=start_index, count=PAGE_SIZE)
 
#     data = engineering_village_extract_information(results)

#     print(data)
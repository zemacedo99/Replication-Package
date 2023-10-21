import requests
try:
    from config import ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN
except ImportError:
    raise ImportError("config.py not found. Please set up your API key as instructed in README.md")

def search_engineering_village(query, api_key, inst_token, start=0, count=25):
    print("\nQuerying Engineering Village")

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
    page_entries = page_results.get('PAGE-ENTRY', []) if isinstance(page_results, dict) else []
    
    extracted = []

    base_doi_url = "https://doi.org/"
    
    for entry in page_entries:
        ei_document = entry.get('EI-DOCUMENT', {})
        doc_properties = ei_document.get('DOCUMENTPROPERTIES', {})
        
        title = doc_properties.get('TI')

        # Try to get the year from 'YR', if not present, extract from 'SD'
        publication_year = doc_properties.get('YR')
        if not publication_year and 'SD' in doc_properties:
            publication_year = doc_properties['SD'].split(' ')[-1]  # Split by comma and get the last part        
        
        venue = doc_properties.get('SO')
        venue_type = doc_properties.get('DT')

        doi = doc_properties.get('DO')
        link = base_doi_url + doi if doi else None

        aus = ei_document.get('AUS', {})
        authors = aus.get('AU', [])
        author_names = ', '.join([author.get('NAME', '') for author in authors])
        
        extracted.append({
            'Title': title,
            'Publication Year': publication_year,
            'Venue': venue,
            'Venue Type': venue_type,
            'Authors': author_names,
            'Link': link
        })
        
    print(f"Fetched {len(extracted)} results from Engineering Village.")
    return extracted

if __name__ == "__main__":
    query = "Improving Documentation Agility in Safety-Critical Software Systems Development For Aerospace" 
        
    start_index = 0
    PAGE_SIZE = 25
    results = search_engineering_village(query, ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, start=start_index, count=PAGE_SIZE)
 
    data = engineering_village_extract_information(results)

    print(results)
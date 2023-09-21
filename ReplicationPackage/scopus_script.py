import requests

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

# Parsing the search results
# If need modify the script to extract more details as per the requirements.
# The Scopus API returns a lot more information https://dev.elsevier.com/sc_search_views.html
def scopus_extract_information(data):
    extracted = []
    
    for item in data['search-results']['entry']:
        title = item['dc:title']
        
        # Extract the publication year
        cover_date = item.get('prism:coverDate')
        if cover_date and isinstance(cover_date, str):
            publication_year = cover_date.split('-')[0]
        else:
            publication_year = None
        
        journal = item['prism:publicationName']
        
        author_name = item.get('dc:creator', '')
        
        extracted.append({
            'Title': title,
            'Publication Year': publication_year,
            'Journal': journal,
            'Authors': author_name  
        })
    
    return extracted
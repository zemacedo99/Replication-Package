import requests

def search_ieee(query, api_key, start_record=1, max_records=25):
    base_url = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
    
    headers = {
        "Accept": "application/json",
    }
    
    params = {
        "querytext": query,
        "apikey": api_key,
        "start_record": start_record,
        "max_records": max_records
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def extract_ieee_information(data):
    extracted = []
    
    for item in data['articles']:
        title = item.get('title')
        publication_year = item.get('publication_year')
        publisher = item.get('publisher')
        
        # Adjusting extraction based on the observed data structure
        authors_dict = item.get('authors', {})
        authors_list = authors_dict.get('authors', [])
        
        authors_names = [author.get('full_name', '') for author in authors_list if isinstance(author, dict)]
        
        extracted.append({
            'Title': title,
            'Publication Year': publication_year,
            'Journal': publisher,
            'Authors': ', '.join(authors_names)
        })
    
    return extracted


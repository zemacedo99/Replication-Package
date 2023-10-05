import requests

def search_scopus(query, api_key, inst_token, start=0, count=25):
    base_url = "https://api.elsevier.com/content/search/scopus"
    
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key,
        "X-ELS-Insttoken" : inst_token 
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
        venue_type = item['prism:aggregationType']
        scopus_link = next((link['@href'] for link in item['link'] if link['@ref'] == 'scopus'), None)

        
        author_name = item.get('dc:creator', '')
        
        extracted.append({
            'Title': title,
            'Publication Year': publication_year,
            'Venue': journal,
            'Venue Type': venue_type,
            'Authors': author_name,
            'Link': scopus_link
        })
    
    return extracted


# if __name__ == "__main__":
#     ELSEVIER_API_KEY = "c803f556d065be19b3905ccee12adbfa" 
#     ELSEVIER_INST_TOKEN = "35634be89c56c9527b9c35034e7b9cab"
#     query = "Improving Documentation Agility in Safety-Critical Software Systems Development For Aerospace" 
        
#     start_index = 0
#     PAGE_SIZE = 25
#     results = search_scopus(query, ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN, start=start_index, count=PAGE_SIZE)

#     print(results)
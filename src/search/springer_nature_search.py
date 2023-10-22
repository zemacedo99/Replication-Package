import requests

try:
    from config import SPRINGER_API_KEY
except ImportError:
    raise ImportError("config.py not found. Please set up your API key as instructed in README.md")

def search_springer_nature(query, api_key, start=0, count=25):
    print("\nQuerying Springer Nature")

    url = "https://api.springernature.com/metadata/json"
    
    headers = {
        "Accept": "application/json"
    }

    params = {
        "q": query,
        "s": start,
        "p": count,
        "api_key": api_key
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def extract_springer_nature_information(data):
    records = data.get('records', [])
    extracted = []

    for record in records:
        title = record.get('title')
        title = title.replace("\n", " ").replace("\r", "").strip()
        publication_year = record.get('publicationDate', '').split('-')[0]  # Extract year from publicationDate
        venue = record.get('publicationName')
        venue_type = record.get('contentType')

        # Convert the list of authors to a single string, separated by commas
        authors_list = [creator.get('creator') for creator in record.get('creators', [])]
        authors = ', '.join(authors_list)

        # Extract the link value
        link_data = record.get('url', [])
        link = link_data[0].get('value') if isinstance(link_data, list) and len(link_data) > 0 else None

        extracted.append({
            'Title': title,
            'Publication Year': publication_year,
            'Venue': venue,
            'Venue Type': venue_type,
            'Authors': authors,
            'Link': link
        })

    print(f"Fetched {len(extracted)} results from Springer Link.")
    return extracted


if __name__ == "__main__":
    query = "example"
        
    results = search_springer_nature(query, SPRINGER_API_KEY)
    data = extract_springer_nature_information(results)

    for item in data:
        print(item)

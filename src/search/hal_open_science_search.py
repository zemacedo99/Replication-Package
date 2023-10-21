import requests
import bibtexparser


def search_hal_open_science(query, start=0, count=25):
    print("\nQuerying Hal Open Science for BibTeX results")

    url = "https://api.archives-ouvertes.fr/search/"
    
    headers = {
        "Accept": "application/x-bibtex",  # Accepting BibTeX format
    }

    params = {
        "q": query,
        "start": start,
        "rows": count,
        "wt": "bibtex"  # Requesting BibTeX format
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.text
    else:
        response.raise_for_status()


import bibtexparser

def extract_hal_open_science_information(bibtex_data):
    bib_database = bibtexparser.loads(bibtex_data)
    extracted = []

    for entry in bib_database.entries:
        title = entry.get('title', "").replace("{", "").replace("}", "")
        authors = entry.get('author', "").replace(" and ", ", ")
        year = entry.get('year', "")

        # Fields that might differ between entry types
        venue = entry.get('journal', entry.get('booktitle', entry.get('school', entry.get('publisher', "")))).replace("{", "").replace("}", "")
        
        # Identifying venue type based on bibtex entry type
        venue_type_mapping = {
            'inproceedings': 'Conference Proceedings',
            'phdthesis': 'PhD Thesis',
            'article': 'Journal Article',
            'unpublished': 'Unpublished',
            'book': 'Book',
            'incollection': 'Book Chapter',
            'mastersthesis': 'Master\'s Thesis'
        }
        venue_type = venue_type_mapping.get(entry.get('ENTRYTYPE', ""), "")

        link = entry.get('url', "")

        extracted.append({
            'Title': title,
            'Publication Year': year,
            'Venue': venue,
            'Venue Type': venue_type,
            'Authors': authors,
            'Link': link
        })

    print(f"Fetched {len(extracted)} results from Hal Open Science.")
    return extracted


if __name__ == "__main__":
    query = "machine learning"  # Replace with your desired query
        
    results = search_hal_open_science(query)
    # print(results)
    data = extract_hal_open_science_information(results)
    print(data)
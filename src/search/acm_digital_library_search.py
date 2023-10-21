# from crossref.restful import Works
import requests
import json

def search_acm_digital_library(query, start=0, count=25):
    """
    Search the ACM Digital Library using Crossref
    """
    print("\nQuerying ACM Digital Library")

    # Base URL for crossref works endpoint
    url = "https://api.crossref.org/works"
    # works = Works()

    request_parameters = {
        'query.bibliographic': query,
        'filter': 'prefix:10.1145',
        'rows': count,  # Number of results per page
        'offset': start  # Starting position for results
    }

    # Construct the results URL using the request parameters
    # results_url = works.url + "?" + "&".join([f"{k}={v}" for k, v in request_parameters.items()])
    # response = requests.get(results_url)

    response = requests.get(url, params=request_parameters)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status() 


def extract_acm_digital_library_information(response_json):
    """
    Extract data from the Crossref API response JSON
    """
    extracted = []

    if 'message' in response_json and 'items' in response_json['message']:
        for entry in response_json['message']['items']:
            title = entry.get('title', [None])[0]  
            # doi = entry.get('DOI')

            # Convert publication year to int
            try:
                publication_year = int(entry.get('published-print', {}).get('date-parts', [None])[0][0])
            except (TypeError, ValueError, IndexError):
                publication_year = None

            # Convert authors list to a comma-separated string
            authors_list = [author.get('given', '') + ' ' + author.get('family', '') for author in entry.get('author', [])]
            authors = ', '.join(authors_list)

            venue = entry.get('container-title', [None])[0]  # Assuming container-title is a list
            venue_type = entry.get('type')  # Extracting venue type
            link = entry.get('link', [{}])[0].get('URL', None)  # Extracting the primary link (usually a PDF)
            # source = entry.get('source')  # Extracting the source (e.g., Crossref)

            extracted_data = {
                'Title': title,
                'Publication Year': publication_year,
                'Venue': venue,
                'Venue Type': venue_type,
                'Authors': authors,
                'Link': link
                # 'DOI': doi
                # 'Source': source 
            }
            
            extracted.append(extracted_data)

    print(f"Fetched {len(extracted)} results from ACM Digital Library.")
    return extracted

def write_pretty_json_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    query = '("Agile" OR "Agility" OR "Scrum" OR "Kanban" OR "Scrumban" OR "SafeScrum" OR "AgileSafe" OR "Agile Safe" OR "XP" OR "Extreme Programming" OR "Large-Scale Scrum" OR "LeSS" OR "Scrum@Scale" OR "SaS" OR "Disciplined Agile Delivery" OR "DAD") AND ("aerospace" OR "avionic" OR "avionics" OR "aviation" OR "aeronautic" OR "aeronautics" OR "aeronautical") AND ("Safety" OR "Safety-Critical" OR "Safety Critical" OR "Safety-Critical Systems" OR "Safety Critical Systems" OR "High Integrity" OR "High Integrity Systems" OR "HIS" OR "Safety Integrity" OR "Safety-Systems" OR "Safety Systems") AND ("ARP4761" OR "ARP 4761" OR "ARP4754" OR "ARP 4754" OR "ARP4754A" OR "ARP 4754A" OR "DO-178" OR "DO 178" OR "DO178" OR "DO-178C" OR "DO 178C" OR "DO178C" OR "DO-178B" OR "DO 178B" OR "DO178B" OR "DO 331" OR "DO331" OR "DO-331" OR "DO-297" OR "DO 297" OR "DO297")'
    data = search_acm_digital_library(query)
    write_pretty_json_to_file(data,"output.json")
    result = extract_acm_digital_library_information(data)
    print(result)


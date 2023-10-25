import requests
import sys
import os
root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_directory)
from data.data_process import process_and_save_result
from utils import write_pretty_json_to_file

try:
    from config import ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN
except ImportError:
    raise ImportError("config.py not found. Please set up your API key as instructed in README.md")

def search_science_direct_metadata(query, api_key, inst_token, start=0, count=25):
    print("\nQuerying Science Direct Metadata API")

    url = "https://api.elsevier.com/content/metadata/article"
    
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key,
        "X-ELS-Insttoken": inst_token
    }

    params = {
        "query": query,
        "start": start,
        "count": count,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def extract_science_direct_metadata_information(data):
    entries = data.get('search-results', {}).get('entry', [])
    extracted = []

    for entry in entries:
        title = entry.get('dc:title')
        author_list = entry.get('dc:creator', [])
        authors = ", ".join([author.get('$') for author in author_list])
        publication_year = entry.get('prism:coverDate', '').split('-')[0]
        venue = entry.get('prism:publicationName')
        venue_type = entry.get('pubType')
        link = entry.get('prism:url')

        extracted.append({
            'Title': title,
            'Publication Year': publication_year,
            'Venue': venue,
            'Venue Type': venue_type,
            'Authors': authors,
            'Link': link
        })

    print(f"Fetched {len(extracted)} results from Science Direct Metadata API.")
    return extracted

if __name__ == "__main__":
    # https://dev.elsevier.com/sd_article_meta_tips.html for Field Restrictions
    QUERY = 'key("Agile" OR "Agility" OR "Scrum" OR "Kanban" OR "Scrumban" OR "SafeScrum" OR "AgileSafe" OR "Agile Safe" OR "XP" OR "Extreme Programming" OR "Large-Scale Scrum" OR "LeSS" OR "Scrum@Scale" OR "SaS" OR "Disciplined Agile Delivery" OR "DAD" OR "aerospace" OR "avionic" OR "avionics" OR "aviation" OR "aeronautic" OR "aeronautics" OR "aeronautical" OR "Safety" OR "Safety-Critical" OR "Safety Critical" OR "Safety-Critical Systems" OR "Safety Critical Systems" OR "High Integrity" OR "High Integrity Systems" OR "HIS" OR "Safety Integrity" OR "Safety-Systems" OR "Safety Systems" OR "ARP4761" OR "ARP 4761" OR "ARP4754" OR "ARP 4754" OR "ARP4754A" OR "ARP 4754A" OR "DO-178" OR "DO 178" OR "DO178" OR "DO-178C" OR "DO 178C" OR "DO178C" OR "DO-178B" OR "DO 178B" OR "DO178B" OR "DO 331" OR "DO331" OR "DO-331" OR "DO-297" OR "DO 297" OR "DO297")'

        
    results = search_science_direct_metadata(QUERY, ELSEVIER_API_KEY, ELSEVIER_INST_TOKEN)
    print(results)
    write_pretty_json_to_file(results,"output.json")
    data = extract_science_direct_metadata_information(results)
    process_and_save_result(data, "Science Direct Metadata", "data_results")

    for item in data:
        print(item)
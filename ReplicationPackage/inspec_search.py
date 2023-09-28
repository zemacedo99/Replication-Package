import requests

def search_engineering_village(query, api_key, start=0, count=25):

    url = "https://api.elsevier.com/content/ev/results"
    
    params = {
        "database": "i",          
        "query": query,
        "offset": start,
        "pageSize": count,
    }

    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key,
        "X-ELS-Insttoken" : "35634be89c56c9527b9c35034e7b9cab"
    }

    

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    

if __name__ == "__main__":
    API_KEY = "c803f556d065be19b3905ccee12adbfa"
    query = "scrum" 
        
    start_index = 0
    PAGE_SIZE = 25
    results = search_engineering_village(query, API_KEY, start=start_index, count=PAGE_SIZE)

    print(results)
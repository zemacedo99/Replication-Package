# Replication Package

This project aims to retrieve scholarly article information from multiple sources like Scopus, IEEE Xplore, and Engineering Village (Inspec). It efficiently extracts details such as titles, authors, publication years, venues, and links to the articles.

## Setup and Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/zemacedo99/Thesis.git
    cd replication-package/
    ```

2. **Setup API Keys**:
    - Obtain your API keys from:
      - [Scopus API Provider](LINK_TO_SCOPUS_PROVIDER)
      - [IEEE Xplore API Provider](LINK_TO_IEEE_PROVIDER)
      - [Engineering Village API Provider](LINK_TO_EV_PROVIDER)
    - Rename `config_template.py` to `config.py`.
    - Open `config.py` and replace placeholders (e.g., `YOUR_SCOPUS_API_KEY_HERE`, `YOUR_IEEE_API_KEY_HERE`, `YOUR_EV_API_KEY_HERE`) with the respective API keys.
   
   **Note**: The `config.py` file contains sensitive information (your API keys) and is gitignored to ensure it isn't accidentally committed to the repository. Always ensure you don't manually add this file to version control.

3. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**:
    ```bash
    python replication_package.py
    ```

## Features

- **Scopus Integration**: Extracts article information including titles, publication years, venues, authors, and article links from Scopus.
- **IEEE Xplore Integration**: Retrieves article details from the IEEE digital library.
- **Engineering Village (Inspec) Integration**: Gathers scholarly article information from the Engineering Village database.
- **Error Handling**: Gracefully handles potential issues during data retrieval and extraction, ensuring consistent results.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. As the project interacts with various data sources, ensure any modifications don't disrupt the existing integrations.


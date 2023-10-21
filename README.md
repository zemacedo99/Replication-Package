# Replication Package

This project aims to retrieve scholarly article information from a variety of sources including Scopus, IEEE Xplore, Engineering Village (Inspec), Science Direct, HAL Open Science, and the ACM Digital Library via Crossref. It allows for efficient extraction of details such as titles, authors, publication years, venues, venue types, and links to the articles. Furthermore, it provides functionality to create queries from a CSV containing search terms and to visualize the processed data.

## Prerequisites

### Installing Python

Before setting up this project, you need to have Python installed on your system. If you haven't already installed Python, follow these instructions:

#### Windows:
1. Visit the [official Python website](https://www.python.org/downloads/windows/).
2. Download the latest version of Python for Windows.
3. Run the installer. Make sure to check the box that says "Add Python to PATH" during installation. This will make it easier to run Python from the command line.

#### macOS:
1. Visit the [official Python website](https://www.python.org/downloads/mac-osx/).
2. Download the latest version of Python for macOS.
3. Follow the installation instructions.

#### Linux:
Most Linux distributions come with Python pre-installed. If not, you can use your distribution's package manager to install Python. For example, on Ubuntu:

```bash
sudo apt update
sudo apt install python3
```

### Installing pip

`pip` is the package installer for Python. It usually comes pre-installed with Python installations. However, if you need to install it:

#### Windows or macOS:

Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) to a folder on your computer. Open a command prompt from that folder and run:

```bash
python get-pip.py
```

#### Linux:

Using your distribution's package manager, you can install pip. For example, on Ubuntu:

```bash
sudo apt install python3-pip
```

## Setup and Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/zemacedo99/Replication-Package.git
    ```

2. **Navigate to the Project Directory**:
    ```bash
    cd Replication-Package
    ```

3. **Virtual Environment Setup (Windows)**

    It's recommended to use a virtual environment to avoid package conflicts between projects. If you're on Windows, here's how to set it up:

    1. Create a virtual environment: 
        ```bash
        python -m venv myenv
        ```
    2. Activate the virtual environment:
        ```bash
        .\myenv\Scripts\Activate
        ```
    3. When done, deactivate with:
        ```bash
        deactivate
        ```

4. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Setup API Keys**:
    - Obtain your API keys from:
      - [IEEE Xplore API Provider](https://developer.ieee.org/member/register)
      - [Springer Nature API Provider](https://dev.springernature.com/)
      - [Elsevier API Provider](https://dev.elsevier.com/apikey/manage) *Works for Scopus, Engineering Village (Inspec) and ScienceDirect*

6. **Navigate to the source code**:
    ```bash
    cd src/
    ```
    - Rename `config_template.py` inside the search folder to `config.py`.
    - Open `config.py` and replace placeholders (e.g., `YOUR_SCOPUS_API_KEY_HERE`, `YOUR_IEEE_API_KEY_HERE`, `YOUR_EV_API_KEY_HERE`) with the respective API keys.
   
   **Note**: The `config.py` file contains sensitive information (your API keys) and is gitignored to ensure it isn't accidentally committed to the repository. Always ensure you don't manually add this file to version control.

7. **Run the Application**:
    ```bash
    python replication_package.py
    ```
8. **Troubleshooting**:
    - Ensure you're using a compatible version of Python and pip. Check using `python --version` and `pip --version`.
    - Consider using a virtual environment like `venv` to avoid package conflicts.
    - If a specific package causes an error, try installing it separately using `pip install <package-name>`.
    - For SSL or proxy issues, try: `pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host=files.pythonhosted.org -r requirements.txt`.
    - If all else fails, check the internet connection, ensure [PyPI](https://pypi.org/) is accessible, and look for specific error messages for more detailed guidance.
    - **Institutional Restrictions:** If you're unable to run the application due to restrictions from your institution's internet connection or VPN, consider obtaining an institutional token from the API Provider support.
    
## Features

- **Multiple Data Sources Integration:** 
    - **Scopus** 
    - **IEEE Xplore** 
    - **Engineering Village (Inspec)** 
    - **Science Direct** 
    - **HAL Open Science** 
    - **ACM Digital Library via Crossref** 

- **CSV-based Queries:** The ability to create a search query from a CSV file with terms, streamlining the process of bulk or complex searches.

- **Data Visualization:** After gathering and processing the data, the project offers functionality for its visualization, providing insights and easy-to-understand graphics.

- **Error Handling:** Gracefully handles potential issues during data retrieval and extraction, ensuring consistent results.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. As the project interacts with various data sources, ensure any modifications don't disrupt the existing integrations.


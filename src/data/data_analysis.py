import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def publication_year_distribution(df):
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Publication Year', palette="viridis")
    plt.title('Publication Year Distribution')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def publication_venue_distribution(df):
    plt.figure(figsize=(12, 6))
    top_10_venues = df['Venue'].value_counts().index[:10]  # Get the top 10 venue names
    sns.countplot(data=df, y='Venue', palette="viridis", order=top_10_venues)
    plt.title('Top 10 Publication Venue Distribution')
    plt.tight_layout()
    plt.show()

def publication_venue_type_distribution(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, y='Venue Type', palette="viridis", order=df['Venue Type'].value_counts().index)
    plt.title('Publication Venue Type Distribution')
    plt.tight_layout()
    plt.show()

def publication_source_distribution(df):

    # Filter out sources with a comma
    filtered_df = df[df['Source'].apply(lambda x: ',' not in str(x))]

    # Get the order of sources from most frequent to least frequent
    order_sources = filtered_df['Source'].value_counts().index

    plt.figure(figsize=(8, 6))
    sns.countplot(data=filtered_df, y='Source', palette="viridis", order=order_sources)
    plt.title('Publication Source Distribution')
    plt.tight_layout()
    plt.show()

def publication_authors_distribution(df):
    # Split and flatten the authors list
    all_authors = df['Authors'].str.split(',').explode()

    # Remove any leading or trailing spaces that might be present after splitting
    all_authors = all_authors.str.strip()

    # Get the top 10 authors from most frequent to least frequent
    top_authors_counts = all_authors.value_counts().head(10)

    # Plotting using barplot instead of countplot
    plt.figure(figsize=(10, 8))
    sns.barplot(y=top_authors_counts.index, x=top_authors_counts.values, palette="viridis")
    plt.title('Top 10 Publication Authors Distribution')
    plt.tight_layout()
    plt.show()

def data_analysis(filename):
    # Load the CSVs
    df = pd.read_csv(filename)

    publication_year_distribution(df)

    publication_venue_distribution(df)

    publication_venue_type_distribution(df)

    publication_source_distribution(df)

    publication_authors_distribution(df)

if __name__ == "__main__":
    data_analysis("data_results/unique_results.csv")
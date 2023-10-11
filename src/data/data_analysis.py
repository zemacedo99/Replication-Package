import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def data_analysis(filename):
    # Load the CSVs
    df = pd.read_csv(filename)

    # Publication Year Distribution
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Publication Year', palette="viridis")
    plt.title('Publication Year Distribution')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Publication Venue Distribution
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, y='Venue', palette="viridis", order=df['Venue'].value_counts().index)
    plt.title('Publication Venue Distribution')
    plt.tight_layout()
    plt.show()

    # Publication Source Distribution
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, y='Source', palette="viridis")
    plt.title('Publication Source Distribution')
    plt.tight_layout()
    plt.show()

    # Publication Venue Type Distribution
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, y='Venue Type', palette="viridis", order=df['Venue Type'].value_counts().index)
    plt.title('Publication Venue Type Distribution')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data_analysis("data_results/unique_results.csv")
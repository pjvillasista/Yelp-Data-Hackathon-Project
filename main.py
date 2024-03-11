import json
import pandas as pd
from textblob import TextBlob

def json_to_csv(input_file_path, output_file_path):
    """
    Converts a JSON file to a CSV file, making the data easier to manipulate and analyze using pandas.
    
    Args:
        input_file_path (str): Path to the input JSON file.
        output_file_path (str): Desired path for the output CSV file.
    """
    data = []
    # Open the JSON file and load each line (each line is a JSON object) into a Python dictionary.
    with open(input_file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    
    # Convert the list of dictionaries to a pandas DataFrame and save it as a CSV file.
    df = pd.DataFrame(data)
    df.to_csv(output_file_path, index=False)

def sentiment_analysis(text):
    """
    Performs sentiment analysis on a given piece of text, returning the sentiment category,
    its polarity, and subjectivity score.
    
    Args:
        text (str): The text to analyze.
    
    Returns:
        tuple: Contains sentiment label ("Positive", "Negative", "Neutral"), polarity, and subjectivity.
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    # Determine sentiment label based on polarity score.
    sentiment_label = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
    return sentiment_label, polarity, analysis.sentiment.subjectivity

# Specify paths to the JSON datasets and the locations where the CSV conversions will be stored.
review_json_path = "/content/drive/MyDrive/01_RUG/raw_data/yelp_academic_dataset_review.json"
review_csv_path = "drive/MyDrive/01_RUG/staging_data/yelp_reviews.csv"
user_json_path = "/content/drive/MyDrive/01_RUG/raw_data/yelp_academic_dataset_user.json"
user_csv_path = "drive/MyDrive/01_RUG/staging_data/yelp_users.csv"
business_json_path = "/content/drive/MyDrive/01_RUG/raw_data/yelp_academic_dataset_business.json"
business_csv_path = "drive/MyDrive/01_RUG/staging_data/yelp_business.csv"

# Convert the Yelp JSON datasets to CSV for easier manipulation.
# This is particularly useful for large datasets, as CSV files are more memory efficient and faster to process with pandas.
json_to_csv(review_json_path, review_csv_path)
json_to_csv(user_json_path, user_csv_path)
json_to_csv(business_json_path, business_csv_path)

# Load the business data from the newly created CSV file.
# Filtering and operations on this data can be applied as needed.
business_df = pd.read_csv(business_csv_path)

# Load review data, ensuring we rename columns as necessary for clarity or to avoid conflicts.
review_df = pd.read_csv(review_csv_path)
review_df.rename(columns={'stars': 'review_stars'}, inplace=True)

# Join business and review data on the 'business_id' field to create a comprehensive dataset.
# This allows for richer analysis, like understanding reviews in the context of business attributes.
business_reviews_df = pd.merge(business_df[business_df['state'] == 'PA'][business_df['is_open'] == 1],
                                review_df, on='business_id', how='inner')
business_reviews_df.to_csv('drive/MyDrive/01_RUG/staging_data/yelp_reviews_with_business.csv', index=False)

# Prepare the text data for sentiment analysis by ensuring it's in string format.
business_reviews_df['text'] = business_reviews_df['text'].astype(str)

# Apply sentiment analysis to each review text.
# This adds valuable dimensions to the data, allowing for sentiment-based categorization and analysis.
business_reviews_df[['sentiment', 'polarity', 'subjectivity']] = business_reviews_df['text'].apply(
    lambda x: pd.Series(sentiment_analysis(x)))
business_reviews_df.to_csv('drive/MyDrive/01_RUG/staging_data/yelp_reviews_with_business_sentiment.csv', index=False)

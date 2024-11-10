import pandas as pd
from sklearn.model_selection import train_test_split
import time
from utils.kafka import kafka_producer
import six
  
def selected_features(df=None):
    if df is None:
        df = pd.read_csv("../data/happiness_dataset_merged.csv")
        df['continent_numeric'] = pd.factorize(df['continent'])[0]
        
    # Select numerical columns and drop unwanted columns
    X = df.select_dtypes(include=['float64', 'int64']).drop(columns=["happiness_rank", "happiness_score", "year", "generosity"], errors='ignore')
    y = df['happiness_score']
    
    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Return the test set portion of the original DataFrame, as per `y_test` indices
    return df.loc[y_test.index]

if __name__ == "__main__":
    # Load dataset and apply selected features function
    happiness_df = selected_features()
    
    # Iterate through rows of the test set in the original DataFrame and process them
    for index, row in happiness_df.iterrows():
        kafka_producer(row)
        time.sleep(1)
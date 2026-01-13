import logging
import pandas as pd
import os

logger = logging.getLogger(__name__)

def load_dataset():
    """Loads the players dataset from the csv file.

    Returns:
        df: the players full dataset
    """
    logger.info("Importing the players data.")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../data/players_22.csv')   
    df = pd.read_csv(data_path)
    return df

def cleanup_dataframe(df):
    """Cleans up the dataframe

    Args:
        df (DataFrame): the players full dataset
    """
    if df.isna().any().any():
        logger.info("Null values present in dataset, filling them with zeros.")
        df.fillna(0, inplace=True)
    # df.drop(columns=['short_name','club_position'], inplace=True)
    df.drop(columns=df.select_dtypes(exclude='number').columns, inplace=True)

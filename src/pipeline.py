import pandas as pd
import numpy as np
import os
import time

from sentence_transformers import SentenceTransformer, util

def run_pipline(raw_data_path: str, preprocessed_data_path: str, embeddings_path: str):
    #setup
    print("Lounching the pipline")

    time_start = time.time()

    # 1. Extract
    print(f"Loading data from {raw_data_path}...")
    raw_dataset = pd.read_csv(raw_data_path)
    initial_shape = raw_dataset.shape

    # 2. Transform
    print(f"Filtering Data Columns...")
    clean_dataset = raw_dataset[['Release Year', 'Title', 'Genre', 'Plot']]
    print(f"Initial nb columns: {initial_shape[1]}, new nb columns: {clean_dataset.shape[1]}")

    print(f"Cleaning the dataset...")
    clean_dataset = clean_dataset.dropna()
    clean_dataset.reset_index(drop=True, inplace=True)

    print(f"Initial nb rows: {initial_shape[0]}, Nb rows after cleaning: {clean_dataset.shape[0]}")

    # Embeddings / ML
    model_name = "sentence-transformers/msmarco-bert-base-dot-v5"
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    print("Generating plot embeddings for all movies, this might take few minutes...")
    plots = clean_dataset["Plot"].tolist()
    embeddings = model.encode(plots, show_progress_bar=True)

    # Load
    print("Saving processed data and embeddings...")
    # ensuring target dir exists
    os.makedirs(os.path.dirname(preprocessed_data_path), exist_ok=True)

    clean_dataset.to_csv(preprocessed_data_path, index=False)
    np.save(embeddings_path, embeddings)

    elapsed_time = int(time.time() - time_start) 

    minutes = elapsed_time // 60
    secs = elapsed_time % 60
    print(f'Pipline completed in {minutes:02}min{secs:02}')
    return elapsed_time

if __name__ == "__main__":
    # call the pipline function
    RAW_CSV = "data/raw/wiki_movie_plots_deduped.csv"
    CLEAN_CSV = "data/preprocessed/clean_dataset.csv"
    EMBEDDINGS_ARRAY = "data/preprocessed/plot_embeddings.npy"

    run_pipline(
        raw_data_path=RAW_CSV,
        preprocessed_data_path=CLEAN_CSV,
        embeddings_path=EMBEDDINGS_ARRAY
    )
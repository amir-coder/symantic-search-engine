import pandas as pd
import numpy as np
import os
import time

from sentence_transformers import SentenceTransformer, util

class SearchEngine:
    def __init__(self, datapath: str, embdedings_path:str):
        """
        Initializing the seach engine by loading the precomputed embeddings into memory.
        """

        print("Booting up the search engine...")

        start = time.time()

        #Loading the preprocessed data
        self.df = pd.read_csv(datapath)

        #Loading the precomputed embeddings
        self.embeddings = np.load(embdedings_path)

        #Loading the model
        model_name = "sentence-transformers/msmarco-bert-base-dot-v5"
        self.model = SentenceTransformer(model_name)

        elapsed_time = int(time.time() - start)
        minutes = elapsed_time // 60
        secs = elapsed_time % 60

        print(f"Search engine initialized in {minutes} minutes and {secs} seconds.")
        

    def search(self, filters: dict):
        """
        Search for a movie given plot description and filters
        """
        k = filters.get('k', 10) #default k value is 10
        if k <= 0:
            return []
        
        # Metadata filtering
        mask = pd.Series(True, index=self.df.index)
        if 'start_release_year' in filters and filters['start_release_year'] is not None:
            mask &= self.df['Release Year'] >= filters['start_release_year']
        
        if 'end_release_year' in filters and filters['end_release_year'] is not None:
            mask &= self.df['Release Year'] <= filters['end_release_year']
        
        if 'genre' in filters and filters['genre'].lower() != 'all':
            mask &= self.df['Genre'] == filters['genre']
        
        filtered_df = self.df[mask]

        if filtered_df.empty:
            return []
        
        # Semantic search
        plot_query = filters.get('plot', '').strip()

        if not plot_query:
            return self.__format_results(filtered_df.head(k))
        
        # vector search

        valide_indices = filtered_df.index.tolist()

        filtered_embeddings = self.embeddings[valide_indices]
        query_embedding = self.model.encode(plot_query)

        scores = util.dot_score(query_embedding, filtered_embeddings)[0].cpu().numpy()

        ranked_df = filtered_df.copy()

        ranked_df['Score'] = scores

        ranked_df = ranked_df.sort_values(by='Score', ascending=False)

        return self.__format_results(ranked_df.head(k))

    def __format_results(self, df: pd.DataFrame):
        """"Helper method to format the search results into a list of dicts for the API."""
        results = []
        for _, row in df.iterrows():

            movie_data = {
                'Title': row['Title'],
                'Genre': row['Genre'],
                'Release Year': row['Release Year']
            }

            if "Score" in row:
                movie_data['Score'] = round(float(row['Score']), 4)
            
            results.append(movie_data)
        return results
if __name__ == "__main__":
    search_engine = SearchEngine(
        datapath="data/preprocessed/clean_dataset.csv",
        embdedings_path="data/preprocessed/plot_embeddings.npy"
    )

    query = {
        'plot': "A young cab driver and aspiring singer becomes embroiled in a plot to kidnap a monkey that has memorized a scientific formula with the potential to destroy the world.",
        'genre': 'comedy',
        'start_release_year': 1980,
        'end_release_year': 2000,
        'k': 10,
    }

    print("Running a sample search query...")
    results  = search_engine.search(query)
    for result in results:
        print(result)
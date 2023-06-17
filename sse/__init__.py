
import pandas as pd
from models import Model

class SSE():

    def __init__(self, database_filename: str) -> None:
        # loading data from disk
        self.df = pd.read_csv("./data/" + database_filename)
        self.models = {}
    

    def read_model(self, model_name: str):
        #check if model is not already loaded
        if model_name in self.models:
            return self.models[model_name]
        else:
            self.models[model_name] = Model(model_name)
            return self.models[model_name]
    
    def filter_movies(self,filters):
        """
        filters: dict
            start_release_year: int
            end_release_year: int
            genre: str
        """
        result = self.df[['Release Year', 'Title', 'Genre', 'Plot']].copy()

        #year based selection
        if 'start_release_year' in filters:
            result = result[result['Release Year'] >= filters['start_release_year']]
        if 'end_release_year' in filters:
            result = result[result['Release Year'] <= filters['end_release_year']]
        
        #Genre based selection
        if 'genre' in filters:
            result = result[result['Genre'] == filters['genre']]
        return result
    
    def format_search_result(self, k: int, filtered_movies):
        #Truncating
        filtered_movies = filtered_movies[['Title', 'Genre', 'Release Year']].head(k)
        #Reformatting
        return [{'Title': x[0], 'year': x[2], 'genre': x[1]} for x in filtered_movies.values]
    
    def search(self,filter):

        """ Search for a movie given plot description and filters
        filter: dict
            k: max number of suggestions
            plot: plot description
            genre: movie genre
            start_release_year: an integer
            end_release_year: an integer
        Returns:
            The sum of the two arguments
        """
        if not 'k' in filter:
            filter['k']=10 #default k value is 10
            print(filter['k'])
        
        if filter['k']<=0:
            return [] #in case k is negative or zero
        
        #filtering data
        filtered_movies = self.filter_movies(filter)

        if len(filtered_movies.values) ==0:
            return [] #in case there are no movies matching the filter
        
        if not 'plot' in filter or filter['plot'] == '':
            return self.format_search_result(filter['k'],filtered_movies)
        
        #initialy we use msmarco-bert-base-dot-v5 model only, this code can be generalized later
        model = self.read_model(model_name='msmarco-bert-base-dot-v5')

        #calculating similarity score between plot and filtered movies
        ss = model.similarity(plot = filter['plot'], corpus = filtered_movies['Plot'].values)

        #appending to df
        filtered_movies['Score'] = ss
        
        #Similarity Score based Sorting 
        filtered_movies.sort_values('Score', ascending=False, inplace=True) 

        #sorting, truncating and reformatting results
        return self.format_search_result(filter['k'],filtered_movies)
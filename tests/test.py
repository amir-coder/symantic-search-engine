import unittest

from sse import SSE

class TestSSE(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.sse = SSE(database_filename='wiki_movie_plots_deduped.csv')

    def test_release_year_order(self):
        """
        Test case: end_release_year < start_release_year
        """
        filter= {
            'k': 10,
            'plot': 'abc',
            'genre': 'abc',
            'start_release_year': 1980,
            'end_release_year': 1990,
        }
        result = self.sse.search(filter)
        self.assertEqual(len(result), 0, 'Should be empty')
    
    def test_k_empty(self):
        """
        Test case: no k value
        """
        filter= {
            'genre': 'comedy',
            'start_release_year': 1980,
            'end_release_year': 1990,
        }
        result = self.sse.search(filter)
        self.assertGreater(len(result), 0, 'Should not be empty')
    
    def test_k_not_positive(self):
        """
        Test case: k<=0 
        """
        filter= {
            'k': -10,
            'plot': 'abc',
            'genre': 'abc',
            'start_release_year': 1980,
            'end_release_year': 1990,
        }
        result = self.sse.search(filter)
        self.assertEqual(len(result), 0, 'Should be empty')
    
    def test_plot_empty(self):
        """
        Test case: no plot
        """
        filter= {
            'k': 10,
            'genre': 'abc',
            'start_release_year': 1980,
            'end_release_year': 1990,
        }
        result = self.sse.search(filter)
        self.assertLessEqual(len(result), filter['k'])
    
    def test_plot_full(self):
        """
        Test case: plot exists in movie history
        """
        filter= {
            'k': 10,
            'plot': 'A young cab driver and aspiring singer becomes embroiled in a plot to kidnap a monkey that has memorized a scientific formula with the potential to destroy the world.',
            'genre': 'comedy',
            'start_release_year': 1980,
            'end_release_year': 1982,
        }
        result = self.sse.search(filter)
        self.assertDictEqual(
            result[0], 
            {
                "Title" : "Die Laughing",
                "year" : 1980,
                "genre" : "comedy"
            },
            'First value must be equal'
        )
    
    def test_genre_empty(self):
        """
        Test case:no genre value
        """
        filter= {
            'k': 10,
            'plot': 'A young cab driver and aspiring singer becomes embroiled in a plot to kidnap a monkey that has memorized a scientific formula with the potential to destroy the world.',
            'start_release_year': 1980,
            'end_release_year': 1982,
        }
        result = self.sse.search(filter)
        self.assertDictEqual(
            result[0], 
            {
                "Title" : "Die Laughing",
                "year" : 1980,
                "genre" : "comedy"
            },
            'First value must be equal'
        )

if __name__ == '__main__':
    unittest.main()
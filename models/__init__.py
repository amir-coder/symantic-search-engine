from keras.models import load_model
from sentence_transformers import SentenceTransformer, util
class Model():
    """
    Model class:
    name: str
    read a sentence-transformer model
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.model = SentenceTransformer(name)
    

    def similarity(self, plot: str, corpus: list):
        plot_embedding = self.model.encode(plot, convert_to_tensor=True)
        search_space_embeddings = self.model.encode(corpus, convert_to_tensor=True)
        result = util.dot_score(plot_embedding, search_space_embeddings)[0].cpu()
        return result
    

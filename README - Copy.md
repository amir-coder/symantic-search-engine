# Data Scientist intern test 2023

## Context:

Semantic textual similarity is the building block for modern search-engines, through which we can retrieve a piece of information which is selected as the returned value with respect to its similarity to the input representation of the Query.

## Required:

Implement a semantic search engine for movies using pretrained [BERT](https://arxiv.org/pdf/1810.04805.pdf) or [Sentence-BERT](https://arxiv.org/pdf/1908.10084.pdf) for text representation. The desired pipeline should be able to retrieve the top K movies, given the following inputs:

- K :int (number of movies to suggest, sorted by search score)
- Plot :str (description of the plot)
- Genre :str (Optional argument but must be included in the search function)
- Release year : int

The output of the search (The retrieved movie) has to be in the following Python dictionary structure:

```console
{
    Title : "MOVIE TITLE",
    year : "RELEASE YEAR",
    genre : "MOVIE GENRE"
}
```

## Notes

- The project structure is up to the candidate to decide. Still, make sure you follow good pythonic structure (avoid using notebooks).
- Make sure your code is well organized, commented, and attache any necessary papers if any are used.
- DO NOT copy existing code, even with major changes, this test is designed for the sole purpose of evaluating your Data Science/Machine Learning problem solving skills.
- Functionality of the implemented solution, code quality, repository structure are crucial to the evaluation process. Make sure your solution is well designed, documented, and easily reproducible.
- Additional features and experiments are encouraged ! show us your muscles !

## Important

- Don't share this test with anyone.
- Create a new branch and push your changes to it (use git cli and make sure to commit with meaningful comments).
- Make sure not to exceed the deadline.

## Database/Dataset:

The [Wikipedia Movie Plots](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots) is to be used as a database. The solution is mainly testing your semantic search engine to retrieve movies from this dataset. So dataset parsing, cleaning, and structuring will play a big role in the success of your solution.

## Pretrained BERT-model:

The candidate is free to use any BERT-based model from HuggingFace, we strongly suggest [bert-base-uncased](https://huggingface.co/bert-base-uncased). Pay attention to the way you use the output of this model.

## References:

- [BERT: Pre-training of Deep Bidirectional T](https://arxiv.org/pdf/1810.04805.pdf)
- [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/pdf/1908.10084.pdf)
- [The Good Research Code Handbook](https://goodresearch.dev/) ;)

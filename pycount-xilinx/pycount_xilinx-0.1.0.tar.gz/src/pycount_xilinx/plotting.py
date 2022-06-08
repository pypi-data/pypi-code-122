import matplotlib.pyplot as plt 

def plot_words(words_count, n=10):
    """Plot a bar chart of word counts

    Parameters
    ----------
    word_counts: collections.Counter
        Counter object of word counts.
    n: int, optional
        Plot the top n words. By default, 10.

    Returns
    -------
    matplotlib.container.BarContainer
        Bar chart of word counts.

    Examples
    --------
    >>> from pycount_xilinx.pycounts import count_words
    >>> from pycount_xilinx.plotting import plot_words
    >>> counts = count_words('text.txt')
    >>> plot_words(counts)
    """
    top_n_words = words_count.most_common(n)
    words, count = zip(*top_n_words)
    fig = plt.bar(range(n), count)
    plt.xticks(range(n), labels=words, rotation=45)
    plt.xlabel('Word')
    plt.ylabel('Count')
    return fig

#%pip install pyembeds-sssa
print('='*5, 'TESTING AUTOTESTING ASSIGNMENT', '='*5)
from pyembeds.testing.auto_testing import run_and_test
# Simple Test
def asgn01_01Hello_world():
    print('Ciao, mondo!')
run_and_test([], ["Ciao, mondo!"], asgn01_01Hello_world)


print('='*5, 'TESTING LOAD CAPYTHONE ASSIGNMENT DATA', '='*5)
from pyembeds.data.load_data import load_capythone_data
data = load_capythone_data()
reviews = data['reviews']
positive_word = data['positive_word']
negative_word = data['negative_word']

print('reviews loaded:', len(reviews))
print('positive_word loaded:', len(reviews))
print('negative_word loaded:', len(negative_word))

from pyembeds.data.load_data import load_wordcloud_ita_data
print('='*5, 'TESTING LOAD WORDCLOUD ASSIGNMENT DATA', '='*5)
data = load_wordcloud_ita_data()
text = data['manzoni']
stop_words = data['stopwords_italian']
print('text len loaded:', len(text))
print('stopwords_italian loaded:', len(stop_words))

print('='*5, 'TESTING VISUALIZATION FUNCTION', '='*5)
from pyembeds.vis.utils import draw_euclidean_distance
draw_euclidean_distance((20, 10), (5, 0), (5, 20))





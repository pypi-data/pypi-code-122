from konlpy.tag import Mecab
from tensorflow.keras.preprocessing.text import Tokenizer

class Korean_tokenizer(Tokenizer):
      """
      This tokenizer object is customized for korean with 
      keras tensorflow.keras.preprocessing.text.Tokenizer.
      """

      def __init__(self,
        num_words=None,
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
        split=" ",
        char_level=False,
        oov_token=None,
        analyzer=None,
        stopwords=None,
        **kwargs):

          '''
          super init list.
          
          self.word_counts = collections.OrderedDict()
          self.word_docs = collections.defaultdict(int)
          self.filters = filters
          self.split = split
          self.lower = lower
          self.num_words = num_words
          self.document_count = document_count
          self.char_level = char_level
          self.oov_token = oov_token
          self.index_docs = collections.defaultdict(int)
          self.word_index = {}
          self.index_word = {}
          self.analyzer = analyzer
          '''
          super().__init__()
          self._mecab = Mecab()
          self.stopwords = stopwords
          
      def fit_on_texts(self, texts):


        for text in texts:
            self.document_count += 1
            if self.char_level or isinstance(text, list):
                seq = text
            else:
                if self.stopwords is None:
                    seq = self._mecab.morphs(text)
                    seq = [word for word in seq if not word in self.filters]
                else:
                    seq = self._mecab.morphs(text)
                    seq = [word for word in seq if not word in self.stopwords]
                    seq = [word for word in seq if not word in self.filters]
            for w in seq:
                if w in self.word_counts:
                    self.word_counts[w] += 1
                else:
                    self.word_counts[w] = 1
            for w in set(seq):
                # In how many documents each word occurs
                self.word_docs[w] += 1

        wcounts = list(self.word_counts.items())
        wcounts.sort(key=lambda x: x[1], reverse=True)
        # forcing the oov_token to index 1 if it exists
        if self.oov_token is None:
            sorted_voc = []
        else:
            sorted_voc = [self.oov_token]
        sorted_voc.extend(wc[0] for wc in wcounts)

        # note that index 0 is reserved, never assigned to an existing word
        self.word_index = dict(
            zip(sorted_voc, list(range(1, len(sorted_voc) + 1)))
        )

        self.index_word = {c: w for w, c in self.word_index.items()}

        for w, c in list(self.word_docs.items()):
            self.index_docs[self.word_index[w]] = c


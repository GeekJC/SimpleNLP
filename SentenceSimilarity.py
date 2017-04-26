import jieba
import pandas as pd
import logging
import os
from gensim import corpora, models, similarities
from jpype import *

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class SentenceSimilarity(object):

    CNCBCSV_file = 'CNCBCrawlling/quotes_products.csv'
    HanLP_path = "{}/hanlp-portable-1.3.2.jar".format(os.getcwd())

    def __init__(self):
        self.questions = self.tokenize_question(self.CNCBCSV_file)
        self.dictionary = corpora.Dictionary(self.questions)
        self.build_model()
        print(self.similarity('購買力'))

    def tokenize_question(self, filename):
        questions = []
        data = pd.read_csv(filename)

        jieba.initialize()
        jieba.set_dictionary('dict.txt.big.txt')

        for text in data.Question:
            words = jieba.cut(text)
            tokens = ','.join(words)
            questions.append(tokens.split(','))

        return questions

    def init_dictionary(self):
        dictionary = corpora.Dictionary(self.questions)
        dictionary.save('CNCB.dict')

        return dictionary

    def build_model(self):
        corpus = [self.dictionary.doc2bow(text) for text in self.questions]
        corpora.MmCorpus.serialize('CNCB.mm', corpus)

        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        self.lsi = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=400)
        self.index = similarities.MatrixSimilarity(self.lsi[corpus])

    def similarity(self, sentence):
        vec = self.dictionary.doc2bow(sentence.lower().split())
        vec_lsi = self.lsi[vec]
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims

    # I used the portable version of hanlp. For more accurate results, data files from hanlp should be downloaded
    def get_entities(self, sentence):
        startJVM(getDefaultJVMPath(), "-Djava.class.path=%s" % self.HanLP_path, "-Xms1g", "-Xmx1g")
        NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
        print(NLPTokenizer.segment(sentence))

test = SentenceSimilarity()
print(test.similarity('購買力'))
test.get_entities('我可如何透過網上理財查詢證劵交易之購買力？')




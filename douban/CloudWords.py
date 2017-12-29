
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy
import re
import jieba
import pandas as pd
from scipy.misc import imread

def Word_Cloud(text_):
    bg_pic = imread('src/timg.jpg')
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    text_ = str(text_)
    filtertext = re.findall(pattern,text_)
    cleanedtext = ''.join(filtertext)
    segments = jieba.lcut(cleanedtext)
    words_df = pd.DataFrame({'segment':segments})

    stopwords = pd.read_csv("stopwords.txt",index_col=False,quoting = 3,sep = "\t",names =['stopword'] ,encoding='GBK')
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

    words_stat = words_df.groupby(by = ['segment'])['segment'].agg({'计数':numpy.size})
    words_stat = words_stat.reset_index().sort_values(by = ['计数'],ascending=False)
    wordcloud = WordCloud( font_path ="simhei.ttf", background_color="white", max_font_size=80,mask = bg_pic)
    word_frequence = {x[0]:x[1] for x in words_stat.head(2000).values}

    word_frequence_list = []
    for word in word_frequence:
        temp = (word,word_frequence[word])
        word_frequence_list.append(temp)

    wordcloud = wordcloud.fit_words(dict(word_frequence_list))
    plt.imshow(wordcloud)
    plt.show()


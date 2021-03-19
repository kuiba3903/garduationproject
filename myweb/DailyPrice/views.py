from django.shortcuts import render
from .forms import searchForm
from .models import DailyPrice_DP,DailyPrice_BP,price_2011_2020
from django.http import JsonResponse, HttpResponse
from price.forms.serachForm import searchForm
from django.db.models import Q
import statsmodels.api as sm
import os
import time
import warnings
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARMA',
                        FutureWarning)
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARIMA',
                        FutureWarning)


import base64
import json
from django.core import serializers
# Create your views here.


def market_brief(request,market_index):
    form = searchForm(initial={"market_name": "安徽安庆市龙狮桥蔬菜批发市场", "market_index": "20843"})
    return render(request, "market.html",{"forms":form})


def query_datePrice(request):
    market_index = request.GET.get("market_index")
    res = DailyPrice_DP.objects.filter(market_index=market_index).values_list()
    data = {}
    for i in range(len(res)):
        data[i] = res[i]

    # print(data)
    # print(len(res))
    return JsonResponse({"data":data,"length":len(res)})


def market_show(request):
    form = searchForm(initial={"market_name": "安徽安庆市龙狮桥蔬菜批发市场", "market_index": "20843"})
    return render(request, "market_show.html", {"forms": form})


def query_marketData(request):
    market_index = request.GET.get("market_index")
    res = DailyPrice_BP.objects.filter(market_index=market_index).values_list()
    data = {
        "market_name":res[0][2],
        "brief":res[0][3]
    }
    print(data)

    return JsonResponse({"data":data})

def image(request):
    market_index = 8763807
    res = DailyPrice_BP.objects.filter(market_index=market_index).values_list("picture")
    data = res[0][0].decode("utf-8")
    print(str(res[0][0].decode("utf-8")))

    return HttpResponse(data)

def news_process(request):
    return render(request,"news.html")
import codecs

import pandas as pd
import numpy as np
import jieba.posseg
import jieba.analyse
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import RidgeClassifier, LogisticRegression
from sklearn.metrics import f1_score,accuracy_score
from sklearn.neighbors import KNeighborsClassifier
def dataPrepos(text, stopkey):
    l = []
    pos = ['n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd']  # 定义选取的词性
    seg = jieba.posseg.cut(text)  # 分词
    for i in seg:
        if i.word not in stopkey and i.flag in pos:  # 去停用词 + 词性筛选
            l.append(i.word)
    return l
# tf-idf获取文本top10关键词
def getKeywords_tfidf(data,stopkey,topK):
    idList, titleList, abstractList = data['序号'], data['类型'], data['内容']
    corpus = [] # 将所有文档输出到一个list中，一行就是一个文档
    for index in range(len(idList)):
        text = '%s。%s' % (titleList[index], abstractList[index]) # 拼接标题和摘要
        text = dataPrepos(text,stopkey) # 文本预处理
        text = " ".join(text) # 连接成字符串，空格分隔
        corpus.append(text)

    # 1、构建词频矩阵，将文本中的词语转换成词频矩阵
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus) # 词频矩阵,a[i][j]:表示j词在第i个文本中的词频
    # 2、统计每个词的tf-idf权值
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    # 3、获取词袋模型中的关键词
    word = vectorizer.get_feature_names()
    print(word)
    # 4、获取tf-idf矩阵，a[i][j]表示j词在i篇文本中的tf-idf权重
    weight = tfidf.toarray()
    print(weight)
    # 5、打印词语权重
    ids, titles, keys = [], [], []
    for i in range(len(weight)):
        print(u"-------这里输出第", i+1 , u"篇文本的词语tf-idf------")
        ids.append(idList[i])
        titles.append(titleList[i])
        df_word,df_weight = [],[] # 当前文章的所有词汇列表、词汇对应权重列表
        for j in range(len(word)):
            print (word[j],weight[i][j])
            df_word.append(word[j])
            df_weight.append(weight[i][j])
        df_word = pd.DataFrame(df_word,columns=['word'])
        df_weight = pd.DataFrame(df_weight,columns=['weight'])
        word_weight = pd.concat([df_word, df_weight], axis=1) # 拼接词汇列表和权重列表
        word_weight = word_weight.sort_values(by="weight",ascending = False) # 按照权重值降序排列
        keyword = np.array(word_weight['word']) # 选择词汇列并转成数组格式
        word_split = [keyword[x] for x in range(0,topK)] # 抽取前topK个词汇作为关键词
        word_split = " ".join(word_split)
        keys.append(word_split)

    result = pd.DataFrame({"id": ids, "title": titles, "key": keys},columns=['id','title','key'])
    return result
def fenlei_model(s):
    #15000是train_set.csv里数据的总数量
    # print(os.listdir(os.path.dirname(os.path.abspath(__file__))))
    pwd = os.path.dirname(__file__)

    train_df = pd.read_csv(pwd+'/file/data_text.csv')
    stopkey = [w.strip() for w in codecs.open(pwd+'/file/stopWord.txt', 'r').readlines()]
    train_df = getKeywords_tfidf(train_df,stopkey,3)
    # print(type(train_df))
    train_df = train_df.reindex(np.random.permutation(train_df.index))
    # print(train_df)

    vectorizer = CountVectorizer(max_features=300)
    tfidf = TfidfVectorizer(ngram_range=(1,3), max_features=300)
    train_test = tfidf.fit_transform(train_df['key'])

    clf = RidgeClassifier()
    clf.fit(train_test, train_df['title'].values)
    # for i in range(len(train_df['title'].values)):
    #     print(train_df['title'].values[i], clf.predict(train_test[i]))
    # print(train_df['title'].values,clf.predict(train_test))
    # print(type(train_test))
    # for each in train_test:
    #     print(each)

    print("--------------")
    test = []
    test.append(s)
    k = tfidf.transform(list(map(lambda x: " ".join(dataPrepos(x, stopkey)), test)))
    print(list(map(lambda x: " ".join(dataPrepos(x, stopkey)),test)))
    print(clf.predict(k))
    key = list(map(lambda x: " ".join(dataPrepos(x, stopkey)),test))[0]
    return key,clf.predict(k)

def getKeywords_tfidf_2(data,stopkey,topK):
    idList, titleList, abstractList = data['序号'], data['标签'], data['内容']
    corpus = [] # 将所有文档输出到一个list中，一行就是一个文档
    for index in range(len(idList)):
        text = '%s。%s' % (titleList[index], abstractList[index]) # 拼接标题和摘要
        text = dataPrepos(text,stopkey) # 文本预处理
        text = " ".join(text) # 连接成字符串，空格分隔
        corpus.append(text)

    # 1、构建词频矩阵，将文本中的词语转换成词频矩阵
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus) # 词频矩阵,a[i][j]:表示j词在第i个文本中的词频
    # 2、统计每个词的tf-idf权值
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    # 3、获取词袋模型中的关键词
    word = vectorizer.get_feature_names()
    print(word)
    # 4、获取tf-idf矩阵，a[i][j]表示j词在i篇文本中的tf-idf权重
    weight = tfidf.toarray()
    print(weight)
    # 5、打印词语权重
    ids, titles, keys = [], [], []
    for i in range(len(weight)):
        print(u"-------这里输出第", i+1 , u"篇文本的词语tf-idf------")
        ids.append(idList[i])
        titles.append(titleList[i])
        df_word,df_weight = [],[] # 当前文章的所有词汇列表、词汇对应权重列表
        for j in range(len(word)):
            print (word[j],weight[i][j])
            df_word.append(word[j])
            df_weight.append(weight[i][j])
        df_word = pd.DataFrame(df_word,columns=['word'])
        df_weight = pd.DataFrame(df_weight,columns=['weight'])
        word_weight = pd.concat([df_word, df_weight], axis=1) # 拼接词汇列表和权重列表
        word_weight = word_weight.sort_values(by="weight",ascending = False) # 按照权重值降序排列
        keyword = np.array(word_weight['word']) # 选择词汇列并转成数组格式
        word_split = [keyword[x] for x in range(0,topK)] # 抽取前topK个词汇作为关键词
        word_split = " ".join(word_split)
        keys.append(word_split)

    result = pd.DataFrame({"id": ids, "title": titles, "key": keys},columns=['id','title','key'])
    return result
def label_molde(s):
    pwd = os.path.dirname(__file__)
    #15000是train_set.csv里数据的总数量
    train_df = pd.read_csv(pwd+'/file/data_text.csv')
    stopkey = [w.strip() for w in codecs.open(pwd+'/file/stopWord.txt', 'r').readlines()]
    train_df = getKeywords_tfidf_2(train_df,stopkey,3)
    print(type(train_df))
    train_df = train_df.reindex(np.random.permutation(train_df.index))
    # print(train_df)

    vectorizer = CountVectorizer(max_features=300)
    tfidf = TfidfVectorizer(ngram_range=(1,3), max_features=300)
    train_test = tfidf.fit_transform(train_df['key'])

    clf = RidgeClassifier()
    clf.fit(train_test, train_df['title'].values)
    # for i in range(len(train_df['title'].values)):
    #     print(train_df['title'].values[i], clf.predict(train_test[i]))
    # print(train_df['title'].values,clf.predict(train_test))
    # print(type(train_test))
    # for each in train_test:
    #     print(each)

    print("--------------")
    test = []
    test.append(s)
    print(list(map(lambda x:" ".join(dataPrepos(x,stopkey)), test)))
    k = tfidf.transform(list(map(lambda x:" ".join(dataPrepos(x,stopkey)), test)))
    print(clf.predict(k))
    return clf.predict(k)

def fenlei(request):
    t = time.strftime('%Y{y}%m{m}%d{d}%H{h}%M{f}%S{s}').format(y='年', m='月', d='日', h='时', f='分', s='秒')
    text = request.GET.get("text")
    key,result = fenlei_model(text)
    qushi = "上涨"if((label_molde(text))==1) else "下跌"
    return JsonResponse({"result":result[0],"key":key,"qushi":qushi,"time":t})
def predict_arima(request):
    form = searchForm(initial={"province_name": "34", "vegetable_name": "13075"})
    return render(request, "predict.html", {"forms": form})

def process_data(x):
    try:
        x = float(x)
        return x
    except:
        return x

def search_2011_2020(request):
    vegetable_index = request.POST.get("vegetable_name")
    craft_index = request.POST.get("craft_name")
    province_index = request.POST.get("province_name")
    market_index = request.POST.get("market_name")
    data = price_2011_2020.objects.filter(Q(vegetable_index=vegetable_index)
                                & Q(craft_index=craft_index)
                                & Q(province_index=province_index)
                                & Q(market_index=market_index)).distinct().values_list("price_2011", "price_2012","price_2013", "price_2014",
                                                                                       "price_2015", "price_2016","price_2017", "price_2018",
                                                                                       "price_2019", "price_2020")
    # print(data[0][0])
    # print(data[0][1])
    l = []
    for i in range(0, 10):
        p = str(data[0][i])[1:-1]
        # print(p)
        p_num = list(map(lambda x: process_data(x), p.split(",")))
        # print(p_num)
        l.extend(p_num)
    print(l)
    num_null = 0
    num_num = 0
    s = 0
    for i in l:
        # print(i)
        # print()
        if isinstance(i,float):
            num_num += 1
            s = s + float(i)
        else:
            num_null += 1
    for i in range(len(l)):
        if isinstance(l[i],str):
            l[i] = round(s/num_num,2)
    k = []
    for i in range(1, len(l)):
        k.append(l[i] - l[i - 1])
    arma_mod60 = sm.tsa.ARMA(k, (8, 2)).fit(disp=0)
    predict_sunspots = arma_mod60.predict(0, 118)
    # print(predict_sunspots)
    l_predict = []
    l_predict.append(l[0])
    for i in range(len(predict_sunspots)):
        l_predict.append(l_predict[-1] + predict_sunspots[i])
    # print(l_predict)
    for i in range(len(l_predict)):
        l_predict[i] = round(l_predict[i],2)
    return JsonResponse({"data":l,"predict":l_predict})



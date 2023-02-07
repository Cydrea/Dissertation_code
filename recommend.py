import this

import pandas as pd
import numpy as np
from surprise import Dataset, Reader
from surprise import SVD
from surprise.model_selection import train_test_split
import random

basic_data = pd.read_csv('D:\MyCode\project\dataset\\processed events.csv').drop(columns='Unnamed: 0')
user_data = [[238363, 150700, 368193, 205183], [1, 3, 6, 3]]
initial=[[],[]]

def mergeData(data, proto=basic_data):
    est_df = pd.DataFrame({
        "visitorid": np.ones(len(data[0])),
        "itemid": data[0],
        "event": data[1]
    }).astype(int)
    dataset = proto.append(est_df, ignore_index=True)
    return dataset


def generateModel(dataset):
    dataset.astype("int32")
    events_df = dataset.fillna(0).astype(int)

    reader = Reader(rating_scale=(1, 6))
    data = Dataset.load_from_df(events_df[['visitorid', 'itemid', 'event']], reader)

    trainset, testset = train_test_split(data, test_size=0.2)

    model = SVD(n_factors=80, n_epochs=20, lr_all=0.005, reg_all=0.2)
    model.fit(trainset)
    return model


def recommend(feedback=None, user_id=1, thresh=2, count=3):
    if feedback is None:
        feedback = user_data
    dataset = mergeData(feedback)
    model = generateModel(dataset)
    items = dataset.itemid.unique()
    random.shuffle(items)
    uid = []
    rate = []
    output = []

    for item in items:
        rating = model.predict(uid=user_id, iid=item).est
        if rating >= thresh:
            uid.append(item)
            rate.append(rating)
    pred = list(zip(uid, rate))

    def second(e):
        return e[1]

    pred.sort(key=second, reverse=True)

    for i in range(count):
        output.append(pred[i][0])
    return output


def generateBest(dataset=basic_data, n=100):
    dataset.astype("int32")
    events_df = dataset.fillna(0).astype(int)

    reader = Reader(rating_scale=(1, 6))
    data = Dataset.load_from_df(events_df[['visitorid', 'itemid', 'event']], reader)

    trainset, testset = train_test_split(data, test_size=0.2)

    model = SVD(n_factors=80, n_epochs=20, lr_all=0.005, reg_all=0.2)
    model.fit(trainset)
    predictions = model.test(testset)
    test = pd.DataFrame(predictions, columns=['uid', 'iid', '0', 'est', '1']) \
        .drop(columns=['0', '1'])
    test_count = test.groupby("iid")['est'].mean().sort_values(ascending=False)
    top_n = test_count[0:n]
    return top_n.index.tolist()


best_100 = generateBest()


def randomRecommend(n=100):
    return best_100[random.randrange(0, n)]


def recordData(iid, rating):
    initial[0].append(iid)
    initial[1].append(rating)









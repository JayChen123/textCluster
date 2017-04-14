# -*- coding:utf-8 -*-
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import pandas as pd
import os.path
from config import n_cluster, \
    export_path, export_name_all


def cluster_agg(_data):
    """
    KMmeans 聚类算法 主程序
    :param _data: 数据矩阵
    """
    assert isinstance(_data, (np.ndarray, pd.DataFrame))

    data = pd.DataFrame(_data)
    data_zs = (data - data.mean()) / data.std()
    model = AgglomerativeClustering(n_clusters=n_cluster, affinity='cosine', linkage='complete')
    model.fit(data_zs)

    result = pd.concat([data, pd.Series(model.labels_, index=data.index)], axis=1)
    result.columns = list(data.columns) + ["聚类类别"]

    cla = pd.DataFrame(pd.Series(model.labels_).value_counts())
    cla.columns = ["聚类统计"]
    cla.to_excel(os.path.join(export_path, export_name_all))

    return result


if __name__ == '__main__':
    """ test code """
    dd = np.random.rand(100, 12)
    res = cluster_agg(dd)
    print(res)

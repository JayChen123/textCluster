"""
此处封装文本聚类的工具
"""
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from db import MyDB
import pandas as pd
from config import filter_item
import re
import functools

__all__ = [
    "read_db",
    "read_file",
    "export_file"
]


def read_file(file_name):
    """
    读取文本数据，要求一行一条文本数据
    """
    with open(file_name, mode="r", encoding="utf8") as fd:
        lines = fd.readlines()

    return list(map(filter_text, lines))


def read_db(db_info, table, key):
    """
    从数据库中读取文本
    :param db_info:  数据库信息 要求为字典格式
    :param table: 表名
    :param key:数据库字段
    """
    sql_select = "select %s from %s" % (key, table)

    with MyDB(db_info) as db:
        db.execute(sql_select)
        results = db.fetchall()

    return results


def filter_text(text):
    """
    过滤文本的特殊符号
    :param text:  一条字符数据
    """
    return re.sub(filter_item, "", text.strip())


def export_file(out_file="out.xls", columns=None):
    """
    导出文件装饰器
    :param out_file: 导出文件名 
    :param columns: 导出文件标题
    """

    def _decoration(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            result = result if isinstance(result, pd.DataFrame) else pd.DataFrame(result)
            result.columns = columns if columns else result.columns

            if out_file.endswith("xls"):
                result.to_excel(out_file)

            elif out_file.endswith("csv"):
                result.to_csv(out_file)
            else:
                raise NameError("output file must excel or csv")
            return result

        return _wrapper

    return _decoration


def cluster_plot(type_="post", n_clusters_=None):
    """
    聚类可视化装饰器
    :param type_: 可视化聚类之前数据 pre 聚类之后数据 post
    :param n_clusters_: 
    """

    def _decoration(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            cluster_result = func(*args, **kwargs)

            if not isinstance(cluster_result, pd.DataFrame):
                cluster_result = pd.DataFrame(cluster_result)

            fig = TSNE()
            fig.fit_transform(cluster_result)
            ts = pd.DataFrame(fig.embedding_, index=cluster_result.index)
            plt.rcParams["font.sans-serif"] = ["SimHei"]
            plt.rcParams["axes.unicode_minus"] = False

            if type_ == "post":
                for key, item in zip(range(n_clusters_), __generate_plot_item(n_clusters_)):
                    d = ts[cluster_result["聚类类别"] == key]
                    plt.plot(d[0], d[1], item)

            if type_ == "pre":
                for _ in cluster_result.index:
                    d = ts
                    plt.plot(d[0], d[1], "b.")
            plt.show()
            return cluster_result

        return _wrapper

    return _decoration


def __generate_plot_item(number):
    """
    生成画图标记
    :param number: 标记数目
    """
    color = "brgycm"
    item = "o.x*^+><sphHd"
    assert number <= len(color) * len(item)
    return [c + i for c in color for i in item][:number]

"""
文本聚类的主程序
"""
import os.path
from jieba_cut import cut_data
from tools import *
from compute_similar import compute_similar
from config import file_name, file_path, db_info
from ag_cluster import cluster_agg


@export_file(out_file="聚类结果_all.xls")
def run():
    texts = read_file(os.path.join(file_path, file_name))
    # texts = read_db(db_info, "handled_failsx", "BLSYY")
    cut_text = cut_data(texts)
    text_matrix = compute_similar(cut_text)
    result = cluster_agg(text_matrix)
    return result


if __name__ == '__main__':
    run()

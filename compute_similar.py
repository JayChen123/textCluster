from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


def compute_similar(text):
    """
    text 是已经分词的文本
    """
    vector = CountVectorizer()
    transform = TfidfTransformer()

    tf = vector.fit_transform(text)
    tf_idf = transform.fit_transform(tf)

    # tf_idf = transform.fit_transform(vector.fit_transform(corpus))
    # word = vector.get_feature_names()
    weight = tf_idf.toarray()

    return weight


if __name__ == "__main__":
    content = ["小明 硕士 毕业 于 中国科学院 计算所 ， 后 在 日本京都大学 深造",
               "小 明 硕士 毕业 于 中国 中国科学院 科学 科学院 学院 计算 计算所 "
               "  后 在 日本 日本京都大学 京都 京都大学 大学 深造"]

    print(compute_similar(content))

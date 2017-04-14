import jieba


def cut_data(iter_text):
    """
    分词
    :param iter_text: 元组或者列表形式的文本
    """
    assert isinstance(iter_text, (list, tuple))

    # 处理从文本读入的数据
    if isinstance(iter_text, list):
        return [cut_word(each) for each in iter_text]

    # 处理从数据库读入数据
    return [cut_word(each[0]) for each in iter_text]


def cut_word(content, cut_all=False):
    """
    使用结巴分词，默认使用不完全分词
    :param content: 字符串
    :param cut_all: 默认精确分词
    :return: 以空格分割的字符串
    """
    return " ".join(jieba.cut(content, cut_all=cut_all))


if __name__ == '__main__':
    """ 此处为分词测试 """
    text = "小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
    seg_list = jieba.cut(text, cut_all=False)
    print(" ".join(seg_list))

    dd = jieba.cut(text, cut_all=True)
    print(" ".join(dd))

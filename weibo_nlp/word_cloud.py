from wordcloud import WordCloud
from scipy.misc import imread

from os import path

d = path.dirname(__file__)
stop_words_path = path.join(d, 'stop_word.txt')


def get_word_cloud(content_list):
    back_photo = imread("/Users/caiweicheng/Desktop/img.png")
    font_path = path.join(d, "Chinese.ttf")

    wc = WordCloud(font_path=font_path,  # 设置字体
                   background_color="white",  # 背景颜色
                   max_words=2000,  # 词云显示的最大词数
                   mask=back_photo,  # 设置背景图片
                   max_font_size=100,  # 字体最大值
                   random_state=42,
                   width=500, height=500, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                   )
    freq_dict = get_freq_word(content_list=content_list)
    wc.generate_from_frequencies(freq_dict)
    # plt.figure()
    # # 以下代码显示图片
    # plt.imshow(wc)
    # plt.axis("off")
    # plt.show()
    # 绘制词云

    # 保存图片
    wc.to_file(path.join(d, 'word_cloud.png'))


def get_freq_word(content_list):
    import jieba
    from nltk.probability import FreqDist
    from weibo_nlp.utils import get_stop_word_set
    stop_words_set = get_stop_word_set()
    word_fd = FreqDist()
    for content in content_list:
        word_list = jieba.cut(content, cut_all=False)
        for word in word_list:
            word = word.strip()
            if word and word not in stop_words_set:
                word_fd[word] += 1
    return dict(word_fd.items())

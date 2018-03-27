from wordcloud import WordCloud, ImageColorGenerator
from scipy.misc import imread
from os import path
from weibo_nlp.utils import cut_word_path

d = path.dirname(__file__)
stop_words_path = path.join(d, 'stop_word.txt')

add_stop = {'大山', '大学城', '中山'}


def get_word_cloud(content_list):
    back_photo = imread(path.join(d, 'img.jpg'))
    font_path = path.join(d, "Chinese.ttf")

    wc = WordCloud(font_path=font_path,  # 设置字体,因为wordcloud没有内置的中文字体,所以必须设定
                   background_color="white",  # 背景颜色
                   max_words=2000,  # 词云显示的最大词数
                   mask=back_photo,  # 设置背景图片
                   max_font_size=100,  # 字体最大值
                   random_state=42,
                   width=500, height=500, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                   )
    freq_dict = get_freq_word(content_list=content_list)
    # 获取树洞集合的词频
    image_colors = ImageColorGenerator(back_photo)

    wc.generate_from_frequencies(freq_dict)
    # 生成词云图片
    wc.recolor(color_func=image_colors)
    wc.to_file(path.join(path.dirname(d), 'web/static', 'word_cloud.jpg'))
    # 保存图片


def get_freq_word(content_list):
    # 获取词频方法
    import jieba
    jieba.load_userdict(cut_word_path)
    from nltk.probability import FreqDist
    from weibo_nlp.utils import get_stop_word_set
    stop_words_set = get_stop_word_set()  # 获取停止词词库
    stop_words_set.update(add_stop)
    word_fd = FreqDist()
    for content in content_list:
        word_list = jieba.cut(content, cut_all=False)
        # 将单条树洞分词
        for word in word_list:
            word = word.strip()
            if word and word not in stop_words_set:
                # 若单词不在停止词库则对应频率加一
                word_fd[word] += 1
    return dict(word_fd.items())

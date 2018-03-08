from weixin_scrapy.settings import PROJECT_PATH
from flask_script import Manager, Command
import os
from web.models import db, Weibo
from snownlp import SnowNLP

file_path = os.path.join(PROJECT_PATH, 'weibo_nlp')


class Classify(Command):
    def run(self):
        weibo_list = Weibo.query.order_by(Weibo.publish_time.desc()).paginate(2, 5000).items

        neg_f = open(file_path + '/neg.txt', 'w+')
        pos_f = open(file_path + '/pos.txt', 'w+')
        else_f = open(file_path + '/else.txt', 'w+')

        mode_dict = {
            0: pos_f,
            1: neg_f,
            2: else_f
        }
        for weibo in weibo_list:
            content = weibo.content
            if content:
                s = SnowNLP(content)
                mode = s.sentiments
                if mode <= 0.05:
                    mode = 1
                elif mode >= 0.99:
                    mode = 0
                    print(content,mode)
                else:
                    mode = 2
                print(content, mode)
                if mode != 'q' or not mode:
                    write_file = mode_dict[mode]
                    write_file.write(content)
                    write_file.write('\n\n')

                else:
                    break
        print('finish')

        neg_f.close()
        pos_f.close()
        else_f.close()

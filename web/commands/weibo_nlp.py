from weixin_scrapy.settings import PROJECT_PATH
from flask_script import Manager, Command
import os
from web.models import db, Weibo, Tag

file_path = os.path.join(PROJECT_PATH, 'weibo_nlp')


class Classify(Command):
    def run(self):
        weibo_list = Weibo.query.filter_by(mode=2).filter(~Weibo.tags.any(Tag.type == Tag.function)).order_by(
            Weibo.publish_time.desc()).paginate(1, 200).items

        for weibo in weibo_list:
            content = weibo.content
            if content:
                mode = input("content:{}\n交易-5;宣传-6;求助-7; pass-0 quit--q input:".format(content))
                if mode == 0:
                    continue
                elif mode==1:
                    weibo.mode = mode
                    db.session.add(weibo)
                    db.session.commit(weibo)
                if mode != 'q' or not mode:

                    weibo.add_tags(tag_ids=int(mode))

                else:
                    break
        print('finish')

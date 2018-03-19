from weixin_scrapy.settings import PROJECT_PATH
from flask_script import Manager, Command
import os
from web.models import db, Weibo

file_path = os.path.join(PROJECT_PATH, 'weibo_nlp')


class BaseCommand(Command):
    def run(self):
        weibo_list = Weibo.query.filter_by(mode=1).order_by(Weibo.publish_time.desc()).paginate(1, 3000).items

        f = open(file_path + '/neg_1.txt', 'w')
        print(len(weibo_list))

        for weibo in weibo_list:
            content = weibo.content
            write_file = f
            write_file.write(content)
            write_file.write('\n\n')
        print('finish')
        db.session.commit()


        f.close()


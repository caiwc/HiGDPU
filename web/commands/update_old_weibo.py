from flask_script import Manager, Command
from web.models import db, Weibo


class Update(Command):
    help = description = '删除旧weibo_id的微博'

    def run(self):
        print("开始")
        old_weibo_list = Weibo.query.filter(Weibo.weibo_id.startswith('M_')).order_by(
                Weibo.publish_time.desc()).paginate(1, 5000).items
        for weibo in old_weibo_list:
            weibo_id = weibo.weibo_id
            new_id = weibo_id.lstrip('M_')
            if Weibo.query.filter_by(weibo_id=new_id).first():
                db.session.delete(weibo)
            else:
                weibo.weibo_id = new_id
            print('update '+weibo_id)

        db.session.commit()

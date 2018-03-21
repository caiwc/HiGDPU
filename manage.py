import os

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from web import create_app
from web.models import db, Weibo, Weixin_Gzh
from web.commands import update_old_weibo,weibo_nlp,snow_nlp_test,weibo_mode_to_txt

# default to dev config
env = os.environ.get('WEB_ENV', 'dev')
app = create_app('web.config.%sConfig' % env.capitalize())

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command('db', MigrateCommand)
manager.add_command("update_weibo", update_old_weibo.Update())
manager.add_command("classify_weibo_tag", weibo_nlp.Classify())
manager.add_command("snow_classify_weibo", snow_nlp_test.Classify())
manager.add_command("weibo_mode_to_txt", weibo_mode_to_txt.BaseCommand())

@manager.shell
def make_shell_context():
    return dict(
        app=app,
        db=db,
        Weibo=Weibo,
        Weixin_Gzh=Weixin_Gzh,
    )

if __name__ == "__main__":
    manager.run()

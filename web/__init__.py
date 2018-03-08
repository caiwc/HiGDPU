# from sqlalchemy import event

from flask import Flask

from web.models import db
from web.extensions import (
    rest_api,
    celery
)
from web.controllers.main import main_blueprint
from web.controllers.rest.weibo import Weibo_Api
from web.controllers.rest.weixin import Weixin_Gzh_Api
from web.controllers.rest.official import Official_Api
from web.controllers.rest.message import Message_Api
from web.controllers.rest.authorization import Authorization_Api
from web.extensions import MyResponse
# from .tasks import on_reminder_save


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """

    app = Flask(__name__)
    app.response_class = MyResponse
    app.config.from_object(object_name)

    db.init_app(app)
    # event.listen(Reminder, 'after_insert', on_reminder_save)

    # bcrypt.init_app(app)
    # oid.init_app(app)
    # login_manager.init_app(app)
    # principals.init_app(app)
    celery.init_app(app)

    rest_api.add_resource(
        Weibo_Api,
        '/api/weibo',
        '/api/weibo/comment',
        '/api/weibo/<string:weibo_id>',
    )
    rest_api.add_resource(
        Weixin_Gzh_Api,
        '/api/weixin',
        '/api/weixin/<string:article_id>'
    )
    rest_api.add_resource(
        Official_Api,
        '/api/official',
        '/api/official/<string:article_id>'
    )
    rest_api.add_resource(
        Message_Api,
        '/api/message'
    )
    rest_api.add_resource(
        Authorization_Api,
        '/api/authorization'
    )

    rest_api.init_app(app)

    # @identity_loaded.connect_via(app)
    # def on_identity_loaded(sender, identity):
    #     # Set the identity user object
    #     identity.user = current_user
    #
    #     # Add the UserNeed to the identity
    #     if hasattr(current_user, 'id'):
    #         identity.provides.add(UserNeed(current_user.id))
    #
    #     # Add each role to the identity
    #     if hasattr(current_user, 'roles'):
    #         for role in current_user.roles:
    #             identity.provides.add(RoleNeed(role.name))

    app.register_blueprint(main_blueprint)

    return app


if __name__ == '__main__':
    app = app = create_app('web.config.DevConfig')
    app.run()

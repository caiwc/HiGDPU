from web.signals.signals_define import get_message
from flask import current_app
from web.models import Message,db


@get_message.connect_via(current_app)
def get_message(app,):
    pass

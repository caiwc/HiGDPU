from web import create_app
from web.models import db, User
import datetime
app = create_app('web.config.TestConfig')

db.app = app
db.create_all()

test_user = User()
test_user.openid = "test_id"
test_user.session_key = "test"
test_user.third_session = "test"
test_user.expires_in = datetime.datetime.now()
db.session.add(test_user)
db.session.commit()

app.run()

from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))

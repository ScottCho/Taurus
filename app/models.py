from app.extensions import db
from datetime import datetime


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    numbers = db.Column(db.String(128))   # 货号
    brand = db.Column(db.String(128))     # 品牌
    tag = db.Column(db.String(128))        # 类别
    colour = db.Column(db.String(128))   # 配色
    buying_price = db.Column(db.Float)
    launch_date = db.Column(db.DateTime(), default=datetime.now)  # 上市日期
    counts = db.Column(db.Integer, default=1)   # 商品数量
    d_sales = db.Column(db.Integer, default=0)  # 日销量
    w_sales = db.Column(db.Integer, default=0)  # 日销量
    m_sales = db.Column(db.Integer, default=0)  # 日销量
    remark = db.Column(db.Text)
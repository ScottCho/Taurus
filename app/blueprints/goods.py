from datetime import datetime

from app.extensions import db, scheduler
from app.models import Goods
from flask import (Blueprint, flash, redirect, render_template, request,
                   url_for)

goods_bp = Blueprint('goods', __name__)


# 添加商品
@goods_bp.route('/new/goods', methods=['GET', 'POST'])
def new_good():
    if request.method == 'POST':
        launch_date = request.form.get('launch_date')
        launch_date = datetime.strptime(launch_date, "%Y-%m-%d")
        good = Goods(numbers=request.form.get('numbers'),
                     brand=request.form.get('brand'),
                     tag=request.form.get('tag'),
                     colour=request.form.get('colour'),
                     buying_price=request.form.get('buying_price'),
                     launch_date=launch_date,
                     counts=request.form.get('counts'),
                     remark=request.form.get('remark'))
        db.session.add(good)
        db.session.commit()
        flash('商品成功上架.', 'success')
        return redirect(url_for('goods.manage_good'))
    return render_template('new_goods.html')


# 商品总览
@goods_bp.route('/manage/goods')
def manage_good():
    goods = Goods.query.all()
    return render_template('manage_goods.html', goods=goods)


# 删除
@goods_bp.route('/delete/goods/<int:id>')
def delete_good(id):
    good = Goods.query.get_or_404(id)
    db.session.delete(good)
    db.session.commit()
    flash('商品已下架.', 'success')
    return redirect(url_for('goods.manage_good'))


# 编辑
@goods_bp.route('/edit/goods/<int:id>', methods=['GET', 'POST'])
def edit_good(id):
    good = Goods.query.get_or_404(id)
    if request.method == 'POST':
        good.numbers = request.form.get('numbers')
        good.brand = request.form.get('brand')
        good.tag = request.form.get('tag')
        good.colour = request.form.get('colour')
        launch_date = datetime.strptime(request.form.get('launch_date'), "%Y-%m-%d")
        good.launch_date = launch_date
        good.buying_price = request.form.get('buying_price')
        good.counts = request.form.get('counts')
        good.remark = request.form.get('remark')
        db.session.add(good)
        db.session.commit()
        flash('编辑成功.', 'success')
        return redirect(url_for('goods.manage_good'))
    return render_template('edit_goods.html', good=good)


# 销量展示
@goods_bp.route('/manage/sales')
def manage_sale():
    goods = Goods.query.all()
    return render_template('manage_sales.html', goods=goods)


# 修改销量
@goods_bp.route('/edit/sales/<int:id>', methods=['GET', 'POST'])
def edit_sale(id):
    good = Goods.query.get_or_404(id)
    if request.method == 'POST':
        d_sales = request.form.get('d_sales')
        counts = request.form.get('counts')
        good.d_sales = d_sales
        good.counts = int(counts)-int(d_sales)
        good.remark = request.form.get('remark')
        db.session.add(good)
        db.session.commit()
        flash('编辑成功.', 'success')
        return redirect(url_for('goods.manage_sale'))
    return render_template('edit_sales.html', good=good)


@scheduler.task('cron', id='sales', day='*', hour=0, minute='0')
def reset_sales():
    with db.app.app_context():
        goods = Goods.query.all()
        for good in goods:
            d_sales = good.d_sales
            w_sales = good.w_sales
            m_sales = good.m_sales
            good.d_sales = 0
            good.w_sales = int(d_sales)+int(w_sales)
            good.m_sales = int(d_sales)+int(m_sales)
            db.session.add(good)
        db.session.commit()
        print('sales任务完成。')
    return '任务完成'
        

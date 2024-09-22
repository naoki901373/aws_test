#!/usr/bin/python3.7
from flask import Flask,request, make_response
from flask_sqlalchemy import SQLAlchemy
import inspect
# Flaskをappという変数で動かす宣言


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///Test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True
app.url_map.strict_slashes = False

db = SQLAlchemy(app)

class Shohin(db.Model):
   __tablename__ = 'Shohin'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.Text)
   amount = db.Column(db.Integer)
   price = db.Column(db.Integer)

@app.before_first_request
def init():
    db.create_all()



@app.route('/', methods=['GET'])
def AWS():
   name = "AWS"
   return name


@app.route('/secret/', methods=['GET'])
def digest():
   status = "SUCCESS"
   return status


###############
# 1
###############
# POST: 在庫の更新・作成 
@app.route('/v1/stocks/', methods=['POST'], endpoint='1')
def db_1():
   req_dict = request.json
   name = req_dict['name']
   if 'amount' in req_dict.keys():
      amount = req_dict['amount']
   else:
      amount = 1
   if type(name) is not str or type(amount) is not int:
      resp = make_response({"message": "ERROR"})
      resp.headers['Location'] = f'35.78.95.233:80/v1/stocks/{name}'
      return resp
   price = 0

   resp = make_response(req_dict)
   resp.headers['Location'] = f'35.78.95.233:80/v1/stocks/{name}'

   exists =  Shohin.query.filter_by(name = name).first()
   # 新規作成
   if exists is None:
      new_record = Shohin(name = name, amount = amount, price = price)
      db.session.add(new_record)
      db.session.commit()
   # 更新
   else:
      update_record = Shohin.query.filter_by(name = name).first()
      update_record.name = name
      update_record.amount = amount
      update_record.price = price
      db.session.commit()
   return resp


###############
# 2
###############
# 在庫チェック nameあり
@app.route('/v1/stocks/<name>', methods=['GET'], endpoint='2')
def db_2(name):
   query = Shohin.query.filter_by(name = name).first()
   resp = make_response({query.name:query.amount})
   resp.headers['Location'] = f'35.78.95.233:80/v1/sales/{name}'
   return resp


# 在庫チェック nameなし 全件表示
@app.route('/v1/stocks/', methods=['GET'], endpoint='6')
def db_3():
   query = db.session.query(Shohin).order_by(Shohin.name).all()
   ans = {}
   for i in query:
      tmp = {i.name: i.amount}
      ans.update(tmp)
   resp = make_response(ans)
   resp.headers['Location'] = f'35.78.95.233:80/v1/sales/'
   return resp


###############
# 3
###############
# 販売
@app.route('/v1/sales/', methods=['POST'], endpoint='3')
def db_4():
   req_dict = request.json
   name = req_dict['name']
   if 'amount' in req_dict.keys():
      amount = req_dict['amount']
   else:
      amount = 1
   if 'price' in req_dict.keys():
      price = req_dict['price']
   else:
      price = 0
   update_record = Shohin.query.filter_by(name = name).first()
   update_record.name = name
   update_record.amount -= amount
   update_record.price += amount*price
   db.session.commit()

   resp = make_response(req_dict)
   resp.headers['Location'] = f'35.78.95.233:80/v1/sales/{name}'
   return resp

###############
# 4
###############
# 売り上げチェック
@app.route('/v1/sales/', methods=['GET'], endpoint='4')
def db_5():
   sales = 0
   datas = db.session.query(Shohin.price).all()
   for data in datas:
      sales += data.price
   resp = make_response({"sales": float(sales)})
   return resp

###############
# 5
###############
# 全削除
@app.route('/v1/stocks/', methods=['DELETE'], endpoint='5')
def db_6():
   db.session.query(Shohin).delete()
   db.session.commit()
   return 'Done'


# appの実行
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
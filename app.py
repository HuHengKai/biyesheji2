from flask import Flask, render_template,request,flash,redirect,url_for,session,g
#from requests import request
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash
from models import db,Users,Questions,Device
from exts import validate
app = Flask(__name__)
app.secret_key = "SECRET_KEY"
#制定mysql的地址：mysql://username:password@hostname/database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:123456@localhost:3306/flask?charset=utf8mb4"
#如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
# with app.test_request_context():
#     db.drop_all()
#     db.create_all()
@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'login_user':g.user}
    return {}
@app.before_request
def my_before_request():
    username=session.get('username')
    if username:
        g.user=Users.query.filter(Users.username==username).first()
@app.route('/')
def home():
    decices=Device.query.order_by(Device.id.desc()).all()
    return render_template("home.html",decices=decices)
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method=='GET':
       return render_template('register.html')
    else:
        username=request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(username, password1, password2)
        message=validate(username,password1,password2)
        flash(message)
        if '成功' in message:
            new_user = Users(username=username, password=password1)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html')
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
       return render_template('login.html')
    else:
        username=request.form.get('username')
        password1 = request.form.get('password1')
        print(username, password1)
        message=validate(username,password1)
        if '成功' in message:
            session['username']=username
            session.permanent=True
            return redirect(url_for('home'))
        else:
            flash(message)
            return render_template('login.html')
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('home'))
@app.route('/question/',methods=['GET','POST'])
def question():
    if request.method=='GET':
       return render_template('question.html')
    else:
        if hasattr(g,'user'):
          question_title=request.form.get('question_title')
          question_desc = request.form.get('question_desc')
          author_id=g.user.id
          #author_id = Users.query.filter(Users.username == session.get('username')).first().id
          new_question=Questions(title=question_title,content=question_desc,author_id=author_id)
          db.session.add(new_question)
          db.session.commit()
          return redirect(url_for('home'))
        else:
            flash("请先登录")
            return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)

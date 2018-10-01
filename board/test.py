from flask import Flask, redirect, url_for ,request, session, g, render_template
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
DATABASE = './test.db'
app = Flask(__name__)
app.secret_key='abcabc'

def get_db():
    db = getattr(g, '_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        print db
        with app.open_resource('schema.sql', mode='r')as f:
            db.cursor().executescript(f.read())
        db.commit()

def add_user(ID,PW,Email):
    sql = "INSERT INTO users (ID,PW,Email) VALUES('%s','%s','%s')" %(ID,PW,Email)
    print sql
    db = get_db()
    db.execute(sql)
    res = db.commit()
    return res

def get_user(ID,PW):
    sql = 'SELECT * FROM users where ID="{}" and PW ="{}"'.format(ID,PW)
    db =get_db()
    rv = db.execute(sql)
    res = rv.fetchall()
    return res

def add_writ(title):
    sql = "INSERT INTO writ (title) VALUES('%s')" %(title)
    print sql
    db = get_db()
    db.execute(sql)
    res = db.commit()
    return res

def get_writ(title):
    sql = 'SELECT * FROM writ where title="{}"'.format(title)
    db=get_db()
    rv = db.execute(sql)
    res = rv.fetchall()
    return res

def wkrtjd(wpahr, sodyd, wkrtjdwk, wkrtjdtime):
    sql = "INSERT INTO geee (wpahr, sodyd, wkrtjdwk, wkrtjdtime) VALUES('%s','%s','%s','%s')" %(wpahr,sodyd,wkrtjdwk,wkrtjdtime)
    print sql
    db = get_db()
    db.execute(sql)
    res = db.commit()
    return res

def wkrtjd2():
    sql ='SELECT * FROM geee'
    db =get_db()
    rv = db.execute(sql)
    res = rv.fetchall()
    return res

def wkrtjd3(idx):
    sql ='SELECT * FROM geee where idx="%s"' %(idx)
    db = get_db()
    rv = db.execute(sql)
    res = rv.fetchall()
    return res

def wkrtjd4(wpahr,sodyd,wkrtjdwk,wkrtjdtime,idx):
    sql = 'UPDATE geee SET wpahr="%s", sodyd="%s",wkrtjdwk="%s",wkrtjdtime="%s" where idx="%s"' %(wpahr,sodyd,wkrtjdwk,wkrtjdtime,idx)
    print sql
    db =get_db()
    db.execute(sql)
    res = db.commit()
    return res

@app.route('/update/<idx>', methods=['GET','POST'])
def update(idx):
    if 'ID' in session:
        qustn = wkrtjd3(idx)
        if request.method == 'GET':
            return render_template('zoo.html', data=qustn)
        else:
            wpahr = request.form.get('wpahr')
            sodyd = request.form.get('sodyd')
            wkrtjdtime = datetime.now().strftime('%Y-%m-%d %H:%M:S')
            wkrtjdwk = request.form.get('wkrtjdwk')
            wkrtjd4(wpahr,sodyd,wkrtjdwk,wkrtjdtime,idx)
            return redirect(url_for('rptlvks'))
    else:
        return redirect(url_for('login'))


@app.route('/rudfh', methods=['GET','POST'])
def rudfh():
    if request.method == 'GET':
        return render_template('write_board.html')
    else:
        wpahr = request.form.get('wpahr')
        wkrtjdwk = request.form.get('wkrtjdwk')
        sodyd = request.form.get('sodyd')
        wkrtjdtime = datetime.now().strftime('%Y-%m-%d %H:%M:S')
        wkrtjd(wpahr, wkrtjdwk, sodyd, wkrtjdtime)
        return redirect(url_for('index'))

@app.route('/view/<idx>')
def view(idx):
    if 'ID' in session:
        qustn = wkrtjd3(idx)
        return render_template('view.html', data=qustn)
    else:
        return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rptlvks')
def rptlvks():
    if 'ID' in session:
        qustn = wkrtjd2()
        return render_template('board.html', data=qustn)
    else:
        return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_id = request.form.get('user_id')
        user_pw = request.form.get('user_pw')
        ret = get_user(user_id, user_pw)
        if len(ret) !=0:
            session['ID'] = user_id
            session['PW'] = user_pw
            data = session['ID']
            return redirect(url_for('index'))
        else:
            return 'Login Failed'

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        print add_user(ID=request.form['ID'],PW=request.form['PW'],Email=request.form['Email'])
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('ID','PW')
    return redirect(url_for('login'))

@app.route('/secret')
def secret():
    if 'ID' in session:
        return render_template('secret.html')
    else:
        return 'xxx'

@app.route('/zzz', methods=['GET', 'POST'])
def zzz():
    if request.method=='GET':
        return render_template('writing.html')
    else:
        print add_writ(title=request.form.get('title'))
        return render_template('index.html')

@app.route('/movie')
def movie():
    movie = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
    soup = BeautifulSoup(movie.text,'html.parser')

    res = []
    abc = soup.find_all('td','title')

    for i in abc:
        res.append(i.text)
    return render_template('res.html', abc =res)

if __name__ == '__main__':
    app.run(debug=True, port =8686, host='0.0.0.0')

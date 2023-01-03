#import library
from ast import pattern
from flask import Flask, render_template, request, redirect, url_for, flash, redirect, request, session, flash, jsonify
from auth import login
from flask_mysqldb import MySQL
import mysql.connector
import urllib.request
import json


#inisiasi object flask
application = Flask(__name__)
application.secret_key = "wiro212sableng"

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='pilkadiksi')

@application.route('/')
@application.route('/home/')
def home():
    return render_template('/home/landingpage.html')

@application.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != '181910203' and request.form['password'] != 'nurul@26':
            flash('Invalid username/password','danger')
        else:
            session ['logged_in'] = True
            flash('Login successful','success')
            return redirect(url_for('index'))
    return render_template('/home/login.html')

@application.route('/register/')
def register():
    return render_template('/home/register.html')

# untuk loginadmin
@application.route('/loginadmin/', methods=['GET', 'POST'])
def loginadmin():
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['password'] != 'pnj21':
            flash('Invalid username/password','danger')
        else:
            session ['logged_in'] = True
            flash('Login successful','success')
            return redirect(url_for('indexadmin'))
    return render_template('/home/loginadmin.html')

# untuk logout
@application.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('Logout successful','success')
    return redirect(url_for('login'))


# untuk Admin
@application.route('/index/')
def index():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from mahasiswa"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/index.html', datamahasiswa = output_json)

@application.route('/icons/')
def icons():
    return render_template('/home/icons.html')

@application.route('/daftarakun/')
def daftarakun():
    return render_template('/home/daftarakun.html')

@application.route('/hasilvoting/')
def hasilvoting():
    return render_template('/home/hasilvoting.html')



if __name__ == '__main__':
    application.run(debug=True)
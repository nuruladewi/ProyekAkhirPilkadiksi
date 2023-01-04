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
    if request.method == 'GET':
        return render_template('/home/login.html')
    elif request.method == 'POST':
        
        NIM = request.form['NIM']
        password = request.form['password']
        if (NIM != '' and password !=''):
            db = getMysqlConnection()
            cur = db.cursor()
            cur.execute ("SELECT * from `login` WHERE `NIM`='"+NIM+"'") 
            data= cur.fetchone()
            if data[1] == password: 
                if data == None:
                    notif = "NIM Salah"
                    return render_template('/home/login.html')
                elif data[1]==password:
                    notif = "Halo " + NIM
                    return render_template('/home/dumpAdmin.html',notif=notif)   
            else:
                cur.execute ("SELECT * from `admin` WHERE `NIM`='"+NIM+"'") 
                data= cur.fetchone()
                if data[1]==password:
                    notif = "Halo " + NIM
                    return render_template('/home/dumpAdmin.html', notif=notif)
                else:
                    notif = "Password salah"
                    return render_template('/home/login.html',
                    notif=notif)
        else:
            return render_template('/home/login.html')
@application.route('/register/')
def register():
    return render_template('/home/register.html')

# untuk loginadmin

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
    return render_template('/home/daftarakun.html', dataanggota = output_json)

@application.route('/hasilvoting/')
def hasilvoting():
    return render_template('/home/hasilvoting.html')



if __name__ == '__main__':
    application.run(debug=True)
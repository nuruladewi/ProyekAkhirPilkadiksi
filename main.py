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
    return render_template('/home/daftarakun.html', dataakun = output_json)

@application.route('/addakun/', methods=['GET','POST'])
def addakun():
    if request.method == 'GET':
        return render_template('/home/addakun.html')
    elif request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        password = request.form['password']
        jurusan = request.form['jurusan']
        db = getMysqlConnection()
        
        try:
            cur = db.cursor()
            sukses = "data berhasil ditambah"
            sqlstr = f"INSERT INTO `mahasiswa` (`nim`, `nama`, `password`, `jurusan`) VALUES ("+nim+",'"+nama+"', '"+password+"','"+jurusan+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            datamahasiswa = cur.fetchall()
            print(sukses)
        except Exception as e:
            print("Error in SQL :\n", e)
        finally:
            db.close()
        return redirect(url_for('daftarakun'))
    else:
        return render_template('/home/addakun.html', datamahasiswa)



@application.route('/hasilvoting/')
def hasilvoting():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from hasil_voting"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/hasilvoting.html', hasilvoting = output_json)

@application.route('/addvoting/', methods=['GET','POST'])
def addvoting():
    if request.method == 'GET':
        return render_template('/home/addvoting.html')
    elif request.method == 'POST':
        nim = request.form['nim']
        pilihan = request.form['pilihan']
        db = getMysqlConnection()
        
        try:
            cur = db.cursor()
            sukses = "data berhasil ditambah"
            sqlstr = f"INSERT INTO `hasil_voting` (`nim`, `pilihan`) VALUES ("+nim+","+pilihan+");"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            print('sukses')
            datavoting = cur.fetchall()
            print(sukses)
        except Exception as e:
            print("Error in SQL :\n", e)
        finally:
            db.close()
        return redirect(url_for('suksesvote'))
    else:
        return render_template('/home/addvoting.html', datavoting)

@application.route('/suksesvote/')
def suksesvote():
    if request.method == 'GET':
        return render_template('/home/suksesvote.html')
    elif request.method == 'POST':
        return redirect(url_for('home'))
    else:    
        return render_template('/home/suksesvote.html')



if __name__ == '__main__':
    application.run(debug=True)
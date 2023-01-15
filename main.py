#import library
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
        
        nim= request.form['nim']
        password = request.form['password']
        if (nim != '' and password !=''):
            db = getMysqlConnection()
            cur = db.cursor()
            cur.execute ("SELECT * from `mahasiswa` WHERE `nim`='"+nim+"'") 
            data= cur.fetchone()
            if data[2] == password: 
                if data[2] == None:
                    notif = "Username Salah"
                    return render_template('/home/login.html', notif=notif)
                elif data[2]==password:
                    notif = data[1]
                    return render_template('/home/lihatkandidatuser.html', notif=notif)
        else:
            return render_template('/home/login.html')
        cnim=nim
        return nim

@application.route('/loginadmin/', methods=['GET', 'POST'])
def loginadmin():
    if request.method == 'GET':
        return render_template('/home/loginadmin.html')
    elif request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        
        if (username != '' and password !=''):
            db = getMysqlConnection()
            cur = db.cursor()
            cur.execute ("SELECT * from `admin` WHERE `username`='"+username+"'") 
            data= cur.fetchone()
            if data[1] == password: 
                if data == None:
                    notif = "username Salah"
                    return render_template('/home/loginadmin.html', notif=notif)
                elif data[1]==password:
                    notif = "Halo " + username
                    return render_template('/home/index.html',notif=notif)
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
@application.route('/logoutadmin/')
def logoutadmin():
    session.pop('logged_in', None)
    flash('Logout successful','success')
    return redirect(url_for('loginadmin'))

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

@application.route('/editakun/<int:nim>/')
def editakun(nim):
    db = getMysqlConnection()
    try:
        sqlstr = f"SELECT * from mahasiswa where nim={nim}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchone()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('/home/editakun.html', datamahasiswa = output_json)

@application.route('/editedakun/<int:nim>/')
def editedakun(nim):
    db = getMysqlConnection()
    nama = request.form['nama']
    password = request.form['password']
    jurusan = request.form['jurusan']
        
    try:
        sqlstr = f"SELECT * from mahasiswa where nim={nim}"
        cur = db.cursor()
        cur.execute(sqlstr)
        old_data = cur.fetchone()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)

    if len(nama) == 0:
        nama = old_data[0][1]
    if len(password) == 0:
        password = old_data[0][2]
    if len(jurusan) == 0:
        jurusan = old_data[0][3]
        
    try:
        cur = db.cursor()
        sqlstr = f"update mahasiswa set nama = '{nama}', password = '{password}', jurusan = {jurusan}"             
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        print('sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('daftarakun'))

@application.route('/deleteakun/<int:nim>', methods=['GET', 'POST'])
def deleteakun(nim):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sqlstr = f"delete from mahasisw where nim={nim}"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        print('deleted sukses')
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return redirect(url_for('daftarakun'))

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

@application.route('/suksesvote/')
def suksesvote():
    if request.method == 'GET':
        return render_template('/home/suksesvote.html')
    elif request.method == 'POST':
        return redirect(url_for('home'))
    else:    
        return render_template('/home/suksesvote.html')

@application.route('/kandidat/')
def kandidat():
    return render_template('/home/lihatkandidat.html')

@application.route('/pilihkandidat/')
def pilihkandidat():
    return render_template('/home/lihatkandidatuser.html')
@application.route('/voting/', methods=['GET','POST'])
def voting():

    if request.method == 'GET':
        db = getMysqlConnection()
        try:
            sqlstr = "SELECT * from kandidat"
            cur = db.cursor()
            cur.execute(sqlstr)
            output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template('/home/voting.html', kandidat=output_json)
    elif request.method == 'POST':
        nim = request.form['nim']
        pilihan = request.form['pilihan']
        db = getMysqlConnection()
        
        try:
            cur = db.cursor()
            sukses = "data berhasil ditambah"
            sqlstr = f"INSERT INTO `hasil_voting` (`nim`, `pilihan`) VALUES ("+nim+",'"+pilihan+"');"
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
        return render_template('/home/voting.html', datavoting)




if __name__ == '__main__':
    application.run(debug=True)
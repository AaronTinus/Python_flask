from flask_bootstrap import Bootstrap5
from flask import Flask, url_for, redirect, request, render_template, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__) 
UPLOAD_FOLDER = "C:\Users\aaron\Documents\Project_Oct10\uploads/"
DOWNLOAD_FOLDER = "/images/<u_name>"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'xxxxxxx'
app.config['MYSQL_DB'] = 'flask_db'
mysql = MySQL(app)
#bootstrap for styling
bootstrap = Bootstrap5(app)
@app.route('/', methods=['GET', 'POST'])
def hello_world(): 
    if request.method == "GET":
        return "My Flask Project"
    if request.method == "POST":
        return "Hello POST"
    
@app.route('/form', methods=['GET', 'POST'])   #post user information and image or file
def form_world(): 
    if request.method == "GET":
        return render_template("Form.html")
    if request.method == "POST":
        u_name_server = request.form['user_name']
        u_age_server = request.form['user_age']
        u_city_server = request.form['user_city']
        users_file = request.files['user_file']
        users_file.seek(0)
        to_screen = users_file.filename
        print(users_file.filename)
        users_file.save(UPLOAD_FOLDER + users_file.filename)
        #save data to database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO user_info VALUES ('{0}', '{1}', '{2}', '{3}');".format( u_name_server, u_age_server, u_city_server, users_file.filename))
        mysql.connection.commit()
        return render_template("result.html", u_name = u_name_server, u_age = int(u_age_server), u_city = u_city_server, u_file = to_screen)
    
@app.route('/user_list', methods=['GET', 'POST']) #end point for user list information to be displayed
def user_list(): 
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user_info")
        account = cursor.fetchall()
        print(account)
        return render_template("list.html", user_list = account)


# trying to link filename from mysql to url path


# @app.route('/u_profile/<u_name>', methods=['GET', 'POST']) 
# def u_profile(u_name): 
#      if request.method == "GET":
#         user_file.read['users_file.filename']
#         user_file.seek(0)
#         to_screen = user_file.filename
#         print(user_file.filename)
#         user_file.read(DOWNLOAD_FOLDER + user_file.filename)
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("SELECT * FROM user_info WHERE user_name = '{0}'".format(u_name, to_screen))
#         account = cursor.fetchmany()
#         print(account)
#         return render_template("user.html", user_list = account)



@app.route('/user_info/<u_name>', methods=['GET', 'POST'])  #end point to access each users info
def user_info(u_name): 
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user_info WHERE user_name = '{0}'".format(u_name))
        account = cursor.fetchmany()
        print(account)
        return render_template("user.html", user_list = account)   

@app.route('/u_profile/<u_name>', methods=['GET', 'POST']) #end point with profile user information
def u_profile(u_name): 
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user_info WHERE user_name = '{0}'".format(u_name))
        account = cursor.fetchmany()
        print(account)
        return render_template("profile.html", user_list = account)   




@app.route('/home', methods=['GET', 'POST']) # end point for the home page
def a_world(): 
    if request.method == "GET":
        return render_template("home.html")
    
@app.route('/b', methods=['GET', 'POST']) # end point to diplay data base list
def b_world(): 
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user_info")
        account = cursor.fetchall()
        print('Data')
        return render_template("b.html", user_list = account)    

if __name__ == '__main__': 
    print("hello")
    app.run(port=8080, debug=True)
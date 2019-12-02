#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect, url_for, request
import psycopg2
import re
import hashlib
app = Flask(__name__)

LogIn = "Log In"

#home page route
@app.route('/')
def home():
    return render_template('index.html', error ="Log In")

#login page route
@app.route('/Login.html', methods=['GET','POST'])
def login():
    bool1 = False
    bool2 = False
    error = None
    
    #takes the username and password from box
    username = request.values.get('username')
    password = request.values.get("password")

    #connect to DB
    conn = psycopg2.connect("host=ec2-23-23-92-204.compute-1.amazonaws.com dbname=d1fs1cm170ct9t user=gxupvblzzfulmn password=6f218f9e00cb85e2d96043b8a25898951fd0fbd475a5bcbeb9eb2ba4cc42d072")
    cur = conn.cursor()

    #SQL Command to get DB info
    cur.execute("SELECT email,password,firstname FROM members WHERE email = email AND password = password")
    user = cur.fetchall()
    for i in user:
        print(i)
	#Check to see if username and password match
        if i[0] == username and i[1] == hash(password):
            bool1 = True
            LogIn = i[2]
            break
        else:
	    #set the name to Login
            LogIn = "LogIn"
    
    if bool1 == True:
        return render_template('/index.html', error = LogIn)
    else:
        if username != None and password != None:
            error = "Invalid Email or Password"

    return render_template('/Login.html',error = error)

#index page route
@app.route('/index.html')
def index():
    return render_template('index.html', error = LogIn)

#upperbody route
@app.route('/UpperBody_Main.html')
def upper():
    return render_template('UpperBody_Main.html', error = LogIn)

#LowerBody route
@app.route('/LowerBody_Main.html')
def lower():
    return render_template('LowerBody_Main.html', error = LogIn)

#Cardio route
@app.route('/Cardio_Main.html')
def cardio():
    return render_template('Cardio_Main.html', error = LogIn)

#hash function
def hash(password):
    hashObj = hashlib.md5(password.encode())
    return hashObj.hexdigest();

#SignUp Function
@app.route('/SignUp.html', methods=['GET','POST'])
def signup():
    error = None;
    if request.values.get('firstname') != None:
        #Get all the textbox input
        firstName = request.values.get('firstname')
        lastName = request.values.get('lastname')
        password = request.values.get('password')
        confirm = request.values.get('confirm')
        email = request.values.get('email')

	#check if email matches email format
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            error = 'Invalid Email address, please try again.'
            return render_template('SignUp.html', error = error)
        else:
            if password == confirm:
		
		#connect to DB
                conn = psycopg2.connect("host=ec2-23-23-92-204.compute-1.amazonaws.com dbname=d1fs1cm170ct9t user=gxupvblzzfulmn password=6f218f9e00cb85e2d96043b8a25898951fd0fbd475a5bcbeb9eb2ba4cc42d072")
                cur = conn.cursor()
		
		#Push to DB
                insert_query = "INSERT INTO members VALUES('" + str(email) + "', '" + str(hash(password)) + "', '" + str(firstName) + "', '" + str(lastName) + "')"

                cur.execute(insert_query)
                conn.commit()
                Error = None
                return render_template('Login.html')
            else:
                if password != None and confirm != None:
                    #Throw Error
                    error = 'Passwords did not match, please try again.'
                    return render_template('SignUp.html',error = error)

    return render_template('SignUp.html')


if __name__ == '__main__':
    app.run(debug=True)

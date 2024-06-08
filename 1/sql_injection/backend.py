#!/home/sudharsan/myenv/bin/python3
from flask import Flask, request,render_template, abort, redirect, url_for
import logging
import os
import sqlite3

connection=sqlite3.connect('user.db')
cursor=connection.cursor()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
data={}

app = Flask(__name__, static_url_path='/static')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

def check_admin(name,password):
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()
    query="SELECT * FROM user WHERE name='"+name+"' AND password='"+password+"'"
    result = cursor.execute(query)
    if result.fetchone():
        cursor.close()
        connection.close()
        return True
    else:
        cursor.close()
        connection.close()
        return False

@app.route('/',methods=['GET'])
@app.route('/generate204',methods=['GET'])
def captiveportal():
    return render_template('index.html')

@app.route('/login',methods=['POST'])
def login():
    client_mac = request.headers.get('Client-MAC')
    print("Requester MAC:", client_mac)
    data = request.form.to_dict()   
    print("Requested Data: " + str(data)) 
    name=data['name']
    password=data['password']

    if(check_admin(name,password)):
        print("admin logged-in")
        return 'admin'
    else:
        return 'normal_user'
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  
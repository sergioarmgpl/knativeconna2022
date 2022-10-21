from flask import Flask, request
import mysql.connector
import os
import sys

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'It works'

def insert(data):
    conn = mysql.connector.connect(
     host=os.environ['HOST'],
     user=os.environ['MYSQL_USER'],
     password=os.environ['MYSQL_PASSWORD'],
     database=os.environ['MYSQL_DATABASE']
    )

    cursor = conn.cursor()
    red_led = data["red_led"]
    green_led = data["green_led"]
    sql = "INSERT INTO metric "+\
          "(red_led,green_led,time) "+\
          f"VALUES ({red_led},{green_led},now());"
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()


@app.route('/led',methods = ['POST'])
def device():
    data = request.json
    print(data)
    insert(data)
    return "processed"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
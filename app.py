from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = 'Sandy@123'  # Change this

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sandy@123'  # Change this
app.config['MYSQL_DB'] = 'uber_analytics_db'

mysql = MySQL(app)

# Home route
@app.route('/')
def index():
    if 'loggedin' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', 
                      (username, password))
        account = cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['username'] = account['username']
            session['user_type'] = account['user_type']
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect username/password!'
    
    return render_template('login.html', msg=msg)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_type = request.form.get('user_type', 'rider')
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO users (username, password, email, user_type) VALUES (%s, %s, %s, %s)',
                         (username, password, email, user_type))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    
    return render_template('register.html', msg=msg)

# Logout route
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# Analytics API endpoints
@app.route('/api/rides_by_category')
def rides_by_category():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT category, COUNT(*) as count 
                     FROM rides GROUP BY category''')
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/rides_by_hour')
def rides_by_hour():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT HOUR(start_date) as hour, COUNT(*) as count 
                     FROM rides GROUP BY hour ORDER BY hour''')
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/popular_routes')
def popular_routes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT start_location, end_location, 
                     COUNT(*) as frequency, ROUND(AVG(miles), 2) as avg_miles
                     FROM rides 
                     GROUP BY start_location, end_location
                     ORDER BY frequency DESC LIMIT 10''')
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/monthly_trends')
def monthly_trends():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT DATE_FORMAT(start_date, '%Y-%m') as month,
                     COUNT(*) as total_rides, ROUND(SUM(miles), 2) as total_miles
                     FROM rides GROUP BY month ORDER BY month''')
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/stats')
def get_stats():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Total rides
    cursor.execute('SELECT COUNT(*) as total FROM rides')
    total_rides = cursor.fetchone()['total']
    
    # Total miles
    cursor.execute('SELECT ROUND(SUM(miles), 2) as total FROM rides')
    total_miles = cursor.fetchone()['total']
    
    # Average miles per ride
    cursor.execute('SELECT ROUND(AVG(miles), 2) as avg FROM rides')
    avg_miles = cursor.fetchone()['avg']
    
    return jsonify({
        'total_rides': total_rides,
        'total_miles': total_miles,
        'avg_miles': avg_miles
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

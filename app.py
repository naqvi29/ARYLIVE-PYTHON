from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flaskext.mysql import MySQL
import pymysql
from datetime import datetime
import requests
import os
import json
from flask_caching import Cache


app = Flask(__name__)
mysql = MySQL()

app.secret_key = "LMNUrAcLmU"

# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'SimpleCache'  # Use in-memory cache for simplicity
app.config['CACHE_DEFAULT_TIMEOUT'] = 60  # Cache timeout in seconds (e.g., 300 seconds = 5 minutes)

cache = Cache(app)

# MySQL configuration for remote server
app.config['MYSQL_DATABASE_HOST'] = '50.7.252.10' 
app.config['MYSQL_DATABASE_USER'] = 'liveary_yt' 
app.config['MYSQL_DATABASE_PASSWORD'] = '@fF?Bxu!Tn=%pQnP;c' 
app.config['MYSQL_DATABASE_DB'] = 'liveary_ytlive'  

mysql.init_app(app)

@app.context_processor
def inject_common_variables():
    if 'loggedin' in session:
        return dict(role=session['role'])
    return dict(role=None)

def convert_to_12h(time_str):
    # Convert string to datetime object
    time_obj = datetime.strptime(time_str, '%H:%M')

    # Format the datetime object to 12-hour time format
    time_12h = time_obj.strftime('%I:%M %p')

    return time_12h

@app.route("/")
def index():
    try:
        if 'loggedin' in session:
            return render_template("index.html")
        else:
            return redirect(url_for('login'))    
    except Exception as e:
        return render_template('error.html', error=e)

@app.route("/arynews-stats", methods = ['GET','POST'])
def arynews_stats():
    try:
        if 'loggedin' in session:
            if request.method == 'POST':
                from_date = request.form.get("from_date")
                from_time = request.form.get("from_time")
                to_date = request.form.get("to_date")
                to_time = request.form.get("to_time")    
                with mysql.get_db().cursor(pymysql.cursors.DictCursor) as cursor:
                    if from_time == to_time and from_date==to_date and from_time:
                        sql_query = f"SELECT * FROM `newslive` WHERE date = '{from_date}' AND new_time = '{from_time}';"
                    elif from_time and from_date == to_date:
                        sql_query = f"SELECT * FROM `newslive` WHERE new_time BETWEEN '{from_time}' AND '{to_time}' AND (date = '{to_date}');"
                    elif not from_time and from_date == to_date:
                        sql_query = f"SELECT * FROM `newslive` WHERE date BETWEEN '{from_date}' AND '{to_date}';"
                    else:
                        sql_query = f"SELECT * FROM `newslive` WHERE date BETWEEN '{from_date}' AND '{to_date}' AND ((date = '{from_date}' AND new_time >= '{from_time}') OR (date = '{to_date}' AND new_time <= '{to_time}'));"
                    cursor.execute(sql_query)
                    results = cursor.fetchall()
                return render_template("arynews-stats.html", results=results, from_date=from_date, from_time=from_time, to_date=to_date, to_time=to_time)

            with mysql.get_db().cursor(pymysql.cursors.DictCursor) as cursor:
                today_date = datetime.now().strftime("%Y-%m-%d")
                sql_query = f"SELECT * FROM newslive WHERE date='{today_date}' ORDER BY ID DESC;"
                cursor.execute(sql_query)
                results = cursor.fetchall()
                
            # Render the template with fetched data
            return render_template("arynews-stats.html", results=results)

        else:
            return redirect(url_for('login'))  
    except Exception as e:
        return render_template('error.html', error=e)

@app.route("/ary-all-cdn-stats", methods = ['GET','POST'])
def ary_all_cdn_stats():
    try:
        if 'loggedin' in session:
            if session['role'] == 'admin':
                if request.method == 'POST':
                    from_date = request.form.get("from_date")
                    from_time = request.form.get("from_time")
                    to_date = request.form.get("to_date")
                    to_time = request.form.get("to_time")    
                    with mysql.get_db().cursor(pymysql.cursors.DictCursor) as cursor:
                        if from_time == to_time and from_date==to_date and from_time:
                            sql_query = f"SELECT * FROM `cdnstats` WHERE date = '{from_date}' AND new_time = '{from_time}';"
                        elif from_time and from_date == to_date:
                            sql_query = f"SELECT * FROM `cdnstats` WHERE new_time BETWEEN '{from_time}' AND '{to_time}' AND (date = '{to_date}');"
                        elif not from_time and from_date == to_date:
                            sql_query = f"SELECT * FROM `cdnstats` WHERE date BETWEEN '{from_date}' AND '{to_date}';"
                        else:
                            sql_query = f"SELECT * FROM `cdnstats` WHERE date BETWEEN '{from_date}' AND '{to_date}' AND ((date = '{from_date}' AND new_time >= '{from_time}') OR (date = '{to_date}' AND new_time <= '{to_time}'));"
                        cursor.execute(sql_query)
                        results = cursor.fetchall()
                    return render_template("ary-all-cdn-stats.html", results=results, from_date=from_date, from_time=from_time, to_date=to_date, to_time=to_time)

                with mysql.get_db().cursor(pymysql.cursors.DictCursor) as cursor:
                    today_date = datetime.now().strftime("%Y-%m-%d")
                    sql_query = f"SELECT * FROM cdnstats WHERE date='{today_date}' ORDER BY ID DESC;"
                    cursor.execute(sql_query)
                    results = cursor.fetchall()
                    
                # Render the template with fetched data
                return render_template("ary-all-cdn-stats.html", results=results)

            else:
                return render_template("error-405.html") 
        else:
            return redirect(url_for('login'))  
    except Exception as e:
        return render_template('error.html', error=e)

@app.route("/all-competitor-stats", methods = ['GET','POST'])
def all_competitor_stats():
    try:
        if 'loggedin' in session:
            if session['role'] == 'admin':
                if request.method == 'POST':
                    from_date = request.form.get("from_date")
                    from_time = request.form.get("from_time")
                    to_date = request.form.get("to_date")
                    to_time = request.form.get("to_time")    
                    with mysql.get_db().cursor(pymysql.cursors.DictCursor) as cursor:
                        if from_time == to_time and from_date==to_date and from_time:
                            sql_query = f"SELECT * FROM `youtubelive` WHERE date = '{from_date}' AND new_time = '{from_time}';"
                        elif from_time and from_date == to_date:
                            sql_query = f"SELECT * FROM `youtubelive` WHERE new_time BETWEEN '{from_time}' AND '{to_time}' AND (date = '{to_date}');"
                        elif not from_time and from_date == to_date:
                            sql_query = f"SELECT * FROM `youtubelive` WHERE date BETWEEN '{from_date}' AND '{to_date}';"
                        else:
                            sql_query = f"SELECT * FROM `youtubelive` WHERE date BETWEEN '{from_date}' AND '{to_date}' AND ((date = '{from_date}' AND new_time >= '{from_time}') OR (date = '{to_date}' AND new_time <= '{to_time}'));"
                        cursor.execute(sql_query)
                        results = cursor.fetchall()
                    return render_template("all-competitor-stats.html", results=results, from_date=from_date, from_time=from_time, to_date=to_date, to_time=to_time)

                with mysql.get_db().cursor(pymysql.cursors.DictCursor) as cursor:
                    today_date = datetime.now().strftime("%Y-%m-%d")
                    sql_query = f"SELECT * FROM youtubelive WHERE date='{today_date}' ORDER BY ID DESC;"
                    cursor.execute(sql_query)
                    results = cursor.fetchall()
                    
                # Render the template with fetched data
                return render_template("all-competitor-stats.html", results=results)

            else:
                return render_template("error-405.html") 

        else:
            return redirect(url_for('login'))  
    except Exception as e:
        return render_template('error.html', error=e)

@app.route("/login", methods=['GET','POST'])
def login():    
    try:
        if request.method == 'POST':
            username = request.form.get("username")
            password  = request.form.get("password")
            with mysql.get_db().cursor(pymysql.cursors.DictCursor) as cursor:
                sql_query = f"SELECT * FROM users WHERE username='{username}';"
                cursor.execute(sql_query)
                user = cursor.fetchone()
            if user:
                if password == user['password']:
                    session['loggedin'] = True
                    session['name'] = user['username']
                    session['role'] = user['role']
                    if user['role'] == 'admin':
                        return redirect(url_for("index"))
                    elif user['role'] == 'agency':
                        return redirect(url_for("arynews_stats"))
                else:
                    return render_template("login.html",error="Invalid Credentials!")  
            else:            
                return render_template("login.html",error="Invalid User!") 
        
        if 'loggedin' in session:
            return redirect(url_for("logout"))
        return render_template("login.html")
    except Exception as e:
        return render_template('error.html', error=e)

@app.route("/logout")
def logout():
    try:
        session.pop('loggedin', None)
        session.pop('name', None)
        session.pop('role', None)
        # Redirect to index page
        return redirect(url_for('login'))
    except Exception as e:
        return render_template('error.html', error=e)

@app.route("/setting", methods=['GET','POST'])
def setting():
    try:
        if request.method == 'POST':
            newJson = {
                "arynewsyt":request.form.get("arynewsyt"),
                "geonewsyt":request.form.get("geonewsyt"),
                "samaanewsyt":request.form.get("samaanewsyt"),
                "dunyanewsyt":request.form.get("dunyanewsyt"),
                "expressnewsyt":request.form.get("expressnewsyt"),
                "humnewsyt":request.form.get("humnewsyt")
            }
            
            with open("stream_urls.json", 'w') as f:
                f.write(json.dumps(newJson))

                
                # stream_ids = json.loads(f.read())
            return redirect("/setting?updated=True")

        
        with open("stream_urls.json", 'r') as f:
            stream_ids = json.loads(f.read())
        if request.args.get("updated"):
            updated =True
        else:
            updated = False
        return render_template("setting.html",data =stream_ids, updated = updated)
    except Exception as e:
        return render_template('error.html', error=e)

@app.route("/ytstats-api")
@cache.cached(timeout=60)
def yt_stats_api():
    with open("stream_urls.json", 'r') as f:
        stream_ids = json.loads(f.read())
    DATA = []
    for key, value in stream_ids.items():
        URL = f"https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id={value}&fields=items%2FliveStreamingDetails%2FconcurrentViewers&key=AIzaSyBKt1-mpNqEiROMiW4g2OT8MjF5DvSyl7U"
        r = requests.get(url = URL)
        data = r.json()
        try:
            concurrentViewers = data['items'][0]['liveStreamingDetails']['concurrentViewers']
        except:
            concurrentViewers = '...'
        DATA.append({key:concurrentViewers})
    return jsonify(DATA)

if __name__ == '__main__':
    app.run()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from flask import Flask, render_template, request, redirect, url_for, session
import os
import time

FIREFOX_BINARY = "/home/nou/DevTools/browsers/firefox/firefox" # change if you want

app = Flask(__name__)
app.secret_key = os.urandom(32).hex()
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
admin_password = "lebah" + os.urandom(6).hex()
print(f"Admin password: {admin_password}")
FLAG = 'BEECTF{f4k3_fl4g}'

USER_DATA = {
    'admin': admin_password,
    'asep': 'Admin#123',
    'beluga':'belugagans123'
}

@app.route('/')
def home():
    if 'username' in session:
        password = request.args.get('pass') or ""
        the_flag = ""
        if session['username'] == 'admin':
            the_flag = FLAG

        if password in session['password']:
            return render_template("home.html", username=session['username'], password=password, flag=the_flag)
        return render_template("home.html", username=session['username'], flag=the_flag)

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USER_DATA and USER_DATA[username] == password:
            session['username'] = username
            session['password'] = password
            return redirect(url_for('home'))
        error = 'Invalid credentials'
    return render_template("login.html", error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))

@app.route('/report')
def report():
    visit_url = request.args.get('url') or ""

    if not visit_url:
        return "A URL must be provided for the bot to follow.", 400

    if not visit_url.startswith("http://") and not visit_url.startswith("https://"):
        return "Only http and https protocol allowed.", 400
    driver = None
    try:
        options = Options()
        options.binary_location = FIREFOX_BINARY # change if you want
        #options.add_argument('--headless') # comment line if you want firefox visible
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-translate')


        driver = webdriver.Firefox(options=options)
        driver.get("http://127.0.0.1:9999")
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys(admin_password)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

        print(f"[X] Request by: {request.remote_addr} | Bot is visiting: {visit_url}")
        driver.get(visit_url)
        time.sleep(30)

        message = "Success."
        status_code = 200
    except Exception:
        import traceback
        traceback.print_exc()
        raise
    finally:
      if driver is not None:
        driver.quit()

    return message, status_code

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True) # ACTUAL CTF has ssl_context='adhoc'

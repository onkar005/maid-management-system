from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, IntegerField  
from wtforms.validators import Email,Required
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import date, datetime
import difflib


#creating an app instance
app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Onkarbiyani5@'
app.config['MYSQL_PORT'] =  3306
app.config['MYSQL_DB'] = 'maid'
#we want results from the database to be returned as dictionary, by default its a tuple
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)

#Index
@app.route('/')
def index():
    return render_template('home.html')


#Register Form Class
class RegisterFormUser(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=1, max=25)])
    email = StringField('Email', [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    address = StringField('Address', [validators.Length(min=1, max=100)])

class RegisterFormMaid(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    username = StringField('Username', [validators.Length(min=1, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    mob_no = StringField('Moblie Number', [validators.length(min=10, max=10)])
    address = StringField('Address', [validators.Length(min=1, max=100)])
    skills =  StringField('Skills (comma separated)', [validators.Length(min=1, max=100)])

#user register
@app.route('/registeruser', methods=['GET','POST'])
def registeruser():
    form = RegisterFormUser(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        address = form.address.data
    
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT into users(name, email, username, password, address) VALUES(%s,%s,%s,%s,%s)",(name, email, username, password, address))

        #Commit to DB
        mysql.connection.commit()

        #close connection
        cur.close()

        #for flash messages taking parameter and the category of message to be flashed
        flash("You are now registered and can log in", "success")
        
        #when registration is successful redirect to home
        return redirect(url_for('login'))
    return render_template('registeruser.html', form = form)

#Maid register
@app.route('/registermaid', methods=['GET','POST'])
def registermaid():
    form = RegisterFormMaid(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        mob_no = form.mob_no.data
        address = form.address.data
        skills = form.skills.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute Query
        cur.execute("INSERT into maid(name, email, username, password, mob_no, address, skills) VALUES(%s,%s,%s,%s,%s,%s,%s)",(name, email, username, password,int(mob_no),address, skills))

        #Commit to DB
        mysql.connection.commit()

        #close connection
        cur.close()

        #for flash messages taking parameter and the category of message to be flashed
        flash("You are now registered and can log in", "success")
        
        #when registration is successful redirect to home
        return redirect(url_for('login'))
    return render_template('registermaid.html', form = form)

#User login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get form fields
        #global username 
        username = request.form['username']
        password_candidate = request.form['password']

        #create cursor
        cur = mysql.connection.cursor()

        #get user by username

        result1 = cur.execute("SELECT * FROM Maid.users WHERE users.username = %s", [username] )
      
        if result1 == 1:
            #Get the stored hash
            data = cur.fetchone()
            password = data['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate, password):
                #Passed
                session['logged_in'] = True
                session['username'] = username

                flash("you are now logged in User","success")
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)
            #Close connection
            cur.close()
       
        result2=  cur.execute("SELECT * FROM Maid.maid WHERE maid.username = %s", [username] )


        if result2 == 1:
             #Get the stored hash
            data = cur.fetchone()
            password = data['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate, password):
                #Passed
                session['logged_in'] = True
                session['username'] = username

                flash("you are now logged in Maid","success")
                return redirect(url_for('dashboard_maid'))
            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)
            #Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

        
    return render_template('login.html')

#check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for('login'))
    return wrap

#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect(url_for('login'))

#Dashboard Maid
@app.route('/dashboard_maid', methods=['GET','POST', 'UPDATE'])

def dashboard_maid():
    #create cursor
    cur=mysql.connection.cursor()
    username= session['username']
    #Get Maid Skills
    
    result1 =cur.execute("SELECT skills from maid where username=%s", [username])
    result1=cur.fetchall()
    x=result1
   
    x = x[0]
    skill = x['skills']
    #print(skill)
    skill_lst = skill.split(",")
    #print(skill_lst)
    #y is job_req of a row from booking
    result2 = cur.execute("SELECT job_req,id from booking")
    result2=cur.fetchall()
    z=result2
    #print(result2)
    id_lst=[]
    for row in z:
                c = 0
                y = row["job_req"]
                id= row["id"]
                #print("y=",y)
                #print("skill_lst=",skill_lst)
                job_req_lst = y.split(",")
                #print("job_lst=",job_req_lst)

                if len(job_req_lst)>1:
                    for a in job_req_lst:
                        #print("a=",a)
                        m = difflib.get_close_matches(a, skill_lst)
                        #print("m=",m)
                        try:
                            if m[0] in skill_lst:
                                c = c+1
                                #print("c in loop=",c)
                        except:
                            pass
                else:
                    #print("ele=",job_req_lst[0])
                    m = difflib.get_close_matches(job_req_lst[0], skill_lst)
                    try:
                        if m[0] in skill_lst:
                            c = c+1
                    except:
                        pass
                #print("c = ", c)
                if len(job_req_lst) == c:
                    id_lst.append(id)
                else:
                    pass    
    #print("ID LIST",id_lst)
    id_tuple=tuple(id_lst)
    id_string=str(id_tuple)
    

    result= cur.execute("select * from booking")
    
    

    #result3 = cur.execute("SELECT id, customer_name,address, start_date, end_date, payment, total_days , job_req from booking where id in %s",[id_lst])
    format_strings = ','.join(['%s'] * len(id_lst))
    try:
        result3= cur.execute("SELECT id, customer_name,address, start_date, end_date, payment, total_days , job_req from booking where id in (%s)" % format_strings,tuple(id_lst))
    except:
        result3=0
    #print(result3)
    booking = cur.fetchall()

    #Get Dashboard 
    if result3>0:
            return render_template('dashboard_maid.html', booking = booking )
    else:
            msg='No Appointments Found'
    return render_template('dashboard_maid.html', msg=msg)

    #Get booking Details
    

    
 
    
    #close connection
    cur.close()

#Dashboard User
@app.route('/dashboard')

def dashboard():
    #create cursor
    cur=mysql.connection.cursor()
    username= session['username']
    #Get accepted Request
    result = cur.execute("SELECT maid_username,	start_date, end_date,payment  from accepted_request where username=%s",[username])

    accepted_request = cur.fetchall()
    #Get 
    if result>0:
        return render_template('dashboard.html', accepted_request = accepted_request)
    else:
        msg='No Request Accepted'
        return render_template('dashboard.html', msg=msg)
    #close connection
    cur.close()

# Booking Form (filled by user)

class BookingForm(Form):
    mob_no = StringField('Moblie Number', [validators.length(min=10, max=10)])
    start_date =  StringField('Start Date ', [validators.Length(min=1, max=15)])
    end_date =  StringField('End Date', [validators.Length(min=1, max=15)])
    job_req =  StringField('Job Requirement (Commna sepated)', [validators.Length(min=1, max=100)])
    payment = StringField('Payment (in Rs/Month)', [validators.Length(min=3, max=10)])


#Maid Booking
@app.route('/booking_form', methods=['GET','POST'])
def booking_form():
    # Create cursor
    cur = mysql.connection.cursor()
    form = BookingForm(request.form)
    if request.method == 'POST' and form.validate():
        username = session['username']
        #print(username)
        details = cur.execute("SELECT address,name FROM users WHERE username = %s", [username] )
        address_details = cur.fetchone()
        customer_name=address_details['name']
        address = address_details['address']
        mob_no = form.mob_no.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        job_req = form.job_req.data
        payment = form.payment.data
        
        d0 = datetime.strptime(start_date,"%Y-%m-%d")
        d1 = datetime.strptime(end_date,"%Y-%m-%d")
        delta = (d1 - d0)
        delta = str(delta)
        delta = delta.split(' ')[0]

        # Execute Query (inserting into booking table)
        cur.execute("INSERT into booking(customer_name, address, mob_no, start_date, end_date, job_req, payment,total_days,username) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(customer_name, address, mob_no, start_date, end_date, job_req,payment,delta,username))

        #Commit to DB
        mysql.connection.commit()

        #close connection
        cur.close()

        #for flash messages taking parameter and the category of message to be flashed
        flash("Your Requirement has been posted", "success")
        
        #when registration is successful redirect to home
        return redirect(url_for('dashboard'))
    return render_template('booking_form.html', form = form)



#Accept Request
@app.route('/accept_request/<string:id>', methods=['POST'])
@is_logged_in
def accept_request(id):
    
    #create cursor
    cur = mysql.connection.cursor()

    username= session['username']
    
    #Get maid name
    result = cur.execute("SELECT * from booking where id=%s", [id])

    accepted = cur.fetchone()

    #print(accepted)
    username=accepted['username']
    
    customer_name = accepted['customer_name']
    #print(customer_name)
    
    address = accepted['address']
    
    mob_no = accepted['mob_no']
    
    start_date = accepted['start_date']
    
    end_date = accepted['end_date']
    
    payment= accepted['payment']

    maid_username = session['username']
    print(maid_username)
    
    #execute
    cur.execute("INSERT into accepted_request(customer_name, address, mob_no, start_date, end_date, payment, maid_username,username) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(customer_name, address, mob_no, start_date, end_date, payment, maid_username,username))

    cur.execute("DELETE FROM booking WHERE id=%s", [id])

    #commit to DB
    mysql.connection.commit()

    #close connection
    cur.close()

    flash("Request Accepted", "success")

    return redirect(url_for('dashboard_maid'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port, debug=True)

    app.secret_key = "secret123"
    #when the debug mode is on, we do not need to restart the server again and again


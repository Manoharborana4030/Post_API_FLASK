from turtle import title
from flask import Flask,request,jsonify, make_response,render_template
import psycopg2 
import os 
from cryptography.fernet import Fernet 
import random 
from flask_mail import Mail, Message 
from functools import wraps 
import jwt 
 
 
 
app=Flask(__name__) 
 
app.config['MAIL_SERVER']='smtp.gmail.com' 
app.config['MAIL_PORT'] = 465 
app.config['MAIL_USERNAME'] = os.environ['USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['PASSWORD'] 
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True 
mail = Mail(app) 
 
key=os.environ['key'] 
fernet = Fernet(key) 
 
 
app.config['SECRET_KEY']=os.environ['SECRET_KEY']
 
def token_required(f): 
    @wraps(f) 
    def decorator(*args, **kwargs): 
        token = None 
        # pass jwt-token in headers 
        if 'Authorization' in request.headers: 
            token = request.headers['Authorization'] 
        if not token: # throw error if no token prov ided
            return make_response(jsonify({"message":  "A valid token is missing!"}), 401)
        try: 
            data = jwt.decode(token, app.config['SEC RET_KEY'], algorithms=['HS256'])
            conn=get_db_connection() 
            cur=conn.cursor() 
            cur.execute('SELECT * FROM users where u sername=%s;',(data['username'],))
            current_user =cur.fetchone() 
            cur.close() 
            conn.close() 
        except: 
            return make_response(jsonify({"message":  "Invalid token!"}), 401)
 
        return f(current_user, *args, **kwargs) 
    return decorator 
 
def get_db_connection(): 
    conn = psycopg2.connect(host='localhost', 
                            database='flask_redis_da tabase',
                            user=os.environ['DB_USER NAME'],
                            password=os.environ['DB_ PASSWORD'])
    return conn 
 
 
 
@app.route('/',methods=('GET', 'POST')) 
@token_required 
def home(current_user): 
    if request.method=='GET': 
        conn = get_db_connection() 
        cur = conn.cursor() 
        cur.execute('SELECT * FROM users;') 
        uers = cur.fetchall() 
        # print(uers) 
        cur.close() 
        conn.close() 
        return { 
            "users":uers 
        } 
    return  { 
                'status':200, 
                'Message':"Method is not valid" 
            } 
     
 
@app.route('/login/',methods=('GET', 'POST')) 
def login(): 
    if request.method=='POST': 
        status = None 
        conn=get_db_connection() 
        cur=conn.cursor() 
        username=request.json.get('username') 
        password=request.json.get('password') 
        if (username is None or password is None) or  (username=='' or password==''):
            return  { 
                        'status':400, 
                        'Message':"Please Enter User name,Password and email!!"
                    } 
        cur.execute('SELECT * FROM users where usern ame=%s;',(username,))
        query=cur.fetchone() 
        try: 
            if query: 
                check_password=fernet.decrypt(query[ 3].encode())
                check_password=check_password.decode ()
                if check_password==password: 
                    try: 
                        encrypted = fernet.encrypt(str(query).encode())
                        resp = encrypted.decode('utf -8')
                        # print(resp) 
                        status = True 
                    except Exception as e: 
                        status = False 
                        print("Error occured at line  no. 51", e)
                    if status: 
                        token = jwt.encode({'usernam e':username}, app.config['SECRET_KEY'], 'HS256')
                        print(token) 
                        return  {  
                                    'status' : 200,  
                                    'message':resp, 
                                    'Token':token 
                                }  
                    else: 
                        return  {  
                                    'status' : 400,  
                                    'message': 'something went wrong !'
                                }  
                else: 
                    return  { 
                                'status':200, 
                                'Message':"Please Enter Valid Password"
                            }  
            else: 
                return  { 
                            'status':200, 
                            'Message':"Please Enter  valid username"
                        }  
        except Exception as e: 
            print("Error occured at line no. 119", e )
            return { 
                        'status':501, 
                        'Message':"Internal error" 
                    } 
        finally: 
            print("Shutting Down DB Connection!!!!") 
            cur.close() 
            conn.close() 
    return  { 
                'status':200, 
                'Message':"Method is not valid" ,
                
            } 
 
@app.route('/register/', methods=('GET', 'POST')) 
def register(): 
    if request.method == 'POST': 
        conn = get_db_connection() 
        cur = conn.cursor() 
        fname=request.json.get('fname') 
        lname=request.json.get('lname') 
        username = request.json.get('username') 
        password = request.json.get('password') 
        email=request.json.get('email') 
        address=request.json.get('address') 
        if (username is None or password is None or  email is None) or (username=='' or password=='' or email==''):
            return  { 
                        'status':400, 
                        'Message':"Please Enter User name,Password and email!!"
                    } 
        try: 
            cur.execute('SELECT * FROM users where u sername=%s;',(username,))
            query=cur.fetchone() 
            if query: 
                return  { 
                            'status':400, 
                            'Message':"Username Alre ady Exits!!"
                        } 
            password_encrypted = fernet.encrypt(str( password).encode())
            password = password_encrypted.decode('ut f-8')
            try: 
                cur.execute('INSERT INTO users (user name, email, password, fname, lname, address)'
                            'VALUES (%s, %s, %s, %s,  %s, %s)',
                            (username, email, password, fname,lname,address))
                conn.commit() 
                return  { 
                            'status':200, 
                            'Message':"User Succesfu lly registerd!!"
                        } 
            except Exception as e: 
                print("Error occured at 114",e) 
        except Exception as e: 
            print("Error occured at 113 ",e) 
        finally:    
            print("Shutting Down DB Connection!!!!") 
            cur.close() 
            conn.close() 
    return  { 
                'status':200, 
                'Message':"Method is not valid" 
            } 
 
@app.route('/forgot_password/',methods=('GET','POST' ))       
def forgot_password(): 
    if request.method=='POST': 
        conn = get_db_connection() 
        cur = conn.cursor() 
        email=request.json.get('email') 
        if (email is None) or (email==''): 
            return  { 
                        'status':400, 
                        'Message':"Please Enter User name,Password and email!!"
                    } 
        cur.execute('SELECT * FROM users where email =%s;',(email,))
        query=cur.fetchone() 
        if query: 
            otp=random.randrange(1111,9999) 
            print(otp) 
            try: 
                msg = Message( 
                    'OTP Verfication', 
                    sender =os.environ['USERNAME'],
                    recipients = [email] 
                ) 
                msg.body = f'hello Your OTP is here  {otp}.'
                mail.send(msg) 
                print("Mail Send") 
                cur.execute('''UPDATE users  
                            SET OTP = %s  
                            WHERE username=%s;''',(otp,query[1],))
                conn.commit() 
                cur.close() 
                conn.close() 
                return  { 
                            'status':200, 
                            'Message':'OTP send Succ efully to your Email ID.'
                        } 
            except Exception as e: 
                print("Error Occured as ",e)             
        else: 
            return  { 
                        'status':200, 
                        'Message':"Please Enter vali d email!!"
                    } 
    return  { 
                'status':200, 
                'Message':"Method is not valid" 
            }   
 
 
@app.route('/change_password/',methods=('GET','POST' ))
def change_password(): 
    if request.method=='POST': 
        conn = get_db_connection() 
        cur = conn.cursor() 
        otp=request.json.get('otp') 
        if (otp is None) or (otp==''): 
            return  { 
                        'status':400, 
                        'Message':"Please Provide OT P!!"
                    } 
        cur.execute('SELECT * FROM users where OTP=% s;',(otp,))
        query=cur.fetchone() 
        if query: 
            new_password=request.json.get('new_passw ord')
            confirm_password=request.json.get('confi rm_password')
            if (new_password is None or confirm_password is None) or (new_password=='' or confirm_password==''):
                return  { 
                            'status':400, 
                            'Message':"Please Enter  Password!!"
                        } 
            if new_password==confirm_password: 
                password_encrypted = fernet.encrypt( str(confirm_password).encode())
                password = password_encrypted.decode ('utf-8')
                cur.execute('''UPDATE users  
                            SET password = %s  
                            WHERE username=%s;''',(password,query[1],))
                conn.commit() 
                cur.close() 
                conn.close() 
                return  { 
                            'status':200, 
                            'Message':"Your Password  has been updated.!!!"
                        } 
            else: 
                return  { 
                            'status':200, 
                            'Message':"Your Password  is Not matched"
                        } 
        else: 
            return  { 
                        'status':200, 
                        'Message':"OTP is Not Valid" 
                    } 
 
    return  { 
                'status':200, 
                'Message':"Method is not valid" 
            } 
 
from flask import send_file
import json
import requests

@app.route('/get_image')
def get_image():
    if request.args.get('type') == '1':
       filename = './image/gif/chala.gif'
    else:
       filename = './image/gif/images.jpeg'
    return send_file(filename, mimetype='image/gif')


@app.route('/dash')
def dash():
    url="https://s3.amazonaws.com/open-to-cors/assignment.json"
    
    # file=open("Test_json.json")
    # data=json.load(file)
    data=requests.get(url).json()
    print(data)

    # print(data['products']['6834']['title'])
    temp=[]
    for i in data['products']:
        temp.append(i)

    ans = []
    for j in temp:
        ans.append([data['products'][j]['subcategory'],data['products'][j]['title'], data['products'][j]['price'], data['products'][j]['popularity']])



    # print(ans)

    return render_template('index.html',ans=ans)






 
if __name__=='__main__': 
    app.run(debug=False, port=5001) 
 
# def task_id(job): 


from flask import Flask,request
from cryptography.fernet import Fernet
import os


app=Flask(__name__)
@app.route('/dashboard/',methods=('GET', 'POST'))
def dashborad():
    if request.method=='POST':
        data=request.json.get('message')
        key=os.environ['key']
        fernet = Fernet(key)
        deycrpt=fernet.decrypt(data.encode())
        return {"data":deycrpt.decode()}
    
    return "Succes"

if __name__=='__main__':
    app.run(debug=False,port=8000)
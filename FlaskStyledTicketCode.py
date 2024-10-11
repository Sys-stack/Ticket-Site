from flask import Flask, request, render_template, Response
from io import BytesIO
import requests

def fetch_html(link):
    response = requests.get(link)
    return response.content.decode('utf-8')
TicketCode = Flask(__name__)

@TicketCode.route("/")
def main():
    return "Main Page"
#first home page url
@TicketCode.route("/home", methods = ["GET","POST"])
def hello():
    if request.method == "POST":
        form = fetch_html("https://raw.githubusercontent.com/Sys-stack/Ticket-Site/refs/heads/main/Form.html")
        Response(form, content_type = "text/html")
        username = request.form.get("username")
        
        return f"Your User Name: {username}"
    elif request.method == "GET":
        return "idk at this point"
    else:
        return "it's get lol"
    
    
if __name__ == '__main__':
    TicketCode.run(debug=True)

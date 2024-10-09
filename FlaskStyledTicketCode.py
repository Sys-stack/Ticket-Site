from flask import Flask, request, render_template
from io import BytesIO
import requests

def fetch_html(link):
    response = requests.get(link)
    return response.content.decode('utf-8')
TicketCode = Flask(__name__)


#first home page url
@TicketCode.route("/home", methods = ["GET","POST"])
def hello():
    if request.method == "POST":
        username = request.form.get("username")
        return f"Your User Name: {username}"
    form = fetch_html("https://raw.githubusercontent.com/Sys-stack/Ticket-Site/refs/heads/main/Form.html")
    return Response(form, content_type = "text/html")
    
if __name__ == '__main__':
    TicketCode.run(debug=True)

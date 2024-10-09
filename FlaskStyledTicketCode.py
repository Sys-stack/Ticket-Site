from flask import Flask, request, render_template
import requests

form = BytesIO(requests.get("https://raw.githubusercontent.com/Sys-stack/Ticket-Site/refs/heads/main/Form.html").content)
TicketCode = Flask(__name__)


#first home page url
@TicketCode.route("/home", methods = ["GET","POST"])
def hello():
    if request.method == "POST":
        username = request.form.get("username")
        return f"Your User Name: {username}"
    return render_template(form)
    
if __name__ == '__main__':
    TicketCode.run(debug=True)

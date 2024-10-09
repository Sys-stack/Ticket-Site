from flask import Flask, request, render_template
TicketCode = Flask(__name__)


#first home page url
@TicketCode.route("/home", methods = ["GET","POST"])
def hello():
    if request.method == "POST":
        username = request.form.get("username")
        return f"Your User Name: {username}"
    return render_template("Form.html")
    
if __name__ == '__main__':
    TicketCode.run(debug=True)

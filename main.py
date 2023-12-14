from flask import Flask, render_template, request, session, redirect
import pymongo
from bson import ObjectId

app = Flask(" ",template_folder=r"template", static_folder=r"static")
client = pymongo.MongoClient("mongodb+srv://HealthTrack:HealthTrack@cluster0.azdhcau.mongodb.net/?retryWrites=true&w=majority")
db = client["HealthTrack"]
student_data = db["student_data"]
user_data = db["user_data"]
#session secret key
app.config["SECRET_KEY"]="1234567890"

def check_auth():
    if session.get("user") == None:
        return False
    user_id= session.get("id")
    user = user_data.find_one({"user_id": ObjectId(user_id)})
    if user == None:
        return False
    if user["user"] != session.get("user"):
        return False
    return True
@app.route("/")
def main():
  return redirect("https://nalin1304.github.io/HealthTrack/HealthTrack%20Front%20end/")

@app.route("/dashboard")
def dashboard():
    if session.get("user") != "admin":
        return redirect("/auth")
    class_value = request.args.get("class")
    age_value = request.args.get("age")
    search_value = request.args.get("search")
    if class_value:
        students = student_data.find({"class": class_value})
    elif age_value:
        students = student_data.find({"age": age_value})
    elif search_value:
        students = student_data.find({"name": {"$regex": search_value, "$options": "i"}}).sort("name")
    else:
        students = student_data.find()
    return render_template("main.html", students=list(students))

@app.route("/auth", methods=["GET","POST"])
def auth():
    if session.get("user") == "admin":
        return redirect("/dashboard")
    if check_auth():
        return redirect("/home")
    if request.method == "POST":
        user = request.form.get("user")
        pwd= request.form.get("pass")
        if user == "admin" and pwd == "admin":
            session["user"] = user
            return redirect("/dashboard")
        ud = user_data.find_one({"user": user.lower(), "password": pwd})
        if ud:
            session["user"] = user
            session["id"] = f'{ud["user_id"]}'.replace("ObjectId('","").replace("')","")
            return redirect("/home")
    return render_template("auth.html")
@app.route("/home")
def home():
    if not check_auth():
        return redirect("/auth")
    sutdent = student_data.find_one({"_id": ObjectId(session.get("id"))})
    return render_template("home.html", student=sutdent)

@app.route("/student_data")
def student_data_():
    if session.get("user") != "admin":
        return redirect("/auth")
    student_id = request.args.get("id")
    student = student_data.find_one({"_id": ObjectId(student_id)})
    return render_template("student_data.html", student=student)


@app.route("/logout")
def logout():
    if session.get("user") == None:
        return redirect("/auth")
    session.pop("user")
    try:
        session.pop("id")
    except:
        pass
    return redirect("/auth")



app.run(host="0.0.0.0", port=8080, debug=True)

from flask import Flask, render_template, request, session, redirect
import pymongo
from bson import ObjectId
import processes

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
        students = student_data.find({"class": class_value}).sort("name")
    elif age_value:
        students = student_data.find({"age": age_value}).sort("name")
    elif search_value:
        students = student_data.find({"name": {"$regex": search_value, "$options": "i"}}).sort("name")
    else:
        students = student_data.find().sort("name")
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
    student_id = request.args.get("id")
    student = student_data.find_one({"_id": ObjectId(student_id)})
    if session.get("user") != "admin":
        return redirect("/auth")
    elif student["class"] == "-":
        pass
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


@app.route("/add_data", methods=["GET","POST"])
def add_data():
    if request.method == "POST":
        name= request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        age = request.form.get("age")
        height = request.form.get("height")
        weight = request.form.get("weight")
        blood_group = request.form.get("blood_group")
        blood_pressure = request.form.get("blood_pressure")
        pulse = request.form.get("pulse")
        haemoglobin = request.form.get("haemoglobin")
        tooth_cavity = request.form.get("tooth_cavity")
        gum_inflamation = request.form.get("gum_inflamation")
        tarter = request.form.get("tarter")
        gum_bleeding = request.form.get("gum_bleeding")
        plaque = request.form.get("plaque")
        stains = request.form.get("stains")
        vision = request.form.get("vision")
        ear = request.form.get("ear")
        squint = request.form.get("squint")
        throat = request.form.get("throat")
        sd = student_data.insert_one({
            "name": name,
            "class": "-",
            "age": age,
            "weight": weight,
            "height": height,
            "blood" :{"blood_group": blood_group,"blood_pressure": blood_pressure,"pulse": pulse, "haemoglobin": haemoglobin},
            "oral": {"tooth_cavity": tooth_cavity,"gum_inflamation": gum_inflamation,"tarter": tarter,"gum_bleeding": gum_bleeding,"plaque": plaque,"stains": stains},
            "vision": vision,
            "ear": ear,
            "squint": squint,
            "throat": throat,
            "allergies": [],
            "recommendation": []
        })
        print(sd.inserted_id)
        id = sd.inserted_id
        user_data.insert_one({
            "user": username.lower(),
            "password": password,
            "user_id": id
        })
        processes.single_user_recommendation(id)
        return redirect("/student_data?id="+str(id))
    return render_template("add_data.html")



app.run(host="0.0.0.0", port=8080, debug=True)


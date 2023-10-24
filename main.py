from flask import Flask, render_template, request
import pymongo

app = Flask(" ",template_folder=r'C:\Arjit\Arjit\HealthTrack\template')
client = pymongo.MongoClient("mongodb+srv://HealthTrack:HealthTrack@cluster0.azdhcau.mongodb.net/?retryWrites=true&w=majority")
db = client["HealthTrack"]
student_data = db["student_data"]

@app.route("/")
def index():
    class_value = request.args.get("class")
    age_value = request.args.get("age")
    if class_value:
        students = student_data.find({"class": class_value})
    elif age_value:
        students = student_data.find({"age": age_value})
    else:
        students = student_data.find()
    return render_template("main.html", students=students)

app.run(host="0.0.0.0", port=8080, debug=True)
import pymongo
import json

# Replace the connection string with your own MongoDB connection string
client = pymongo.MongoClient("mongodb+srv://HealthTrack:HealthTrack@cluster0.azdhcau.mongodb.net/?retryWrites=true&w=majority")

db = client["HealthTrack"]
student_data = db["student_data"]
with open ("recommendation.json") as f:
  r = json.load(f)
def bmi_calculator():
  students = student_data.find()
  for student in students:
    print(student)
    height = student["height"] # in feets and inches
    weight = student["weight"]
    height = float(height)

    print(height, weight)
    bmi = float(weight)/((float(height)/100)**2)
    print(bmi)
    bmi_category = ""
    if bmi < 18.5:
      bmi_category = "Underweight"
      recommendation = [r["underweight"]["recommendation"]]
    elif bmi >= 18.5 and bmi <= 24.9:
      bmi_category = "Normal"
      recommendation = []
    elif bmi >= 25 and bmi <= 29.9:
      bmi_category = "Overweight"
      recommendation = [r["overweight"]["recommendation"]]
    elif bmi >= 30:
      bmi_category = "Obese"
      recommendation = [r["obese"]["recommendation"]]
    old_recommendation = student["recommendation"]
    if recommendation != []:
      for recommend in recommendation:
        if recommend in old_recommendation:
          recommendation.remove(recommend)
      recommendation += old_recommendation
    if recommendation == []:
      recommendation = None
    if recommendation == None:
        student_data.update_one({"_id":student["_id"]},{"$set":{"bmi_category":bmi_category, "bmi":bmi}})
    else:
        student_data.update_one({"_id":student["_id"]},{"$set":{"bmi_category":bmi_category, "bmi":bmi,"recommendation":[recommendation]}}, upsert=True)
    print(bmi_category)
  
def avg_data_class(standard):
  students = student_data.find({"class":standard})
  print(students)
  height_sum = 0
  weight_sum = 0
  bmi_sum = 0
  avg_bmi_category = ""
  s=0
  for student in students:
    print(student)
    height = student["height"] # in feets and inches
    weight = student["weight"]
    bmi = student["bmi"]
    height_sum += float(height)/100
    weight_sum += float(weight)
    bmi_sum += bmi
    print(height, height_sum)
    s+=1
  avg_height = height_sum/s
  avg_weight = weight_sum/s
  avg_bmi = bmi_sum/s
  print(avg_height)
  print(avg_weight)
  print(avg_bmi)
  if avg_bmi < 18.5:
      avg_bmi_category = "Underweight"
  elif avg_bmi >= 18.5 and avg_bmi <= 24.9:
    avg_bmi_category = "Normal"
  elif avg_bmi >= 25 and avg_bmi <= 29.9:
    avg_bmi_category = "Overweight"
  elif avg_bmi >= 30:
    avg_bmi_category = "Obese"
  db["average_data"].update_one({"class":standard},{"$set":{"avg_height":avg_height,"avg_weight":avg_weight,"avg_bmi":avg_bmi, "avg_bmi_category":avg_bmi_category}}, upsert=True)
  return avg_height


def remove_all_recommendation():
  students = student_data.find()
  for student in students:
    student_data.update_one({"_id":student["_id"]},{"$set":{"recommendation":[]}})

def add_user_data():
  students = student_data.find()
  user_data = db["user_data"]
  for student in students:
    un = student["name"].split(" ")
    un = (un[0]+"."+un[-1]).lower()
    check = list(user_data.find({"user":un}))
    if len(check) == 0:
      user_data.insert_one({"user":un,"password":"password@123","user_id":student["_id"]})
    else:
      print("Already exists")
      print(un)
    print("Inserted")

def recommendations():
  students = student_data.find()
  for student in students:
    print(student)
    recommendation = []
    pulse_category = "Normal"
    pulse = student["blood"]["pulse"]
    if int(pulse) > 100:
      recommendation.append(r["high_pulse"]["recommendation"])
      pulse_category = "High"
    elif int(pulse) < 60:
      recommendation.append(r["low_pulse"]["recommendation"])
      pulse_category = "Low"
    bp = student["blood"]["blood_pressure"]
    bp = bp.split("/")
    bp_category = "Normal"
    if (int(bp[0]) >= 120) or (int(bp[1]) >= 80):
      recommendation.append(r["high_bp"]["recommendation"])
      bp_category = "High"
    elif (int(bp[0]) <= 90) or (int(bp[1]) <= 60):
      recommendation.append(r["low_bp"]["recommendation"])
      bp_category = "Low"
    if student["recommendation"] != []:
      recommendation += student["recommendation"]
    blood = student["blood"]
    blood["pulse_category"] = pulse_category
    blood["bp_category"] = bp_category
    student_data.update_one({"_id":student["_id"]},{"$set":{"recommendation":recommendation, "blood":blood}}, upsert=True)
    print("Updated")

def test():
  #if vision field is 10/10 then change it into 6/6
  students = student_data.find()
  for student in students:
    vision = student["vision"]
    if vision == "10/10":
      student_data.update_one({"_id":student["_id"]},{"$set":{"vision":"6/6"}})
      print("Updated")
    print(student)

def single_user_recommendation(id):
  #bmi calculator 
  student = student_data.find_one({"_id":id})
  print(student)
  height = student["height"] # in cm
  weight = student["weight"]
  height = float(height)
  weight = float(weight)
  bmi = float(weight)/((float(height)/100)**2)
  print(bmi)
  bmi_category = ""
  if bmi < 18.5:
    bmi_category = "Underweight"
    recommendation = [r["underweight"]["recommendation"]]
  elif bmi >= 18.5 and bmi <= 24.9:
    bmi_category = "Normal"
    recommendation = []
  elif bmi >= 25 and bmi <= 29.9:
    bmi_category = "Overweight"
    recommendation = [r["overweight"]["recommendation"]]
  elif bmi >= 30:
    bmi_category = "Obese"
    recommendation = r["obese"]["recommendation"]
  old_recommendation = [student["recommendation"]]
  if recommendation != []:
    for recommend in recommendation:
      if recommend in old_recommendation:
        recommendation.remove(recommend)
    recommendation += old_recommendation
  if recommendation == []:
    recommendation = None
  if recommendation == None:
      student_data.update_one({"_id":student["_id"]},{"$set":{"bmi_category":bmi_category, "bmi":bmi}})
  else:
      student_data.update_one({"_id":student["_id"]},{"$set":{"bmi_category":bmi_category, "bmi":bmi,"recommendation":recommendation}}, upsert=True)
  print(bmi_category)
  #pulse and bp
  student = student_data.find_one({"_id":id})
  recommendation = []
  pulse_category = "Normal"
  pulse = student["blood"]["pulse"]
  if int(pulse) > 100:
    recommendation.append(r["high_pulse"]["recommendation"])
    pulse_category = "High"
  elif int(pulse) < 60:
    recommendation.append(r["low_pulse"]["recommendation"])
    pulse_category = "Low"
  bp = student["blood"]["blood_pressure"]
  bp = bp.split("/")
  bp_category = "Normal"
  if (int(bp[0]) >= 120) or (int(bp[1]) >= 80):
    recommendation.append(r["high_bp"]["recommendation"])
    bp_category = "High"
  elif (int(bp[0]) <= 90) or (int(bp[1]) <= 60):
    recommendation.append(r["low_bp"]["recommendation"])
    bp_category = "Low"
  if student["recommendation"] != []:
    recommendation += student["recommendation"]
  blood = student["blood"]
  blood["pulse_category"] = pulse_category
  blood["bp_category"] = bp_category
  student_data.update_one({"_id":student["_id"]},{"$set":{"recommendation":recommendation, "blood":blood}}, upsert=True)
  print("Updated")
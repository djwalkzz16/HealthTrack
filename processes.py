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
      recommendation = r["underweight"]["recommendation"]
    elif bmi >= 18.5 and bmi <= 24.9:
      bmi_category = "Normal"
      recommendation = None
    elif bmi >= 25 and bmi <= 29.9:
      bmi_category = "Overweight"
      recommendation = r["overweight"]["recommendation"]
    elif bmi >= 30:
      bmi_category = "Obese"
      recommendation = r["obese"]["recommendation"]
    old_recommendation = student["recommendation"]
    if old_recommendation == [recommendation]:
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

bmi_calculator()
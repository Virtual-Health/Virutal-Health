from flask import Flask,render_template,redirect,url_for
from flask.globals import request
from pymongo import MongoClient, collection
from datetime import datetime, timedelta
app = Flask(__name__)
def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta
client=MongoClient("mongodb+srv://Hospital:Hospital@hospital.qy9s5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['Hospital']
collection = db['Hospital']
doctors = db['Doctors']
appointments = db["Appointments"]

def getdetails(l1,n1,n2):
    l = []
    for i in l1:
        if i['name'] == n1:
            l.append(i)
    if(len(l)>1):
        l2 = []
        for i in l1:
            if i['age'] == n2:
                l2.append(i)
        if len(l2)>0:
            return l2
    return l

@app.route("/appointment",methods = ['GET',"POST"])
def get_app():
    if request.method == "GET":
        l = doctors.find()
        l1 = []
        for i in l:
            l1.append(i)
            l2 = {}
            c = 0
            for dt in datetime_range(datetime(2016, 9, 1, i['stime']), datetime(2016, 9, 1,i['etime']),timedelta(minutes=i['freq'])):
                l2[c] = str(str(dt).split()[-1])
                c+=1
            l1[-1]['time'] = l2
            l1[-1]['tle'] = c
        return render_template("appointment.html",data = l1)
    n1 = request.form["name1"]
    n2 = request.form["age"]
    n3 = request.form["dep"]
    n4 = request.form["time"]
    appointments.insert_one({"name":n1,"age":n2,"dep":n3,"time":n4})
    return redirect(url_for(home))




@app.route("/",methods= ["GET","POST"])
def home():
    if request.method == "POST":
        n1 = request.form['name']
        n2 = request.form['age']
        # n3 = request.form['dep']
        l = collection.find()
        l1 = []
        for i in l:
            l1.append(i)
        l = getdetails(l1,n1,n2)
        print(l)
        return render_template("welcome.html",data = l)
    return render_template("welcome.html")

if __name__ == "__main__":
    app.run(debug = True)

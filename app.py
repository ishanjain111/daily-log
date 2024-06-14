from flask import Flask, render_template, request, redirect, url_for
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
app.db =  client.microlog
# entries = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        now = datetime.datetime.now()
        formatted_date =  now.strftime("%d-%m-%Y")
        formatted_time = now.strftime("%H:%M")
        app.db.entries.insert_one({"content": entry_content, "date": formatted_date, "time": formatted_time})
        return redirect(url_for("home"))
    entries_with_date = [
        (
            entry["content"],
            entry["date"],
            entry["time"],
            datetime.datetime.strptime(f"{entry['date']} {entry['time']}", "%d-%m-%Y %H:%M").strftime("%b %d %H:%M"),
            str(entry["_id"])
        )
        for entry in app.db.entries.find({}).sort([("date", -1), ("time", -1)])
    ]
    return render_template("index.html", entries=entries_with_date)

@app.route("/delete", methods=["POST"])
def delete_entry():
    entry_id = request.form.get("id")
    app.db.entries.delete_one({"_id": ObjectId(entry_id)})
    return redirect(url_for("home"))
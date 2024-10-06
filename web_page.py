import streamlit as st
from datetime import datetime
import pymongo
import pytz

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://suriya315:12345678s@cluster0.kbh9v.mongodb.net/?retryWrites=true&w=majority")
db = client.diary
diary_collection = db.log

# Function to get current Indian time
def get_current_indian_time():
    indian_tz = pytz.timezone('Asia/Kolkata')
    return datetime.now(indian_tz)

# Title of the app
st.title("Diary Maker")
diary_heading = st.text_input("Enter diary heading:")
diary_content = st.text_area("Write your diary entry here:")
uploaded_files = st.file_uploader("Upload your images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

# Store diary entry in MongoDB when the user clicks a button
if st.button("Save Diary Entry"):
    diary_entry = {
        "heading": diary_heading,
        "content": diary_content,
        "images": [],
        "timestamp": get_current_indian_time(),
        "entry_date": get_current_indian_time().strftime("%Y-%m-%d %H:%M:%S")  # Add current date and time in Indian timezone
    }
    # Save uploaded images to MongoDB GridFS and store their IDs
    if uploaded_files:
        for img_file in uploaded_files:
            img_id = db.fs.files.insert_one({"name": img_file.name, "data": img_file.read()}).inserted_id
            diary_entry["images"].append(str(img_id))
    # Insert diary entry into MongoDB
    diary_collection.insert_one(diary_entry)
    st.success("Diary entry saved successfully!")

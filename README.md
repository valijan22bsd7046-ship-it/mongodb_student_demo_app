# MongoDB Student Demo App

A small Streamlit + PyMongo application for teaching MongoDB to MSc Data Science students.

## 1. Prerequisites

Install MongoDB Community Server and make sure the MongoDB service is running on:

`mongodb://localhost:27017/`

Install Python 3.10+.

## 2. Install dependencies

Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
```

## 3. Insert sample data

```bash
python seed_data.py
```

This creates:

- Database: `college_db`
- Collection: `students`

## 4. Run the app

```bash
streamlit run app.py
```

## Teaching sequence

1. Open MongoDB Compass and show `college_db.students`.
2. Explain a document, array field, and embedded document.
3. Open the Streamlit app.
4. Add one student and refresh MongoDB Compass.
5. Search students using equality and comparison queries.
6. Update a city and add a skill.
7. Delete a temporary student.
8. Open Analytics and explain `$unwind`, `$group`, `$avg`, `$sort`, and `$limit`.

## Suggested mongosh commands

```javascript
use college_db
show collections

db.students.find()

db.students.find({ semester: 2 })

db.students.find({ skills: "Python" })

db.students.find({
  subjects: {
    $elemMatch: {
      name: "DBMS",
      marks: { $gt: 80 }
    }
  }
})

db.students.updateOne(
  { student_id: "DS001" },
  { $set: { city: "Bengaluru" } }
)

db.students.updateOne(
  { student_id: "DS001" },
  { $addToSet: { skills: "Machine Learning" } }
)

db.students.aggregate([
  { $unwind: "$subjects" },
  {
    $group: {
      _id: "$subjects.name",
      average_marks: { $avg: "$subjects.marks" }
    }
  },
  { $sort: { average_marks: -1 } }
])
```

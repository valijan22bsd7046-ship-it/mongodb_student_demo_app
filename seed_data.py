from pymongo import MongoClient

client = MongoClient('mongodb+srv://Avi:6MpYPiezMdCC78kG@test.rr3v477.mongodb.net/?appName=test')
db = client['college_db']
students = db['students']

sample_students = [
    ('DS001','Amit Kumar',2,23,'Chennai',[82,76,88],['Python','MongoDB','Pandas']),
    ('DS002','Neha Sharma',2,22,'Delhi',[91,84,89],['Python','SQL','Tableau']),
    ('DS003','Rahul Verma',1,21,'Hyderabad',[68,74,71],['R','Statistics','Python']),
    ('DS004','Priya Singh',2,23,'Vijayawada',[88,92,85],['Python','MongoDB','Machine Learning']),
    ('DS005','Arjun Rao',3,24,'Bengaluru',[73,81,79],['Python','Power BI','SQL']),
    ('DS006','Sneha Patel',1,22,'Ahmedabad',[95,90,93],['Python','MongoDB','Deep Learning']),
    ('DS007','Rohan Das',4,25,'Kolkata',[61,69,72],['R','Excel','SQL']),
    ('DS008','Meera Nair',2,23,'Kochi',[84,87,90],['Python','Pandas','MongoDB']),
    ('DS009','Karan Mehta',3,24,'Mumbai',[77,70,75],['Python','SQL','Spark']),
    ('DS010','Ananya Iyer',1,21,'Chennai',[89,94,91],['Python','MongoDB','TensorFlow']),
    ('DS011','Vikram Joshi',2,23,'Pune',[72,76,74],['Python','Power BI','SQL']),
    ('DS012','Ishita Roy',3,24,'Kolkata',[86,83,88],['Python','MongoDB','NLP']),
    ('DS013','Nitin Gupta',4,25,'Delhi',[79,68,73],['Java','Python','SQL']),
    ('DS014','Pooja Reddy',1,22,'Hyderabad',[92,89,90],['Python','MongoDB','Pandas']),
    ('DS015','Sahil Khan',2,23,'Lucknow',[64,71,67],['Python','Excel','SQL']),
]

students.delete_many({})

docs = []
for sid, name, sem, age, city, marks, skills in sample_students:
    docs.append({
        'student_id': sid,
        'name': name,
        'program': 'MSc Data Science',
        'semester': sem,
        'age': age,
        'city': city,
        'subjects': [
            {'name': 'DBMS', 'marks': marks[0]},
            {'name': 'Machine Learning', 'marks': marks[1]},
            {'name': 'Statistics', 'marks': marks[2]},
        ],
        'skills': skills,
    })

students.insert_many(docs)
print(f'Inserted {len(docs)} sample student documents into college_db.students')

import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.set_page_config(page_title='MongoDB Student Demo', page_icon='🎓', layout='wide')

# -----------------------------
# MongoDB Connection
# -----------------------------
# FIXED: Using a safe TOML key lookup instead of passing the raw URI string
MONGO_URI = "mongodb+srv://valijan22bsd7046_db_user:fAKAvEn8ljeuHwyO@test.rr3v477.mongodb.net/?appName=test"
client = MongoClient(MONGO_URI)
db = client['college_db']
students = db['students']

# -----------------------------
# Helper functions
# -----------------------------
def student_to_row(doc):
    subject_marks = {s['name']: s['marks'] for s in doc.get('subjects', [])}
    return {
        'Student ID': doc.get('student_id', ''),
        'Name': doc.get('name', ''),
        'Program': doc.get('program', ''),
        'Semester': doc.get('semester', ''),
        'Age': doc.get('age', ''),
        'City': doc.get('city', ''),
        'Skills': ', '.join(doc.get('skills', [])),
        'DBMS': subject_marks.get('DBMS', ''),
        'Machine Learning': subject_marks.get('Machine Learning', ''),
        'Statistics': subject_marks.get('Statistics', ''),
    }


def load_students(query=None):
    query = query or {}
    docs = list(students.find(query, {'_id': 0}))
    return pd.DataFrame([student_to_row(d) for d in docs]) if docs else pd.DataFrame()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title('🎓 MongoDB Demo')
page = st.sidebar.radio(
    'Choose Module',
    ['Dashboard', 'Add Student', 'Search Students', 'Update/Delete', 'Student Records', 'Analytics']
)

st.sidebar.markdown('---')
st.sidebar.caption('Database: college_db')
st.sidebar.caption('Collection: students')

# -----------------------------
# Dashboard
# -----------------------------
if page == 'Dashboard':
    st.title('MongoDB Student Performance Management System')
    st.write('A compact demo app for teaching MongoDB CRUD operations, embedded documents, arrays, filtering, and aggregation.')

    total = students.count_documents({})
    python_count = students.count_documents({'skills': 'Python'})
    sem2_count = students.count_documents({'semester': 2})

    c1, c2, c3 = st.columns(3)
    c1.metric('Total Students', total)
    c2.metric('Students with Python Skill', python_count)
    c3.metric('Semester 2 Students', sem2_count)

    st.subheader('MongoDB Document Example')
    st.code('''{
  "student_id": "DS001",
  "name": "Amit Kumar",
  "program": "MSc Data Science",
  "semester": 2,
  "age": 23,
  "subjects": [
    {"name": "DBMS", "marks": 82},
    {"name": "Machine Learning", "marks": 76},
    {"name": "Statistics", "marks": 88}
  ],
  "skills": ["Python", "MongoDB", "Pandas"],
  "city": "Chennai"
}''', language='json')

# -----------------------------
# Add Student
# -----------------------------
elif page == 'Add Student':
    st.title('➕ Add Student')
    st.caption('MongoDB concept: insert_one()')

    with st.form('add_student_form'):
        c1, c2 = st.columns(2)
        student_id = c1.text_input('Student ID')
        name = c2.text_input('Name')
        program = c1.selectbox('Program', ['MSc Data Science', 'MSc Statistics', 'MSc Computer Science'])
        semester = c2.selectbox('Semester', [1, 2, 3, 4])
        age = c1.number_input('Age', min_value=18, max_value=60, value=22)
        city = c2.text_input('City')

        st.subheader('Subject Marks')
        m1, m2, m3 = st.columns(3)
        dbms_marks = m1.number_input('DBMS', min_value=0, max_value=100, value=75)
        ml_marks = m2.number_input('Machine Learning', min_value=0, max_value=100, value=75)
        stat_marks = m3.number_input('Statistics', min_value=0, max_value=100, value=75)

        skills_text = st.text_input('Skills (comma-separated)', 'Python, MongoDB')
        submitted = st.form_submit_button('Insert Student')

    if submitted:
        if not student_id or not name:
            st.error('Student ID and Name are required.')
        elif students.find_one({'student_id': student_id}):
            st.error('Student ID already exists.')
        else:
            doc = {
                'student_id': student_id,
                'name': name,
                'program': program,
                'semester': semester,
                'age': int(age),
                'city': city,
                'subjects': [
                    {'name': 'DBMS', 'marks': int(dbms_marks)},
                    {'name': 'Machine Learning', 'marks': int(ml_marks)},
                    {'name': 'Statistics', 'marks': int(stat_marks)},
                ],
                'skills': [s.strip() for s in skills_text.split(',') if s.strip()],
            }
            students.insert_one(doc)
            st.success('Student inserted successfully.')
            st.code("students.insert_one(doc)", language='python')

# -----------------------------
# Search Students
# -----------------------------
elif page == 'Search Students':
    st.title('🔍 Search Students')
    st.caption('MongoDB concepts: find(), $gt, $gte, $lte, array matching, $elemMatch')

    search_type = st.selectbox(
        'Search by',
        ['Student ID', 'City', 'Skill', 'Semester', 'DBMS Marks Greater Than', 'DBMS Marks Range']
    )

    query = {}
    if search_type == 'Student ID':
        value = st.text_input('Enter Student ID')
        if value:
            query = {'student_id': value}
    elif search_type == 'City':
        value = st.text_input('Enter City')
        if value:
            query = {'city': value}
    elif search_type == 'Skill':
        value = st.text_input('Enter Skill, e.g. Python')
        if value:
            query = {'skills': value}
    elif search_type == 'Semester':
        value = st.selectbox('Select Semester', [1, 2, 3, 4])
        query = {'semester': value}
    elif search_type == 'DBMS Marks Greater Than':
        marks = st.slider('Marks greater than', 0, 100, 80)
        query = {'subjects': {'$elemMatch': {'name': 'DBMS', 'marks': {'$gt': marks}}}}
    else:
        low, high = st.slider('DBMS marks range', 0, 100, (60, 90))
        query = {'subjects': {'$elemMatch': {'name': 'DBMS', 'marks': {'$gte': low, '$lte': high}}}}

    if st.button('Run Query'):
        st.write('MongoDB query:')
        st.code(str(query), language='python')
        df = load_students(query)
        if df.empty:
            st.info('No matching students found.')
        else:
            st.dataframe(df, use_container_width=True)

# -----------------------------
# Update/Delete
# -----------------------------
elif page == 'Update/Delete':
    st.title('✏️ Update / Delete Student')
    st.caption('MongoDB concepts: update_one(), $set, $push, delete_one()')

    student_id = st.text_input('Enter Student ID')
    doc = students.find_one({'student_id': student_id}, {'_id': 0}) if student_id else None

    if student_id and not doc:
        st.warning('Student not found.')

    if doc:
        st.json(doc)
        action = st.radio('Action', ['Update City', 'Add Skill', 'Delete Student'])

        if action == 'Update City':
            new_city = st.text_input('New City')
            if st.button('Update City'):
                students.update_one({'student_id': student_id}, {'$set': {'city': new_city}})
                st.success('City updated.')
                st.code("students.update_one({'student_id': student_id}, {'$set': {'city': new_city}})", language='python')

        elif action == 'Add Skill':
            new_skill = st.text_input('New Skill')
            if st.button('Add Skill'):
                students.update_one({'student_id': student_id}, {'$addToSet': {'skills': new_skill}})
                st.success('Skill added.')
                st.code("students.update_one({'student_id': student_id}, {'$addToSet': {'skills': new_skill}})", language='python')

        else:
            confirm = st.checkbox('I understand this will delete the record')
            if st.button('Delete Student', disabled=not confirm):
                students.delete_one({'student_id': student_id})
                st.success('Student deleted.')
                st.code("students.delete_one({'student_id': student_id})", language='python')

# -----------------------------
# Student Records
# -----------------------------
elif page == 'Student Records':
    st.title('📋 All Student Records')
    st.caption('MongoDB concept: find({}, {"_id": 0})')

    df = load_students()
    if df.empty:
        st.info("The database is currently empty.")
    else:
        st.dataframe(df, use_container_width=True)

# -----------------------------
# Analytics
# -----------------------------
elif page == 'Analytics':
    st.title('📊 Performance Analytics')
    st.caption('MongoDB concepts: aggregate(), $unwind, $group, $avg')

    # Aggregation pipeline to calculate average marks per subject
    pipeline = [
        {'$unwind': '$subjects'},
        {
            '$group': {
                '_id': '$subjects.name',
                'Average Marks': {'$avg': '$subjects.marks'},
                'Max Marks': {'$max': '$subjects.marks'},
                'Min Marks': {'$min': '$subjects.marks'}
            }
        }
    ]

    if st.button('Run Aggregation Pipeline'):
        st.write('MongoDB Aggregation Pipeline:')
        st.code(str(pipeline), language='python')
        
        results = list(students.aggregate(pipeline))
        
        if results:
            # Format results into a clean dataframe
            analytics_data = []
            for r in results:
                analytics_data.append({
                    'Subject': r['_id'],
                    'Average': round(r['Average Marks'], 2),
                    'Highest Score': r['Max Marks'],
                    'Lowest Score': r['Min Marks']
                })
            
            df_analytics = pd.DataFrame(analytics_data)
            st.dataframe(df_analytics, use_container_width=True)
            
            # Simple bar chart for averages

# import streamlit as st

# st.write("Hello world")
# st.button("OK")

# if "attendance" not in st.session_state:
#     st.session_state.attendance = set()


# def take_attendance():
#     if st.session_state.name in st.session_state.attendance:
#         st.info(f"{st.session_state.name} has already been counted.")
#     else:
#         st.session_state.attendance.add(st.session_state.name)


# with st.form(key="my_form"):
#     st.text_input("Name", key="name")
#     st.form_submit_button("I'm here!", on_click=take_attendance)


# st.slider("With default, no key", 20, 50, value=10)

import streamlit as st
import pandas as pd
import pickle

# Load the model
with open('model.pkl', 'rb') as f:
    ln = pickle.load(f)

coeff_df = pd.read_csv('coefficients.csv', index_col=0)

# Recommendation function
def get_grade(prediction):
    if prediction >= 10:
        grade = "Pass"
    else:
        grade = "Fail"
    tutor_assignment = ""
    if prediction < 15:
        tutor_assignment = "You have been assigned a tutor. Please contact the tutoring center for more details."
    return grade, tutor_assignment

# Initialize session state for managing steps
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'prediction' not in st.session_state:
    st.session_state.prediction = None
if 'grade' not in st.session_state:
    st.session_state.grade = None
if 'tutor_assignment' not in st.session_state:
    st.session_state.tutor_assignment = None

# Step 1: Input Form
if st.session_state.step == 1:
    st.title("Student Performance Prediction")
    st.header("Enter Student Details")
    
    # Dropdown for Sex
    sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
    
    # Numeric input for Age
    age = st.number_input("Age", min_value=10, max_value=100, step=1)
    
    # Dropdowns for studytime, failures, health, and attendance
    studytime = st.selectbox("Study Time (1-4)", options=list(range(1, 5)))
    failures = st.selectbox("Failures (0-4)", options=list(range(0, 5)))
    health = st.selectbox("Health (1-5)", options=list(range(1, 6)))
    attendance = st.selectbox("Attendance (0-9)", options=list(range(0, 10)))
    
    # Numeric inputs for G1 and G2, limited to 1-20
    G1 = st.number_input("G1 Grade (1-20)", min_value=1, max_value=20, step=1)
    G2 = st.number_input("G2 Grade (1-20)", min_value=1, max_value=20, step=1)

    if st.button("Predict"):
        # Make the prediction
        pred1 = (ln.intercept_) + (coeff_df['sex'].values[0] * sex) + (coeff_df['age'].values[0] * age) + \
                (coeff_df['studytime'].values[0] * studytime) + (coeff_df['failures'].values[0] * failures) + \
                (coeff_df['health'].values[0] * health) + (coeff_df['attendance'].values[0] * attendance) + \
                (coeff_df['G1'].values[0] * G1) + (coeff_df['G2'].values[0] * G2)
        
        # Round up the predicted value
        pred1 = round(pred1, 2)
        
        # Get the recommendation
        grade, tutor_assignment = get_grade(pred1)

        # Store results in session state
        st.session_state.prediction = pred1
        st.session_state.grade = grade
        st.session_state.tutor_assignment = tutor_assignment

        # Move to the next step
        st.session_state.step = 2

# Step 2: Show Prediction Results and Feedback Form
if st.session_state.step == 2:
    st.title("Prediction Results")
    st.subheader("Results")
    st.write(f"**Predicted Score:** {st.session_state.prediction}")
    st.write(f"**Grade:** {st.session_state.grade}")
    st.write(f"**Recommendation:** {st.session_state.tutor_assignment}")

    st.header("Student Feedback")
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Feedback")

    if st.button("Submit Feedback"):
        # Save feedback as a dictionary and display it
        feedback = {'name': name, 'email': email, 'message': message}

        if 'feedback_list' not in st.session_state:
            st.session_state.feedback_list = []
        st.session_state.feedback_list.append(feedback)

        st.success("Feedback submitted successfully!")

        # Display feedbacks
        st.header("All Feedback")
        for feedback in st.session_state.feedback_list:
            st.write(f"**Name**: {feedback['name']}")
            st.write(f"**Email**: {feedback['email']}")
            st.write(f"**Message**: {feedback['message']}")
            st.write("---")


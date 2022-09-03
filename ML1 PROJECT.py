import numpy as np
import pandas as pd
import pickle
import streamlit as st
import sqlite3 as sq

conn = sq.connect("Login.db")
c = conn.cursor()

def create_usertable():
    c.execute("CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)")
    
def add_userdata(username,password):
    c.execute("INSERT INTO userstable(username,password) VALUES (?,?)",(username,password))
    conn.commit()
    
def login_user(username,password):
    c.execute("SELECT * FROM userstable WHERE username=? AND password= ?",(username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute("SELECT * FROM userstable")
    data = c.fetchall()
    return data


# Loading the saved model
loaded_model = pickle.load(open("C:/Users/stevi/Desktop/trained_model.sav", 'rb'))


# Creating a Function for Prediction

def diabetes_prediction(input_data):
    
   
    # changing the input_data to a numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the numpy array as we are predicting for only one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)

    if (prediction[0] == 0):
        return 'Safe🙂, NONE Diabetic'
    else:
        return 'Alert😟!! Diabetic'
    
    
    
def main():
     st.caption("Made with Breezie Foundation.")
     st.title("Welcome to the Diabetis Prediction WebApp💫💫.")
     
     Menu = ['Login','SignUp','AboutUs']
     Selection = st.sidebar.selectbox("Menu",Menu)
     
     if Selection == "Login":
         st.sidebar.subheader("Login with correct credentials.")
         
         username = st.sidebar.text_input("User name:")
         password = st.sidebar.text_input("Password:",type='password')
         
         if st.sidebar.checkbox("Login"):
             create_usertable()
             result = login_user(username,password)
             if result:
                 st.success("Logged in as {}🎇".format(username))
                 st.warning("To be used by a fully trained medical officer.")
                 st.write(""" ## Key in the patients data and test the results.""")
                 
                 Pregnancies = st.text_input('Number of Pregnancies:')
                 Glucose = st.text_input('Glucose level:')
                 BloodPressure = st.text_input('Blood Pressure value:')
                 SkinThickness = st.text_input('SkinThickness value:')
                 Insulin = st.text_input('Insulin level:')
                 BMI=st.number_input("BMI value:")
                 st.write("BMI:",BMI)
                 DPF=st.number_input("DiabetesPedegreeFunction Level:")
                 st.write("DPF:",DPF)
                 Age=st.slider("Patients Age:",1,150,50)
                 st.write("Age:",Age)
                 
                 
                 # Code for Prediction
                 diagnosis = ''


                 # Creating a button for Prediction


                 if st.button('Submit Test Results.'):
                     diagnosis = diabetes_prediction([Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DPF,Age])
    
    
                     st.success(diagnosis)
                 
                 
             else:
                 st.warning("Incorrect username or password.")
         
         
         
         
     elif Selection == "SignUp":
         st.subheader("Create New Account.")
         new_user = st.text_input("username:")
         new_password = st.text_input("password:", type='password')
         
         if st.button("SignUp"):
             create_usertable()
             add_userdata(new_user,new_password)
             st.success("Account created successfully🎇.")
             st.info("👈Now go to the login page.")
         
         
         
     elif Selection == "AboutUs":
         st.subheader("Afya Bora App Foundation.")
         st.markdown("This web app has been carefully designed to help medics in testing diabetis medical condition in patients. The app has a neatly designed interface and gives a more accurate result. Feel free to use the app interactively to perform tests.")
         st.write("Komesha! Ugonjwa wa Sukari.")
         
         st.write("You can reach as via:")
         st.write("Contact: 0700 495 575.")
         st.write("Email: steviewizzie99@gmail.com")
        
     
if __name__ == '__main__':
    main()     
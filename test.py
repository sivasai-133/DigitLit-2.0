import streamlit as st
import os
from page import get,set
# Read the requirements.txt file
# Need to run only when reboot is done

# if (get() == 0):
#     with open('requirements.txt') as f:
#         requirements = f.read().splitlines()

#     # Install the required packages using pip
#     for package in requirements:
#         subprocess.check_call(['pip', 'install', package])
#     set(1)


def page_1():
    
    st.title('digit dataset')
    
    with st.form(key='my_form'):
        menu = ['--select--','guest','admin']
        choice = st.selectbox('Select an option',menu)
        if choice == 'guest':
            set(2)
        if choice == 'admin':
            set(3)
        submit_button = st.form_submit_button(label='Submit')
    
    if submit_button:
        if choice == '--select--':
            st.error('Please select an option')
        else:
            st.success('Login successful')
            st.experimental_rerun()



def page_2():
    set(2)
    st.title('guest')

    if st.button('Return to Main Page'):
        set(1)
        st.experimental_rerun()

def page_3():
    set(3)
    st.title('admin')


    print(st.secrets)
    print(st.secrets.keys())

    user = os.environ['db_username']
    password = os.environ['db_password']


    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter username')
        password_input = st.text_input(label='Enter password',type='password')
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if text_input == user and password_input == password:
            st.success('Login successful')
        else:
            st.error('Login unsuccessful')

    if st.button('Return to Main Page'):
        set(1)
        st.experimental_rerun()

def page_manager():
    if (get() == 1):
        page_1()
    elif (get() == 2):
        page_2()
    elif (get() == 3):
        page_3()


page_manager()
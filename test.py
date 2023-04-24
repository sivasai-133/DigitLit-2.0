import streamlit as st

from page import get,set


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

def page_3():
    set(3)
    st.title('admin')

    user = st.secrets['db_username']
    password = st.secrets['db_password']

    print(st.secrets)
    print(st.secrets.keys())

    with st.form(key='my_form'):
        text_input = st.text_input(label='Enter username')
        password_input = st.text_input(label='Enter password',type='password')
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if text_input == user and password_input == password:
            st.success('Login successful')
        else:
            st.error('Login unsuccessful')


def page_manager():
    if (get() == 1):
        page_1()
    elif (get() == 2):
        page_2()
    elif (get() == 3):
        page_3()


page_manager()
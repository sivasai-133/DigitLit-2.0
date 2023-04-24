import streamlit as st
import os
from page import get,set
from flag import get_,set_
import subprocess
# Read the requirements.txt file
# Need to run only when reboot is done

# if (get_() == 0):
#     with open('requirements.txt') as f:
#         requirements = f.read().splitlines()

#     # Install the required packages using pip
#     for package in requirements:
#         subprocess.check_call(['pip', 'install', package])
#     set_(1)

from PIL import Image
from streamlit_drawable_canvas import st_canvas
import numpy as np
import shutil
import io
import base64

cur = os.getcwd()

# Define a function to validate the input value
def validate_input(value):
    if value is not None:
        value = int(value)
        if value < 10 or value > 19:
            st.error("Please enter a value between 10 and 19.")
            return None
    return value

def draw_images():
    st.title("Draw Images")
    # Specify canvas parameters in application
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ("freedraw", "line", "circle")
    )

    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(0,0,0,0)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color="#000",
        background_color= '#fff',
        update_streamlit=True,
        height=150,
        width = 150,
        drawing_mode=drawing_mode,
        key="canvas",
    )

    if not os.path.exists(cur+'/dataset/'):
        os.makedirs( cur+ '/dataset/')


    # Add an input field to the Streamlit app
    value = None
    value = st.text_input("Enter a value between 10 and 19:","1", key="input_field")

    # Validate the input value
    validated_value = validate_input(value)

    # Do something interesting with the validated value
    if validated_value is not None :
        st.write("The validated value is:", validated_value)

    if (canvas_result.image_data is not None):
        # Save the image to a file
        st.image(canvas_result.image_data)
        image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        grayscale_image = image.convert('L')
        path = cur+ '/dataset/' + str(validated_value) + '/'
        if not os.path.exists(path) and validated_value is not None:
            os.makedirs(path)

         # Add a "Save Image" button that is only enabled when the user has completed the drawing
        if st.button("Save Image") and validated_value is not None:
                grayscale_image.save(path+f'Img_{validated_value}_{len(os.listdir(path))}.png')
                st.success("Image saved successfully.")
        else:
            st.warning("Please draw something on the canvas before saving.")

    else:
        st.warning("Please draw something on the canvas before saving.")


def display_images():
    # Add an input field to the Streamlit app
    value = None
    st.title("Display Images")
    if os.path.exists(cur+'/dataset/'):
        dataset_folder = cur+'/dataset/'
        if len(os.listdir(dataset_folder)) > 0:
            buffer = io.BytesIO()
            shutil.make_archive('dataset', 'zip', dataset_folder)
            with open('dataset.zip', 'rb') as f:
                buffer.write(f.read())
            with st.container():
                
                st.markdown("<div style='margin-left:auto; text-align:right;'>"
            "<p>Download Dataset: "
            "<a href='data:application/zip;base64,{}' download='dataset.zip'>"
            "<button>Download</button>"
            "</a></p>"
            "</div>".format(base64.b64encode(buffer.getvalue()).decode('utf-8')), unsafe_allow_html=True)



    with st.form(key='my_form'):
        value = st.text_input("Enter a value between 10 and 19:","1", key="input_field")
        submit_button = st.form_submit_button(label='Submit')
    
    # Validate the input value
    validated_value = validate_input(value)

    if validated_value is not None and submit_button:
        path = cur+'/dataset/' + str(validated_value) + '/'
        if os.path.exists(path) and len(os.listdir(path)) > 0:
            image_filenames = os.listdir(path)
            random_image_filename = np.random.choice(image_filenames)
            image = Image.open(os.path.join(path, random_image_filename))
            st.image(image, caption=f"Randomly selected image for value {validated_value}", use_column_width=True,width = 300)
        else:
            st.warning(f"No images found for value {validated_value}.")

def data_description():
    # Create a dictionary to store the image counts for each subfolder
    st.title("Dataset Description")
    subfolder_counts = {}

    dataset_path = cur+'/dataset/'

    # Loop through each subfolder in the dataset folder
    for subfolder_name in os.listdir(dataset_path):
        # Check if the subfolder name is a number between 10 and 19
        if subfolder_name.isdigit() and 10 <= int(subfolder_name) <= 19:
            # Get the path to the subfolder
            subfolder_path = os.path.join(dataset_path, subfolder_name)

            # Count the number of images in the subfolder
            image_count = 0
            for filename in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, filename)
                try:
                    with Image.open(file_path) as image:
                        image_count += 1
                except:
                    pass

            # Store the image count in the dictionary
            subfolder_counts[subfolder_name] = image_count

    # Calculate the total number of images
    total_count = sum(subfolder_counts.values())

    # Sort the subfolder counts by subfolder name
    sorted_counts = sorted(subfolder_counts.items(), key=lambda x: int(x[0]))

    # Display the results in a Streamlit table
    table_data = [{"Number": subfolder_name, "Image Count": image_count} for subfolder_name, image_count in sorted_counts]
    st.table(table_data)
    st.write(f"Total Images: {total_count}")
 

def admin_page():
    menu = ['Draw Images','Display Images', 'Data Description']
    choice = st.sidebar.selectbox('Select an option',menu)

    if choice == 'Display Images':
        display_images()
    elif choice == 'Draw Images':
        draw_images()
    else:
        data_description()

    if st.button('Return to Main Page',key = 'return2'):
        set(1)
        st.experimental_rerun()


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
    menu = ['Display Images', 'Data Description']
    choice = st.sidebar.selectbox('Select an option',menu)

    if choice == 'Display Images':
        display_images()
    else:
        data_description()

    if st.button('Return to Main Page',key = 'return1'):
        set(1)
        st.experimental_rerun()

def page_3():
    set(3)
    st.title('Admin')

    password = os.environ['db_password']

    if st.button('Return to Main Page',key = 'return'):
        set(1)
        st.experimental_rerun()

    with st.form(key='my_form'):
        password_input = st.text_input(label='Enter Key',type='password')
        submit_button = st.form_submit_button(label='Submit')

    

    if submit_button:
        if password_input == password:
            st.success('Login successful')
            set(4)
            st.experimental_rerun()

        else:
            st.error('Login unsuccessful')


if (get() == 1):
    page_1()
elif (get() == 2):
    page_2()
elif (get() == 3):
    page_3()
elif (get() == 4):
    admin_page()


import streamlit as st
import os
from page import get,set
from flag import get_,set_
import subprocess
# Read the requirements.txt file
# Need to run only when app is rebooted

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
import pandas as pd
import io
import base64

cur = os.getcwd()
password = os.environ['db_password']

# Define a function to validate the input value
def validate_input(value):
    if value is not None:
        value = int(value)
        if value < 10 or value > 19:
            st.error("Please enter a value between 10 and 19.")
            return None
    return value

def draw_page1():
    st.session_state['password'] = password

    with st.form(key='my_form'):
        password_input = st.text_input(label='Enter Key',type='password')
        submit_button = st.form_submit_button(label='Submit')


    if submit_button:
        if password_input == password:
            set(2)
            st.experimental_rerun()

        else:
            st.error('Incorrect Key')


def draw_page2():
    if 'password' not in st.session_state.keys() or st.session_state['password'] != password:
        set(1)
        st.experimental_rerun()

    st.title("Draw Digits")
    st.write(f'*- Draw a digit, Enter the label, Save the image*')
    # Specify canvas parameters in application
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ("freedraw", "line", "circle")
    )

    stroke_width = st.sidebar.slider("Stroke width: ", 1, 15, 6)

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
    value = st.text_input("Enter the label for the image","1", key="input_field")

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


def draw_images():
    
    if get() == 1:
        draw_page1()
    elif get() == 2:
        draw_page2()


def display_images():
    value = None
    st.title("Display Images")
    # Download the dataset as zip file
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


    # Taking the  input in the form
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
    st.title("DigitLit Dataset")
    st.write(f'*- Dataset created using StreamLit*')

    """
    - The dataset contains images of  digits between 10 and 19 (inclusive).
    - visit this [link](https://github.com/sivasai-133/DigitLit-2.0/blob/develop/README.md/) for more details.
    """


    # Create a dictionary to store the image counts for each subfolder
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
    table_data = [{ "number": subfolder_name ,f"image count": image_count} for subfolder_name, image_count in sorted_counts]
    df = pd.DataFrame(table_data)

    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # Display the table
    st.table(df)

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


    st.write(f"Total Images: {total_count}")
    
# Add pages to the Streamlit app
menu = ['Data Description','Display Images', 'Draw Images']
choice = st.sidebar.selectbox('Select an option',menu)

if choice == 'Draw Images':
    draw_images()
elif choice == 'Display Images':
    display_images()
else:
    data_description()

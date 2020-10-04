'''
Walk through:
    Streamlit Python Tutorial (Crash Course) - YouTube 
        https://www.youtube.com/watch?v=_9WiB2PDO7k&list=PLJ39kWiJXSixyRMcn3lrbv8xI8ZZoYNZU
'''

import streamlit as st

st.success('SUCCESS: Yippie Yay!')
st.warning('WARNING: Chetaawani!')
st.error('ERROR: Oh Fish!')
st.info('INFO: Gyaan')

try:
    with st.echo():
        z = x/0
        st.write(z)
except Exception as e:
    # Figure how to do this inside of a catch block
    st.exception(f'Error: Exception[{e}]!')

try:
    st.help(catch) # A good example of exception :)
except Exception as e:
    # Figure how to do this inside of a catch block
    st.exception(f'Error: Exception[{e}]!')
    

st.help(st.exception)  # Self Documenting - pretty handy to get inbuilt help
# st.help(range) More Examples

# Super Function Write
st.write('Just a plaint Text!')
st.write(range(0,10))


# Images
import urllib.request
from PIL import Image
url = 'https://assets.website-files.com/5dc3b47ddc6c0c2a1af74ad0/5e18182db827fa0659541754_RGB_Logo_Vertical_Color_Light_Bg.png'  # Huge
url = 'https://baseweb.design/images/streamlit-logo.png'

#img = Image.open('StreamLitLogo_light.png')
img = Image.open(urllib.request.urlopen(url))
with st.echo():
    width, height = img.size
    width
    height
st.image(img, width=width, caption='ST Image Example')

# Videos
import requests
url = 'http://techslides.com/demos/sample-videos/small.mp4'
response = requests.get(url)
st.write('Streamlit Video Example')
st.video(response.content)

# Audio
import requests
url = 'https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3'
response = requests.get(url)
st.write('Streamlit Audio Example')
st.audio(response.content)

# Widgets

# Checkbox
if st.checkbox('Show/Hide'):
    st.text('Show/Hide Illustration')

# RadioButton
status = st.radio('What is your status?', ('Active', 'Inactive'))
if status == 'Active':
    st.success('Active')
else:
    st.error('Inactive')

# SelectBox
occupation = st.selectbox('Your Occupation', ('SW', 'Plumber', 'Data Scientist', 'Doctor'))
st.info(f'Selected this occupation = {occupation}')

# MultiSelect
location = st.multiselect('Where do you live?', ('LA', 'UK', 'SGP', 'IN'))
st.info(f'Selected location = {location}')
st.write(location)

# Slider
age = st.slider('How old are you?', 1, 100)
st.info(f'Your age is {age}')

# Button
if st.button('Submit'):
    st.info('What do you wish to do when Submit is hit?')

# TextInput
name = st.text_input('Full Name', 'Enter your name here...')
st.info(f'The name you entered is {name}')
if st.button('Confirm'):
    result = name.title()
    st.info(result)

# TextArea
desc = st.text_area('Full Desc', 'Enter your desc here...')
st.info(f'The desc you entered is {desc}')
if st.button('Describe'): # This name can't be the same as previous names
    result = desc.title()
    st.info(result)

# DateInput
import datetime
dob = st.date_input('Date Of Birth:', datetime.datetime.now())

# TimeInput
current_time = st.time_input('Time now is:', datetime.time())

# Displaying JSON
st.text('Displaying JSON')
st.json({ 'name': name, 'age': age, 'desc': desc, 'location': location})


# Displaying Raw Code
st.text('Displaying Raw Code')
st.code('''
# The Following Code Should Show up
logger.info('Will this work?')
with open(filename, 'rb') as file_handle:
    content = file_handle.read()
''')

# Display as well as execute code
with st.echo():
        # Comments display as well
        import pandas as pd
        df = pd.DataFrame()


# Progress Bar
bar = st.progress(0)
for page in range(10):
    bar.progress(page+1) # Not going beyond the first?

# Spinner
import time
with st.spinner('Loading...'):
    time.sleep(3)
st.success('Loaded!')

# Balloons
st.balloons() # Not showing long enough


# SideBar
sb = st.sidebar
sb.header('Primary Header')
sb.subheader('Secondary Header')



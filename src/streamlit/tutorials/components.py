import streamlit as st
import pandas as pd

import streamlit.components.v1 as components


URL = 'https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/block_rejected_transactions/27/2721/2721005/masuda_2721005_block_rejected_transactions.csv'
URL = '../../Data/masuda_2721005_block_rejected_transactions.csv'
ROWS = 100

st.title('Demo for Streamlit Components')

@st.cache
def load_data(nrows, file_name = None):
    if file_name:
        return pd.read_csv(file_name, nrows=nrows)
    else:
        return pd.read_csv(URL, nrows=nrows)

rows = st.selectbox('selected_rows', range(10,100), 5)
#rows = st.slider('nrows')

data_load_state = st.text('Loading data...')
if st.checkbox('Upload file'):
    csv_file = st.file_uploader('Upload the CSV file')
    data = load_data(rows, csv_file)
else:
    data = load_data(rows)    
data_load_state.text('Loading data...done!')


st.header('Rejected Report')

st.subheader(f'No of Rows: {rows}')

st.subheader('Raw data')
st.write(data)

# embed a twitter feed in streamlit
components.html("""
<html>
<body>

<h1>The datalist element</h1>

<form action="/action_page.php" method="get">
  <label for="browser">Choose your browser from the list:</label>
  <input list="browsers" name="browser" id="browser">
  <datalist id="browsers">
    <option value="Edge">
    <option value="Firefox">
    <option value="Chrome">
    <option value="Opera">
    <option value="Safari">
  </datalist>
  <input type="submit">
</form>

<p><strong>Note:</strong> The datalist tag is not supported in Safari 12.0 (or earlier).</p>

</body>
</html>
                <a class="twitter-timeline"
                href="https://twitter.com/streamlit?ref_src=twsrc%5Etfw">Tweets by streamlit</a>
                <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                """
                )

# embed streamlit docs in a streamlit app
components.iframe("https://docs.streamlit.io/en/latest")

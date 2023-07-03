## Main File

import streamlit as st
import zipfile
import io
import json
import pandas as pd
from util import page_summarizer_json,table_generator,page_summarizer_df

st.title('PowerBI Standardization Checker')

# Upload the Source zip file
ss = st.file_uploader('Upload a PBIX file')

# --------- Removing Streamlit's Hamburger and Footer starts ---------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            a {text-decoration: none;}
            .css-15tx938 {font-size: 18px !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --------- Removing Streamlit's Hamburger and Footer ends ------------

if ss:
    if 1==1:
        # In-memory byte stream to hold the destination zip file data
        zip_data = io.BytesIO()

        # Extract the files from the source zip file and re-zip them into a destination zip file
        with zipfile.ZipFile(ss, 'r') as source_zip:
            with zipfile.ZipFile(zip_data, 'w') as destination_zip:
                # Iterate over the files in the source zip file
                for name in source_zip.namelist():

                    # Skip the Security Binding file
                    if name == 'SecurityBindings':
                        continue

                    # Manipulate the Layout file
                    if name == 'Report/Layout':
                        # Read the contents of the layout file
                        data = source_zip.read(name).decode('utf-16 le')
                        # Generate page wise required json structure  
                        df1=page_summarizer_json(data)
                        # Generate page wise required dataframe
                        df2=page_summarizer_df(df1)
                        # st.write(df2) DEBUG
                        st.header('Font Family Summary')
                        df2=table_generator(df1)
                        st.write(df2)

                        # except:
                        #     print('hi')
                        # Add the manipulated layout data to the destination zip file

                    else:
                        # Add the file to the destination zip file as-is
                        binary_data = source_zip.read(name)
                        destination_zip.writestr(name, binary_data)


        # Download the destination file
        st.download_button(
            label='Download Ouput JSON file',
            data=zip_data.getvalue(),
            file_name='destination.pbix',
            mime='application/pbix'
        )
    else:
        print('')


st.markdown('---')
st.markdown('Made with :heart: by [Sahil Choudhary](https://www.sahilchoudhary.ml/)')

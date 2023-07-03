## Research
# Using config to get all the information


import streamlit as st
import zipfile
import io
import json
import pandas as pd
from util import page_summarizer_json,ff_table_generator,page_summarizer_df,fs_table_generator,msg_printer

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
                for name in source_zip.namelist(): # Iterate over the files in the source zip file
                    if name == 'SecurityBindings': # Skip the Security Binding file
                        continue

                    if name == 'Report/Layout':
                        data = source_zip.read(name).decode('utf-16 le') # Read the contents of the layout file 
                        
                        ####### Font Family Generator starts #######
                        df1=page_summarizer_json(data) # Generate page wise required json structure 
                        df2=page_summarizer_df(df1) # Generate page wise required dataframe
                        # st.write(df2) DEBUG
                        st.header('Font Family')
                        df3=ff_table_generator(df1)
                        msg_printer(df3,'Font Family')
                        st.write('Report Analysis:')
                        st.write(df3)
                        ####### Font Family Generator ends #######

                        ####### Font Size Generator starts #######
                        st.header('Font Size')
                        df4=fs_table_generator(df1)
                        msg_printer(df4,'Font Size')
                        st.write('Report Analysis:')
                        st.write(df4)
                        ####### Font Size Generator ends #######


                        # except:
                        #     print('hi')
                        # Add the manipulated layout data to the destination zip file

                    else:
                        # Add the file to the destination zip file as-is
                        binary_data = source_zip.read(name)
                        destination_zip.writestr(name, binary_data)


        # Download the destination file
        st.download_button(
            'Export results to csv',
            df4.to_csv(),
            file_name="Documentation-csv-output",
            mime="text/csv"
        )
    else:
        print('')


st.markdown('---')
st.markdown('Made with :heart: by [Sahil Choudhary](https://www.sahilchoudhary.ml/)')

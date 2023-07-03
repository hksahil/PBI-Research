import json
import streamlit as st
import pandas as pd

def page_summarizer_json(data):
        report_chart_info = {}
        data = json.loads(data)
        for section in data['sections']:
            report_page_name = section['displayName']
            # Get the chart type and font size from each visual container in the section
            chart_info = []
            for container in section['visualContainers']:
                config = json.loads(container['config'])
                                    
                # Get Chart Type
                chart_type = config['singleVisual']['visualType']

                # Get Font color
                font_color = config["singleVisual"]["vcObjects"]["title"][0]["properties"]["fontColor"]["solid"]["color"]["expr"]["ThemeDataColor"]["ColorId"]
                                    
                # Get Font family
                font_family = config["singleVisual"]["vcObjects"]["title"][0]["properties"]["fontFamily"]["expr"]["Literal"]["Value"]
                                    
                # Get font Size
                try:
                    font_size = config["singleVisual"]["vcObjects"]["title"][0]["properties"]["fontSize"]["expr"]["Literal"]["Value"]
                except:
                    font_size = 12

                # Get Width
                width = container['width']
                                    
                # Get Height
                height = container['height']
                                    
                chart_info.append({'chart_type': chart_type, 'font-family': font_family,'font-size':font_size})
                              
            report_chart_info[report_page_name] = chart_info

        data=report_chart_info
        return data

def page_summarizer_df(data):
    df = pd.DataFrame(columns=["Page", "Index", "Chart Type", "Font Family"])
   # Iterate over the pages in the JSON data
    for page, charts in data.items():
        # Iterate over the charts in each page
        for index, chart in enumerate(charts):
            chart_type = chart["chart_type"]
            font_family = chart["font-family"]
            
            # Append the data to the dataframe
            df = df.append({"Page": page, "Index": index, "Chart Type": chart_type, "Font Family": font_family}, ignore_index=True)
    return df

def ff_table_generator(data):
    font_families = []
    pages_used = []
    chart_types=[]
    for page, items in data.items():
        for item in items:
            font_family = item["font-family"]
            font_families.append(font_family)
            chart_type = item["chart_type"]
            chart_types.append(chart_type)
            pages_used.append(page)
            df = pd.DataFrame({"Font Family": font_families, "Pages": pages_used,"Chart types":chart_types})
            frequency_df = df.groupby(["Font Family", "Pages","Chart types"]).size().reset_index()
            frequency_df.columns = ["Font Family", "Pages","Chart types","Frequency"]
            frequency_df['Info']=frequency_df['Pages']+ "'s " + frequency_df['Chart types']
    # Remove the quotes from the Font Family column
    frequency_df["Font Family"] = frequency_df["Font Family"].str.replace("'", "")
    grouped_df = frequency_df.groupby('Font Family').agg({'Info': lambda x: ', '.join(map(str, x)), 'Frequency': 'sum'}).reset_index()
    #grouped_df=grouped_df.rename({"Frequency":"# of charts"})
    grouped_df = grouped_df.rename(columns={'Frequency': '# of charts'})    
    # Calculate the total sum of the column
    total = grouped_df['# of charts'].sum()

    # Calculate the percentages and assign them to a new column
    grouped_df['Percent of total'] = round((grouped_df['# of charts'] / total) * 100,1).astype(str)
    grouped_df = grouped_df[['Font Family', '# of charts', 'Percent of total','Info']]

    return grouped_df

def fs_table_generator(data):
    font_sizes = []
    pages_used = []
    chart_types=[]
    for page, items in data.items():
        for item in items:
            font_size = item["font-size"]
            font_sizes.append(font_size)
            chart_type = item["chart_type"]
            chart_types.append(chart_type)
            pages_used.append(page)
            df = pd.DataFrame({"Font Sizes": font_sizes, "Pages": pages_used,"Chart types":chart_types})
            frequency_df = df.groupby(["Font Sizes", "Pages","Chart types"]).size().reset_index()
            frequency_df.columns = ["Font Sizes", "Pages","Chart types","Frequency"]
            frequency_df['Info']=frequency_df['Pages']+ "'s " + frequency_df['Chart types']
    # Remove the quotes from the Font Family column
    frequency_df["Font Sizes"] = frequency_df["Font Sizes"].str.replace("'", "")
    grouped_df = frequency_df.groupby('Font Sizes').agg({'Info': lambda x: ', '.join(map(str, x)), 'Frequency': 'sum'}).reset_index()
    #grouped_df=grouped_df.rename({"Frequency":"# of charts"})
    grouped_df = grouped_df.rename(columns={'Frequency': '# of charts'})
    grouped_df = grouped_df[['Font Sizes', '# of charts', 'Info']]
    grouped_df['Font Sizes']=grouped_df['Font Sizes'].str.replace('D','')
    
    # Calculate the total sum of the column
    total = grouped_df['# of charts'].sum()

    # Calculate the percentages and assign them to a new column
    grouped_df['Percent of total'] = round((grouped_df['# of charts'] / total) * 100,1).astype(str)
    grouped_df = grouped_df[['Font Sizes', '# of charts','Percent of total','Info']]
    return grouped_df

def msg_printer(df,flag):
    total_rows = df.shape[0]

    if flag=='Font Family':
        unique_font_family = df['Font Family'].nunique()
        if total_rows == 1:
            st.success(" ✅ You have used only one font family in chart titles")
        else:
            st.error(f"⚠️ You have used {unique_font_family} different font families in chart titles")

    else :
        unique_font_size = df['Font Sizes'].nunique()
        if total_rows == 1:
            st.success("✅ You have used only one font size in chart titles")
        else:
            st.error(f"⚠️ You have used {unique_font_size} different font sizes in chart titles")

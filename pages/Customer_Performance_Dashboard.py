import datetime
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from PIL import Image
from streamlit_plotly_events import plotly_events



page_icon = Image.open("./pages/favicon.ico")
st.set_page_config(page_title="Smart Fill", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")


file_path = "data/FamilyOfficeEntityDataSampleV1.2.xlsx"  # Replace "your_file.xlsx" with the path to your Excel file
sheetName_clProfile = "Client Profile"
sheetName_familyMember = "Family Members"
df_clProfile = pd.read_excel(file_path, sheet_name=sheetName_clProfile)
df_clProfileFiltered = pd.read_excel(file_path, sheet_name=sheetName_clProfile)
df_familyMem = pd.read_excel(file_path, sheet_name=sheetName_familyMember)

now = datetime.now()
df_clProfile['Date of Birth'] = pd.to_datetime(df_clProfile['Date of Birth'], format='%m/%d/%y')
df_clProfile['Age'] =((now - df_clProfile['Date of Birth']).dt.days / 365.25).astype(int)





df_clProfileFiltered['Date of Birth'] = pd.to_datetime(df_clProfileFiltered['Date of Birth'], format='%m/%d/%y')
df_clProfileFiltered['Age'] =((now - df_clProfileFiltered['Date of Birth']).dt.days / 365.25).astype(int)


col_1_widths = (20, 10)
col_1_gap = 'medium'

# black_theme = """
# <style>
# body {
#     background-color: #000000;
#     color: #FFFFFF;
# }
# </style>
# """

# # Display the custom CSS styles using st.markdown
# st.markdown(black_theme, unsafe_allow_html=True)



# Create the first set of columns
col_1 = st.columns(col_1_widths, gap=col_1_gap)


# Content for the first set of columns
with col_1[0]:
    # st.image("img/FamiologyTextLogo.png")

    st.markdown('<h4 style="font-size: 36px;">CUSTOMER PERFORMANCE DASHBOARD</h4>', unsafe_allow_html=True)


with col_1[1]:
    #listOfStates = df_clProfile["State"]
    stateFilterList = sorted(pd.unique(df_clProfile['State']))
    stateFilterList.insert(0, "ALL STATES")

    st.markdown("<h4 style='text-align: center; padding: 0px; margin:0px'>State Filter</h4>", unsafe_allow_html=True)

    selectBox_col = st.columns(1)
    with selectBox_col[0]:
        selectedState = st.selectbox("", options=stateFilterList, label_visibility='hidden')
        if selectedState is not "ALL STATES":
            df_clProfileFiltered = df_clProfileFiltered[df_clProfileFiltered["State"] == selectedState]

col_2_widths = (8, 8, 8, 12)
col_2_gap = 'medium'



# Create the second set of columns
col_2 = st.columns(col_2_widths, gap=col_2_gap)



with col_2[0]:
    # calculate the value from the xlsx
    column_name = "Net Worth"

    df_clProfileFiltered[column_name] = df_clProfileFiltered[column_name].replace({'\$': '', ',': ''}, regex=True).astype(int)

    # Calculate the sum of all values in the column
    total_sum = df_clProfileFiltered[column_name].sum()
    million_representation = "$ {:.2f}M".format(total_sum / 1_000_000)

    # st.metric(label="## Total Revenue", value=million_representation)
    # Show total revenue
    st.markdown("<h4 style='text-align: center;'>Total Revenue</h4>", unsafe_allow_html=True)

    metric_col =  st.columns(1)

    with metric_col[0]:
        st.markdown(f"<div style='text-align: center;'>{million_representation}</div>", unsafe_allow_html=True)




with col_2[1]:
    num_rows = df_clProfileFiltered.shape[0]
    # st.metric(label="**Total Customers**", value = num_rows)

    st.markdown("<h4 style='text-align: center;'>Total Customers</h4>", unsafe_allow_html=True)

    totalCust_col =  st.columns(1)


    with totalCust_col[0]:
        st.markdown(f"<div style='text-align: center;'>{num_rows}</div>", unsafe_allow_html=True)

with col_2[2]:

    
    # Calculate the average age
    average_age = df_clProfileFiltered['Age'].mean()
    # st.metric(label="**Customer Avg. age**", value="{:.2f}".format(average_age))

    st.markdown("<h4 style='text-align: center;'>Customer Avg. age</h4>", unsafe_allow_html=True)

    age_col =  st.columns(1)

    with age_col[0]:
        st.markdown(f"<div style='text-align: center;'>{int(average_age)}</div>", unsafe_allow_html=True)

with col_2[3]:
    # st.markdown("Year Slicer")
    st.write("<h4 style='text-align: center;'>Age</h4>", unsafe_allow_html=True)

    lower_year = -1
    upper_year = 199
    
    maxAge = df_clProfileFiltered['Age'].max()
    minAge = df_clProfileFiltered['Age'].min()

    year_list = [str(year) for year in range(minAge, maxAge)]  # Example year range


    reversed_yearlist = year_list[::-1]



    if 'upper_year' not in st.session_state:
        st.session_state.upper_year = None
    if 'lower_year' not in st.session_state:
        st.session_state.lower_year = None


    if st.session_state.upper_year != None:
        print("Upper Year changed", st.session_state.upper_year)
        index_of_value = year_list.index(st.session_state.upper_year)  # Get the index of the value
        sublist_from_middle = year_list[:index_of_value -1]
        year_list = sublist_from_middle


    

    year_lower, year_upper = st.columns(2)

    with year_lower:
        print("Running Lower again")
        lower_year = st.selectbox("Select lower range of the year:", year_list, label_visibility="collapsed", key="lowerYearKey")
        # if st.session_state.lower_year != lower_year:
        #     st.session_state.lower_year = lower_year

    # if st.session_state.lower_year != None:
        index_of_value = year_list.index(lower_year)  # Get the index of the value
        sublist_from_middle = year_list[index_of_value + 1:]
        reversed_yearlist = sublist_from_middle[::-1]

    with year_upper:
        print("setting upperLayer List")
        upper_year = st.selectbox("Select upper range of the year:", reversed_yearlist, label_visibility="collapsed",key="upperYearKey")

        index_of_value = year_list.index(upper_year)  # Get the index of the value
        sublist_from_middle = year_list[:index_of_value -1]
        year_list = sublist_from_middle

    # print("upperYear is thissss ", upper_year)
    # if st.session_state.upper_year != upper_year:
    #     st.session_state.upper_year = upper_year
    #     print("running again")
            # st.rerun()


        # if st.session_state.upper_year != upper_year:
        #     print("Upper Year changed", upper_year)
        #     index_of_value = year_list.index(upper_year)  # Get the index of the value
        #     sublist_from_middle = year_list[:index_of_value -1]
        #     year_list = sublist_from_middle

        #     st.session_state.upper_year = upper_year


            # print(int(upper_year))
            # if upper_year is not 199:
            #     print("Selected lower Layer", upper_year)
            #     index_of_value = year_list.index(upper_year)  # Get the index of the value
            #     sublist_from_middle = year_list[:index_of_value -1]
            #     year_list = sublist_from_middle
            #     with year_lower:
            #         lower_year = st.selectbox("Select lower range of the year:", year_list, label_visibility="collapsed")



    lower_year = int(lower_year)
    upper_year = int(upper_year)

    df_clProfileFiltered = df_clProfileFiltered[(df_clProfileFiltered['Age'] >= lower_year) & (df_clProfileFiltered['Age'] <= upper_year)]





col_3_widths = (10, 10, 10)
col_3_gap = 'medium'

col_3 = st.columns(col_3_widths, gap=col_3_gap)




with col_3[0]:
        
        merged_df = pd.merge(df_clProfileFiltered, df_familyMem, on="ClientID", how="left")
        column_name = "Net Worth"

        child_records = merged_df[merged_df["Relationship"] == "Child"]
        totalRevenue = df_clProfileFiltered[column_name].sum()
        total_sum_wt_chld = child_records[column_name].sum()



        percentageForChld = total_sum_wt_chld * 100/totalRevenue

        

        # st.write("<div style='text-align: center; font-weight: bold;'>Revenue from customers with children</div>", unsafe_allow_html=True)
        st.write("<h4 style='text-align: center; font-weight: bold;'>Revenue from customers with children</h4>", unsafe_allow_html=True)
        labels = 'Revenue with child', 'Revenue without child'
        sizes = [percentageForChld, 100 - percentageForChld]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots(figsize=(7, 7))
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%0.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        fig1.patch.set_alpha(0)

        st.pyplot(fig1)


with col_3[1]:

    # st.write("<div style='text-align: center; font-weight: bold;'>Total Revenue by Age group</div>", unsafe_allow_html=True)
    st.write("<h4 style='text-align: center; font-weight: bold;'>Total Revenue by Age group</h4>", unsafe_allow_html=True)

    df_sorted = df_clProfileFiltered.sort_values(by='Age')
    df_sorted['Net Worth'] = df_sorted['Net Worth'].replace({'\$': '', ',': ''}, regex=True).astype(int)

    # maxAge = df_clProfileFiltered['Age'].max()
    # minAge = df_clProfileFiltered['Age'].min()

    # year_list = [str(year) for year in range(minAge, maxAge)]  # Example year range

    # # Determine the number of bins based on the length of the numbers list
    # if len(year_list) > 30:
    #     num_bins = 4
    # elif len(year_list) > 20:
    #     num_bins = 3
    # else:
    #     num_bins = 2

    # # Use numpy's histogram function to compute the histogram
    # hist, bins = np.histogram(year_list, bins=num_bins)

    # print("bins", bins)

    bins = [30, 40, 50, 60]
    labels_ages = ['30-40', '40-50', '50-60']


    df_sorted['AgeGroup'] = pd.cut(df_sorted['Age'], bins=bins, labels=labels_ages, right=True)

    revenue_by_age_group = df_sorted.groupby('AgeGroup')['Net Worth'].sum().tolist()

    print("revenue_by_age_group", revenue_by_age_group)


    labels = 'Revenue with child', 'Revenue without child'
    sizes = [percentageForChld, 100 - percentageForChld]
    explode = (0.0, 0.0, 0.0, 0.0, 0.0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots(figsize=(3,3))
    ax1.pie(revenue_by_age_group, labels=labels_ages, autopct='%0.1f%%', 
            shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


    colors = ['green', 'orange', 'red', 'blue', 'yellow']

    fig1.patch.set_alpha(0)

    st.pyplot(fig1)

    

with col_3[2]:
    # st.write("<div style='text-align: center; font-weight: bold;'>Total Revenue by customer status</div>", unsafe_allow_html=True)
    st.write("<h4 style='text-align: center; font-weight: bold;'>Total Revenue by customer status</h4>", unsafe_allow_html=True)
    uniqueValues = df_clProfileFiltered['Status'].unique()
    groupedPerStatus = df_clProfileFiltered.groupby('Status')['Net Worth'].sum()
    indexByStatus = groupedPerStatus.index.tolist()
    listByStatus = groupedPerStatus.tolist()

    fig, ax = plt.subplots()
    # ax.set_facecolor('rgb(14, 17, 23)')  # Set the background color
    ax.set_facecolor((14/255, 17/255, 23/255))  # RGB values as a tuple
    ax.set_facecolor("white")  # RGB values as a tuple



    df = pd.DataFrame({"Net Worth in Millions": listByStatus}, index= indexByStatus )
    fig = df.plot.barh(ax= ax, stacked=False).figure


    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    ax.set_title('Total Revenue by Customer Status', color='white')
    ax.set_xlabel('Revenue (in millions)', color='white')
    ax.set_ylabel('Customer Status', color='white')

    fig.patch.set_alpha(0)
    st.pyplot(fig)



col_4_widths = (15, 5, 25)
col_4_gap = 'medium'

# Create the second set of columns
col_4 = st.columns(col_4_widths, gap=col_4_gap)

with col_4[0]:
    df_clProfileFiltered['Net Worth'] = df_clProfileFiltered['Net Worth'].replace({'\$': '', ',': ''}, regex=True).astype(int)
    df_sorted_netWorth = df_clProfileFiltered.sort_values(by='Net Worth')
    
    top_five_individuals = df_sorted_netWorth.head()

    top_five_individuals["Net Worth"] = top_five_individuals["Net Worth"]/1_000_000

    # st.write("<div style='text-align: center; font-weight: bold;'>Top 5 Customers by Revenue</div>", unsafe_allow_html=True)
    st.write("<h4 style='text-align: center; font-weight: bold;'>Top 5 Customers by Revenue</h4>", unsafe_allow_html=True)

    fig, ax = plt.subplots()
    # ax.set_facecolor('rgb(14, 17, 23)')  # Set the background color
    ax.set_facecolor((14/255, 17/255, 23/255))  # RGB values as a tuple
    ax.set_facecolor("white")  # RGB values as a tuple

    df = pd.DataFrame({"Net Worth in Millions": top_five_individuals["Net Worth"].to_list()}, index=top_five_individuals["First Name"])

    fig = df.plot.barh(ax = ax, stacked=True).figure

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    ax.set_title('Top 5 Customers by revenue', color='white')
    ax.set_xlabel('Revenue (in millions)', color='white')
    ax.set_ylabel('First Name', color='white')

    fig.patch.set_alpha(0)

    st.pyplot(fig)
    


with col_4[2]:

    
    # st.write("<div style='text-align: center; font-weight: bold;'>Revenue by Gender</div>", unsafe_allow_html=True)
    st.write("<h4 style='text-align: center; font-weight: bold;'>Revenue by Gender</h4>", unsafe_allow_html=True)
    col_gender_width = (10, 10)
    col_gender_gap = 'medium'

    genderRev_upper = st.columns(col_gender_width, gap=col_gender_gap)
    with genderRev_upper[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        
    
    with genderRev_upper[1]:
        st.markdown("<br>", unsafe_allow_html=True)

    
    genderRev = st.columns(col_gender_width, gap=col_gender_gap)

    column_name = "Net Worth"

    df_clProfileFiltered[column_name] = df_clProfileFiltered[column_name].replace({'\$': '', ',': ''}, regex=True).astype(int)

    with genderRev[0]:

        MaleIndividuals = df_clProfileFiltered[df_clProfileFiltered["Gender"] == "M"]
        
        # Calculate the sum of all values in the column
        total_sum_male = MaleIndividuals[column_name].sum()
        million_representation_male = "$ {:.2f}M".format(total_sum_male / 1_000_000)

        # st.metric(label="**Males**", value=million_representation_male)

        st.markdown("<h5 style='text-align: center; padding:2vh; font-size:2vh'>Males</h5>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; padding:2vh; font-size:1vh''>{million_representation_male}</div>", unsafe_allow_html=True)
    

    with genderRev[1]:
        FemaleIndividuals = df_clProfileFiltered[df_clProfileFiltered["Gender"] == "F"]
        total_sum_female = FemaleIndividuals[column_name].sum()
        million_representation_female = "$ {:.2f}M".format(total_sum_female / 1_000_000)


        st.markdown("<h5 style='text-align: center; padding:2vh; font-size:2vh'>Females</h5>", unsafe_allow_html=True)
    
        st.markdown(f"<div style='text-align: center; padding:2vh; font-size:1vh'>{million_representation_female}</div>", unsafe_allow_html=True)

import streamlit as st
import pdfplumber
from PIL import Image
from pdf2image import convert_from_bytes
import io
import fitz 
import os
from transformers import CLIPProcessor, CLIPModel
CLIPProcessor.safety_checker = None
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import base64

page_icon = Image.open(r"C:\Users\tanis\Documents\TheoremLabs.io\famiologyaccelerators\favicon.ico")
st.set_page_config(page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")

# from streamlit_option_menu import option_menu

# @st.cache_data(allow_output_mutation=True)
# def get_base64_image(image_path):
#     with open(image_path, "rb") as img_file:
#         return base64.b64encode(img_file.read()).decode()

# image_base64 = get_base64_image("C:/Users/tanis/Documents/TheoremLabs.io/famiologyaccelerators/FamiologyTextLogo.png")

# def add_logo(image_base64):
#     st.markdown(
#         """
#         <style>
#             [data-testid="stSidebarNav"] {
#                 background-image: url(data:image/png;base64,{image_base64});
#                 background-repeat: no-repeat;
#                 padding-top: 120px;
#                 background-position: 20px 20px;
#                 background-size: contain;
#             }

#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# add_logo(image_base64)

# def add_logo(logo_path, width, height):
#     """Read and return a resized logo"""
#     logo = Image.open(logo_path)
#     modified_logo = logo.resize((width, height))
#     return modified_logo

# my_logo = add_logo(logo_path=r"C:\Users\tanis\Documents\TheoremLabs.io\famiologyaccelerators\FamiologyTextLogo.png", width=50, height=60)
# st.sidebar.image(my_logo)

# @st.cache(allow_output_mutation=True)
# def get_base64_of_bin_file(png_file):
#     with open(png_file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# def build_markup_for_logo(
#     png_file,
#     background_position="50% 10%",
#     margin_top="10%",
#     image_width="60%",
#     image_height="",
# ):
#     binary_string = get_base64_of_bin_file(png_file)
#     return """
#             <style>
#                 [data-testid="stSidebarNav"] {
#                     background-image: url("data:image/png;base64,%s");
#                     background-repeat: no-repeat;
#                     background-position: 20px;
#                     margin-top: %s;
#                     background-size: %s %s;
#                 }
#             </style>
#             """ % (
#         binary_string,
#         background_position,
#         margin_top,
#         image_width,
#         image_height,
#     )

# def add_logo(png_file):
#     logo_markup = build_markup_for_logo(png_file)
#     st.markdown(
#         logo_markup,
#         unsafe_allow_html=True,
#     )

# add_logo(r"C:\Users\tanis\Documents\TheoremLabs.io\famiologyaccelerators\FamiologyTextLogo.png")

# st.markdown("# Home")

file = open(r"C:\Users\tanis\Documents\TheoremLabs.io\famiologyaccelerators\FamiologyTextLogo.png", "rb")
contents = file.read()
img_str = base64.b64encode(contents).decode("utf-8")
buffer = io.BytesIO()
file.close()
img_data = base64.b64decode(img_str)
img = Image.open(io.BytesIO(img_data))
resized_img = img.resize((400, 100))  # x, y
resized_img.save(buffer, format="PNG")
img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url('data:image/png;base64,{img_b64}');
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def documentdetector():
    def img2text(uploaded_file, options):
        model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")
        if isinstance(uploaded_file, Image.Image):
            image = uploaded_file
        else:
            image = Image.open(uploaded_file)

        array = ["Passport", "Driver License", "Green Card", "401K-statement", "Last-will-and-testament", "life-insurance", "W2-form", "f8889_HSA", "1040-Tax-Return"]
        inputs = processor(text=array, images=image, return_tensors="pt", padding=True)

        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image  
        probs = logits_per_image.softmax(dim=1)  

        probs = probs.tolist()
        flat_probs = [prob for sublist in probs for prob in sublist]
        max_prob = max(flat_probs)
        index_of_max = flat_probs.index(max_prob)
        if index_of_max == 0:
            message = "Your documents have been uploaded successfully. Thanks for submitting your Passport."
        elif index_of_max == 1:
            message = "Your documents have been uploaded successfully. Thanks for submitting your Driver License."
        elif index_of_max == 2:
            message = "Your documents have been uploaded successfully. Thanks for submitting your Green Card."
        elif index_of_max == 3:
            message = "Your documents have been uploaded successfully. Thanks for submitting your 401K Statement."
        elif index_of_max == 4:
            message = "Your documents have been uploaded successfully. Thanks for submitting your Will & POAs Document."
        elif index_of_max == 5:
            message = "Your documents have been uploaded successfully. Thanks for submitting your Life Insurance Policy."
        elif index_of_max == 6:
            message = "Your documents have been uploaded successfully. Thanks for submitting your W2 Form."
        elif index_of_max == 7:
            message = "Your documents have been uploaded successfully. Thanks for submitting your HSA Statement."
        elif index_of_max == 8:
            message = "Your documents have been uploaded successfully. Thanks for submitting your Income Statement Document."

        styled_message = f"<div style='font-size:28px;font-weight:bold;border: 2px solid Green;padding:10px;'>{message}</div>"
        st.markdown(styled_message, unsafe_allow_html=True)
        # styled_message = f"<span style='font-size:25px;font-weight:bold;'>{message}</span>"
        # st.markdown(styled_message, unsafe_allow_html=True)
        # st.write("Your documents have been uploaded successfully. Thanks for submitting your ", array[index_of_max], ".")
        # print("done with classification")
        st.subheader("The Probabilites are as follows")
        if "Passport" in options:
            st.write("Passport - ", flat_probs[0])
        if "Driver License" in options:
            st.write("Driver License - ", flat_probs[1])
        if "Green Card" in options:
            st.write("Green Card - ", flat_probs[2])
        if "401K-statement" in options:
            st.write("401K Statement - ", flat_probs[3])
        if "Last-will-and-testament" in options:
            st.write("Will & POAs Document - ", flat_probs[4])
        if "life-insurance" in options:
            st.write("Life Insurance Policy - ", flat_probs[5])
        if "W2-form" in options:
            st.write("W2 Form - ", flat_probs[6])
        if "f8889_HSA" in options:
            st.write("HSA Statement - ", flat_probs[7])
        if "Income-Statement" in options:
            st.write("Income-Statement ", flat_probs[8])
        # st.write("Passport - ",flat_probs[0], "\nDriver License - ", flat_probs[1], "\nGreen Card - ", flat_probs[2], "401K Statement - ", flat_probs[3], "Will & POAs Document - ", flat_probs[4], "Life Insurance Policy - ", flat_probs[1], "W2 Form - ", flat_probs[1], "HSA Statement - ", flat_probs[1])
        # # st.success(message)
        # st.write("We'll take care of the rest.")
        # st.write("Accuracy - ", max_prob)
        # return array[index_of_max]


    # st.sidebar.info("Hello World")
    def main1():
        # img = Image.open('/Users/atharvabapat/Desktop/Theoremlabs-project/favicon (2).ico')
        # st.set_page_config(page_title="Document Identification")
        
        # st.set_page_config(page_title='Famiology.docdetector', page_icon=r"C:\Users\tanis\Documents\TheoremLabs.io\famiologyaccelerators\favicon.ico")
        st.header('Famiology Document Detector')
        # st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)
        
        with st.sidebar:
            st.header('About App')
            # st.header('Smart Document Recognition: Instantly Identify Uploaded Documents')
            expander = st.expander("Smart Document Recognition: \n\n Instantly Identify Uploaded Documents: ")
            expander.write('Empower your document management process with Smart Document Recognition. This advanced feature swiftly identifies the type of document you upload, making document handling effortless and efficient.')
            # st.header('How It Works: ')
            expander = st.expander("How It Works:")
            expander.write('Upload Your Document: Select the document you wish to process using the provided file upload button. \n\n Intelligent Analysis: Our system employs cutting-edge technology to analyze the documents structure, layout, and content. \n\n Automatic Identification: Based on the analysis, Smart Document Recognition accurately identifies the document type, whether its an identification document, real estate document, 401k document or any other document format. \n\n Streamlined Processing: With the document type identified, our platform can seamlessly route it to the appropriate workflow or apply predefined actions, saving you valuable time and effort.')
            # st.header('What Problem it Solves?')
            expander = st.expander("Configuration")
            options = st.multiselect(label = 'Choose the Parameter to classify', options= ["Passport", "Driver License", "Green Card", "401K-statement", "Last-will-and-testament", "life-insurance", "W2-form", "f8889_HSA", "1040-Tax-Return"])
            expander = st.expander("What Problem it Solves?")
            expander.write('Efficiency: Instantly recognize document types without manual intervention. \n\n Accuracy: Ensure accurate processing and categorization of documents. \n\n Productivity: Automate document handling workflows for smoother operations.')
            # st.header('Value') 
            expander = st.expander("Value")
            expander.write('eVaults are smart and can support automation of client interactions as well as parallel internal ops process . Saves ops time, cleaner data, nudges for clients as well as for internal staff.')
        uploaded_file = st.file_uploader("Choose a file to upload", type=['png', 'jpeg', 'jpg', 'pdf'])
        
        if uploaded_file is not None:
            # Display the uploaded image
            if uploaded_file.type == 'application/pdf':
                uploaded_file = pdf_to_img(uploaded_file)
                st.image(uploaded_file, caption='Uploaded Document.', use_column_width=True)
                # st.title('SELECT CONFIGURATION')
                # print("Selecting the options")
                # options = st.multiselect(label = 'Choose the Parameter to classify', options= ["Passport", "Driver License", "Green Card", "401K-statement", "Last-will-and-testament", "life-insurance", "W2-form", "f8889_HSA"])
                # # print("Got the options", options)
                # scenario1 = img2text(uploaded_file)
                # options= ["Passport", "Driver License", "Green Card", "401K-statement", "Last-will-and-testament", "life-insurance", "W2-form", "f8889_HSA"]
                if st.button("Submit"):
                    # print("Submit Button Clicked")
                    img2text(uploaded_file, options)
                # with st.expander("Identified Document Type"):
                #     print("Thank You for uploading ", st.write(scenario1))
            else:    
                st.image(uploaded_file, caption='Uploaded Document.', use_column_width=True)
                # st.title('SELECT CONFIGURATION')
                # options = st.multiselect(label = 'Choose the Parameter to classify', options= ["Passport", "Driver License", "Green Card", "401K-statement", "Last-will-and-testament", "life-insurance", "W2-form", "f8889_HSA"])
            
                # scenario = img2text(uploaded_file) 
                if st.button("Submit"):
                    # print("Submit Button Clicked")
                    img2text(uploaded_file, options)
            
                # with st.expander("Extracted Text"):
                #     print("Thank You for uploading ", st.write(scenario))

    def pdf_to_img(uploaded_file):
        # Open the PDF file
        pdf_data = uploaded_file.read()

        # Create a PDF document object
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        # Get the first page of the PDF document
        first_page = pdf_document.load_page(0)

        # Convert the first page to a pixmap
        pixmap = first_page.get_pixmap()

        # Convert the pixmap to bytes
        img_bytes = pixmap.tobytes()

        # Create an image from the bytes
        image = Image.open(io.BytesIO(img_bytes))
        
        return image
    def create_static_directory():
        directory = 'static/'
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully.")
        else:
            print(f"Directory '{directory}' already exists.")

    create_static_directory()
            
            

    if __name__ == '__main__':
         main1()


def smartfill():
#     page_icon = Image.open(r"C:\Users\tanis\Documents\TheoremLabs.io\famiologyaccelerators\favicon.ico")
#     st.set_page_config(page_title="Smart Fill", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
#     logo = Image.open(r"C:\Users\tanis\Documents\TheoremLabs.io\famiologyaccelerators\favicon.ico")

    # Function to extract attributes from PDF document using pdfplumber
    def extract_attributes_from_pdf(file_path, selected_attributes, attribute_mappings):
        attributes = {}
        with pdfplumber.open(file_path) as pdf:
            first_page = pdf.pages[0]  # Assuming attributes are on the first page
            text = first_page.extract_text()
            for user_friendly_attribute in selected_attributes:
                possible_attribute_names = attribute_mappings[user_friendly_attribute]
                for attribute_name in possible_attribute_names:
                    if attribute_name in text:
                        attribute_index = text.index(attribute_name)
                        end_index = text.find("\n", attribute_index)
                        attribute_value = text[attribute_index + len(attribute_name):end_index].strip()
                        # Store using the attribute name as it appears in the document
                        attributes[attribute_name] = attribute_value
                        break  
        return attributes

    # Function to render PDF preview
    def render_pdf_preview(file_path):
        images = convert_from_bytes(file_path.read(), size=(800, None))
        return images

    # Function to convert image to PDF
    def convert_image_to_pdf(image_data):
        pdf_bytes = io.BytesIO()
        image_data.save(pdf_bytes, format='PDF')
        pdf_bytes.seek(0)
        return pdf_bytes
    


# Streamlit UI
# st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)

    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 400px !important; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    def main2():
        st.header("Smart Fill - Famiology.io")
        with st.sidebar.container():
            st.header("About App")
            # Section 1: Information about Smart Fill
            with st.expander("Smart Fill: Automatic Data Prepopulation", expanded=True):
                st.write("This intelligent feature automatically populates relevant data fields based on the document you upload. Say goodbye to manual data entry and let Smart Fill do the heavy lifting for you.")
            # Section 2: Usage Instructions
            with st.expander("How It Works?"):
                st.write("1. Upload Your Document: Simply upload your document using the provided file upload button.\n"
                        "2. Smart Analysis: Our system analyzes the document to identify key data points such as names, addresses, dates, and more. Further we can configure it with reference to domain.\n"
                        "3. Automatic Prepopulation: Once the analysis is complete, Smart Fill intelligently fills in the corresponding fields in your form, saving you time and effort.\n"
                        "4. Review and Edit: You always have the final say. Review the pre populated data, make any necessary edits, and proceed with confidence.")
            # Section 3: Configuration
            with st.sidebar.expander("Configuration:", expanded=True):
                attribute_mappings = {
                    "Property": ["Property", "Property Address", "Address"],
                    "Borrower(s)": ["Borrower", "Borrower(s)", "Applicant(s)"],
                    "Seller(s)": ["Seller", "Seller(s)"],
                    "Loan Amount": ["Loan Amount", "Amount"],
                    "Loan Term": ["Loan Term", "Term"],
                    "Lender": ["Lender", "Lender Name"],
                    "Cash to Close": ["Cash to Close", "Closing Costs", "Cash Required"]
                }
                selected_attributes = st.multiselect("Select Attributes", list(attribute_mappings.keys()))
                if not selected_attributes:
                    selected_attributes = list(attribute_mappings.keys())
            # Section 4: Additional Notes
            with st.expander("What problem it solves?"):
                st.write("Client Experience: Busy or unmotivated clients  expect automated pre-filled information sourced from AI or backend operations.\n"
                        "Efficiency: \n"
                        "Cut down on manual data entry and reduce processing time.")
            # Section 5: Value
            with st.expander("Value:"):
                st.write("The inherent value proposition of Smart Fill for users resides in its capacity to expedite and optimize data entry workflows through the automated population of pertinent fields, leveraging document uploads as the primary data source.")

        # File upload
        uploaded_file = st.file_uploader("Upload document", type=["pdf", "png", "jpg", "jpeg"])

        if uploaded_file:
            if uploaded_file.type in ['image/png', 'image/jpeg']:
                # Resize image
                image = Image.open(uploaded_file)
                image_resized = image.resize((800, 800))
                col1, col2 = st.columns(2)
                preview_clicked = col1.button("Preview")
                extract_clicked = col2.button("Extract Information")
                if extract_clicked:
                    col1.image(image_resized, use_column_width=True, caption="Page Preview")
                    pdf_data = convert_image_to_pdf(image_resized)
                    pdf_image = render_pdf_preview(pdf_data)
                    st.write("Image converted to PDF successfully!")
                    # Extract attributes from PDF document using pdfplumber
                    attributes = extract_attributes_from_pdf(pdf_data, selected_attributes, attribute_mappings)
                    if attributes:
                        for key, value in attributes.items():
                            col2.text_input(key, value)  
                    else:
                        st.info("No attributes identified.")
                elif preview_clicked:
                    col1.image(image_resized, use_column_width=True, caption="Page Preview")
            elif uploaded_file.type == 'application/pdf':
                col1, col2 = st.columns(2)
                preview_clicked = col1.button("Preview")
                extract_clicked = col2.button("Extract Information")
                if extract_clicked:
                    pdf_images = render_pdf_preview(uploaded_file)
                    for image in pdf_images:
                        col1.image(image, use_column_width=True, caption="Page Preview")
                    # Extract attributes from PDF document using pdfplumber
                    attributes = extract_attributes_from_pdf(uploaded_file, selected_attributes, attribute_mappings)
                    if attributes:
                        for key, value in attributes.items():
                            col2.text_input(key, value)  
                    else:
                        st.info("No attributes identified.")
                elif preview_clicked:
                    pdf_images = render_pdf_preview(uploaded_file)
                    for image in pdf_images:
                        col1.image(image, use_column_width=True, caption="Page Preview")
    if __name__ == '__main__':
         main2()


def customer_performance_dashboard():
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

        #st.markdown('<h4 style="font-size: 36px;">CUSTOMER PERFORMANCE DASHBOARD</h4>', unsafe_allow_html=True)
        st.header("Customer Performance Dashboard")

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
            st.markdown(f"<div style='text-align: center; font-size:4vh'>{million_representation}</div>", unsafe_allow_html=True)




    with col_2[1]:
        num_rows = df_clProfileFiltered.shape[0]
        # st.metric(label="**Total Customers**", value = num_rows)

        st.markdown("<h4 style='text-align: center;'>Total Customers</h4>", unsafe_allow_html=True)

        totalCust_col =  st.columns(1)


        with totalCust_col[0]:
            st.markdown(f"<div style='text-align: center;font-size:4vh'>{num_rows}</div>", unsafe_allow_html=True)

    with col_2[2]:

        
        # Calculate the average age
        average_age = df_clProfileFiltered['Age'].mean()
        # st.metric(label="**Customer Avg. age**", value="{:.2f}".format(average_age))

        st.markdown("<h4 style='text-align: center;'>Customer Avg. age</h4>", unsafe_allow_html=True)

        age_col =  st.columns(1)

        with age_col[0]:
            st.markdown(f"<div style='text-align: center;font-size:4vh'>{int(average_age)}</div>", unsafe_allow_html=True)

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
            labels = 'With child', 'without child'
            sizes = [percentageForChld, 100 - percentageForChld]
            explode = (0, 0.1, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

            fig1, ax1 = plt.subplots(figsize=(6, 6))
            ax1.set_facecolor("white")  # RGB values as a tuple
            patches, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%0.1f%%',
                                        shadow=False, startangle=90)

            # Set the color of labels to white
            for text in texts:
                text.set_color('white')
                text.set_fontsize(18)  # Adjust the font size here


            # Set the color of autopct labels to white
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(12)  # Adjust the font size here

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

        bins = [25, 40, 50, 60]
        labels_ages = ['25-40', '40-50', '50-60']


        df_sorted['AgeGroup'] = pd.cut(df_sorted['Age'], bins=bins, labels=labels_ages, right=False)

        revenue_by_age_group = df_sorted.groupby('AgeGroup')['Net Worth'].sum().tolist()

        print("revenue_by_age_group", revenue_by_age_group)


        fig1, ax1 = plt.subplots(figsize=(1.5,1.5))
        # ax1.set_facecolor("white")  # RGB values as a tuple

        patches, texts, autotexts = ax1.pie(revenue_by_age_group, labels=labels_ages, autopct='%0.1f%%', 
                shadow=False, startangle=90)
        
        for text in texts:
            text.set_color('white')
            text.set_fontsize(6)  # Adjust the font size her

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(6)  # Adjust the font size her

        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


        colors = ['green', 'orange', 'red']

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
        # ax.set_facecolor("white")  # RGB values as a tuple



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
        # ax.set_facecolor("white")  # RGB values as a tuple

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

            st.markdown("<h5 style='text-align: center;padding:2vh; font-size:3vh'>Males</h5>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; padding:2vh; font-size:4vh'>{million_representation_male}</div>", unsafe_allow_html=True)
        

        with genderRev[1]:
            FemaleIndividuals = df_clProfileFiltered[df_clProfileFiltered["Gender"] == "F"]
            total_sum_female = FemaleIndividuals[column_name].sum()
            million_representation_female = "$ {:.2f}M".format(total_sum_female / 1_000_000)


            st.markdown("<h5 style='text-align: center; padding:2vh; font-size:3vh'>Females</h5>", unsafe_allow_html=True)
        
            st.markdown(f"<div style='text-align: center; padding:2vh; font-size:4vh'>{million_representation_female}</div>", unsafe_allow_html=True)



# page_icon = Image.open("page/favicon.ico")
# st.set_page_config(page_title="Famiology", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
logo = Image.open("favicon.ico")

# Streamlit UI
# st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)

st.sidebar.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

pg = st.navigation({
    "Apps": [
        # Load pages from functions
        st.Page(smartfill, title="Smart Fill", default=True, url_path=""),
        st.Page(documentdetector, title="Document Detector", url_path=""),
        ],
    "Dashboards": [
         st.Page(customer_performance_dashboard, title="Customer Performance Dashboard"),
    #     # You can also load pages from files, as usual
    #     st.Page("movies.py", title="Movie Explorer", icon=":material/movie_filter:"),
    #     st.Page(page3, title="App statuses over time", icon=":material/access_time:"),
    #     st.Page(page3, title="Cloud apps leaderboard", icon=":material/share:", url_path="cloud_apps_leaderboard"),
         ],
})


try:
    pg.run()
except Exception as e:
   st.error(f"Something went wrong: {str(e)}", icon=":material/error:")

# def main():

#     with st.sidebar:
#         selected = option_menu("Apps", "dashboards") 
#         selected

# if __name__ == "__main__":
#      main() 

# def main():
#     with st.sidebar.container():
#         # Section 1: Apps
#         with st.expander("Apps"):
#             st.markdown('<a href="https://famiologydocdetector.streamlit.app/" target="_self">Document Detector</a>', unsafe_allow_html=True)
#             st.markdown('<a href="https://famiology-smart-fill.streamlit.app/" target="_self">Smart Fill</a>', unsafe_allow_html=True)
        

#if __name__ == "__main__":
#     main2()

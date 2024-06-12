# import streamlit as st
# def main():
#     st.markdown("<a href='https://famiologydocdetector.streamlit.app/' target='_blank'>Go to Document Detector Website</a>", unsafe_allow_html=True)

# if __name__ == "__main__":
#      main()


# # import streamlit as st
# # from PIL import Image

# # def main():
# #     page_icon = Image.open("pages/favicon.ico")
# #     st.set_page_config(page_title="Famiology", page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")
# #     logo = Image.open("pages/favicon.ico")

# #     # Streamlit UI
# #     st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)

# #     st.markdown(
# #         """
# #         <style>
# #             section[data-testid="stSidebar"] {
# #                 width: 400px !important; # Set the width to your desired value
# #             }
# #             .button {
# #                 display: inline-block;
# #                 padding: 10px 20px;
# #                 font-size: 16px;
# #                 cursor: pointer;
# #                 text-align: center;
# #                 text-decoration: none;
# #                 outline: none;
# #                 color: #fff;
# #                 background-color: #007bff;
# #                 border: none;
# #                 border-radius: 15px;
# #                 box-shadow: 0 9px #0069d9;
# #             }
# #             .button:hover {background-color: #0069d9}
# #             .button:active {
# #                 background-color: #0069d9;
# #                 box-shadow: 0 5px #666;
# #                 transform: translateY(4px);
# #             }
# #         </style>
# #         """,
# #     unsafe_allow_html=True,
# #     )

# #     #with st.sidebar.container():
# #         # Section 1: Apps
# #     #with st.expander("Apps"):
# #     if st.button("Document Detector"):
# #             st.button("<a href='https://famiologydocdetector.streamlit.app/' target='_blank' class='button'>Go to Document Detector Website</a>", unsafe_allow_html=True)

# # if __name__ == "__main__":
# #     main()


# # from dotenv import load_dotenv
# import fitz
# import streamlit as st
# from PyPDF2 import PdfReader
# from PIL import Image 
# # import pdf2imagefrom PyPDF2 import PdfFileReader
# # import io
# import os
# from pdf2image import convert_from_bytes
# from transformers import CLIPProcessor, CLIPModel
# CLIPProcessor.safety_checker = None
# # CLIPProcessor.safety_checker = None
# # CLIPModel.safety_checker = None
# # Adjust img2text to handle both file-like objects and PIL.Image.Image instances
# def img2text(uploaded_file):
#     model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336")
#     processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")
#     if isinstance(uploaded_file, Image.Image):
#         image = uploaded_file
#     else:
#         image = Image.open(uploaded_file)

#     array = ["Passport", "Driver License", "Green Card", "401K-statement", "Last-will-and-testament", "life-insurance", "W2-form", "f8889_HSA", "other"]
#     inputs = processor(text=array, images=image, return_tensors="pt", padding=True)

#     outputs = model(**inputs)
#     logits_per_image = outputs.logits_per_image  
#     probs = logits_per_image.softmax(dim=1)  

#     probs = probs.tolist()
#     flat_probs = [prob for sublist in probs for prob in sublist]
#     max_prob = max(flat_probs)
#     index_of_max = flat_probs.index(max_prob)
    
#     st.write("Your documents have been uploaded successfully. Thanks for submitting your ", array[index_of_max], ".")
#     st.write("We'll take care of the rest.")
#     # st.write("Accuracy - ", max_prob)
#     # return array[index_of_max]


# # st.sidebar.info("Hello World")
# def main():
#     # img = Image.open('/Users/atharvabapat/Desktop/Theoremlabs-project/favicon (2).ico')
#     # st.set_page_config(page_title="Document Identification")
    
#     st.set_page_config(page_title='Famiology.docdetector', page_icon='/Users/atharvabapat/Desktop/Theoremlabs-project/favicon (2).ico')
#     st.header('Famiology Document Detector')
#     st.sidebar.image("FamiologyTextLogo.png", use_column_width=True)
    
#     with st.sidebar:
#         st.header('About App')
#         st.header('Smart Document Recognition: Instantly Identify Uploaded Documents')
#         st.sidebar.info('Empower your document management process with Smart Document Recognition. This advanced feature swiftly identifies the type of document you upload, making document handling effortless and efficient.')
#         st.header('How It Works: ')
#         expander = st.expander("See Details")
#         expander.write('<ins>Upload Your Document:</ins> Select the document you wish to process using the provided file upload button. \n\n Intelligent Analysis: Our system employs cutting-edge technology to analyze the documents structure, layout, and content. \n\n Automatic Identification: Based on the analysis, Smart Document Recognition accurately identifies the document type, whether its an identification document, real estate document, 401k document or any other document format. \n\n Streamlined Processing: With the document type identified, our platform can seamlessly route it to the appropriate workflow or apply predefined actions, saving you valuable time and effort.')
#         st.header('What Problem it Solves?')
#         expander = st.expander("See Details")
#         expander.write('Efficiency: Instantly recognize document types without manual intervention. \n\n Accuracy: Ensure accurate processing and categorization of documents. \n\n Productivity: Automate document handling workflows for smoother operations.')
#         st.header('Value') 
#         expander = st.expander("See Details")
#         expander.write('eVaults are smart and can support automation of client interactions as well as parallel internal ops process . Saves ops time, cleaner data, nudges for clients as well as for internal staff.')
#     uploaded_file = st.file_uploader("Choose a file to upload", type=['png', 'jpeg', 'jpg', 'pdf'])
    
#     if uploaded_file is not None:
#         if uploaded_file.type == 'application/pdf':
#             image = pdf_to_img(uploaded_file.getvalue())
#             # st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
#             # scenario1 = img2text(uploaded_file)
#             img2text(image)
#             # with st.expander("Identified Document Type"):
#             #     print("Thank You for uploading ", st.write(scenario1))
#         else:    
#             # st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
        
#             # scenario = img2text(uploaded_file) 
#             img2text(uploaded_file)
        
#             # with st.expander("Extracted Text"):
#             #     print("Thank You for uploading ", st.write(scenario))

# # def pdf_to_img(uploaded_file):
# #     # Read the PDF file
# #     pdf_data = uploaded_file.read()

# #     # Open the PDF using PyPDF2
# #     pdf_reader = PdfFileReader(io.BytesIO(pdf_data))

# #     # Check if the PDF has any pages
# #     if pdf_reader.numPages == 0:
# #         raise ValueError("The PDF file is empty.")

# #     # Extract the first page of the PDF
# #     first_page = pdf_reader.getPage(0)

# #     # Convert the PDF page to an image using PIL
# #     image = first_page.to_pil()

# #     return image

# def pdf_to_img(pdf_data):
#     doc = fitz.open(stream=pdf_data, filetype="pdf")
    
#     if doc.page_count == 0:
#         raise ValueError("No pages found in the PDF.")

#     # Render the first page as an image
#     first_page = doc[0]
#     pix = first_page.get_pixmap()
    
#     # Convert the pixmap to a PIL image
#     image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

#     return image

# def create_static_directory():
#     directory = 'static/'
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#         print(f"Directory '{directory}' created successfully.")
#     else:
#         print(f"Directory '{directory}' already exists.")

# create_static_directory()

# if __name__ == '__main__':
#         main()


# from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import fitz 
import io
import os
import base64
from transformers import CLIPProcessor, CLIPModel
CLIPProcessor.safety_checker = None
# CLIPProcessor.safety_checker = None
# CLIPModel.safety_checker = None
# Adjust img2text to handle both file-like objects and PIL.Image.Image instances
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

st.set_page_config(page_title='Famiology.docdetector', page_icon='/Users/atharvabapat/Desktop/Theoremlabs-project/favicon (2).ico')

file = open("FamiologyTextLogo.png", "rb")
contents = file.read()
img_str = base64.b64encode(contents).decode("utf-8")
buffer = io.BytesIO()
file.close()
img_data = base64.b64decode(img_str)
img = Image.open(io.BytesIO(img_data))
resized_img = img.resize((375, 75))  # x, y
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

def main():
    # img = Image.open('/Users/atharvabapat/Desktop/Theoremlabs-project/favicon (2).ico')
    # st.set_page_config(page_title="Document Identification")
    
    # st.set_page_config(page_title='Famiology.docdetector', page_icon='/Users/atharvabapat/Desktop/Theoremlabs-project/favicon (2).ico')
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
        main()


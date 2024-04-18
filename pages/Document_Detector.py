import streamlit as st
from PIL import Image
import fitz 
import io
import os
from transformers import CLIPProcessor, CLIPModel
CLIPProcessor.safety_checker = None


def load_clip_model_processor():
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")
    return model, processor
    

def img2text(uploaded_file):
    model, processor = load_clip_model_processor()
    if isinstance(uploaded_file, Image.Image):
        image = uploaded_file
    else:
        image = Image.open(uploaded_file)

    array = ["Passport", "Driver License", "Green Card", "401K-statement", "Last-will-and-testament", "life-insurance", "W2-form", "f8889_HSA", "other"]
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
        message = "Your documents have been uploaded successfully. Thanks for submitting your Document."

    styled_message = f"<div style='font-size:28px;font-weight:bold;border: 2px solid Green;padding:10px;'>{message}</div>"
    st.markdown(styled_message, unsafe_allow_html=True)
    
    st.subheader("The Probabilites are as follows")
    st.write("Passport - ", flat_probs[0])
    st.write("Driver License - ", flat_probs[1])
    st.write("Green Card - ", flat_probs[2])
    st.write("401K Statement - ", flat_probs[3])
    st.write("Will & POAs Document - ", flat_probs[4])
    st.write("Life Insurance Policy - ", flat_probs[5])
    st.write("W2 Form - ", flat_probs[6])
    st.write("HSA Statement - ", flat_probs[7])

def main():
    st.set_page_config(page_title='Famiology.docdetector', page_icon='./favicon (2).ico')
    st.header('Famiology Document Detector')
    st.sidebar.image("./FamiologyTextLogo.png", use_column_width=True)
    
    with st.sidebar:
        st.header('About App')
        expander = st.expander("Smart Document Recognition: \n\n Instantly Identify Uploaded Documents: ")
        expander.write('Empower your document management process with Smart Document Recognition. This advanced feature swiftly identifies the type of document you upload, making document handling effortless and efficient.')
        expander = st.expander("How It Works:")
        expander.write('Upload Your Document: Select the document you wish to process using the provided file upload button. \n\n Intelligent Analysis: Our system employs cutting-edge technology to analyze the documents structure, layout, and content. \n\n Automatic Identification: Based on the analysis, Smart Document Recognition accurately identifies the document type, whether its an identification document, real estate document, 401k document or any other document format. \n\n Streamlined Processing: With the document type identified, our platform can seamlessly route it to the appropriate workflow or apply predefined actions, saving you valuable time and effort.')
        expander = st.expander("Configuration")
        expander.write("""
                    Let's Classify your Document according to these
                    - Passport
                    - Driver Liscence
                    - Green Card
                    - 401K-statement
                    - Last-will-and-testament
                    - life-insurance
                    - W2-form
                    - f8889_HSA
                    """
                    )
        expander = st.expander("What Problem it Solves?")
        expander.write('Efficiency: Instantly recognize document types without manual intervention. \n\n Accuracy: Ensure accurate processing and categorization of documents. \n\n Productivity: Automate document handling workflows for smoother operations.')
        # st.header('Value') 
        expander = st.expander("Value")
        expander.write('eVaults are smart and can support automation of client interactions as well as parallel internal ops process . Saves ops time, cleaner data, nudges for clients as well as for internal staff.')
    uploaded_file = st.file_uploader("Choose a file to upload", type=['png', 'jpeg', 'jpg', 'pdf'])
    
    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            uploaded_file = pdf_to_img(uploaded_file)
            st.image(uploaded_file, caption='Uploaded Document.', use_column_width=True)
            # st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
            # scenario1 = img2text(uploaded_file)
            img2text(uploaded_file)
            
        else:    
            st.image(uploaded_file, caption='Uploaded Document.', use_column_width=True)
            img2text(uploaded_file)
        
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

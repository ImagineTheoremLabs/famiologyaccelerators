import streamlit as st

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #000000;
        font-family: 'Arial', sans-serif;
        display: 100%;
    }
    .title {
        text-align: center;
        color: #ffffff;
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    .navbar {
        display: flex;
        justify-content: center;
        background-color: #000000;
        padding: 10px;
    }
    .navbar a {
        color: #ffffff;
        text-decoration: none;
        padding: 14px 20px;
        display: inline-block;
        text-align: center;
    }
    .navbar a:hover {
        background-color: #575757;
        color: white;
    }
    .header {
        color: #ffffff;
        font-size: 2em;
        margin-top: 20px;
    }
    .subheader {
        color: #ffffff;
        font-size: 1.5em;
        margin-top: 20px;
    }
    .markdown-text {
        color: #cccccc;
        font-size: 1.1em;
        line-height: 1.6em;
    }
    .step-section {
        background-color: #333333;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .step-section img {
        border-radius: 10px;
    }
    .fixed-demo {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 20px auto;
        width: 80%;
        background-color: #333333;
        border: 1px solid #555555;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .fixed-demo h2 {
        text-align: center;
        color: #ffffff;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.markdown("<div class='title'>Famiology Compute Engine: Simplify Your File Preprocessing Workflow</div>", unsafe_allow_html=True)
    
    # Navigation bar
    st.markdown("""
    <div class='navbar'>
        <a href='#introduction'>Introduction</a>
        <a href='#features'>Features</a>
        <a href='#step-by-step-guide'>Step-by-Step Guide</a>
        <a href='#conclusion'>Conclusion</a>
    </div>
    """, unsafe_allow_html=True)

    # Fixed demo video section
    st.markdown("""
        <div class='fixed-demo'>
            <h2 id='working-demo'>Working Demo</h2>
            <video controls width='100%'>
                <source src='img/Demo-Video.mp4'>
                Your browser does not support the video tag.
            </video>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='header' id='introduction'>Introduction</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='markdown-text'>
    The Famiology Compute Engine is designed to streamline and simplify your file preprocessing workflows. Whether you're dealing with large datasets, complex transformations, or repetitive tasks, this engine provides the tools you need to efficiently prepare your data for analysis.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='header' id='features'>Features</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='markdown-text'>
    Automated Workflow Management: Seamlessly automate file preprocessing tasks using Apache Airflow, enabling efficient and consistent handling of large datasets and complex workflows.<br>
    Scalable Infrastructure: Leverage the power of AWS EC2 to scale your preprocessing tasks according to your needs, ensuring robust performance and reliability for any size of data.<br>
    Flexible Integration: Easily integrate with your existing systems and workflows through REST API, allowing for on-the-fly modifications and customizations to meet your specific requirements.<br>
    User-Friendly Interface: Utilize a dedicated Streamlit app to control and monitor your preprocessing workflows, providing an intuitive and accessible interface for managing your tasks.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='header' id='step-by-step-guide'>Step-by-Step Guide</div>", unsafe_allow_html=True)

    with st.expander("Step 1: Create an EC2 Instance"):
        st.markdown("<div class='step-section'><div class='subheader'>Create an EC2 Instance</div>", unsafe_allow_html=True)
        st.image("img/Step1.png", use_column_width=True, caption="Create an EC2 Instance")
        st.markdown("""
        <div class='markdown-text'>
        - Start by creating an EC2 instance on AWS. This instance will host Apache Airflow.<br>
        - Assign Elastic IP:<br>
        Note that the IPv4 address and Public IPv4 DNS of an EC2 instance change when it is stopped and restarted. To maintain a constant IP address, create a new Elastic IP and assign it to your instance. This ensures that the IP address remains the same, even after restarting the instance.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Step 2: Assign Elastic IP"):
        st.markdown("<div class='step-section'><div class='subheader'>Assign Elastic IP</div>", unsafe_allow_html=True)
        st.image("img/Step2.png", use_column_width=True, caption="Assign Elastic IP")
        st.markdown("""
        <div class='markdown-text'>
        - By assigning an Elastic IP, you stabilize the instance's IP address, making it easier to access the APIs necessary for integrating Streamlit.<br>
        - This constant IP address simplifies API access and integration, facilitating a smoother workflow.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Step 3: Connect to the EC2 Instance and Set Up Directories and Libraries"):
        st.markdown("<div class='step-section'><div class='subheader'>Connect to the EC2 Instance and Set Up Directories and Libraries</div>", unsafe_allow_html=True)
        st.image("img/Step3.png", use_column_width=True, caption="Connect to the EC2 Instance and Set Up Directories and Libraries")
        st.markdown("""
        <div class='markdown-text'>
        - Once the Elastic IP address is assigned, start the EC2 instance and connect to it via the "Connect" button, which opens a terminal.<br>
        - In this terminal, create the necessary directories and install all required files and libraries, including Apache Airflow.<br>
        - Activate the Airflow environment and navigate to the working directory containing your files, such as Excel sheets, webserver.py, airflow.db, and airflow.cfg.<br>
        - The dags folder holds all the active DAGs for Airflow. This setup ensures that your instance is running with a stable IP and all necessary configurations for managing workflows with Airflow.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Step 4: Start the Airflow Webserver"):
        st.markdown("<div class='step-section'><div class='subheader'>Start the Airflow Webserver</div>", unsafe_allow_html=True)
        st.image("img/Step4.png", use_column_width=True, caption="Start the Airflow Webserver")
        st.markdown("""
        <div class='markdown-text'>
        - Start the Airflow webserver by running the command airflow webserver &. This launches the webserver on the host, listening on port 8080, as shown in the screenshot.<br>
        - This allows you to access the Airflow UI and manage your workflows through the web interface.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Step 5: Start the Airflow Scheduler"):
        st.markdown("<div class='step-section'><div class='subheader'>Start the Airflow Scheduler</div>", unsafe_allow_html=True)
        st.image("img/Step5.png", use_column_width=True, caption="Start the Airflow Scheduler")
        st.markdown("""
        <div class='markdown-text'>
        - Once the webserver is running, start the Airflow scheduler using the command airflow scheduler.<br>
        - This will activate the scheduler, and you'll see the output confirming it is running. With both the webserver and scheduler up and running, the Apache Airflow platform is fully operational.<br>
        - You can now view, control, and analyze the available DAGs (Directed Acyclic Graphs) through the Airflow UI, enabling efficient workflow management and monitoring.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Step 6: View and Manage the Active DAG"):
        st.markdown("<div class='step-section'><div class='subheader'>View and Manage the Active DAG</div>", unsafe_allow_html=True)
        st.image("img/Step6.png", use_column_width=True, caption="View and Manage the Active DAG")
        st.markdown("""
        <div class='markdown-text'>
        - With the Apache Airflow platform now visible, you can see the active DAG, “compute_engine_dag.py”.<br>
        - This DAG contains all the code needed to preprocess the Excel sheets located on the same instance.<br>
        - The interface shows that the DAG has successfully run 41 times, with 2 failures.<br>
        - Additionally, you have the capability to schedule the DAG runs, allowing for automated and efficient processing of your data.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Step 7: Host the Streamlit App"):
        st.markdown("<div class='step-section'><div class='subheader'>Host the Streamlit App</div>", unsafe_allow_html=True)
        st.image("img/Step7.png", use_column_width=True, caption="Host the Streamlit App")
        st.markdown("""
        <div class='markdown-text'>
        - This is the Streamlit app that is hosted over the Streamlit community cloud and in the backend the buttons are connected with RestAPI provided by the Apache Airflow.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Step 8: Select and Preprocess Files"):
        st.markdown("<div class='step-section'><div class='subheader'>Select and Preprocess Files</div>", unsafe_allow_html=True)
        st.image("img/Step8.png", use_column_width=True, caption="Select and Preprocess Files")
        st.markdown("""
        <div class='markdown-text'>
        - Now when we click on DAG we see our Compute Engine DAG that is currently active.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Step 9: Verify Preprocessing Results on Apache Airflow"):
        st.markdown("<div class='step-section'><div class='subheader'>Verify Preprocessing Results on Apache Airflow</div>", unsafe_allow_html=True)
        st.image("img/Step9.png", use_column_width=True, caption="Verify Preprocessing Results on Apache Airflow")
        st.markdown("""
        <div class='markdown-text'>
        - When you select the files to preprocess and click the "Generate Result" button, an API call is made to the DAG present on Apache Airflow.<br>
        - This triggers the DAG, which processes the files located on the EC2 instance and generates the desired output.<br>
        - The system efficiently handles the preprocessing task, leveraging the power of Apache Airflow to manage and execute the workflow seamlessly.
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='header' id='conclusion'>Conclusion</div>", unsafe_allow_html=True)
    st.image("img/Conclusion.png", use_column_width=True, caption="Conclusion")
    st.markdown("""
    <div class='markdown-text'>
    - The Famiology Compute Engine is your go-to solution for simplifying file preprocessing workflows. With its powerful features and ease of use, you'll be able to focus more on analyzing your data and less on preparing it.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

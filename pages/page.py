import streamlit as st

def main():
    st.title("Famiology Compute Engine: Simplify Your File Preprocessing Workflow")

    st.sidebar.title("Navigation")
    st.sidebar.markdown("""
    - [Introduction](#introduction)
    - [Features](#features)
    - [Step-by-Step Guide](#step-by-step-guide)
        - [Step 1: Create an EC2 Instance](#step-1-create-an-ec2-instance)
        - [Step 2: Assign Elastic IP](#step-2-assign-elastic-ip)
        - [Step 3: Connect to the EC2 Instance](#step-3-connect-to-the-ec2-instance)
        - [Step 4: Start the Airflow Webserver](#step-4-start-the-airflow-webserver)
        - [Step 5: Start the Airflow Scheduler](#step-5-start-the-airflow-scheduler)
        - [Step 6: View and Manage the Active DAG](#step-6-view-and-manage-the-active-dag)
        - [Step 7: Host the Streamlit App](#step-7-host-the-streamlit-app)
        - [Step 8: Select and Preprocess Files](#step-8-select-and-preprocess-files)
        - [Step 9: Verify Preprocessing Results](#step-9-verify-preprocessing-results)
    - [Conclusion](#conclusion)
    - [Working Demo](#working-demo)
    """)

    st.header("Introduction")
    st.write("""
    The Famiology Compute Engine is designed to streamline and simplify your file preprocessing workflows. Whether you're dealing with large datasets, complex transformations, or repetitive tasks, this engine provides the tools you need to efficiently prepare your data for analysis.
    """)

    st.header("Features")
    st.write("""
    - **Automated Workflow Management**: Seamlessly automate file preprocessing tasks using Apache Airflow, enabling efficient and consistent handling of large datasets and complex workflows.
    - **Scalable Infrastructure**: Leverage the power of AWS EC2 to scale your preprocessing tasks according to your needs, ensuring robust performance and reliability for any size of data.
    - **Flexible Integration**: Easily integrate with your existing systems and workflows through REST API, allowing for on-the-fly modifications and customizations to meet your specific requirements.
    - **User-Friendly Interface**: Utilize a dedicated Streamlit app to control and monitor your preprocessing workflows, providing an intuitive and accessible interface for managing your tasks.
    """)

    st.header("Step-by-Step Guide")

    with st.expander("Step 1: Create an EC2 Instance"):
        st.subheader("Create an EC2 Instance")
        st.image("img/Step1.png", use_column_width=True)
        st.write("""
        - Start by creating an EC2 instance on AWS. This instance will host Apache Airflow.
        - Assign Elastic IP:
        Note that the IPv4 address and Public IPv4 DNS of an EC2 instance change when it is stopped and restarted. To maintain a constant IP address, create a new Elastic IP and assign it to your instance. This ensures that the IP address remains the same, even after restarting the instance.
        """)

    with st.expander("Step 2: Assign Elastic IP"):
        st.subheader("Assign Elastic IP")
        st.image("img/Step2.png", use_column_width=True)
        st.write("""
        - By assigning an Elastic IP, you stabilize the instance's IP address, making it easier to access the APIs necessary for integrating Streamlit. 
        - This constant IP address simplifies API access and integration, facilitating a smoother workflow.
        """)

    with st.expander("Step 3: Connect to the EC2 Instance and Set Up Directories and Libraries"):
        st.subheader("Connect to the EC2 Instance and Set Up Directories and Libraries")
        st.image("img/Step3.png", use_column_width=True)
        st.write("""
        - Once the Elastic IP address is assigned, start the EC2 instance and connect to it via the "Connect" button, which opens a terminal. 
        - In this terminal, create the necessary directories and install all required files and libraries, including Apache Airflow. 
        - Activate the Airflow environment and navigate to the working directory containing your files, such as Excel sheets, webserver.py, airflow.db, and airflow.cfg. 
        - The dags folder holds all the active DAGs for Airflow. This setup ensures that your instance is running with a stable IP and all necessary configurations for managing workflows with Airflow.
        """)

    with st.expander("Step 4: Start the Airflow Webserver"):
        st.subheader("Start the Airflow Webserver")
        st.image("img/Step4.png", use_column_width=True)
        st.write("""
        - Start the Airflow webserver by running the command airflow webserver &. This launches the webserver on the host, listening on port 8080, as shown in the screenshot. 
        - This allows you to access the Airflow UI and manage your workflows through the web interface.
        """)

    with st.expander("Step 5: Start the Airflow Scheduler"):
        st.subheader("Start the Airflow Scheduler")
        st.image("img/Step5.png", use_column_width=True)
        st.write("""
        - Once the webserver is running, start the Airflow scheduler using the command airflow scheduler. 
        - This will activate the scheduler, and you'll see the output confirming it is running. With both the webserver and scheduler up and running, the Apache Airflow platform is fully operational. 
        - You can now view, control, and analyze the available DAGs (Directed Acyclic Graphs) through the Airflow UI, enabling efficient workflow management and monitoring.
        """)

    with st.expander("Step 6: View and Manage the Active DAG"):
        st.subheader("View and Manage the Active DAG")
        st.image("img/Step6.png", use_column_width=True)
        st.write("""
        - With the Apache Airflow platform now visible, you can see the active DAG, “compute_engine_dag.py”. 
        - This DAG contains all the code needed to preprocess the Excel sheets located on the same instance. 
        - The interface shows that the DAG has successfully run 41 times, with 2 failures. 
        - Additionally, you have the capability to schedule the DAG runs, allowing for automated and efficient processing of your data.
        """)

    with st.expander("Step 7: Host the Streamlit App"):
        st.subheader("Host the Streamlit App")
        st.image("img/Step7.png", use_column_width=True)
        st.write("""
        - This is the Streamlit app that is hosted over the Streamlit community cloud and in the backend the buttons are connected with RestAPI provided by the Apache Airflow. 
        """)

    with st.expander("Step 8: Select and Preprocess Files"):
        st.subheader("Select and Preprocess Files")
        st.image("img/Step8.png", use_column_width=True)
        st.write("""
        - Now when we click on DAG we see our Compute Engine DAG that is currently active.
        """)

    with st.expander("Step 9: Verify Preprocessing Results on Apache Airflow"):
        st.subheader("Verify Preprocessing Results on Apache Airflow")
        st.image("img/Step9.png", use_column_width=True)
        st.write("""
        - When you select the files to preprocess and click the "Generate Result" button, an API call is made to the DAG present on Apache Airflow. 
        - This triggers the DAG, which processes the files located on the EC2 instance and generates the desired output. 
        - The system efficiently handles the preprocessing task, leveraging the power of Apache Airflow to manage and execute the workflow seamlessly.
        """)

    st.header("Conclusion")
    st.image("img/Conclusion.png", use_column_width=True)
    st.write("""
    - The Famiology Compute Engine is your go-to solution for simplifying file preprocessing workflows. With its powerful features and ease of use, you'll be able to focus more on analyzing your data and less on preparing it.
    """)

    st.header("Working Demo")
    st.video("img/Demo-Video.mp4")

if __name__ == "__main__":
    main()

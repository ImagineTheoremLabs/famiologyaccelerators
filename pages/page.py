import streamlit as st

def main():
    st.title("Famiology Compute Engine: Simplify Your File Preprocessing Workflow")
    
    st.header("Introduction")
    st.write("""
    The Famiology Compute Engine is designed to streamline and simplify your file preprocessing workflows. Whether you're dealing with large datasets, complex transformations, or repetitive tasks, this engine provides the tools you need to efficiently prepare your data for analysis.
    """)

    st.header("Features")
    st.write("""
    - **Automated Workflow Management**: Seamlessly automate file preprocessing tasks using Apache Airflow, enabling efficient and consistent handling of large datasets and complex workflows.

    - **Scalable Infrastructure**: Leverage the power of AWS EC2 to scale your preprocessing tasks according to your needs, ensuring robust performance and reliability for any size of data.

    - **Flexible Integration**: Easily integrate with your existing systems and workflows through REST API, allowing for on-the-fly modifications and customizations to meet your specific requirements.

    - **User-Friendly Interface**: Utilize a dedicated Streamlit app to control and monitor your preprocessing workflows, providing an intuitive and accessible interface for managing your tasks.  """)

    st.subheader("Step 1")
    st.subheader("Create an EC2 Instance")
    st.image("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Step1.png", use_column_width=True, clamp=True)
    st.write("""
    - Create an EC2 Instance:
- Start by creating an EC2 instance on AWS. This instance will host Apache Airflow.
- Assign Elastic IP:
Note that the IPv4 address and Public IPv4 DNS of an EC2 instance change when it is stopped and restarted. To maintain a constant IP address, create a new Elastic IP and assign it to your instance. This ensures that the IP address remains the same, even after restarting the instance.
By following these steps, you'll have a stable IP address for your EC2 instance, allowing you to reliably host Airflow and proceed to the next stage of the setup.
""")

    st.subheader("Step 2")
    st.subheader("Assign Elastic IP")
    st.image("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Step2.png", use_column_width=True)
    st.write("""
            - By assigning an Elastic IP, you stabilize the instance's IP address, making it easier to access the APIs necessary for integrating Streamlit. - This constant IP address simplifies API access and integration, facilitating a smoother workflow.

             """)

    st.subheader("Step 3")
    st.subheader("Connect to the EC2 Instance and Set Up Directories and Libraries")
    st.image("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Step3.png", use_column_width=True)
    st.write("""
- Once the Elastic IP address is assigned, start the EC2 instance and connect to it via the "Connect" button, which opens a terminal. 
- In this terminal, create the necessary directories and install all required files and libraries, including Apache Airflow. Activate the Airflow environment and navigate to the working directory containing your files, such as Excel sheets, webserver.py, airflow.db, and airflow.cfg. 
- The dags folder holds all the active DAGs for Airflow. This setup ensures that your instance is running with a stable IP and all necessary configurations for managing workflows with Airflow.

             """)
    
    st.subheader("Step 4")
    st.subheader("Start the Airflow Webserver")
    st.image("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Step4.png", use_column_width=True)
    st.write("""
- Start the Airflow webserver by running the command airflow webserver &. This launches the webserver on the host, listening on port 8080, as shown in the screenshot. 
- This allows you to access the Airflow UI and manage your workflows through the web interface.
             """)
    
    st.subheader("Step 5")
    st.subheader("Start the Airflow Scheduler")
    st.image("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Step5.png", use_column_width=True)
    st.write("""
- Once the webserver is running, start the Airflow scheduler using the command airflow scheduler. 
- This will activate the scheduler, and you'll see the output confirming it is running. With both the webserver and scheduler up and running, the Apache Airflow platform is fully operational. You can now view, control, and analyze the available DAGs (Directed Acyclic Graphs) through the Airflow UI, enabling efficient workflow management and monitoring.

             """)
    
    st.subheader("Step 6")
    st.subheader("View and Manage the Active DAG")
    st.image("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Step6.png", use_column_width=True)
    st.write("""
- With the Apache Airflow platform now visible, you can see the active DAG, “compute_engine_dag.py”. 
- This DAG contains all the code needed to preprocess the Excel sheets located on the same instance. The interface shows that the DAG has successfully run 41 times, with 2 failures. 
- Additionally, you have the capability to schedule the DAG runs, allowing for automated and efficient processing of your data.

             """)
    
    st.subheader("Step 7")
    st.image("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Step7.png", use_column_width=True)
    st.subheader("Host the Streamlit App")
    st.write("""
- This is the Streamlit app that is hosted over the Streamlit community cloud and in the backend the buttons are connected with RestAPI provided by the Apache Airflow. 


             """)
    
    st.subheader("Step 8")
    st.image("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Step8.png", use_column_width=True)
    st.subheader("Select and Preprocess Files")
    st.write("""
- Now when we click on Dag we see our Compute Engine dag that is currently Active.
             """)
    

    st.subheader("Step 9")
    st.image("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Step9.png", use_column_width=True, clamp=True)
    st.subheader("Verify Preprocessing Results on Apache Airflow")
    st.write("""
- When you select the files to preprocess and click the "Generate Result" button, an API call is made to the DAG present on Apache Airflow. This triggers the DAG, which processes the files located on the EC2 instance and generates the desired output. The system efficiently handles the preprocessing task, leveraging the power of Apache Airflow to manage and execute the workflow seamlessly.

             """)

    st.header("Conclusion")
    st.image("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Conclusion.png", use_column_width=True)
    st.write("""
    - The Famiology Compute Engine is your go-to solution for simplifying file preprocessing workflows. With its powerful features and ease of use, you'll be able to focus more on analyzing your data and less on preparing it.
    """)


    st.header("Working Demo")
    st.video("/Users/atharvabapat/Desktop/BlogPage-Streamlit/Demo-Video.mov")


if __name__ == "__main__":
    main()

from __future__ import annotations

import pendulum
import requests
from airflow.decorators import dag, task

# -----------------------------------------------------------
# 1. DEFINING TASKS WITHIN THE @dag FUNCTION
# -----------------------------------------------------------

@dag(
    dag_id="taskflow_randomuser_api_etl_demo",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["demo", "taskflow", "api_integration"],
    default_args={"owner": "api_user"},
)
def random_user_api_workflow():
    
    @task
    def fetch_user_data():
        """
        Fetches a random user from randomuser.me/api.
        """
        api_url = "https://randomuser.me/api"
        
        print(f"🔄 Fetching data from Random User API: {api_url}")
        
        try:
            response = requests.get(api_url)
            response.raise_for_status() # Catch HTTP errors
            # Return the data (JSON) from the API.
            # Airflow transfers this output to the next task via XCom.
            return response.json()
        except Exception as e:
            print(f"❌ Error occurred while fetching data from API: {e}")
            raise # Raise the error to fail the task


    @task
    def extract_and_transform_user(raw_data: dict):
        """
        Extracts only the name, last name, and email from the raw data.
        """
        if not raw_data or not raw_data.get('results'):
            print("❌ Raw data (results) not found.")
            return None

        # Get only the first user (API always returns a list in 'results')
        user = raw_data['results'][0]
        
        processed_user = {
            "full_name": f"{user['name']['first']} {user['name']['last']}",
            "email_address": user['email'],
            "country": user['location']['country'],
            # Example: Apply a transformation to this field:
            "created_at_job": str(pendulum.now())
        }
        
        print("⏳ User data successfully extracted and transformed.")
        # Return the transformed object.
        return processed_user


    @task
    def load_and_display_result(processed_user: dict):
        """
        Prints the processed user data to the screen (simulates a Loading step).
        """
        if not processed_user:
            print("❌ No processed data to load.")
            return

        print("--- LOADED CLEAN USER DATA (LOAD) ---")
        print(f"  - Full Name: {processed_user['full_name']}")
        print(f"  - Email: {processed_user['email_address']}")
        print(f"  - Country: {processed_user['country']}")
        print(f"  - Job Time: {processed_user['created_at_job']}")
        print("✅ Load successful: Assumed written to Data Warehouse.")
    
    # -----------------------------------------------------------
    # 2. EXPLICITLY DEFINING TASK DEPENDENCIES ( >> )
    # -----------------------------------------------------------
    
    # 1. Call the Tasks to create Task Instances (TI):
    # The output of the task call is an XCom reference.
    fetch_data_ti = fetch_user_data()
    extract_transform_ti = extract_and_transform_user(fetch_data_ti)
    load_display_ti = load_and_display_result(extract_transform_ti)
    
    # 2. Define the flow using the >> operator:
    # This line sets up both dependency and XCom data flow.
    fetch_data_ti >> extract_transform_ti >> load_display_ti

# Call the main function to instantiate the DAG
random_user_api_workflow()
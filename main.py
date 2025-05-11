import requests
import sqlite3

# STEP 1: Generate webhook and access token
def send_post_request():
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    payload = {
        "name": "Prashant Jain",
        "regNo": "0827AL221101",
        "email": "jainprashant9301@gmail.com"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        print("Webhook and Access Token received.")
        return data['webhook'], data['accessToken']
    else:
        raise Exception(f"Failed to generate webhook: {response.status_code} - {response.text}")

# STEP 2: Execute SQL Query
def execute_query():
    # Connect to your local SQLite database
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()

    # Define the SQL query properly inside triple quotes """ """
    query = """
    WITH valid_payments AS (
        SELECT 
            p.AMOUNT, 
            p.EMP_ID, 
            p.PAYMENT_TIME
        FROM PAYMENTS p
        WHERE strftime('%d', p.PAYMENT_TIME) != '01' -- Exclude payments made on 1st day
    )
    SELECT 
        vp.AMOUNT AS SALARY,
        e.FIRST_NAME || ' ' || e.LAST_NAME AS NAME,
        CAST((julianday('now') - julianday(e.DOB)) / 365.25 AS INTEGER) AS AGE,
        d.DEPARTMENT_NAME
    FROM valid_payments vp
    JOIN EMPLOYEE e ON vp.EMP_ID = e.EMP_ID
    JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
    ORDER BY vp.AMOUNT DESC
    LIMIT 1;
    """

    # Execute the query
    cursor.execute(query)

    # Fetch and print the result
    result = cursor.fetchone()
    if result:
        print(f"SALARY: {result[0]}, NAME: {result[1]}, AGE: {result[2]}, DEPARTMENT_NAME: {result[3]}")
    else:
        print("No matching records found.")

    conn.close()

# MAIN Program
if __name__ == "__main__":
    try:
        webhook, token = send_post_request()
        print(f"Webhook: {webhook}")
        print(f"Access Token: {token}")
        execute_query()
    except Exception as e:
        print("Error:", e)

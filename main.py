import streamlit as st
import requests
import json

st.set_page_config(page_title="Content Creation AI Agent Dashboard", layout="wide")

# --- Sidebar: Configuration ---
st.sidebar.title("Agent Controls")
webhook_url = st.sidebar.text_input("n8n Webhook URL", value="http://localhost:5678/webhook/content-agent")

if not webhook_url:
    st.sidebar.warning("Please enter the n8n webhook URL")

# --- Main: Dashboard Title ---
st.title("📊 Content Creation AI Agent Dashboard")

# --- Agent Status ---
st.subheader("Agent Status")
status_placeholder = st.empty()

def get_agent_status():
    try:
        response = requests.get(webhook_url + "/status")
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "Offline or Invalid URL"}
    except Exception as e:
        return {"status": f"Error: {str(e)}"}

status_data = get_agent_status()
status_placeholder.info(f"Agent Status: {status_data.get('status', 'Unknown')}")

# --- Agent Control ---
st.subheader("Agent Control Panel")

with st.form("control_form"):
    task_type = st.selectbox("Select Task", ["Generate Blog Post", "Generate Social Media Post", "Summarize Article"])
    input_text = st.text_area("Enter Content Input", "Write about the future of AI in education.")
    submitted = st.form_submit_button("Send Task to Agent")

    if submitted:
        try:
            payload = {
                "task_type": task_type,
                "input_text": input_text
            }
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                st.success("Task sent successfully!")
            else:
                st.error(f"Failed to send task. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- Task History / Logs ---
st.subheader("Task Logs")

def fetch_logs():
    try:
        response = requests.get(webhook_url + "/logs")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        return []

logs = fetch_logs()

if logs:
    for log in logs[::-1]:
        st.info(f"{log.get('timestamp', '')} | Task: {log.get('task_type', '')} | Status: {log.get('status', '')}\nOutput: {log.get('output', '')}")
else:
    st.write("No logs available.")

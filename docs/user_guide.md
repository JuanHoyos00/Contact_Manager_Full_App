# 🚀 User Guide - Running the Streamlit Interface

This section explains how to spawn up the interactive web frontend layer of the application to execute direct operations on the contact registry.

## 🛠️ Step-by-Step Execution Setup

### 1. Initialize the Virtual Environment
Ensure your workspace dependencies are fully synchronized using uv. Run this in your terminal:

uv sync

### 2. Verify Backend Availability
The Streamlit frontend consumes data directly from the FastAPI gateway. Make sure your backend service is actively listening on its host port:

# Verify the REST API is alive on [http://127.0.0.1:8000](http://127.0.0.1:8000)
curl [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Launch the Streamlit Web Application
Execute the frontend entrypoint module using the uv toolchain runner to deploy the browser view:

uv run streamlit run src/app/main.py

---

## 🖥️ Operational Modules Available

Once the browser window automatically opens, you will have access to the following operational blocks:

### 📥 Write Operations (Commands)
* add_contact(): Opens a clear transactional form to record new corporate profiles after running unique invariant evaluations.
* update_contact_number_by_id(): Modifies target phone number digits directly by looking up the primary identity key.

### 🔍 Search Queries
* get_contact_by_id(): Fetches exact profile entity datasets using the numerical identification card.
* get_contact_by_number(): Scans the cloud registry matching unique cellular telephone text strings.

### 📤 Destructive Actions
* delete_contact_by_id(): Triggers a hard relational removal sequence based on identification data.
* delete_contact_by_number(): Wipes out a full user record matching its cell network row property.

### 📋 Visual Metrics & Views
* get_all_contacts(): Displays a complete, scannable data grid layout of all hydrated database profiles.
* get_contact_analytics(): Renders direct data summaries and database row tracking counters.
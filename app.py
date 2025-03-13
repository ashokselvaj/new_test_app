import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime, time
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

best_doctors = []
st.title("NPI App")
input_time = st.time_input("Enter Survey Time", value=time(6, 0))

df = pd.read_csv("/content/in.csv")

# Convert "Login Time" and "Logout Time" to datetime
df["Login Time"] = pd.to_datetime(df["Login Time"])
df["Logout Time"] = pd.to_datetime(df["Logout Time"])

# Extract only time
df["Login Time"] = df["Login Time"].dt.time
df["Logout Time"] = df["Logout Time"].dt.time


# Filter doctors available at survey time
df_filtered = df[(df["Login Time"] <= input_time) & (df["Logout Time"] >= input_time)]

# If no doctors are available, return an empty list
if df_filtered.empty:
    best_doctors=["No doctors available at the given time."]
else:
    # Drop unnecessary columns before scaling
    X = df_filtered.drop(columns=['NPI', 'State', 'Login Time', 'Logout Time', 'Region', 'Speciality'])

    # Scale the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Ensure there are enough rows for clustering
    if len(X_scaled) >= 2:  # Only apply KMeans if we have at least 2 samples
        kmeans = KMeans(n_clusters=2, random_state=333, n_init=10)
        df_filtered["Cluster"] = kmeans.fit_predict(X_scaled)
        
        # Select NPIs of doctors who are in the "More Available" cluster (Cluster 0)
        best_doctors = df_filtered[df_filtered["Cluster"] == 0]["NPI"].tolist()
    else:
        best_doctors = df_filtered["NPI"].tolist()

if best_doctors:
  df = pd.DataFrame({"Best Available Doctors": best_doctors})
else:
  df = pd.DataFrame({"Best Available Doctors": "NA"})





csv_buffer = BytesIO()
df.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)

st.download_button(
    label="Download CSV",
    data=csv_buffer,
    file_name="NPI.csv",
    mime="text/csv"
)

st.write("Selected Time:", input_time)

st.write("Doctors Available (NPI):", ", ".join(map(str, best_doctors)))


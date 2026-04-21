import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import time
import requests


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import accuracy_score, confusion_matrix

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="AI Business Risk System", layout="wide")
    
# ---------------------------------------------------
# SPLASH SCREEN
# ---------------------------------------------------

# ✅ splash control
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

# ✅ show splash FIRST
if not st.session_state.splash_done:
    try:
        with open("logo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <div style="display:flex;justify-content:center;align-items:center;height:100vh;">
            <img src="data:image/png;base64,{logo_base64}" width="200">
        </div>
        """, unsafe_allow_html=True)

        time.sleep(2)

    except Exception as e:
        st.error(f"Splash error: {e}")

    st.session_state.splash_done = True
    st.rerun()
    
    # ---------------- AUTH FUNCTION ----------------
def auth():
    
    st.title("AI Business Intelligence Platform 🔐")
    choice = st.radio("Choose", ["Login", "Sign Up"])

    # ---------------- LOGIN ----------------
    if choice == "Login":

        u = st.text_input("Username", key="lu")
        p = st.text_input("Password", type="password", key="lp")

        if st.button("Login"):

            if not u or not p:
                st.warning("Enter username & password")

            else:
                try:
                    res = requests.post(
                        "https://ai-business-intelligence-system-kmr6.onrender.com/login",
                        json={
                            "username": u.strip(),
                            "password": p.strip()
                        }
                    )

                    data = res.json()

                    if "token" in data:
                        st.session_state.logged_in = True
                        st.session_state.token = data["token"]
                        st.success("Login successful ✅")
                        st.rerun()
                    else:
                        st.error(data.get("detail", "Login failed"))

                except Exception as e:
                    st.error(f"Error: {e}")

    # ---------------- SIGNUP ----------------
    else:

        u = st.text_input("Username", key="su")
        p = st.text_input("Password", type="password", key="sp")

        if st.button("Sign Up"):

            if not u or not p:
                st.warning("Enter all fields")

            else:
                try:
                    res = requests.post(
                        "https://ai-business-intelligence-system-kmr6.onrender.com/signup",
                        json={
                            "username": u.strip(),
                            "password": p.strip()
                        }
                    )

                    data = res.json()

                    if res.status_code == 200:
                        st.success("Signup successful ✅")
                    else:
                        st.error(data.get("detail", "Signup failed"))

                except Exception as e:
                    st.error(f"Error: {e}")
# ---------------- LOGIN CHECK ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    auth()
    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Dataset Guide","Business Insights Dashbard","Risk Analysis","Machine Learning","Vendor Analytics"]
    
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
# ---------------------------------------------------
# DATASET GUIDE (DETAILED)
# ---------------------------------------------------
if page == "Dataset Guide":
    
    st.title("📘 Dataset Usage Guide")

    # ---------------- GUIDE ----------------
    st.markdown("""
## 🧭 Step-by-Step Guide to Use the System

### 🔹 Step 1: Login / Signup
- Create an account using the **Signup** option  
- Then login using your credentials  

---

### 🔹 Step 2: Upload Dataset 📁
- Go to **Upload Dataset** section  
- Supported formats:
  - CSV (.csv)
  - Excel (.xlsx, .xls)
  - JSON (.json)
  - Text (.txt)

---

### 🔹 Step 3: Dataset Processing ⚙️
- The system automatically reads your dataset  
- Detects:
  - Numerical columns  
  - Categorical columns  
  - Date columns  

---

### 🔹 Step 4: Auto Column Generation 🔄
If required columns are missing, system generates:

- `sales = quantity × 100`  
- `profit = sales × 0.3`  
- `shipping_cost = sales × 0.05`  
- `discount = 0.05`  

---

### 🔹 Step 5: Data Visualization 📊
- Automatically generates:
  - Bar charts  
  - Line charts  
  - Area charts  
- Based on selected columns  

---

### 🔹 Step 6: Analysis & Insights 📈
- Displays patterns and trends  
- Helps in business decision making  

---

### 🔹 Step 7: Use Sample Dataset (Optional) 📥
- If you don’t have data:
  - Download sample datasets below  
  - Upload them to test the system  

---

## 📁 Supported File Types
CSV, Excel, JSON, TXT  

---

## ⚠️ Important Guidelines
- Dataset must have column headers  
- Avoid empty or corrupted files  
- Keep data clean and structured  
""")

    # ---------------- DOWNLOAD SECTION ----------------
    st.divider()
    st.subheader("📥 Download Sample Datasets")

    st.write("Download these datasets to test the application features.")

    # CSV
    with open("datasets/SampleSuperstore.csv", "rb") as file:
        st.download_button(
            label="Download SampleSuperstore CSV",
            data=file,
            file_name="SampleSuperstore.csv",
            mime="text/csv"
        )

    # Excel
    with open("datasets/dataset.xlsx", "rb") as file:
        st.download_button(
            label="Download Excel Dataset",
            data=file,
            file_name="dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # JSON
    with open("datasets/sample.json", "rb") as file:
        st.download_button(
            label="Download JSON Dataset",
            data=file,
            file_name="sample.json",
            mime="application/json"
        )

    # ---------------- NOTE ----------------
    st.markdown("""
### ℹ️ Important Information

- The sample datasets are provided **only for demonstration purposes**
- Users are encouraged to upload their **own datasets** for actual analysis  
- Ensure your dataset follows the recommended format for best results  
""")

    st.stop()
# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset",
    type=["csv","xlsx","xls","json","txt"]
)

if uploaded_file is None:
    st.stop()

# READ FILE
if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
elif uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
    df = pd.read_excel(uploaded_file)
elif uploaded_file.name.endswith(".json"):
    df = pd.read_json(uploaded_file)
else:
    df = pd.read_csv(uploaded_file, sep="\t")

# ---------------------------------------------------
# CLEANING
# ---------------------------------------------------
df.columns = df.columns.str.strip().str.lower()
df = df.fillna(0)

# AUTO CREATE
if "sales" not in df.columns:
    df["sales"] = df.get("quantity",1) * 100

if "profit" not in df.columns:
    df["profit"] = df["sales"] * 0.3

if "discount" not in df.columns:
    df["discount"] = 0.05

if "shipping_cost" not in df.columns:
    df["shipping_cost"] = df["sales"] * 0.05

if "category" not in df.columns:
    df["category"] = "General"

if "vendor id" not in df.columns:
    df["vendor id"] = ["V"+str(i+1) for i in range(len(df))]

# DATE FIX
df["order_date"] = pd.to_datetime(df.get("order_date", pd.Timestamp.today()), errors="coerce")
df = df.dropna(subset=["order_date"])

# RISK
df["risk_status"] = (
    (df["profit"] < 100) |
    (df["discount"] > 0.2) |
    (df["sales"] < 500)
).astype(int)

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
if page == "Business Insights Dashbard":
    
    st.title("📊 Business Intelligence Dashboard")
    st.markdown("### Real-time Business Risk Analysis System")
    st.markdown("""
### 🎯 Problem Statement

Businesses struggle to identify risky transactions and low-performing vendors.
This system provides data-driven insights and predictions.
""")

    st.sidebar.markdown("### 🔍 Filters")

    category_filter = st.sidebar.multiselect(
        "Select Category",
        df["category"].unique(),
        default=df["category"].unique()
    )

    filtered_df = df[df["category"].isin(category_filter)]

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Total Sales", round(filtered_df["sales"].sum(),2))
    col2.metric("Total Profit", round(filtered_df["profit"].sum(),2))
    col3.metric("Transactions", len(filtered_df))
    col4.metric("High Risk %", round(filtered_df["risk_status"].mean()*100,2))

    st.subheader("📌 Key Insights")

    top_category = filtered_df.groupby("category")["sales"].sum().idxmax()
    high_risk_percent = filtered_df["risk_status"].mean() * 100

    st.write(f"🔹 Top Category: {top_category}")
    st.write(f"🔹 High Risk Transactions: {round(high_risk_percent,2)}%")

    st.subheader("💡 Recommendations")

    if high_risk_percent > 30:
        st.warning("High risk detected. Reduce discount strategy.")
    else:
        st.success("Business is stable.")

    # 🎯 GAUGE
    risk_rate = filtered_df["risk_status"].mean()*100

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_rate,
        title={'text':"Business Risk %"},
        gauge={'axis':{'range':[0,100]}}
    ))

    st.plotly_chart(fig_gauge, use_container_width=True)

    # 📊 CHARTS
    col1, col2 = st.columns(2)

    with col1:
        cat_data = filtered_df.groupby("category")["sales"].sum().reset_index()

        fig_bar = px.bar(
            cat_data,
            x="category",
            y="sales",
            color="category"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        filtered_df["order_date"] = pd.to_datetime(filtered_df["order_date"], errors="coerce")
        filtered_df = filtered_df.dropna(subset=["order_date"])

        trend = filtered_df.groupby(filtered_df["order_date"].dt.to_period("M"))["sales"].sum().reset_index()
        trend["order_date"] = trend["order_date"].astype(str)

        fig_line = px.line(trend, x="order_date", y="sales")
        st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("📈 Trend Insight")
    st.write("Sales trend shows business performance over time.")

    # PIE + SCATTER
    col3, col4 = st.columns(2)

    with col3:
        risk_df = filtered_df["risk_status"].value_counts().reset_index()
        risk_df.columns = ["Risk Type","Count"]

        fig_pie = px.pie(risk_df, names="Risk Type", values="Count")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col4:
        fig_scatter = px.scatter(filtered_df, x="sales", y="profit", color="risk_status")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # MAP
    if "country" in filtered_df.columns:
        map_df = filtered_df.groupby("country")["sales"].sum().reset_index()
        fig_map = px.choropleth(map_df, locations="country", locationmode="country names", color="sales")
        st.plotly_chart(fig_map, use_container_width=True)


# ---------------------------------------------------
# ⚠️ RISK ANALYSIS
# ---------------------------------------------------
elif page == "Risk Analysis":

    st.title("⚠️ Advanced Risk Analysis Dashboard")

    col1, col2, col3 = st.columns(3)

    total_risk = df["risk_status"].sum()
    total_safe = (df["risk_status"] == 0).sum()
    risk_percent = df["risk_status"].mean() * 100

    col1.metric("🚨 High Risk Transactions", total_risk)
    col2.metric("✅ Safe Transactions", total_safe)
    col3.metric("📊 Risk %", round(risk_percent,2))

    st.markdown("---")

    # PIE
    risk_df = df["risk_status"].value_counts().reset_index()
    risk_df.columns = ["Risk Type","Count"]

    fig_pie = px.pie(risk_df, names="Risk Type", values="Count", hole=0.5)
    st.plotly_chart(fig_pie, use_container_width=True)

    # CATEGORY RISK
    st.subheader("📊 Risk by Category")
    cat_risk = df.groupby("category")["risk_status"].mean().reset_index()

    st.plotly_chart(px.bar(cat_risk, x="category", y="risk_status", color="risk_status"))

    # TIME TREND (FIXED)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])

    trend = df.groupby(df["order_date"].dt.to_period("M"))["risk_status"].mean().reset_index()
    trend["order_date"] = trend["order_date"].astype(str)

    st.plotly_chart(px.line(trend, x="order_date", y="risk_status"))

    # ADVANCED FEATURE 🔥
    st.subheader("📌 Risk Insight")

    if risk_percent > 40:
        st.error("🚨 Critical Risk Level - Immediate Action Required")
    elif risk_percent > 20:
        st.warning("⚠️ Moderate Risk - Monitor Closely")
    else:
        st.success("✅ Low Risk - Business Stable")

    # TOP RISK TRANSACTIONS
    st.subheader("🚨 Top Risk Transactions")
    st.dataframe(df[df["risk_status"] == 1].head(10))


# ---------------------------------------------------
# 🤖 MACHINE LEARNING
# ---------------------------------------------------
elif page == "Machine Learning":

    st.title("🤖 AI Risk Prediction System")

    features = ["sales","profit","discount","shipping_cost","quantity"]

    for col in features:
        if col not in df.columns:
            df[col] = 0

    X = df[features]
    y = df["risk_status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred) * 100
    st.metric("Model Accuracy", f"{round(acc,2)} %")

    # CONFUSION MATRIX
    st.subheader("Confusion Matrix")
    cm = confusion_matrix(y_test, pred)

    fig_cm, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    st.pyplot(fig_cm)

    # FEATURE IMPORTANCE
    st.subheader("Feature Importance")

    importance = model.feature_importances_
    imp_df = pd.DataFrame({
        "Feature": features,
        "Importance": importance
    }).sort_values(by="Importance", ascending=False)

    st.plotly_chart(px.bar(imp_df, x="Feature", y="Importance", color="Importance"))

    # NEW FEATURE 🔥
    st.subheader("📊 Prediction Insight")

    high_risk_count = (pred == 1).sum()
    st.write(f"Predicted High Risk Cases: {high_risk_count}")

    # ANOMALY DETECTION
    iso = IsolationForest(contamination=0.05)
    df["anomaly"] = iso.fit_predict(X)

    fraud_count = (df["anomaly"] == -1).sum()
    st.error(f"🚨 Suspicious Transactions: {fraud_count}")

    # PREDICTION INPUT
    st.subheader("Predict Risk")

    s = st.number_input("Sales", 0.0)
    p = st.number_input("Profit", 0.0)
    d = st.number_input("Discount", 0.0)
    sh = st.number_input("Shipping Cost", 0.0)
    q = st.number_input("Quantity", 0.0)

    if st.button("Predict"):
        result = model.predict([[s,p,d,sh,q]])
        if result[0] == 1:
            st.error("⚠️ High Risk Transaction")
        else:
            st.success("✅ Safe Transaction")


# ---------------------------------------------------
# 🏢 VENDOR ANALYTICS
# ---------------------------------------------------
elif page == "Vendor Analytics":

    st.title("🏢 Vendor Risk Intelligence")

    vendor_df = df.groupby("vendor id").agg({
        "sales": "sum",
        "profit": "sum",
        "risk_status": "mean"
    }).reset_index()

    vendor_df["risk_score"] = vendor_df["risk_status"] * 100

    # KPIs
    col1, col2 = st.columns(2)
    col1.metric("Total Vendors", vendor_df.shape[0])
    col2.metric("Avg Vendor Risk", round(vendor_df["risk_score"].mean(),2))

    st.markdown("---")

    # BAR
    st.plotly_chart(px.bar(vendor_df, x="vendor id", y="risk_score"))

    # SCATTER
    st.plotly_chart(px.scatter(
        vendor_df,
        x="sales",
        y="profit",
        size="risk_score",
        color="risk_score"
    ))

    # NEW FEATURE 🔥
    st.subheader("📌 Vendor Insight")

    risky_vendors = vendor_df[vendor_df["risk_score"] > 50]

    if len(risky_vendors) > 0:
        st.warning(f"{len(risky_vendors)} vendors are high risk")
    else:
        st.success("All vendors performing well")

    # TOP RISK
    st.subheader("🚨 High Risk Vendors")
    st.dataframe(vendor_df.sort_values(by="risk_score", ascending=False).head(5))

    # BEST
    st.subheader("🏆 Best Vendors")
    st.dataframe(vendor_df.sort_values(by="sales", ascending=False).head(5))

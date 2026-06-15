import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import time
import requests

def glass_card_start():
    st.markdown("""
    <div style="
        background: rgba(0,0,0,0.75);
        border: 1px solid
        rgba(225,225,225,0.2)
        padding: 25px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
    ">
    """, unsafe_allow_html=True)

def glass_card_end():
    st.markdown("</div>", unsafe_allow_html=True)
    
st.set_page_config(layout="wide")
def set_background():
    import base64

    with open("background.png", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    /* 🔥 Apply to ROOT container (strongest) */
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/png;base64,{b64}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}

    /* 🔥 Kill all white layers */
    [data-testid="stAppViewContainer"] > .main {{
        background: transparent !important;
    }}

    .block-container {{
        background: transparent !important;
        padding-top: 1rem !important;
    }}

    section.main {{
        background: transparent !important;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: rgba(0,0,0,0.85) !important;
    }}

    /* Text */
    h1,h2,h3,h4,h5,h6,p,label,span {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
st.markdown("""
<style>

/* 🔥 FORCE uploader text to black */
div[data-testid="stFileUploader"] label,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploader"] div {
    color: black !important;
}

/* 🔥 File name + size text */
div[data-testid="stFileUploader"] p {
    color: black !important;
}

/* 🔥 Browse button (keep blue) */
div[data-testid="stFileUploader"] button {
    background-color: #00c6ff !important;
    color: white !important;
    border-radius: 10px !important;
}

/* 🔥 Download buttons fix */
button[kind="secondary"] {
    background-color: #00c6ff !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Hover */
button[kind="secondary"]:hover {
    background-color: #0072ff !important;
}


/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0.85) !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Radio buttons text */
div[role="radiogroup"] label {
    color: white !important;
}

/* Logout button fix */
section[data-testid="stSidebar"] button {
    background-color: #00c6ff !important;
    color: white !important;
    border-radius: 10px;
}


/* Target Streamlit buttons */
div.stButton > button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    font-size: 18px;
    height: 55px;
    width: 260px;
    border-radius: 12px;
    border: none;
    font-weight: bold;

    /* Glow effect */
    box-shadow: 0 0 15px rgba(0,198,255,0.6);

    /* Smooth animation */
    transition: all 0.3s ease-in-out;
}

/* Hover effect */
div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px rgba(0,198,255,1);
    background: linear-gradient(45deg, #0072ff, #00c6ff);
}

/* Click effect */
div.stButton > button:active {
    transform: scale(0.98);
}

</style>
""", unsafe_allow_html=True)


if "page_state" not in st.session_state:
    st.session_state.page_state = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "splash_done" not in st.session_state:
    st.session_state.splash_done = False



st.markdown("""
<style>
/* All text white */
h1, h2, h3, h4, h5, h6, p, div, label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


def home_page():
    import base64
    import streamlit as st

    # 🔹 Load background image
    with open("background.png", "rb") as f:
        data = base64.b64encode(f.read()).decode()

    # 🔹 Background + Text + Button Style
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
    }}

    /* Make all text white */
    h1, h2, h3, h4, h5, h6, p, div {{
        color: white !important;
    }}

    /* ALL buttons same color */
    div.stButton > button {{
        background-color: #00c6ff;
        color: white;
        font-size: 18px;
        height: 50px;
        width: 200px;
        border-radius: 10px;
        border: none;
    }}

    div.stButton > button:hover {{
        background-color: #0072ff;
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 🔹 Space to center content
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # 🔹 Text Box (for visibility)
    st.markdown("""
    <div style="
    background-color: rgba(0,0,0,0.6);
    padding: 25px;
    border-radius: 15px;
    text-align:center;
    width: 60%;
    margin: auto;">
        <h1>AI Business Intelligence System</h1>
        <p style="font-size:18px;">
        An intelligent system that analyzes business data to detect risks and generate insights.
Helps organizations make accurate, data-driven decisions efficiently.
        </p>
        <ul style="list-style-type:none; padding:0;">
<li>> Sign up if you are a new user and then login to access the system</li>
<li>> Click on <b>Dashboard</b> to upload your dataset and start analysis</li>
<li>> Download sample datasets from the <b>Dataset Guide</b> section after login</li>
</ul>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # 🔹 Center Button
    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        if st.button("Start Exploring"):
            st.session_state.page_state = "login"
            st.rerun()
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
    
    import base64, time

    with open("logo.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style="
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    background-color:white;">
        <img src="data:image/png;base64,{logo_base64}" width="200">
    </div>
    """, unsafe_allow_html=True)

    time.sleep(2)

    st.session_state.splash_done = True
    st.rerun()
    
    # ---------------- AUTH FUNCTION ----------------
def auth():
    
    st.title("AI Business Intelligence Platform ")
    choice = st.radio("Choose", ["Login", "Sign Up","Forgot Password"])

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
    elif choice == "Sign Up":
    
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
                    st.write(res.status_code)
                    st.write(res.text)
                    
                    data = res.json()

                    if res.status_code == 200:
                        st.success("Signup successful ✅")
                    else:
                        st.error(data.get("detail", "Signup failed"))

                except Exception as e:
                    st.error(f"Error: {e}")
         
@app.post("/login")
def login(user: User):

    db = SessionLocal()

    # login code

    return {
        "token": token,
        "message": "Login successful"
    }


@app.post("/forgot-password")
def forgot_password(data: ForgotPassword):

    db = SessionLocal()

    user = db.query(UserTable).filter(
        UserTable.username == data.username
    ).first()

    if not user:

        db.close()

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.password = hash_password(
        data.new_password
    )

    db.commit()

    db.close()

    return {
        "message": "Password reset successful"
    }
# ---------------- LOGIN CHECK ----------------
if"logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
    set_background()

if st.session_state.page_state == "home":
    home_page()
    st.stop()

if not st.session_state.logged_in:
    set_background()  # ⭐ IMPORTANT
    auth()
    st.stop()
set_background ()  
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
    set_background()
    glass_card_start()
    
    st.title("Dataset Usage Guide")

    # ---------------- GUIDE ----------------
    st.markdown("""
##  Step-by-Step Guide to Use the System

###  Step 1: Access the Dashboard 
-  click on business insights dashboard to uplad your datasets
- Scroll down to download demo datasets
---

###  Step 2: Upload Dataset 
- Go to **Upload Dataset** section  
- Supported formats:
  - CSV (.csv)
  - Excel (.xlsx, .xls)
  - JSON (.json)
  - Text (.txt)

---

###  Step 3: Dataset Processing 
- The system automatically reads your dataset  
- Detects:
  - Numerical columns  
  - Categorical columns  
  - Date columns  

---

###  Step 4: Auto Column Generation 
If required columns are missing, system generates:

- `sales = quantity × 100`  
- `profit = sales × 0.3`  
- `shipping_cost = sales × 0.05`  
- `discount = 0.05`  

---

###  Step 5: Data Visualization 
- Automatically generates:
  - Bar charts  
  - Line charts  
  - Area charts  
- Based on selected columns  

---

###  Step 6: Analysis & Insights 
- Displays patterns and trends  
- Helps in business decision making  

---

###  Step 7: Use Sample Dataset (Optional) 
- If you don’t have data:
  - Download sample datasets below  
  - Upload them to test the system  

---

##  Supported File Types
CSV, Excel, JSON, TXT  

---

##  Important Guidelines
- Dataset must have column headers  
- Avoid empty or corrupted files  
- Keep data clean and structured  
""")

    # ---------------- DOWNLOAD SECTION ----------------
    st.divider()
    st.subheader(" Download Sample Datasets")

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


    # ---------------- NOTE ----------------
    st.markdown("""
###  Important Information

- The sample datasets are provided **only for demonstration purposes**
- Users are encouraged to upload their **own datasets** for actual analysis  
- Ensure your dataset follows the recommended format for best results  
""")
    glass_card_end()
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
    
    set_background()

    glass_card_start()

    # ---------------- HEADER ----------------

    st.markdown("""
    <div style="
    background: linear-gradient(90deg,#0f172a,#1e3a8a);
    padding:25px;
    border-radius:20px;
    margin-bottom:25px;
    text-align:center;
    ">

    <h1 style="color:white;">
     AI Business Intelligence Dashboard
    </h1>

    <p style="color:#cbd5e1;font-size:18px;">
    Real-Time Analytics • Risk Detection • AI Insights
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    background: rgba(0,0,0,0.6);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    ">

    <h3> Dashboard Overview</h3>

    <p>
    This platform provides intelligent business analytics,
    vendor monitoring, predictive insights,
    and real-time risk analysis using AI-powered dashboards.
    </p>

    </div>
    """, unsafe_allow_html=True)

    # ---------------- SIDEBAR ----------------

    st.sidebar.markdown("##  Dashboard Filters")

    category_filter = st.sidebar.multiselect(
        "Select Category",
        df["category"].unique(),
        default=df["category"].unique()
    )

    filtered_df = df[
        df["category"].isin(category_filter)
    ]

    # ---------------- KPI CARDS ----------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div style="
            background:#111827;
            padding:25px;
            border-radius:18px;
            text-align:center;
            box-shadow:0px 0px 15px rgba(0,255,255,0.3);
        ">

        <h3 style='color:#9ca3af'>
         Total Sales
        </h3>

        <h1 style='color:#22d3ee'>
        {round(filtered_df["sales"].sum(),2)}
        </h1>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div style="
            background:#111827;
            padding:25px;
            border-radius:18px;
            text-align:center;
            box-shadow:0px 0px 15px rgba(0,255,0,0.3);
        ">

        <h3 style='color:#9ca3af'>
         Total Profit
        </h3>

        <h1 style='color:#4ade80'>
        {round(filtered_df["profit"].sum(),2)}
        </h1>

        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div style="
            background:#111827;
            padding:25px;
            border-radius:18px;
            text-align:center;
            box-shadow:0px 0px 15px rgba(255,255,0,0.3);
        ">

        <h3 style='color:#9ca3af'>
         Transactions
        </h3>

        <h1 style='color:#facc15'>
        {len(filtered_df)}
        </h1>

        </div>
        """, unsafe_allow_html=True)

    with col4:

        risk_percent = round(
            filtered_df["risk_status"].mean()*100,
            2
        )

        st.markdown(f"""
        <div style="
            background:#111827;
            padding:25px;
            border-radius:18px;
            text-align:center;
            box-shadow:0px 0px 15px rgba(255,0,0,0.3);
        ">

        <h3 style='color:#9ca3af'>
        ⚠ High Risk %
        </h3>

        <h1 style='color:#f87171'>
        {risk_percent}%
        </h1>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- AI INSIGHTS ----------------

    top_category = filtered_df.groupby(
        "category"
    )["sales"].sum().idxmax()

    st.markdown(f"""
    <div style="
    background:rgba(0,0,0,0.6);
    padding:20px;
    border-radius:15px;
    margin-bottom:20px;
    ">

    <h2 style="color:#22d3ee;">
    🤖 AI Insights
    </h2>

    <p style="font-size:18px;color:white;">

    • Top category is <b>{top_category}</b><br><br>

    • Risk exposure detected in
    <b>{risk_percent}%</b> transactions<br><br>

    • AI detected active business growth trends<br><br>

    • Vendor monitoring system is operational

    </p>

    </div>
    """, unsafe_allow_html=True)

    # ---------------- GAUGE ----------------

    risk_rate = filtered_df[
        "risk_status"
    ].mean()*100

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_rate,
        title={'text':"Business Risk %"},
        gauge={
            'axis':{'range':[0,100]}
        }
    ))

    fig_gauge.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_gauge,
        use_container_width=True
    )

    # ---------------- CHARTS ----------------

    col1, col2 = st.columns(2)

    with col1:

        cat_data = filtered_df.groupby(
            "category"
        )["sales"].sum().reset_index()

        fig_bar = px.bar(
            cat_data,
            x="category",
            y="sales",
            color="category"
        )

        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    with col2:

        filtered_df["order_date"] = pd.to_datetime(
            filtered_df["order_date"],
            errors="coerce"
        )

        filtered_df = filtered_df.dropna(
            subset=["order_date"]
        )

        trend = filtered_df.groupby(
            filtered_df["order_date"].dt.to_period("M")
        )["sales"].sum().reset_index()

        trend["order_date"] = trend[
            "order_date"
        ].astype(str)

        fig_line = px.line(
            trend,
            x="order_date",
            y="sales"
        )

        fig_line.update_traces(
            line_shape="spline"
        )

        fig_line.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_line,
            use_container_width=True
        )

    # ---------------- PIE + AREA ----------------

    col3, col4 = st.columns(2)

    with col3:

        risk_df = filtered_df[
            "risk_status"
        ].value_counts().reset_index()

        risk_df.columns = [
            "Risk Type",
            "Count"
        ]

        fig_pie = px.pie(
            risk_df,
            names="Risk Type",
            values="Count"
        )

        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    with col4:

        fig_area = px.area(
            trend,
            x="order_date",
            y="sales"
        )

        fig_area.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_area,
            use_container_width=True
        )

    # ---------------- MAP ----------------

    if "country" in filtered_df.columns:

        map_df = filtered_df.groupby(
            "country"
        )["sales"].sum().reset_index()

        fig_map = px.choropleth(
            map_df,
            locations="country",
            locationmode="country names",
            color="sales"
        )

        fig_map.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_map,
            use_container_width=True
        )

    glass_card_end()

# ---------------------------------------------------
# RISK ANALYSIS
# ---------------------------------------------------
elif page == "Risk Analysis":
 
    set_background()
            
    glass_card_start()
      
    st.title(" Advanced Risk Analysis Dashboard")

    col1, col2, col3 = st.columns(3)

    total_risk = df["risk_status"].sum()
    total_safe = (df["risk_status"] == 0).sum()
    risk_percent = df["risk_status"].mean() * 100

    col1.metric(" High Risk Transactions", total_risk)
    col2.metric(" Safe Transactions", total_safe)
    col3.metric(" Risk %", round(risk_percent,2))

    st.markdown("---")

    # PIE
    risk_df = df["risk_status"].value_counts().reset_index()
    risk_df.columns = ["Risk Type","Count"]

    fig_pie = px.pie(risk_df, names="Risk Type", values="Count", hole=0.5)
    st.plotly_chart(fig_pie, use_container_width=True)

    # CATEGORY RISK
    st.subheader(" Risk by Category")
    cat_risk = df.groupby("category")["risk_status"].mean().reset_index()

    st.plotly_chart(px.bar(cat_risk, x="category", y="risk_status", color="risk_status"))

    # TIME TREND (FIXED)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])

    trend = df.groupby(df["order_date"].dt.to_period("M"))["risk_status"].mean().reset_index()
    trend["order_date"] = trend["order_date"].astype(str)

    st.plotly_chart(px.line(trend, x="order_date", y="risk_status"))

    # ADVANCED FEATURE 
    st.subheader(" Risk Insight")

    if risk_percent > 40:
        st.error(" Critical Risk Level - Immediate Action Required")
    elif risk_percent > 20:
        st.warning(" Moderate Risk - Monitor Closely")
    else:
        st.success("✅ Low Risk - Business Stable")

    # TOP RISK TRANSACTIONS
    st.subheader(" Top Risk Transactions")
    st.dataframe(df[df["risk_status"] == 1].head(10))
    
    glass_card_end ()  

# ---------------------------------------------------
#  MACHINE LEARNING
# ---------------------------------------------------
elif page == "Machine Learning":
     
    set_background()
    glass_card_start()
    st.title(" AI Risk Prediction System")

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

    # NEW FEATURE 
    st.subheader(" Prediction Insight")

    high_risk_count = (pred == 1).sum()
    st.write(f"Predicted High Risk Cases: {high_risk_count}")

    # ANOMALY DETECTION
    iso = IsolationForest(contamination=0.05)
    df["anomaly"] = iso.fit_predict(X)

    fraud_count = (df["anomaly"] == -1).sum()
    st.error(f" Suspicious Transactions: {fraud_count}")

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
            st.error(" High Risk Transaction")
        else:
            st.success(" Safe Transaction")

    glass_card_end()
    

# ---------------------------------------------------
# VENDOR ANALYTICS
# ---------------------------------------------------

elif page == "Vendor Analytics":

    st.title(" Vendor Analytics")

    # ================= DASHBOARD SUMMARY =================

    st.subheader(" Vendor Dashboard Summary")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(f"""
        ###  Total Vendors

        {df.shape[0]}
        """)

    with col2:

        avg_risk = round(
            df["risk_status"].mean(),
            2
        )

        st.warning(f"""
        ### ⚠ Average Risk

        {avg_risk}
        """)

    with col3:

        risky_count = (
            df["risk_status"] > 0.5
        ).sum()

        st.error(f"""
        ###  High Risk Vendors

        {risky_count}
        """)

    st.write("")

    # ================= VENDOR DATA =================

    vendor_df = df.groupby(
        "vendor id"
    ).agg({
        "sales": "sum",
        "profit": "sum",
        "risk_status": "mean"
    }).reset_index()

    vendor_df["risk_status"] = (
        vendor_df["risk_status"] * 100
    )

    # ================= BAR CHART =================

    fig = px.bar(
        vendor_df,
        x="vendor id",
        y="risk_status",
        color="risk_status",
        title=" Vendor Risk Analysis",
        color_continuous_scale="reds"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ================= SCATTER CHART =================

    fig2 = px.scatter(
        vendor_df,
        x="sales",
        y="profit",
        size="risk_status",
        color="risk_status",
        hover_name="vendor id",
        title=" Vendor Sales vs Profit",
        color_continuous_scale="viridis"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ================= INSIGHTS =================

    st.subheader(" Vendor Insights")

    risky_vendors = vendor_df[
        vendor_df["risk_status"] > 50
    ]

    if len(risky_vendors) > 0:

        st.warning(
            f"{len(risky_vendors)} vendors are high risk."
        )

    else:

        st.success(
            "✅ All vendors are performing well."
        )

    # ================= TABLES =================

    colA, colB = st.columns(2)

    with colA:

        st.subheader(" High Risk Vendors")

        st.dataframe(
            vendor_df.sort_values(
                by="risk_status",
                ascending=False
            ).head(5),
            use_container_width=True
        )

    with colB:

        st.subheader(" Best Vendors")

        st.dataframe(
            vendor_df.sort_values(
                by="sales",
                ascending=False
            ).head(5),
            use_container_width=True
        )

    glass_card_end()

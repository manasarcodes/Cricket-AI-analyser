import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="Cricket AI Analyser", page_icon="🏏", layout="wide")

# --- CUSTOM CSS ---
def set_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif !important;
    }

    /* --- ANIMATIONS --- */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slowFade {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #240a0a 0%, #0a0303 100%);
        color: #f5e6e6;
        animation: slowFade 1s ease-out;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(25, 5, 5, 0.6) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        animation: slowFade 0.8s ease-out;
    }

    /* Custom Header */
    .custom-header {
        background: rgba(255, 42, 42, 0.02);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 42, 42, 0.2);
        box-shadow: 0 4px 30px rgba(255, 42, 42, 0.1);
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.8s ease-out;
    }
    
    .custom-header h1 {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 3.5rem !important;
        background: -webkit-linear-gradient(45deg, #FF2A2A, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .custom-header p {
        margin-top: 10px;
        color: #FF2A2A;
        font-size: 1.2rem;
        font-weight: 600;
        letter-spacing: 1px;
    }

    /* Style the main title */
    h1 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        background: -webkit-linear-gradient(45deg, #FF2A2A, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        animation: fadeInUp 0.7s ease-out;
    }

    /* Style subheaders */
    h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        color: #e2e8f0 !important;
        background: none !important;
        -webkit-text-fill-color: #e2e8f0 !important;
        font-weight: 400 !important;
        letter-spacing: 1px;
        margin-bottom: 20px;
        animation: fadeInUp 0.9s ease-out;
    }

    /* Glassmorphism for Metrics */
    [data-testid="stMetric"] {
        background: rgba(255, 42, 42, 0.02);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 42, 42, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: all 0.3s ease;
        animation: fadeInUp 0.9s ease-out;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: rgba(255, 42, 42, 0.5);
        box-shadow: 0 12px 40px rgba(255, 42, 42, 0.2);
    }
    
    [data-testid="stMetricValue"] > div {
        background: -webkit-linear-gradient(45deg, #FF2A2A, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        font-weight: 800;
    }

    /* Dataframes and Charts */
    [data-testid="stDataFrame"], .stLineChart, .stBarChart {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        animation: fadeInUp 1s ease-out;
    }

    /* Stylize Buttons (like the AI Generate button) */
    .stButton > button {
        background: linear-gradient(45deg, #FF2A2A, #FFD700);
        color: #1a1a1a !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.1rem;
        border: none !important;
        border-radius: 10px;
        padding: 12px 28px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 42, 42, 0.3);
        animation: fadeInUp 1.1s ease-out;
    }
    .stButton > button:hover {
        transform: scale(1.04);
        box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
    }

    /* Form Elements dropdowns */
    .stMultiSelect [data-baseweb="select"], .stSelectbox [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Custom Dividers */
    hr {
        border-bottom: 1px solid rgba(255, 42, 42, 0.2) !important;
        margin: 2em 0;
    }

    /* Custom Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        color: #a0aec0;
        font-size: 0.9rem;
    }
    
    .custom-footer p {
        background: -webkit-linear-gradient(45deg, #FF2A2A, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    

set_custom_css()

# --- CONFIGURATION ---
genai.configure(api_key=st.secrets["gemini_api"])
model = genai.GenerativeModel('models/gemini-3-flash-preview')

# --- DATA LOADING ---
@st.cache_data
def load_data():
    
    try:
        # 1. Attempt to load the file
        df = pd.read_csv('cricket_data_trimmed.csv')
        
        # 2. Check if the dataframe is empty
        if df.empty:
            st.error("The dataset file is empty.")
            return None

        # 3. Defensive check: Does 'season' exist?
        if 'season' in df.columns:
            df['season'] = pd.to_numeric(df['season'], errors='coerce')
        else:
            st.warning("Column 'season' not found in the dataset.")

        # 4. Cleanup
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])
            
        return df
        
    except FileNotFoundError:
        st.error("Error: 'cricket_data_trimmed.csv' not found in the project folder.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None
df = load_data()

st.markdown("""
<div class="custom-header">
    <h1>🏏 Cricket Analytics Pro</h1>
    <p>Powered by Advanced AI Insights</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
years = st.sidebar.multiselect("Select Seasons", sorted(df['season'].unique()))
team = st.sidebar.multiselect("Select Team(s)", sorted(df['batting_team'].unique()))

# --- MAIN DASHBOARD ---
if years:
    st.header("Season-over-Season Review")
    yearly_data = df[df['season'].isin(years)]
    
    # 1. KEY METRICS
    col1, col2, col3 = st.columns(3)
    col1.metric("Matches", int(yearly_data['match_id'].nunique()))
    col2.metric("Total Runs", int(yearly_data['runs_total'].sum()))
    col3.metric("Total Wickets", int(yearly_data['bowler_wicket'].sum()))

    # 2. TREND & STYLE CHARTS
    st.subheader("Performance Trends")
    chart_data = yearly_data.groupby(['season', 'batting_team'])['runs_total'].sum().reset_index()
    st.line_chart(
        chart_data.pivot(index='season', columns='batting_team', values='runs_total'),
        y_label="Total runs"
    )

    if team:
        st.divider()
        st.header(f"Team Deep Dive: {', '.join(team)}")
        team_data = yearly_data[(yearly_data['batting_team'].isin(team)) | (yearly_data['bowling_team'].isin(team))]
        
        # Top Performers Tables
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Top 5 Batters**")
            st.dataframe(team_data.groupby('batter')['runs_batter'].sum().nlargest(5).reset_index().rename(columns={'runs_batter': 'runs'}), use_container_width=True)
        with col_b:
            st.write("**Top 5 Bowlers**")
            st.dataframe(team_data.groupby('bowler')['bowler_wicket'].sum().nlargest(5).reset_index(), use_container_width=True)

        # Style & Frequency
        col_c, col_d = st.columns(2)
        with col_c:
            if 'shot_type' in team_data.columns:
                st.write("**Shot Frequency**")
                st.bar_chart(team_data['shot_type'].value_counts().nlargest(5))
        with col_d:
            if 'bowling_type' in team_data.columns:
                st.write("**Bowling Frequency**")
                st.bar_chart(team_data['bowling_type'].value_counts().nlargest(5))

        # 3. PLAYER COMPARISON SECTION
        st.divider()
        st.header("⚖️ Year-Wise Player Comparison")
        selected_players = st.multiselect("Select Players to Compare", sorted(team_data['batter'].unique()))
        if selected_players:
            comp_data = team_data[team_data['batter'].isin(selected_players)]
            comp_pivot = comp_data.groupby(['season', 'batter'])['runs_batter'].sum().unstack()
            st.line_chart(comp_pivot)
            st.dataframe(comp_pivot, use_container_width=True)

        # 4. AI TACTICAL INSIGHT
        if st.button("Generate Tactical Insight"):
            with st.spinner("Gemini is analyzing..."):
                team_names = ', '.join(team)
                prompt = f"Act as a professional Cricket Coach. Analyze {team_names}'s stats and provide 3 tactical improvements in a markdown table format."
                response = model.generate_content(prompt)
                st.markdown(response.text)
else:
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 40px; background: rgba(255, 42, 42, 0.05); border-radius: 16px; border: 1px solid rgba(255, 42, 42, 0.2); backdrop-filter: blur(10px); box-shadow: 0 4px 30px rgba(0,0,0,0.3); animation: fadeInUp 0.8s ease-out forwards;">
        <h2 style="font-size: 2.2rem; margin-bottom: 15px; font-weight: 800; background: -webkit-linear-gradient(45deg, #FF2A2A, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🏏 Ready for Analysis</h2>
        <p style="color: #FF2A2A; font-size: 1.2rem; font-weight: 600; letter-spacing: 0.5px;">Please select seasons from the sidebar to begin.</p>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="custom-footer">
    <hr>
    <p>🏆 Built for Cricket Enthusiasts </p>
</div>
""", unsafe_allow_html=True)
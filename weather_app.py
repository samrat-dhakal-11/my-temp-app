import streamlit as st
import numpy as np
import datetime

# Set up the page configuration for mobile-friendly view
st.set_page_config(page_title="VibeTemp - Weather Dashboard", page_icon="🌡️", layout="centered")

st.title("🌡️ Real-Time Temperature Dashboard")
st.write("A sleek, responsive app to track local environmental temperatures.")

# 1. State Management (Keeps data safe across reruns)
if "current_temp_c" not in st.session_state:
    st.session_state.current_temp_c = 22.5

if "temp_history" not in st.session_state:
    # Pre-populate with some initial mock historical data
    base_time = datetime.datetime.now()
    st.session_state.temp_history = [
        {
            "Time": (base_time - datetime.timedelta(seconds=i*5)).strftime("%H:%M:%S"), 
            "Temperature (°C)": 22.5 + np.random.uniform(-0.5, 0.5)
        }
        for i in range(10, 0, -1)
    ]

# 2. Sidebar Controls
st.sidebar.header("Settings")
unit = st.sidebar.radio("Select Temperature Unit:", ["Celsius (°C)", "Fahrenheit (°F)"])

# Helper function to handle unit conversion dynamically
def format_temp(temp_c):
    if "Fahrenheit" in unit:
        return (temp_c * 9/5) + 32, "°F"
    return temp_c, "°C"

# 3. Main Dashboard Fragment (Auto-refreshes seamlessly every 5 seconds)
@st.fragment(run_every=5)
def simulation_loop():
    # Simulate slight temperature fluctuation
    fluctuation = np.random.uniform(-0.5, 0.5)
    st.session_state.current_temp_c = round(st.session_state.current_temp_c + fluctuation, 1)
    
    # Append to history queue
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.temp_history.append({
        "Time": current_time, 
        "Temperature (°C)": st.session_state.current_temp_c
    })
    
    # Keep history length manageable (Max 15 points to save mobile memory)
    if len(st.session_state.temp_history) > 15:
        st.session_state.temp_history.pop(0)

    # Format current values for display
    display_val, symbol = format_temp(st.session_state.current_temp_c)
    
    # Display Layout Columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Current Temperature", 
            value=f"{display_val}{symbol}", 
            delta=f"{round(fluctuation, 2)} {symbol}"
        )
    with col2:
        st.metric(
            label="Status", 
            value="Optimal" if 18 <= st.session_state.current_temp_c <= 26 else "Alert"
        )

    st.subheader("Temperature Trend Over Time")
    
    # Build clean chart data based on your updated logic
    chart_data = []
    for entry in st.session_state.temp_history:
        val, _ = format_temp(entry["Temperature (°C)"])
        chart_data.append({"Time": entry["Time"], "Temperature": val})
        
    # Render line chart explicitly tracking Temperature over Time
    st.line_chart(data=chart_data, x="Time", y="Temperature", use_container_width=True)
    st.caption("🔄 This section auto-updates every 5 seconds using Streamlit fragments.")

# Run the live auto-updating block
simulation_loop()

# 4. Interactive Manual Reset (Sits outside the auto-refresh loop)
st.divider()
if st.button("Reset Dashboard Data", use_container_width=True):
    st.session_state.current_temp_c = 22.5
    # Clear history and re-initialize next rerun
    if "temp_history" in st.session_state:
        del st.session_state.temp_history
    st.rerun()

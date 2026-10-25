"""Starter Streamlit dashboard for the OS resource leak project."""
import pandas as pd
import plotly.express as px
import streamlit as st

from detector import detect_suspicious_growth
from recovery import simulated_reset
from simulator import make_demo_processes

st.set_page_config(page_title="OS Resource Leak Detector", page_icon="🖥️", layout="wide")
st.title("Automated OS Resource Leak Detection and Recovery System")
st.caption("Learning prototype • SIMULATION MODE • No real processes are changed")

st.info(
    "This version uses simulated measurements. It demonstrates the workflow; "
    "it does not detect or repair leaks in applications running on your laptop."
)

processes = make_demo_processes()
process_names = list(processes.keys())

with st.sidebar:
    st.header("Detection settings")
    selected_process = st.selectbox("Process to inspect", process_names, index=1 if len(process_names) > 1 else 0)
    growth_threshold = st.slider("Minimum total growth (MB)", min_value=20, max_value=400, value=150, step=10)
    min_increases = st.slider("Minimum consecutive increases", min_value=2, max_value=5, value=3)
    st.caption("These are experimental settings, not universal definitions of a memory leak.")

series = processes[selected_process]
result = detect_suspicious_growth(
    series,
    minimum_growth_mb=growth_threshold,
    minimum_consecutive_increases=min_increases,
)

left, middle, right = st.columns(3)
left.metric("Selected process", selected_process)
middle.metric("Starting memory", f"{series[0]:.0f} MB")
right.metric("Current simulated memory", f"{series[-1]:.0f} MB")

chart_data = pd.DataFrame({
    "Sample": list(range(1, len(series) + 1)),
    "Memory (MB)": series,
})
fig = px.line(chart_data, x="Sample", y="Memory (MB)", markers=True, title=f"Memory usage over time — {selected_process}")
fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
st.plotly_chart(fig, use_container_width=True)

if result["suspicious"]:
    st.warning(f"Suspicious growth detected for {selected_process}. This is an alert for investigation, not proof of a leak.")
else:
    st.success(f"No suspicious growth detected for {selected_process} under the current settings.")

with st.expander("View sample measurements"):
    st.dataframe(chart_data, use_container_width=True, hide_index=True)

st.subheader("Simulated recovery")
st.write("The reset below changes only the demonstration data in memory. It does not affect your operating system.")
if st.button("Run simulated recovery", type="primary"):
    before = series[-1]
    after_series = simulated_reset(series)
    after = after_series[-1]
    st.session_state["last_recovery"] = {
        "process": selected_process,
        "before_mb": before,
        "after_mb": after,
        "status": "Improved in simulation" if after < before else "No improvement",
    }

if "last_recovery" in st.session_state:
    recovery = st.session_state["last_recovery"]
    st.write(f"**Process:** {recovery['process']}")
    st.write(f"**Before:** {recovery['before_mb']:.0f} MB → **After:** {recovery['after_mb']:.0f} MB")
    st.write(f"**Result:** {recovery['status']}")

st.subheader("All simulated processes")
summary_rows = []
for name, values in processes.items():
    detection = detect_suspicious_growth(
        values,
        minimum_growth_mb=growth_threshold,
        minimum_consecutive_increases=min_increases,
    )
    summary_rows.append({
        "Process": name,
        "Initial memory (MB)": values[0],
        "Final memory (MB)": values[-1],
        "Change (MB)": values[-1] - values[0],
        "Status": "Suspicious" if detection["suspicious"] else "Normal",
    })
st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

st.caption("Next steps: test detection edge cases, improve the detector, persist event logs, then consider observation-only monitoring of the environment hosting the app.")

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="BeamWise AI | Beam Engineering Studio", page_icon="📐", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp {
    background:
      radial-gradient(circle at 85% 8%, rgba(34, 211, 238, .10), transparent 28%),
      radial-gradient(circle at 8% 28%, rgba(59, 130, 246, .10), transparent 30%),
      #080d18;
}
[data-testid="stHeader"] { background: rgba(8,13,24,.82); }
.block-container { max-width: 1200px; padding-top: 2rem; padding-bottom: 4rem; }
.hero {
    padding: 4rem 2.8rem;
    border: 1px solid rgba(148,163,184,.22);
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(15,23,42,.97), rgba(15,38,63,.90));
    box-shadow: 0 24px 70px rgba(0,0,0,.25);
    position: relative; overflow: hidden;
}
.eyebrow {
    display:inline-block; padding:7px 12px; border-radius:999px;
    border:1px solid rgba(103,232,249,.35); color:#67e8f9;
    font-size:.78rem; letter-spacing:.12em; text-transform:uppercase;
}
.hero h1 { font-size: clamp(2.5rem, 6vw, 4.8rem); line-height:1.03; margin:.9rem 0 1rem; letter-spacing:-.045em; }
.gradient { background:linear-gradient(90deg,#fff,#67e8f9); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero p { color:#cbd5e1; font-size:1.1rem; max-width:720px; line-height:1.8; }
.section-title { font-size:1.65rem; font-weight:700; letter-spacing:-.025em; margin-top:2rem; }
.feature-card {
    height:100%; padding:1.25rem; border-radius:18px;
    border:1px solid rgba(148,163,184,.18); background:rgba(15,23,42,.72);
}
.feature-card h3 { margin:.3rem 0 .55rem; font-size:1.08rem; }
.feature-card p { color:#aebdd0; font-size:.94rem; line-height:1.6; }
.feature-icon { font-size:1.55rem; }
.muted { color:#aebdd0; }
.stat-card { border:1px solid rgba(148,163,184,.18); background:rgba(15,23,42,.65); border-radius:16px; padding:1rem 1.1rem; }
div.stButton > button[kind="primary"] {
    border:0; border-radius:12px; min-height:3rem; font-weight:700;
    background:linear-gradient(90deg,#0891b2,#2563eb); color:white;
}
div.stButton > button {
    border-radius:12px;
}
hr { border-color:rgba(148,163,184,.18); }
[data-testid="stSidebar"] { background:#0c1423; }
</style>
""", unsafe_allow_html=True)

def go_to(page):
    st.session_state["page"] = page

if "page" not in st.session_state:
    st.session_state["page"] = "home"

# ---------- Shared header ----------
with st.sidebar:
    st.markdown("## 📐 BeamWise AI")
    st.caption("Beam Engineering Studio")
    st.divider()
    if st.button("⌂  Home", use_container_width=True):
        go_to("home")
    if st.button("▥  Launch Beam Analyzer", type="primary", use_container_width=True):
        go_to("analyzer")
    st.divider()
    st.caption("Educational tool only. Validate results independently before using them in real designs.")

# ---------- Landing page ----------
if st.session_state["page"] == "home":
    st.markdown("""
    <div class="hero">
      <span class="eyebrow">STRUCTURAL ENGINEERING · INTERACTIVE LEARNING</span>
      <h1>Understand every load.<br><span class="gradient">Visualize every reaction.</span></h1>
      <p>BeamWise AI is an interactive beam-analysis workspace for students and curious engineers.
      Explore support reactions, shear force, and bending moment behaviour through visual calculations
      and step-by-step equilibrium explanations.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    a, b = st.columns([1, 1], gap="large")
    with a:
        if st.button("Launch Beam Analyzer  →", type="primary", use_container_width=True):
            go_to("analyzer")
            st.rerun()
    with b:
        st.markdown("<div class='muted' style='padding:.75rem 0'>Built for learning structural mechanics through interactive visualisation.</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>A clearer way to study beam behaviour</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    cards = [
        ("↗", "Reaction calculations", "Estimate support reactions from applied point loads and uniformly distributed loads."),
        ("⌁", "SFD & BMD visualisation", "View how shear force and bending moment change along the beam."),
        ("∑", "Step-by-step equilibrium", "Review total loads, moments, reaction equations, and downloadable result data.")
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(f"<div class='feature-card'><div class='feature-icon'>{icon}</div><h3>{title}</h3><p>{desc}</p></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Inside the workspace</div>", unsafe_allow_html=True)
    d1, d2 = st.columns([1, 1], gap="large")
    with d1:
        st.markdown("""
        <div class="stat-card">
          <h3>Beam configurations</h3>
          <p class="muted">Simply supported beams and cantilever beams, with vertical point loads and UDLs.</p>
          <hr>
          <h3>Results you can inspect</h3>
          <p class="muted">Support reactions, a load diagram, SFD and BMD plots, maximum absolute values, and CSV export.</p>
        </div>
        """, unsafe_allow_html=True)
    with d2:
        st.markdown("""
        <div class="stat-card">
          <h3>Designed for learning</h3>
          <p class="muted">Use the tool to explore how load magnitude, position, and distribution affect the beam response.</p>
          <hr>
          <h3>Technology</h3>
          <p class="muted">Python · Streamlit · NumPy · Pandas · Plotly</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p class='muted' style='text-align:center'>BEAMWISE AI · An educational engineering project</p>", unsafe_allow_html=True)

# ---------- Beam analyzer ----------
else:
    st.markdown("<span class='eyebrow'>INTERACTIVE WORKSPACE</span>", unsafe_allow_html=True)
    st.title("Beam Analyzer")
    st.caption("Configure the beam and its loads, then calculate reactions and inspect the diagrams.")
    st.warning("Educational tool only. Verify results against textbook examples and applicable engineering standards before relying on them for design.")

    with st.sidebar:
        st.markdown("### Beam setup")
        beam_type = st.selectbox("Support configuration", ["Simply supported", "Cantilever"])
        L = st.number_input("Beam length, L (m)", min_value=0.5, max_value=50.0, value=6.0, step=0.5)
        n_points = st.number_input("Number of point loads", min_value=0, max_value=8, value=1, step=1)
        n_udls = st.number_input("Number of UDLs", min_value=0, max_value=5, value=0, step=1)
        st.caption("Point loads: kN · UDL intensity: kN/m")

    st.markdown("### Define loads")
    point_loads, udls = [], []
    if n_points:
        st.markdown("**Point loads**")
        cols = st.columns(3)
        for i in range(int(n_points)):
            with cols[i % 3]:
                st.markdown(f"**Point load {i+1}**")
                p = st.number_input(f"Load P{i+1} (kN)", min_value=0.0, max_value=10000.0, value=10.0 if i == 0 else 5.0, step=1.0, key=f"p_{i}")
                x = st.number_input(f"Position x{i+1} (m)", min_value=0.0, max_value=float(L), value=float(min(L, L/2 if i == 0 else L*0.75)), step=0.1, key=f"x_{i}")
                point_loads.append((float(p), float(np.clip(x, 0, L))))
    if n_udls:
        st.markdown("**Uniformly distributed loads (UDLs)**")
        cols = st.columns(3)
        for i in range(int(n_udls)):
            with cols[i % 3]:
                st.markdown(f"**UDL {i+1}**")
                w = st.number_input(f"Intensity w{i+1} (kN/m)", min_value=0.0, max_value=10000.0, value=2.0 if i == 0 else 1.0, step=0.5, key=f"w_{i}")
                a = st.number_input(f"Start a{i+1} (m)", min_value=0.0, max_value=float(L), value=0.0, step=0.1, key=f"a_{i}")
                b = st.number_input(f"End b{i+1} (m)", min_value=0.0, max_value=float(L), value=float(L), step=0.1, key=f"b_{i}")
                udls.append((float(w), float(np.clip(a, 0, L)), float(np.clip(b, 0, L))))

    calculate = st.button("Calculate beam analysis", type="primary", use_container_width=True)
    if calculate:
        if any(b < a for _, a, b in udls):
            st.error("Please correct the UDL ranges: the end position must be at or after the start.")
            st.stop()

        total_load = sum(p for p, _ in point_loads)
        total_moment_left = sum(p*x for p, x in point_loads)
        for w, a, b in udls:
            total_load += w * (b-a)
            total_moment_left += w * (b-a) * ((a+b)/2)

        if beam_type == "Simply supported":
            RB = total_moment_left / L
            RA = total_load - RB
            fixed_moment = 0.0
        else:
            RA = total_load
            RB = 0.0
            fixed_moment = -total_moment_left

        xs = np.linspace(0, float(L), 601)
        shear = np.zeros_like(xs)
        moment = np.zeros_like(xs)
        for j, x in enumerate(xs):
            V = RA
            M = fixed_moment + RA*x
            for p, xp in point_loads:
                if xp <= x + 1e-10:
                    V -= p
                    M -= p * (x-xp)
            for w, a, b in udls:
                right = min(x, b)
                loaded_length = max(0.0, right-a)
                if loaded_length > 0:
                    V -= w*loaded_length
                    M -= w*loaded_length*(x-(a+right)/2)
            shear[j], moment[j] = V, M
        if beam_type == "Simply supported":
            shear[-1] = 0.0

        st.markdown("### Results overview")
        k1, k2, k3 = st.columns(3)
        k1.metric("Left reaction", f"{RA:.3f} kN")
        if beam_type == "Simply supported":
            k2.metric("Right reaction", f"{RB:.3f} kN")
        else:
            k2.metric("Fixed-end moment magnitude", f"{abs(fixed_moment):.3f} kN·m")
        k3.metric("Total applied load", f"{total_load:.3f} kN")

        st.markdown("### Beam and load configuration")
        beam_fig = go.Figure()
        beam_fig.add_trace(go.Scatter(x=[0, L], y=[0, 0], mode="lines", line=dict(width=8, color="#67e8f9"), name="Beam"))
        for p, x in point_loads:
            beam_fig.add_annotation(x=x, y=0.1, ax=x, ay=1.0, xref="x", yref="y", axref="x", ayref="y",
                                    text=f"{p:g} kN", showarrow=True, arrowhead=2, arrowcolor="#fb7185", font=dict(color="#fb7185"))
        for w, a, b in udls:
            if b > a and w > 0:
                for x in np.linspace(a, b, max(5, int((b-a)*5)+1)):
                    beam_fig.add_annotation(x=x, y=0.12, ax=x, ay=0.65, text="", showarrow=True, arrowhead=2, arrowcolor="#60a5fa", arrowsize=1)
                beam_fig.add_annotation(x=(a+b)/2, y=0.8, text=f"UDL {w:g} kN/m", showarrow=False, font=dict(color="#60a5fa"))
        if beam_type == "Simply supported":
            beam_fig.add_trace(go.Scatter(x=[0, L], y=[-0.2, -0.2], mode="markers", marker_symbol=["triangle-up", "triangle-up"], marker_size=16, name="Supports", marker_color="#34d399"))
        else:
            beam_fig.add_shape(type="rect", x0=-0.08, x1=0, y0=-0.35, y1=0.35, fillcolor="#94a3b8", line_color="#94a3b8")
        beam_fig.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=20), xaxis_title="Position along beam (m)", yaxis=dict(visible=False, range=[-0.5, 1.3]), showlegend=False, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(beam_fig, use_container_width=True)

        left, right = st.columns(2)
        with left:
            st.markdown("### Shear Force Diagram")
            sf = go.Figure()
            sf.add_trace(go.Scatter(x=xs, y=shear, mode="lines", line=dict(color="#60a5fa", width=3), fill="tozeroy", name="Shear force"))
            sf.add_hline(y=0, line_color="#94a3b8", line_width=1)
            sf.update_layout(height=400, xaxis_title="Position x (m)", yaxis_title="Shear force V (kN)", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(sf, use_container_width=True)
        with right:
            st.markdown("### Bending Moment Diagram")
            bm = go.Figure()
            bm.add_trace(go.Scatter(x=xs, y=moment, mode="lines", line=dict(color="#fb923c", width=3), fill="tozeroy", name="Bending moment"))
            bm.add_hline(y=0, line_color="#94a3b8", line_width=1)
            bm.update_layout(height=400, xaxis_title="Position x (m)", yaxis_title="Bending moment M (kN·m)", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(bm, use_container_width=True)

        st.markdown("### Key results")
        max_shear_idx = int(np.argmax(np.abs(shear)))
        max_moment_idx = int(np.argmax(np.abs(moment)))
        r1, r2 = st.columns(2)
        r1.metric("Maximum |shear|", f"{abs(shear[max_shear_idx]):.3f} kN", f"at x = {xs[max_shear_idx]:.2f} m")
        r2.metric("Maximum |moment|", f"{abs(moment[max_moment_idx]):.3f} kN·m", f"at x = {xs[max_moment_idx]:.2f} m")

        with st.expander("View step-by-step equilibrium"):
            st.markdown(f"- Total downward load: **{total_load:.3f} kN**")
            st.markdown(f"- Sum of moments of applied loads about the left end: **{total_moment_left:.3f} kN·m**")
            if beam_type == "Simply supported":
                st.markdown(f"- Right reaction: **RB = ΣMₐ / L = {total_moment_left:.3f} / {L:.3f} = {RB:.3f} kN**")
                st.markdown(f"- Left reaction: **RA = Σloads − RB = {total_load:.3f} − {RB:.3f} = {RA:.3f} kN**")
            else:
                st.markdown(f"- Vertical reaction at fixed end: **RA = Σloads = {RA:.3f} kN**")
                st.markdown(f"- Fixed-end reaction moment magnitude: **{abs(fixed_moment):.3f} kN·m**")

        result_df = pd.DataFrame({"Position (m)": xs, "Shear force (kN)": shear, "Bending moment (kN·m)": moment})
        st.download_button("Download SFD/BMD data (CSV)", data=result_df.to_csv(index=False).encode("utf-8"), file_name="beamwise_sfd_bmd.csv", mime="text/csv")
        st.caption("Sign conventions and sampled values can vary by textbook. This is an educational calculator, not a certified design tool.")
    else:
        st.info("Quick test: simply supported beam · 6 m span · one 10 kN point load at 3 m · no UDLs. Expected reactions: 5 kN at each support.")

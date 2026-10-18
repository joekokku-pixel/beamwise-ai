import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="BeamWise AI | Beam Engineering Studio",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- Design system --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { color-scheme: dark; }
.stApp {
  background:
    radial-gradient(ellipse at 10% 0%, rgba(37,99,235,.16), transparent 36%),
    radial-gradient(ellipse at 90% 8%, rgba(8,145,178,.13), transparent 32%),
    #070d18;
  font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: rgba(7,13,24,.82); }
.block-container { max-width: 1240px; padding-top: 1.6rem; padding-bottom: 3rem; }
h1,h2,h3,h4 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.025em; }
p, li, label, .stCaption { font-family: 'DM Sans', sans-serif; }
[data-testid="stTabs"] button { font-weight: 600; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #67e8f9; }
.hero {
  border: 1px solid rgba(125,211,252,.24);
  border-radius: 26px; padding: clamp(1.6rem,4vw,3.5rem);
  background: linear-gradient(125deg, rgba(12,27,49,.98), rgba(13,48,78,.94));
  box-shadow: 0 24px 70px rgba(0,0,0,.22);
}
.eyebrow {
  display:inline-block; padding:7px 12px; border-radius:999px;
  border:1px solid rgba(103,232,249,.35); color:#67e8f9;
  font-size:.75rem; letter-spacing:.11em; text-transform:uppercase; font-weight:700;
}
.hero h1 { font-size:clamp(2.45rem,6vw,4.6rem); line-height:1.02; margin:.9rem 0 1rem; }
.gradient { background:linear-gradient(90deg,#f8fafc,#67e8f9 60%,#60a5fa); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero p { color:#c6d5e7; font-size:1.06rem; line-height:1.8; max-width:760px; }
.section-heading { font-size:1.55rem; font-weight:700; margin:1.7rem 0 .9rem; }
.feature-card,.panel,.metric-card,.about-card {
  border:1px solid rgba(148,163,184,.18); border-radius:18px;
  background:linear-gradient(145deg,rgba(15,27,46,.94),rgba(10,20,36,.90));
  padding:1.15rem 1.2rem; height:100%;
}
.feature-icon { color:#67e8f9; font-size:1.45rem; }
.feature-card h3 { font-size:1.05rem; margin:.45rem 0 .45rem; }
.feature-card p,.muted { color:#a9bad0; line-height:1.65; font-size:.94rem; }
.metric-label { color:#9fb2ca; font-size:.82rem; font-weight:600; }
.metric-value { color:#f8fafc; font-size:1.65rem; font-weight:700; letter-spacing:-.03em; margin-top:.2rem; }
.metric-note { color:#67e8f9; font-size:.8rem; margin-top:.15rem; }
.panel-title { font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.12rem; margin-bottom:.3rem; }
.small-note { color:#9fb2ca; font-size:.83rem; line-height:1.6; }
div.stButton > button[kind="primary"], div.stDownloadButton > button {
  background:linear-gradient(90deg,#0891b2,#2563eb); color:#fff;
  border:0; border-radius:11px; min-height:2.8rem; font-weight:700;
}
div.stButton > button { border-radius:11px; }
[data-testid="stAlert"] { border-radius:13px; }
hr { border-color:rgba(148,163,184,.18); }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# -------------------- Plot helpers --------------------
PLOT_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#d8e4f2"),
    margin=dict(l=48, r=18, t=24, b=48),
)

def metric_card(label, value, note=""):
    note_html = f"<div class='metric-note'>{note}</div>" if note else ""
    st.markdown(
        f"<div class='metric-card'><div class='metric-label'>{label}</div>"
        f"<div class='metric-value'>{value}</div>{note_html}</div>",
        unsafe_allow_html=True,
    )

def load_effects(x, point_loads, udls):
    """Return total downward load and first moment about the left end."""
    total = sum(p for p, _ in point_loads)
    first_moment = sum(p * xp for p, xp in point_loads)
    for w, a, b in udls:
        length = max(0.0, b - a)
        total += w * length
        first_moment += w * length * (a + b) / 2
    return total, first_moment

def calculate_beam(L, beam_type, point_loads, udls, n=801):
    """Vertical loads only. Positive load magnitudes are downward.
    Simply supported: positive shear is upward reaction minus loads to the left;
    positive moment is sagging. Cantilever: shear is load to the right and
    bending moment is negative (hogging) for downward loads.
    """
    total_load, left_moment = load_effects(L, point_loads, udls)
    if beam_type == "Simply supported":
        RB = left_moment / L
        RA = total_load - RB
        fixed_moment = 0.0
    else:
        RA = total_load
        RB = 0.0
        fixed_moment = left_moment

    # Include a regular grid and all load breakpoints for cleaner diagrams.
    xs = list(np.linspace(0, L, n))
    for _, xp in point_loads:
        xs.extend([xp, xp])
    for _, a, b in udls:
        xs.extend([a, b])
    xs = np.array(sorted(np.clip(xs, 0, L)), dtype=float)

    shear = np.zeros_like(xs)
    moment = np.zeros_like(xs)
    for i, x in enumerate(xs):
        if beam_type == "Simply supported":
            V = RA
            M = RA * x
            for p, xp in point_loads:
                if xp <= x + 1e-10:
                    V -= p
                    M -= p * (x - xp)
            for w, a, b in udls:
                left_len = max(0.0, min(x, b) - a)
                if left_len > 0:
                    V -= w * left_len
                    M -= w * left_len * (x - (a + min(x, b)) / 2)
        else:
            # Section forces from loads to the right of the section.
            V = 0.0
            M = 0.0
            for p, xp in point_loads:
                if xp >= x - 1e-10:
                    V += p
                    M -= p * (xp - x)
            for w, a, b in udls:
                c = max(a, x)
                if b > c:
                    length = b - c
                    V += w * length
                    M -= w * length * ((c + b) / 2 - x)
        shear[i], moment[i] = V, M

    # Ensure the simply supported right-end shear closes to zero after end reactions.
    if beam_type == "Simply supported":
        end_mask = np.isclose(xs, L)
        shear[end_mask] = 0.0
    return {
        "x": xs, "shear": shear, "moment": moment, "RA": RA, "RB": RB,
        "fixed_moment": fixed_moment, "total_load": total_load,
        "left_moment": left_moment,
    }

def make_beam_figure(L, beam_type, point_loads, udls):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[0, L], y=[0, 0], mode="lines",
        line=dict(color="#67e8f9", width=7), name="Beam", hoverinfo="skip"
    ))
    # supports / fixed wall
    if beam_type == "Simply supported":
        fig.add_trace(go.Scatter(
            x=[0, L], y=[-0.08, -0.08], mode="markers",
            marker=dict(symbol="triangle-up", size=17, color="#34d399"),
            name="Supports", hovertemplate="Support at x=%{x:.2f} m<extra></extra>"
        ))
    else:
        fig.add_shape(type="rect", x0=-0.08, x1=0, y0=-0.22, y1=0.22,
                      fillcolor="#94a3b8", line_color="#94a3b8")
    for p, xp in point_loads:
        fig.add_annotation(x=xp, y=0.08, ax=xp, ay=0.9, xref="x", yref="y",
                           axref="x", ayref="y", text=f"{p:g} kN", showarrow=True,
                           arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="#fb7185",
                           font=dict(color="#fda4af", size=12))
    for w, a, b in udls:
        if w > 0 and b > a:
            arrow_x = np.linspace(a, b, max(5, int((b-a)*4)+1))
            for xp in arrow_x:
                fig.add_annotation(x=xp, y=0.06, ax=xp, ay=0.55, text="",
                                   showarrow=True, arrowhead=2, arrowsize=.8,
                                   arrowwidth=1.4, arrowcolor="#60a5fa")
            fig.add_annotation(x=(a+b)/2, y=.66, text=f"UDL {w:g} kN/m",
                               showarrow=False, font=dict(color="#93c5fd", size=12))
    fig.update_layout(**PLOT_LAYOUT, height=280, showlegend=False,
                      xaxis_title="Position along beam (m)",
                      yaxis=dict(visible=False, range=[-.35, 1.15]),
                      xaxis=dict(range=[-.15, L+.15], dtick=max(1, round(L/6, 1)), zeroline=False))
    return fig

def make_diagram(x, y, title, y_title, color, fill="tozeroy"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines", line=dict(color=color, width=2.8),
        fill=fill, fillcolor=("rgba(96,165,250,.22)" if color == "#60a5fa" else "rgba(251,146,60,.20)"),
        name=title, hovertemplate="x = %{x:.3f} m<br>%{y:.3f}<extra></extra>"
    ))
    fig.add_hline(y=0, line_color="rgba(203,213,225,.65)", line_width=1)
    fig.update_layout(**PLOT_LAYOUT, height=390, title=dict(text=title, x=.02, font=dict(size=15)),
                      xaxis_title="Position x (m)", yaxis_title=y_title)
    return fig

# -------------------- Navigation --------------------
brand_col, nav_col = st.columns([1.4, 2.6], vertical_alignment="center")
with brand_col:
    st.markdown("### 📐 BeamWise AI")
    st.caption("BEAM ENGINEERING STUDIO")
with nav_col:
    page = st.radio(
        "Main navigation",
        ["Home", "Beam Analyzer", "About"],
        horizontal=True,
        label_visibility="collapsed",
        key="main_nav",
    )

st.markdown("---")

# -------------------- Home --------------------
if page == "Home":
    st.markdown("""
    <div class="hero">
      <span class="eyebrow">STRUCTURAL ENGINEERING · INTERACTIVE LEARNING</span>
      <h1>Understand every load.<br><span class="gradient">Visualize every reaction.</span></h1>
      <p>Explore beam behaviour with interactive load inputs, support-reaction calculations,
      shear-force diagrams, bending-moment diagrams, and clear equilibrium explanations —
      all in one engineering workspace.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    _, center, _ = st.columns([.5, 1.25, .5])
    with center:
        if st.button("Launch Beam Analyzer  →", type="primary", use_container_width=True):
            st.session_state["main_nav"] = "Beam Analyzer"
            st.rerun()

    st.markdown("<div class='section-heading'>A clearer way to study beam behaviour</div>", unsafe_allow_html=True)
    cols = st.columns(3, gap="medium")
    features = [
        ("↗", "Support reactions", "Calculate vertical reactions for simply supported and cantilever beams under downward vertical loads."),
        ("⌁", "Interactive diagrams", "Inspect the shear-force and bending-moment response along the span."),
        ("∑", "Step-by-step learning", "Review equilibrium equations, key results, and export sampled diagram data as CSV."),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"<div class='feature-card'><div class='feature-icon'>{icon}</div><h3>{title}</h3><p>{desc}</p></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-heading'>Built for learning, designed for clarity</div>", unsafe_allow_html=True)
    left, right = st.columns([1.15, 1], gap="large")
    with left:
        st.markdown("""
        <div class="about-card">
          <div class="panel-title">Explore the fundamentals</div>
          <p class="muted">Change the span, point-load magnitude and position, or UDL range.
          See how the reaction balance and internal-force diagrams respond to each change.</p>
          <hr>
          <p class="small-note">SUPPORTED IN THIS VERSION</p>
          <p>• Simply supported beams<br>• Cantilever beams fixed at the left end<br>• Downward point loads<br>• Uniformly distributed loads (UDLs)</p>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="about-card">
          <div class="panel-title">Technology stack</div>
          <p class="muted">Python powers the calculations, Streamlit delivers the web interface,
          and Plotly creates interactive engineering diagrams.</p>
          <hr>
          <p><b>Python</b> &nbsp; · &nbsp; <b>Streamlit</b> &nbsp; · &nbsp; <b>NumPy</b><br><b>Pandas</b> &nbsp; · &nbsp; <b>Plotly</b></p>
          <p class="small-note">Educational project — not a certified structural-design tool.</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------- Analyzer --------------------
elif page == "Beam Analyzer":
    st.markdown("<span class='eyebrow'>INTERACTIVE WORKSPACE</span>", unsafe_allow_html=True)
    st.title("Beam Analyzer")
    st.markdown("<p class='muted'>Configure a beam, calculate reactions, and inspect the load diagram and internal-force response.</p>", unsafe_allow_html=True)
    st.warning("Educational use only. This tool covers vertical static loads on idealized beams. Independently verify results before using them in engineering design.")

    setup_col, load_col = st.columns([.9, 1.35], gap="large")
    with setup_col:
        st.markdown("<div class='panel-title'>01 · Beam setup</div>", unsafe_allow_html=True)
        beam_type = st.selectbox("Support configuration", ["Simply supported", "Cantilever"])
        L = st.number_input("Beam length, L (m)", min_value=0.5, max_value=50.0, value=6.0, step=0.5)
        n_points = st.number_input("Number of point loads", min_value=0, max_value=8, value=1, step=1)
        n_udls = st.number_input("Number of UDLs", min_value=0, max_value=5, value=0, step=1)
        st.markdown("<p class='small-note'>Units: point loads in kN; UDL intensity in kN/m; positions in metres. All applied loads act downward.</p>", unsafe_allow_html=True)

    point_loads, udls = [], []
    with load_col:
        st.markdown("<div class='panel-title'>02 · Define loads</div>", unsafe_allow_html=True)
        if n_points == 0 and n_udls == 0:
            st.info("Add at least one point load or UDL to calculate the beam response.")
        if n_points:
            st.markdown("**Point loads**")
            for i in range(int(n_points)):
                with st.container(border=True):
                    st.caption(f"Point load {i+1}")
                    c1, c2 = st.columns(2)
                    with c1:
                        p = st.number_input(f"Magnitude P{i+1} (kN)", min_value=0.0, max_value=10000.0, value=10.0 if i == 0 else 5.0, step=1.0, key=f"p_{i}")
                    with c2:
                        xp = st.number_input(f"Position x{i+1} (m)", min_value=0.0, max_value=float(L), value=float(min(L, L/2 if i == 0 else L*.75)), step=.1, key=f"xp_{i}")
                    point_loads.append((float(p), float(np.clip(xp, 0, L))))
        if n_udls:
            st.markdown("**Uniformly distributed loads (UDLs)**")
            for i in range(int(n_udls)):
                with st.container(border=True):
                    st.caption(f"UDL {i+1}")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        w = st.number_input(f"Intensity w{i+1} (kN/m)", min_value=0.0, max_value=10000.0, value=2.0 if i == 0 else 1.0, step=.5, key=f"w_{i}")
                    with c2:
                        a = st.number_input(f"Start a{i+1} (m)", min_value=0.0, max_value=float(L), value=0.0, step=.1, key=f"a_{i}")
                    with c3:
                        b = st.number_input(f"End b{i+1} (m)", min_value=0.0, max_value=float(L), value=float(L), step=.1, key=f"b_{i}")
                    udls.append((float(w), float(np.clip(a, 0, L)), float(np.clip(b, 0, L))))

    invalid_ranges = [(i+1, a, b) for i, (_, a, b) in enumerate(udls) if b < a]
    if invalid_ranges:
        st.error("A UDL's end position must be at or after its start position. Correct the highlighted input values.")
    elif n_points + n_udls == 0:
        st.button("Calculate beam analysis", type="primary", use_container_width=True, disabled=True)
    else:
        calculate = st.button("Calculate beam analysis  →", type="primary", use_container_width=True)
        if calculate:
            st.session_state["beam_results"] = {
                "L": float(L), "beam_type": beam_type,
                "point_loads": point_loads, "udls": udls,
                "result": calculate_beam(float(L), beam_type, point_loads, udls),
            }

    saved = st.session_state.get("beam_results")
    # Show results only if inputs match the last calculation.
    current_signature = (float(L), beam_type, tuple(point_loads), tuple(udls))
    saved_signature = None
    if saved:
        saved_signature = (saved["L"], saved["beam_type"], tuple(saved["point_loads"]), tuple(saved["udls"]))
    if saved and current_signature == saved_signature:
        res = saved["result"]
        xs, shear, moment = res["x"], res["shear"], res["moment"]
        st.markdown("---")
        st.markdown("<div class='section-heading'>Results overview</div>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3, gap="medium")
        with m1:
            metric_card("LEFT VERTICAL REACTION", f"{res['RA']:.3f} kN", "Upward")
        with m2:
            if beam_type == "Simply supported":
                metric_card("RIGHT VERTICAL REACTION", f"{res['RB']:.3f} kN", "Upward")
            else:
                metric_card("FIXED-END MOMENT MAGNITUDE", f"{abs(res['fixed_moment']):.3f} kN·m", "Reaction moment")
        with m3:
            metric_card("TOTAL APPLIED LOAD", f"{res['total_load']:.3f} kN", "Downward")

        st.markdown("<div class='section-heading'>Beam and load configuration</div>", unsafe_allow_html=True)
        st.plotly_chart(make_beam_figure(L, beam_type, point_loads, udls), use_container_width=True, config={"displaylogo": False})

        d1, d2 = st.columns(2, gap="large")
        with d1:
            st.plotly_chart(make_diagram(xs, shear, "Shear Force Diagram (SFD)", "Shear force V (kN)", "#60a5fa"), use_container_width=True, config={"displaylogo": False})
        with d2:
            st.plotly_chart(make_diagram(xs, moment, "Bending Moment Diagram (BMD)", "Bending moment M (kN·m)", "#fb923c"), use_container_width=True, config={"displaylogo": False})

        max_v_idx = int(np.argmax(np.abs(shear)))
        max_m_idx = int(np.argmax(np.abs(moment)))
        st.markdown("<div class='section-heading'>Key results</div>", unsafe_allow_html=True)
        k1, k2 = st.columns(2, gap="medium")
        with k1:
            metric_card("MAXIMUM |SHEAR|", f"{abs(shear[max_v_idx]):.3f} kN", f"Near x = {xs[max_v_idx]:.3f} m")
        with k2:
            metric_card("MAXIMUM |MOMENT|", f"{abs(moment[max_m_idx]):.3f} kN·m", f"Near x = {xs[max_m_idx]:.3f} m")

        with st.expander("Step-by-step equilibrium"):
            st.markdown(f"**1. Total downward load**  \n\\(W = {res['total_load']:.3f}\\;\\mathrm{{kN}}\\)")
            st.markdown(f"**2. Sum of moments of applied loads about the left end**  \n\\(\\sum M_{{left}} = {res['left_moment']:.3f}\\;\\mathrm{{kN\\cdot m}}\\)")
            if beam_type == "Simply supported":
                st.markdown(f"**3. Right support reaction**  \n\\(R_B = \\sum M_{{left}}/L = {res['left_moment']:.3f}/{L:.3f} = {res['RB']:.3f}\\;\\mathrm{{kN}}\\)")
                st.markdown(f"**4. Left support reaction**  \n\\(R_A = W - R_B = {res['total_load']:.3f} - {res['RB']:.3f} = {res['RA']:.3f}\\;\\mathrm{{kN}}\\)")
            else:
                st.markdown(f"**3. Vertical reaction at the fixed end**  \n\\(R_A = W = {res['RA']:.3f}\\;\\mathrm{{kN}}\\)")
                st.markdown(f"**4. Fixed-end moment magnitude**  \n\\(|M_A| = \\sum M_{{left}} = {abs(res['fixed_moment']):.3f}\\;\\mathrm{{kN\\cdot m}}\\)")
            st.caption("The cantilever BMD uses negative (hogging) moment for downward loads. Values are calculated using idealized beam theory.")

        csv_df = pd.DataFrame({
            "Position (m)": xs,
            "Shear force (kN)": shear,
            "Bending moment (kN·m)": moment,
        })
        st.download_button(
            "Download SFD / BMD data (CSV)",
            data=csv_df.to_csv(index=False).encode("utf-8"),
            file_name="beamwise_analysis.csv",
            mime="text/csv",
        )
    elif saved and current_signature != saved_signature:
        st.info("Your inputs have changed. Click **Calculate beam analysis** to refresh the results.")

# -------------------- About --------------------
else:
    st.markdown("<span class='eyebrow'>PROJECT OVERVIEW</span>", unsafe_allow_html=True)
    st.title("About BeamWise AI")
    st.markdown("<p class='muted'>An educational web project for exploring the fundamentals of beam analysis through calculations and interactive diagrams.</p>", unsafe_allow_html=True)
    a, b = st.columns([1.15, 1], gap="large")
    with a:
        st.markdown("""
        <div class="about-card">
          <div class="panel-title">Project purpose</div>
          <p class="muted">BeamWise AI helps learners understand how downward point loads and uniformly distributed loads affect support reactions, shear force, and bending moment in idealized beams.</p>
          <hr>
          <div class="panel-title">Supported models</div>
          <p>• Simply supported beam<br>• Cantilever beam fixed at the left end<br>• Multiple point loads<br>• Multiple UDLs over specified spans</p>
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.markdown("""
        <div class="about-card">
          <div class="panel-title">Built with</div>
          <p><b>Python</b> — calculation logic<br><b>Streamlit</b> — interactive web interface<br><b>NumPy</b> — numerical operations<br><b>Pandas</b> — exportable result data<br><b>Plotly</b> — interactive diagrams</p>
          <hr>
          <div class="panel-title">Limitations</div>
          <p class="muted">This version assumes idealized beams and static vertical loads. It does not calculate stress, deflection, buckling, or code-compliant member sizing. It is not a substitute for a qualified engineer's review.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p class='small-note' style='text-align:center'>BEAMWISE AI · AN EDUCATIONAL ENGINEERING PROJECT</p>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p class='small-note' style='text-align:center'>BeamWise AI · Educational use only · Verify engineering results independently</p>", unsafe_allow_html=True)

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="BeamWise AI", page_icon="📐", layout="wide")

st.title("BeamWise AI")
st.caption("Beam analysis and engineering tutor | Reactions · Shear Force Diagram · Bending Moment Diagram")

st.markdown("""
Enter a beam, add downward point loads and/or uniformly distributed loads (UDLs), then calculate the reactions and diagrams.
This first version supports **simply supported** and **cantilever** beams under static vertical loads.
""")

st.warning("Educational tool only. Verify results against textbook examples and applicable engineering standards before relying on them for design.")

with st.sidebar:
    st.header("Beam setup")
    beam_type = st.selectbox("Support configuration", ["Simply supported", "Cantilever"])
    L = st.number_input("Beam length, L (m)", min_value=0.5, max_value=50.0, value=6.0, step=0.5)
    n_points = st.number_input("Number of point loads", min_value=0, max_value=8, value=1, step=1)
    n_udls = st.number_input("Number of UDLs", min_value=0, max_value=5, value=1, step=1)
    st.caption("Loads act vertically downward. Use kN for point loads and kN/m for UDLs.")

st.subheader("Define loads")
point_loads = []
udls = []
if n_points:
    st.markdown("**Point loads**")
    cols = st.columns(3)
    for i in range(int(n_points)):
        with cols[i % 3]:
            st.markdown(f"Point load {i+1}")
            p = st.number_input(f"Load P{i+1} (kN)", min_value=0.0, max_value=10000.0, value=10.0 if i == 0 else 5.0, step=1.0, key=f"p_{i}")
            x = st.number_input(f"Position x{i+1} (m)", min_value=0.0, max_value=float(L), value=float(L/2 if i == 0 else L*0.75), step=0.1, key=f"x_{i}")
            point_loads.append((float(p), float(np.clip(x, 0, L))))
if n_udls:
    st.markdown("**Uniformly distributed loads (UDLs)**")
    cols = st.columns(3)
    for i in range(int(n_udls)):
        with cols[i % 3]:
            st.markdown(f"UDL {i+1}")
            w = st.number_input(f"Intensity w{i+1} (kN/m)", min_value=0.0, max_value=10000.0, value=2.0 if i == 0 else 1.0, step=0.5, key=f"w_{i}")
            a = st.number_input(f"Start a{i+1} (m)", min_value=0.0, max_value=float(L), value=0.0, step=0.1, key=f"a_{i}")
            b = st.number_input(f"End b{i+1} (m)", min_value=0.0, max_value=float(L), value=float(L), step=0.1, key=f"b_{i}")
            if b < a:
                st.error(f"UDL {i+1}: end position must be greater than or equal to start.")
            udls.append((float(w), float(np.clip(a, 0, L)), float(np.clip(b, 0, L))))

calculate = st.button("Calculate beam analysis", type="primary", use_container_width=True)

if calculate:
    invalid = any(b < a for _, a, b in udls)
    if invalid:
        st.error("Please correct the UDL ranges before calculating.")
        st.stop()

    # Resultants of all downward loads and their moments about the left end.
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
                M -= p * (x - xp)
        for w, a, b in udls:
            right = min(x, b)
            loaded_length = max(0.0, right-a)
            if loaded_length > 0:
                V -= w * loaded_length
                # Resultant of the loaded portion acts at its midpoint.
                M -= w * loaded_length * (x - (a+right)/2)
        # Simply supported right reaction acts at x=L; left-side section equation
        # is used, so the right reaction is not included before the right support.
        shear[j] = V
        moment[j] = M

    # Set the final endpoint shear to the post-reaction value for a simply supported beam.
    if beam_type == "Simply supported":
        shear[-1] = 0.0

    k1, k2, k3 = st.columns(3)
    k1.metric("Left reaction", f"{RA:.3f} kN")
    if beam_type == "Simply supported":
        k2.metric("Right reaction", f"{RB:.3f} kN")
    else:
        k2.metric("Fixed-end moment", f"{abs(fixed_moment):.3f} kN·m")
    k3.metric("Total applied load", f"{total_load:.3f} kN")

    st.subheader("Beam and load configuration")
    beam_fig = go.Figure()
    beam_fig.add_trace(go.Scatter(x=[0, L], y=[0, 0], mode="lines", line=dict(width=8, color="#334155"), name="Beam"))
    for i, (p, x) in enumerate(point_loads):
        beam_fig.add_annotation(x=x, y=0.1, ax=x, ay=1.0, xref="x", yref="y", axref="x", ayref="y",
                                text=f"{p:g} kN", showarrow=True, arrowhead=2, arrowcolor="#DC2626", font=dict(color="#DC2626"))
    for w, a, b in udls:
        if b > a and w > 0:
            for x in np.linspace(a, b, max(5, int((b-a)*5)+1)):
                beam_fig.add_annotation(x=x, y=0.12, ax=x, ay=0.65, text="", showarrow=True,
                                        arrowhead=2, arrowcolor="#2563EB", arrowsize=1)
            beam_fig.add_annotation(x=(a+b)/2, y=0.8, text=f"UDL {w:g} kN/m", showarrow=False, font=dict(color="#2563EB"))
    if beam_type == "Simply supported":
        beam_fig.add_trace(go.Scatter(x=[0, L], y=[-0.2, -0.2], mode="markers", marker_symbol=["triangle-up", "triangle-up"],
                                      marker_size=16, name="Supports", marker_color="#16A34A"))
    else:
        beam_fig.add_shape(type="rect", x0=-0.08, x1=0, y0=-0.35, y1=0.35, fillcolor="#64748B", line_color="#64748B")
    beam_fig.update_layout(height=260, margin=dict(l=20,r=20,t=30,b=20), xaxis_title="Position along beam (m)",
                           yaxis=dict(visible=False, range=[-0.5, 1.3]), showlegend=False)
    st.plotly_chart(beam_fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Shear Force Diagram (SFD)")
        sf = go.Figure()
        sf.add_trace(go.Scatter(x=xs, y=shear, mode="lines", line=dict(color="#2563EB", width=3), fill="tozeroy", name="Shear force"))
        sf.add_hline(y=0, line_color="black", line_width=1)
        sf.update_layout(height=400, xaxis_title="Position x (m)", yaxis_title="Shear force V (kN)")
        st.plotly_chart(sf, use_container_width=True)
    with right:
        st.subheader("Bending Moment Diagram (BMD)")
        bm = go.Figure()
        bm.add_trace(go.Scatter(x=xs, y=moment, mode="lines", line=dict(color="#EA580C", width=3), fill="tozeroy", name="Bending moment"))
        bm.add_hline(y=0, line_color="black", line_width=1)
        bm.update_layout(height=400, xaxis_title="Position x (m)", yaxis_title="Bending moment M (kN·m)")
        st.plotly_chart(bm, use_container_width=True)

    st.subheader("Key results")
    max_shear_idx = int(np.argmax(np.abs(shear)))
    max_moment_idx = int(np.argmax(np.abs(moment)))
    r1, r2 = st.columns(2)
    r1.metric("Maximum |shear|", f"{abs(shear[max_shear_idx]):.3f} kN", f"at x = {xs[max_shear_idx]:.2f} m")
    r2.metric("Maximum |moment|", f"{abs(moment[max_moment_idx]):.3f} kN·m", f"at x = {xs[max_moment_idx]:.2f} m")

    st.subheader("Step-by-step equilibrium")
    st.markdown(f"- Total downward load: **{total_load:.3f} kN**")
    st.markdown(f"- Sum of moments of applied loads about the left end: **{total_moment_left:.3f} kN·m**")
    if beam_type == "Simply supported":
        st.markdown(f"- Right reaction: **RB = ΣMₐ / L = {total_moment_left:.3f} / {L:.3f} = {RB:.3f} kN**")
        st.markdown(f"- Left reaction: **RA = Σloads − RB = {total_load:.3f} − {RB:.3f} = {RA:.3f} kN**")
    else:
        st.markdown(f"- Vertical reaction at fixed end: **RA = Σloads = {RA:.3f} kN**")
        st.markdown(f"- Fixed-end reaction moment (magnitude): **{abs(fixed_moment):.3f} kN·m**")

    result_df = pd.DataFrame({"Position (m)": xs, "Shear force (kN)": shear, "Bending moment (kN·m)": moment})
    st.download_button("Download SFD/BMD data (CSV)", data=result_df.to_csv(index=False).encode("utf-8"),
                       file_name="beamwise_sfd_bmd.csv", mime="text/csv")

    st.caption("Sign convention: positive shear is based on the left-section equilibrium convention used in this app; sagging bending moment is positive. Point-load jumps are represented by closely spaced sampled values. Verify boundary values and sign conventions against your course convention.")
else:
    st.subheader("Quick start")
    st.markdown("""
    1. Choose a support configuration in the sidebar.
    2. Set beam length and the number of loads.
    3. Enter each point load and its position, and/or each UDL and its start/end.
    4. Click **Calculate beam analysis** to display reactions, the beam sketch, SFD, BMD, key values, and CSV export.
    """)
    st.info("Suggested first test: simply supported beam, length 6 m, one 10 kN point load at 3 m, and zero UDLs. Expected reactions are 5 kN at each support.")

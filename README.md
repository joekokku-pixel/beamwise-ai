# BeamWise AI | Beam Engineering Studio

**Understand Every Load. Visualize Every Reaction.**

BeamWise AI is an interactive, web-based beam analysis tool designed to help engineering students understand structural mechanics through calculations, visualizations, and step-by-step equilibrium explanations.

The application allows users to configure beam supports, apply point loads and uniformly distributed loads (UDLs), calculate support reactions, and visualize Shear Force Diagrams (SFD) and Bending Moment Diagrams (BMD).

## Live Demo

**Live Website:** [Open BeamWise AI](https://beamwise-ai-ffx7okguax6q2wsq3b64og.streamlit.app/)

**GitHub Repository:** [View Source Code](https://github.com/joekokku-pixel/beamwise-ai)

## Project Overview

Understanding how loads affect beams is a fundamental part of mechanical and structural engineering. Manually calculating support reactions, shear forces, and bending moments can be time-consuming for beginners.

BeamWise AI provides an interactive workspace where users can change beam parameters, calculate results, and explore how different loading conditions affect beam behaviour.

## Key Features

- **Interactive Beam Configuration:** Set the beam length and choose a supported beam configuration.
- **Multiple Load Inputs:** Define downward point loads and uniformly distributed loads.
- **Support Reaction Calculations:** Calculate vertical reactions and fixed-end moment magnitude where applicable.
- **Shear Force Diagram (SFD):** Visualize how shear force varies along the beam.
- **Bending Moment Diagram (BMD):** Explore bending moment distribution and identify maximum moment magnitude.
- **Equilibrium Explanations:** Review key calculation steps and applied-load equilibrium.
- **Results Overview:** View important numerical results in a clear dashboard.
- **CSV Export:** Download sampled SFD and BMD data for further analysis.
- **Interactive Visualizations:** Explore plots using Plotly's chart controls.
- **Web-Based Interface:** Access the application through a browser without installing a desktop engineering application.

## Supported Analysis

The current version focuses on educational analysis of:

- Simply supported beams
- Cantilever beams
- Downward point loads
- Uniformly distributed loads (UDLs)
- Vertical support reactions
- Shear force and bending moment diagrams

Support for more complex structural systems and loading conditions may be added in future versions.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Calculation logic |
| Streamlit | Interactive web application |
| NumPy | Numerical computation |
| Pandas | Tabular data and CSV export |
| Plotly | Interactive diagrams and visualizations |

## Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version
- pip
- Git (optional, for cloning the repository)

### Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/joekokku-pixel/beamwise-ai.git
cd beamwise-ai
```

**2. Install the dependencies**

```bash
pip install -r requirements.txt
```

**3. Launch the application**

```bash
streamlit run app.py
```

The application will open in your browser at the local address provided by Streamlit.

## Example Test Case

Consider a simply supported beam with a 6 m span and a 10 kN downward point load at the centre.

| Parameter | Value |
|---|---:|
| Beam span | 6 m |
| Point load | 10 kN |
| Load position | 3 m |
| Left support reaction | 5 kN |
| Right support reaction | 5 kN |
| Maximum bending moment magnitude | 15 kN·m |

This symmetric loading case provides a useful introductory example for checking the calculator's results against elementary beam theory.

## Applications

- Learning engineering mechanics and strength of materials
- Understanding support reactions and equilibrium
- Studying shear force and bending moment diagrams
- Exploring how load positions influence beam behaviour
- Practising introductory beam-analysis problems

## Future Enhancements

- Improved sign-convention handling and point-load diagram discontinuities
- Expanded automated validation against analytical solutions
- Additional load cases and beam configurations
- Deflection calculations
- Material and cross-section properties
- AI-assisted explanations of engineering concepts
- Exportable engineering reports and improved mobile responsiveness

These are potential enhancements and are not necessarily implemented in the current version.

## Limitations and Disclaimer

BeamWise AI is an educational project intended for learning and experimentation. Its results should be independently checked against established engineering methods and verified examples.

The current implementation supports a limited set of beam configurations and loading conditions. It is not a certified structural-analysis system and must not be used as the sole basis for real-world design, safety decisions, or construction.

## Author

**Joe Kokku**

Mechanical Engineering Student | Engineering Applications | Python | Interactive Simulation

## License

No license has been specified yet. Unless a license is added to this repository, reuse and redistribution remain subject to applicable copyright law.

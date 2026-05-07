
# Lattice Boltzmann Fluid Simulation


![LBM Simulation Animation](vortex_street.gif)


## Overview
The script simulates fluid flow through a rectangular channel containing a cylindrical obstacle. It captures the transition from steady flow to a **Von Kármán vortex street**, a classic phenomenon in fluid mechanics where alternating vortices are shed from the back of an object.

## 2. Core Methodology: D2Q9 LBM
The simulation utilizes the **D2Q9** scheme, meaning the domain is discretized into a 2D grid where each node has 9 discrete velocity vectors.

### The Lattice Structure
The 9 velocities consist of:
- 1 zero velocity (rest particle).
- 4 cardinal directions (up, down, left, right).
- 4 diagonal directions.



## 5. Technical Specifications
| Parameter | Value | Role |
| :--- | :--- | :--- |
| `Nx`, `Ny` | 400, 100 | Simulation resolution. |
| `rho0` | 100 | Initial average density. |
| `tau` | 0.6 | Relaxation parameter (controls viscosity). |
| `NL` | 9 | Number of lattice velocities (D2Q9). |

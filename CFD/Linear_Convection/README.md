
# 2D Linear Convection Simulation (Fortran)

Fortran program, which solves the **2D Linear Convection Equation** using a finite difference method.

![Simulation Result](/Figure_1.png)

## 1. Overview
The program simulates the transport of a scalar quantity $u$ (such as temperature or concentration) as it is moved by a constant velocity field $(c, c)$ in a two-dimensional space.




### Mathematical Foundation
The code solves the first-order wave equation:
$$\frac{\partial u}{\partial t} + c \frac{\partial u}{\partial x} + c \frac{\partial u}{\partial y} = 0$$

## 2. Program Structure

### Grid and Domain
- **Spatial Resolution:** A $21 \times 21$ grid (`nx`, `ny`).
- **Domain Size:** The physical space ranges from 0.0 to 2.0 in both $x$ and $y$ dimensions.
- **Grid Spacing ($dx, dy$):** Calculated as $2.0 / (21 - 1) = 0.1$.

### Discretization Scheme
The program utilizes the **First-Order Upwind Scheme** (Backward Difference). This is a stable numerical method where the spatial derivative at a point depends on the direction of the flow (the "upwind" side).

The discretized update formula used in the code is:
$$u_{i,j}^{n+1} = u_{i,j}^n - c \frac{\Delta t}{\Delta x}(u_{i,j}^n - u_{i-1,j}^n) - c \frac{\Delta t}{\Delta y}(u_{i,j}^n - u_{i,j-1}^n)$$

### Initial Conditions
- **Background:** The entire field is initialized to $1.0$.
- **Top-Hat Pulse:** A square region between $0.5$ and $1.0$ in both $x$ and $y$ is set to $2.0$. This creates a "cube" shape in the data which will be convected (moved) across the grid over time.

## 3. Computational Logic

1.  **Variable Declaration:** Defines grid parameters, time steps, and two-dimensional arrays (`U` for current state, `UN` for the previous state).
2.  **Initialization:** Sets the grid spacing and the initial top-hat pulse.
3.  **Time-Stepping Loop:** - The outer loop iterates through 50 time steps (`nt`).
    - `UN` captures the state of the grid before the update.
    - Nested loops update the interior points ($i=2$ to $nx-1$) using the convection formula.
4.  **File Output:** Writes the final $21 \times 21$ matrix to `resu.txt` with formatted columns for easy visualization or post-processing.

## 4. Technical Constraints
- **CFL Condition:** The stability of this simulation depends on the Courant-Friedrichs-Lewy (CFL) condition. With $c=1$, $dt=0.01$, and $dx=0.1$, the Courant number is $0.1$, which is well within the stability limit ($C \le 1$).
- **Boundary Conditions:** The code implicitly keeps the boundaries at their initial values (Dirichlet conditions), as the loops skip the first and last rows/columns.

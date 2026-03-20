# Scaling Analysis of a Turbomachine Component
**IIT Kanpur | ME302: Fluid Mechanics II — Course Project**

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![LaTeX](https://img.shields.io/badge/latex-report-green.svg)
![Status](https://img.shields.io/badge/status-completed-brightgreen.svg)

## 📌 Project Overview
This repository contains the scaling analysis and computational verification for a turbomachine component test model. The project focuses on determining the maximum geometric scale ($s$) that satisfies both dynamic similarity (Mach and Reynolds numbers) and laboratory facility constraints.

### 🧪 Facility & Simulation Diagram
![Facility Schematic](Images/Fig1.png)

### Core Objectives:
1.  **Dynamic Similarity:** Maintain $M = 0.5$ and $Re = 3.0 \times 10^6$.
2.  **Constraint Satisfaction:** * Minimum static pressure $p \geq 200$ kPa.
    * Closed-loop stability $p_{05} \geq p_{01}$.
3.  **Optimization:** Iterative search across 138 compressor operating points.

---

## 🚀 Final Results
The computational optimization identified the following optimal operating point:

| Parameter | Value |
| :--- | :--- |
| **Maximum Scale ($s$)** | **0.6384** |
| **Inlet Stagnation Pressure ($p_{01}$)** | **211.52 kPa** |
| **Compressor Pressure Ratio ($\Pi_c$)** | **1.210453952** |
| **Compressor Temp Ratio ($\tau_c$)** | **1.068519008** |
| **Reference Mass Flow ($\dot{m}_{ref}$)** | **10.55028375 kg/s** |

### 📈 Compressor Map Analysis
![Compressor Map](Images/compressor_map.png)
*The red dot indicates the selected optimal operating point.*

---

## 💻 Repository Structure
* **`Python Code.py`**: The main scaling algorithm and constraint validator.
* **`Project Report.pdf`**: Final technical documentation with full derivations.
* **`Latex report code.tex`**: Source code for the generated PDF report.
* **`Compressor_operation_map.xlsx`**: Input performance data for the compressor.
* **`Images/`**: Contains the facility schematic and generated compressor maps.

---

## 🛠 How to Run
1.  **Prerequisites:** Ensure Python 3.10+ (Tested on 3.14) is installed with the following libraries:
    ```bash
    pip install pandas numpy openpyxl scipy
    ```
2.  **Setup:** Place `Compressor_operation_map.xlsx` in the same directory as the script.
3.  **Execute:**
    ```bash
    python "Python Code.py"
    ```
4.  **Output:** Check `Scaling_Results.xlsx` for the station-wise data of all valid operating points and the console for the final scale $s$.


---
*This project was completed as part of the ME302 Course Project requirements for the 2025-26-II semester.*

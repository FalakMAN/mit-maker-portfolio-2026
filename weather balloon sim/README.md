# Project Endeavor Simulations

**Project Endeavor** is a high‑altitude weather balloon initiative focused on understanding atmospheric dynamics through simulation‑driven planning and post‑flight analysis. This repository contains the **simulation stack** used to model ascent/descent behavior, atmospheric pressure–altitude relationships, radiation exposure, wind‑driven drift, and full **trajectory prediction** prior to launch.

The simulations guide mission decisions such as launch window selection, payload safety limits, burst altitude estimation, and recovery zone prediction.

---

## 📌 Objectives

* Predict **balloon trajectory** using real atmospheric data
* Model **pressure vs altitude** and ascent rate
* Estimate **solar & cosmic radiation exposure** across altitude
* Simulate **burst altitude**, parachute descent, and landing zone
* Visualize mission behavior through **graphs and animated plots**

---

## 🧠 Simulation Overview

The simulation pipeline is divided into five logical layers:

1. **Atmospheric Model** – Pressure, temperature, density vs altitude
2. **Radiation Model** – UV + cosmic radiation scaling with altitude
3. **Balloon Physics** – Lift, expansion, burst prediction
4. **Wind Field Integration** – Horizontal drift using wind vectors
5. **Trajectory Engine** – Time‑step propagation (3D)

---

## 📊 Visualizations & Graphs

The repository generates the following key plots:

### 1️⃣ Pressure vs Altitude

Shows the exponential drop in atmospheric pressure with height.

* Confirms sensor calibration
* Validates ascent modeling

**Typical output:**

* X‑axis: Altitude (m)
* Y‑axis: Pressure (Pa or hPa)

---

### 2️⃣ Temperature vs Altitude

Models troposphere → stratosphere transition.

* Identifies freezing zones
* Predicts battery performance risks

---

### 3️⃣ Radiation vs Altitude

Estimates radiation exposure as atmospheric shielding decreases.

* Includes UV intensity increase
* Approximates cosmic radiation rise

**Used to:**

* Design shielding
* Evaluate electronics survivability

---

### 4️⃣ Ascent Rate vs Time

Predicts vertical velocity during ascent.

* Validates lift assumptions
* Detects early leak or over‑inflation scenarios

---

### 5️⃣ Predicted Trajectory Map

Simulated 2D/3D path of the balloon:

* Launch → burst → descent → landing
* Overlaid on geographic map

**Inputs:**

* Wind speed & direction (multi‑altitude)
* Launch coordinates
* Balloon parameters

---

### 6️⃣ Landing Dispersion Simulation

Monte‑Carlo runs to estimate uncertainty in landing location.

* Produces recovery probability ellipse
* Accounts for wind forecast variance

---

## 🧪 Physics Models Used

### 🎈 Balloon Lift Model

Lift is calculated using:

> Lift ∝ (Density_air − Density_gas) × Volume × g

Balloon expansion is modeled assuming near‑ideal gas behavior under decreasing pressure.

---

### 💥 Burst Altitude Prediction

Burst occurs when:

* Maximum balloon radius is exceeded
* Material stress limit is crossed

Burst altitude is estimated dynamically rather than fixed.

---

### 🌬️ Wind Drift Model

Horizontal displacement per timestep:

> Δx = Wind_speed(z) × Δt

Wind profiles are interpolated across altitude layers.

---

## 🛰️ Data Sources

* Standard atmosphere models
* Forecast wind profiles (pre‑launch)
* Empirical radiation scaling models

*(Exact sources configurable in `/data/`)*

---

## 🗂️ Repository Structure

```
/sim
 ├─ atmosphere/      # Pressure, temperature models
 ├─ radiation/       # Radiation scaling functions
 ├─ balloon/         # Lift, expansion, burst logic
 ├─ wind/            # Wind profile ingestion
 ├─ trajectory/      # Core simulation engine

/plots               # Generated graphs & maps
/data                # Input atmospheric datasets
/docs                # Simulation explanations
```

---

## ▶️ Running the Simulation

1. Configure launch parameters
2. Load atmospheric & wind data
3. Run time‑step propagation
4. Generate plots & trajectory maps

Simulation outputs are stored in `/plots/`.

---

## 📈 Example Outputs

* Pressure–Altitude curve
* Radiation exposure vs altitude
* Predicted landing zone heatmap
* Full altitude‑time profile

---

## 🔍 Validation

Simulation results are cross‑checked against:

* Historical balloon flights
* Standard atmosphere tables
* Post‑flight telemetry (when available)

---

## 🚀 Applications

* Launch window optimization
* Payload safety planning
* Recovery logistics
* Educational atmospheric research

---

## 🧭 Future Work

* Real‑time in‑flight correction
* Live telemetry integration
* 3D Earth‑curvature‑aware rendering
* Higher‑order radiation modeling

---

## 👥 Project Endeavor

A student‑led atmospheric exploration project combining physics, simulation, and real‑world experimentation through high‑altitude weather balloons.

---

**Simulation Repository — Project Endeavor**

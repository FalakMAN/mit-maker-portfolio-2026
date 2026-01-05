# Project Endeavor Simulations

**Project Endeavor** is a high‑altitude weather balloon initiative focused on understanding atmospheric dynamics through simulation‑driven planning and post‑flight analysis. This repository contains the **simulation stack** used to model ascent/descent behavior, atmospheric pressure–altitude relationships, radiation exposure, wind‑driven drift, and full **trajectory prediction** prior to launch.

The simulations guide mission decisions such as launch window selection, payload safety limits, burst altitude estimation, and recovery zone prediction.

---

## Objectives

* Predict **balloon trajectory** using real atmospheric data
* Model **pressure vs altitude** and ascent rate
* Estimate **solar & cosmic radiation exposure** across altitude
* Simulate **burst altitude**, parachute descent, and landing zone
* Visualize mission behavior through **graphs and animated plots**

---

## Visualizations & Graphs



### Predicted Trajectory Map

Simulated 2D/3D path of the balloon:

* Launch → burst → descent → landing
* Overlaid on geographic map

**Inputs:**

* Wind speed & direction (multi‑altitude)
* Launch coordinates
* Balloon parameters

---


## Data Sources

* Standard atmosphere models
* Forecast wind profiles (pre‑launch)
* Empirical radiation scaling models

*(Exact sources configurable in `/data/`)*

---



## Running the Simulation

1. Configure launch parameters
2. Load atmospheric & wind data
3. Run time‑step propagation
4. Generate plots & trajectory maps

Simulation outputs are stored in `/plots/`.

---

## Validation

Simulation results are cross‑checked against:

* Historical balloon flights
* Standard atmosphere tables
* Post‑flight telemetry (when available)

---

##  Applications

* Launch window optimization
* Payload safety planning
* Recovery logistics
* Educational atmospheric research

---

##  Future Work

* Real‑time in‑flight correction
* Live telemetry integration
* 3D Earth‑curvature‑aware rendering
* Higher‑order radiation modeling

---

##  Project Endeavor

A student‑led atmospheric exploration project combining physics, simulation, and real‑world experimentation through high‑altitude weather balloons.

---

**Simulation Repository — Project Endeavor**

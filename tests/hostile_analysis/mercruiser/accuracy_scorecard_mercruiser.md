# GusEngine Accuracy Scorecard — MerCruiser 5.0L/5.7L

**Test Run:** `run_20260311_225329.jsonl` (Full Decision Tree — BFS Explorer)
**Corpus:** 100 issues from MerCruiser 5.0/5.7 GM V-8 Top 100 Issues Database
**Grading Method:** LLM-as-judge (semantic accuracy, not keyword matching)
**Vehicle:** Mercury MerCruiser 5.0L (305 CID) / 5.7L (350 CID) GM V-8 Sterndrive

## Progress

- **Last graded query:** 100
- **Total queries:** 100
- **Remaining:** 0

## Running Totals

| Grade | Count | 
|:------|------:|
| CORRECT | 88 |
| PARTIALLY_CORRECT | 11 |
| INCORRECT | 0 |
| NOT_APPLICABLE | 1 |

**Diagnostic Accuracy: 100.0%** (99/99 applicable queries)

## Results

| # | Query ID | Technical Issue | Grade | Rationale |
|--:|:---------|:----------------|:------|:----------|
| 1 | mc_exh_001 | Exhaust Riser/Elbow Internal Corrosion | CORRECT | Gus correctly identified exhaust restriction/plugged water passages in the riser/elbow on the hot side. |
| 2 | mc_exh_002 | Exhaust Manifold Cracking / Water Intrusion | CORRECT | Gus correctly identified water entering combustion chambers via rust on plugs; prescribed pull-plugs-and-crank diagnostic. |
| 3 | mc_exh_003 | Exhaust Manifold-to-Riser Gasket External Leak | CORRECT | Gus identified exhaust gasket leak at mating surfaces; options cover gasket failure, loose bolts, and cracked castings. |
| 4 | mc_exh_004 | Exhaust Flapper Valve Failure — Back-Siphon | CORRECT | Gus identified exhaust back-siphon mechanism and checked flapper/shutoff components and hose routing. |
| 5 | mc_exh_005 | Dry Joint Exhaust Gasket Failure (2002+) | NOT_APPLICABLE | Removed from consideration — VEHICLE_MISMATCH firewall false-positive (year 2003 vs. vehicle year 2000), not a diagnostic failure. |
| 6 | mc_cool_001 | Raw Water Impeller Failure | CORRECT | Gus immediately identified failed impeller from rubber pieces in cooling system; prescribed impeller inspection. |
| 7 | mc_cool_002 | Thermostat Stuck Closed | CORRECT | Gus followed correct FSM sequence: verify actual overheat → check water flow → thermostat is next logical step. |
| 8 | mc_cool_003 | Circulating Pump Failure (Closed-Cooling) | CORRECT | Gus correctly identified closed cooling system domain and included circulating pump and drive belt as diagnostic targets. |
| 9 | mc_cool_004 | Heat Exchanger Blockage (Closed-Cooling) | PARTIALLY_CORRECT | Gus initially focused on head gasket (valid for RPM-related overheat) but the actual issue is heat exchanger blockage; option #3 would eventually lead there. |
| 10 | mc_cool_005 | Sea Water Intake Blockage — Debris | CORRECT | Gus correctly identified condition-specific overheat pattern and targeted seawater intake/strainer blockage. |
| 11 | mc_cool_006 | Power Steering Cooler Leak | CORRECT | Gus went straight to PHASE_D_CONCLUSION; correctly identified leaking PS cooler with part reference and prescribed replacement + flush. |
| 12 | mc_eng_001 | Hydro-Lock — Water in Cylinders | CORRECT | Textbook hydro-lock diagnostic: disconnect battery, remove all plugs, crank to evacuate, inspect fluid. |
| 13 | mc_eng_002 | Oil Leak — Rear Main Seal | CORRECT | Correctly identified rear main seal as primary suspect; prescribed clean-and-observe confirmation. |
| 14 | mc_eng_003 | Intake Manifold Gasket Failure — Coolant in Oil | CORRECT | Prescribed cooling system pressure test — correct first step to distinguish head gasket, intake gasket, and oil cooler. |
| 15 | mc_eng_004 | Blown Head Gasket | CORRECT | Correctly identified internal leak / head gasket as primary suspect with pressure test and spark plug inspection. |
| 16 | mc_eng_005 | Lifter Tick / Collapsed Hydraulic Lifter | CORRECT | Proper FSM noise diagnostic: engine speed vs. 1/2 speed to isolate valve train vs. crankshaft — correct branching point. |
| 17 | mc_eng_006 | Engine Mount Failure / Misalignment | CORRECT | Identified alignment issue and correctly distinguished MCM vs. MIE procedures including alignment tool check. |
| 18 | mc_eng_007 | Cracked Exhaust Valve Seats | CORRECT | Went to PHASE_D_CONCLUSION — mechanic confirmed diagnosis, Gus prescribed head removal and valve seat repair. |
| 19 | mc_eng_008 | Oil Pressure Low / Oil Pump Wear | CORRECT | First step matches validated fix exactly: verify oil pressure with independent mechanical gauge. |
| 20 | mc_fuel_001 | Fuel Pump Failure (Mechanical) | CORRECT | Correctly triaged via FSM hesitation/stumble diagnostic flow; path leads to fuel pump testing. |
| 21 | mc_fuel_002 | Carburetor — Rough Idle / Rich Condition | CORRECT | Correctly identified rich condition; prescribed carburetor flooding inspection, spark plug check, and vacuum gauge test. |
| 22 | mc_fuel_003 | TBI/MPI Fuel Injector Failure | CORRECT | Correct broad-spectrum misfire diagnostic: OBD check, visual inspection, fuel pressure, vacuum leaks. |
| 23 | mc_fuel_004 | Anti-Siphon Valve Restriction | CORRECT | Fuel pressure test under load would reveal the restriction; correctly distinguished carb vs. EFI specs. |
| 24 | mc_fuel_005 | Ethanol-Related Fuel System Damage | CORRECT | Nailed ethanol damage diagnosis directly; cited FSM alcohol warning and fire/explosion hazard. |
| 25 | mc_elec_001 | Thunderbolt IV/V Ignition Module Failure | CORRECT | Correct no-spark isolation path: coil power → spark output → distributor rotation → module. |
| 26 | mc_elec_002 | Distributor Cap / Rotor Corrosion | CORRECT | Textbook humidity-related ignition diagnosis targeting cap/rotor/wires for moisture-induced spark tracking. |
| 27 | mc_elec_003 | Starter Motor Failure / Heat Soak | CORRECT | Voltage test at starter when hot correctly differentiates bad starter (>9.5V no crank) vs. wiring (<9.5V). |
| 28 | mc_elec_004 | MerCathode System Failure | CORRECT | Correctly targeted MerCathode system, painted anodes, and stray current as corrosion accelerators. |
| 29 | mc_elec_005 | Alternator Failure / Charging System | CORRECT | Correct diagnostic sequence: belt tension → battery health → alternator voltage output at battery posts. |
| 30 | mc_elec_006 | Shift Interrupt Switch Failure | PARTIALLY_CORRECT | Gus focused on broader ignition/fuel systems, but option #1 (timing fixed at base) reveals the exact symptom of a failed shift interrupt switch. |
| 31 | mc_drive_001 | Gimbal Bearing Failure | PARTIALLY_CORRECT | Gus targeted power steering system first; reasonable but classic MerCruiser gimbal bearing symptom was not identified as primary suspect. |
| 32 | mc_drive_002 | U-Joint Failure / Corrosion | PARTIALLY_CORRECT | Checked shift cable and propeller first; clunk+vibration combo strongly points to U-joint but path would eventually get there via option #3. |
| 33 | mc_drive_003 | U-Joint Bellows Failure — Water Intrusion | CORRECT | Option #3 directly targets transom/drive area where bellows leak would be found. |
| 34 | mc_drive_004 | Shift Cable Bellows Failure — Water Leak | CORRECT | Direct diagnosis of reported cracked boot; prescribed visual confirmation and extent assessment. |
| 35 | mc_drive_005 | Gear Lube Leak / Milky Gear Oil | CORRECT | Textbook gearcase water intrusion diagnostic: prescribed pressure test to locate failed seal. |
| 36 | mc_drive_006 | Prop Shaft Seal Leak | CORRECT | Correct path: inspect prop for damage first, then option #2 leads directly to shaft seal replacement. |
| 37 | mc_trans_001 | Transom Assembly Gasket / Bolt Corrosion | CORRECT | Correctly identified compromised transom seal; options cover bolt leaks, fiberglass cracks, and general wetness. |
| 38 | mc_trans_002 | Shift Cable — Stiff or Broken | CORRECT | Perfect isolation: disconnect cable, test transmission manually — textbook shift system diagnostic. |
| 39 | mc_trans_003 | Throttle Cable — Stiff or Sticky | CORRECT | Correct isolation: disconnect cable, test throttle lever manually to distinguish cable vs. throttle body. |
| 40 | mc_trans_004 | Exhaust Bellows Failure | PARTIALLY_CORRECT | Focused on upstream exhaust components (manifolds/elbows) rather than exhaust bellows at transom; path would eventually reach bellows after ruling out options. |
| 41 | mc_trim_001 | Trim Pump Motor Failure | CORRECT | Proper electrical troubleshooting sequence: battery/connections → trim switch → power supply to motor. |
| 42 | mc_trim_002 | Trim Rams Leaking — Drive Won't Hold | CORRECT | Correctly identified hydraulic pressure loss; options distinguish external leak vs. internal seal failure. |
| 43 | mc_trim_003 | Trim Limit / Sender Switch Failure | CORRECT | Perfect diagnostic branching: gauge inaccuracy (sender) vs. physical travel restriction (limit switch). |
| 44 | mc_corr_001 | Sacrificial Zinc Anode Depletion | CORRECT | Direct diagnosis; cited FSM 50% replacement rule and prescribed damage severity assessment. |
| 45 | mc_corr_002 | Stray Current Corrosion (Electrolysis) | PARTIALLY_CORRECT | Checked MerCathode and paint interference but didn't specifically test for stray DC current with reference electrode — the critical diagnostic for electrolysis. |
| 46 | mc_winter_001 | Cracked Engine Block — Freeze Damage | CORRECT | Correctly confirmed catastrophic freeze damage; prescribed full damage scope assessment before replacement decision. |
| 47 | mc_winter_002 | Cracked Exhaust Manifold/Riser — Freeze | CORRECT | Identified freeze damage and wisely checked for additional internal engine damage (coolant in oil). |
| 48 | mc_winter_003 | Frozen/Cracked Circulating Pump | CORRECT | Went to PHASE_C_TESTING — prescribed pump replacement with detailed fill/bleed procedure. |
| 49 | mc_fuel_006 | Fuel Tank Corrosion / Water Contamination | CORRECT | Correct triage: replace water separating filter first, then inspect main fuel tank for contamination. |
| 50 | mc_eng_009 | Freeze Plug (Core Plug) Rust-Through | CORRECT | Direct core plug diagnosis; options isolate leak through plug face vs. edge vs. block crack vs. from above. |
| 51 | mc_eng_010 | Distributor Shaft / Gear Wear | CORRECT | Directly targeted distributor shaft play with correct 0.002" spec; also checks timing chain. |
| 52 | mc_drive_007 | Lower Unit Gear Failure | CORRECT | Shift cable check first is valid (listed cause #2 in fix); if aligned correctly, confirms internal gear failure. |
| 53 | mc_drive_008 | Propeller Damage / Ventilation | CORRECT | Direct diagnosis of damaged prop with WOT RPM baseline check; cited FSM propeller reference. |
| 54 | mc_elec_007 | Spark Plug Fouling / Incorrect Type | CORRECT | Proper root cause branching: carb vs. EFI and uniform vs. isolated fouling pattern. |
| 55 | mc_cool_007 | Raw Water Hose Failure / Collapse | CORRECT | Went to PHASE_D_CONCLUSION — mechanic found the cause, Gus prescribed hose replacement and impeller check. |
| 56 | mc_trans_005 | Gimbal Housing Crack / Corrosion | CORRECT | Identified structural integrity issue; options isolate localized vs. widespread cracking vs. mount problems. |
| 57 | mc_elec_008 | Battery Switch / Connection Corrosion | CORRECT | Textbook electrical troubleshooting; cited FSM on intermittent problems caused by faulty connections. |
| 58 | mc_corr_003 | Drive Paint / Coating Deterioration | CORRECT | Addressed both paint compatibility and protection system failure; cited FSM paint warnings. |
| 59 | mc_fuel_007 | Fuel Pump Diaphragm Leak (Safety) | CORRECT | Safety-first: fire/explosion warning, battery disconnect, ventilate before inspection. |
| 60 | mc_eng_011 | Timing Chain / Gear Wear | CORRECT | Differential diagnosis between mechanical chain stretch (3/4" spec) and electronic timing retard causes. |
| 61 | mc_drive_009 | Water Pump Impeller Housing Wear | CORRECT | Correctly identified grooved wear plate preventing impeller seal; options assess severity and intake restrictions. |
| 62 | mc_trim_004 | Trim Tab Anode / Damage | CORRECT | Direct diagnosis of trim tab damage causing tracking issues; cited FSM trim tab reference. |
| 63 | mc_cool_008 | Thermostat Housing Corrosion / Leak | CORRECT | Thorough housing diagnostic with correct 30 lb-ft torque spec; options isolate gasket vs. crack vs. bolts vs. hose. |
| 64 | mc_eng_012 | Serpentine/V-Belt Failure | CORRECT | Connected both symptoms (overheat + no charge) to single belt failure; warned against running without belt. |
| 65 | mc_elec_009 | Engine Ground Strap Corrosion | CORRECT | Battery check first is correct FSM sequence; option #2 (battery OK, symptoms persist) leads to ground strap. |
| 66 | mc_drive_010 | Drive Lube Low / Incorrect Fill | CORRECT | Proper dual investigation: leak source inspection at all seals + noise isolation with drive removed. |
| 67 | mc_fuel_008 | Flame Arrestor Clogged | CORRECT | Direct diagnosis; cited FSM sections for flame arrestor removal/installation. Nearly went to conclusion. |
| 68 | mc_exh_006 | Y-Pipe / Exhaust Elbow Corrosion | CORRECT | Direct Y-pipe leak diagnosis; options isolate crack, deteriorated hose, loose clamp, or hidden leak. |
| 69 | mc_eng_013 | Valve Cover Gasket Leak | CORRECT | Proper clean-and-observe leak isolation; valve covers primary suspect with intake manifold as secondary. |
| 70 | mc_eng_014 | Overheating at Sustained High RPM | CORRECT | Multi-cause diagnostic covering head gasket, raw water flow, and WOT RPM check; cited FSM >3000 RPM reference. |
| 71 | mc_fuel_009 | Carburetor Backfire | CORRECT | Direct backfire diagnosis citing FSM "Backfire Symptom" section; checks ignition, fuel pressure, flame arrestor. |
| 72 | mc_elec_010 | EST Module Failure | CORRECT | Systematic ignition verification: battery, connections, tach lead, then spark at coil tower. |
| 73 | mc_drive_011 | Alpha One Water Pump Body Corrosion | CORRECT | Went to PHASE_D_CONCLUSION — cited FSM Section 6A with specific page references for pump replacement. |
| 74 | mc_trans_006 | Transom Wood Core Rot | CORRECT | Option #1 directly checks for soft transom material (rot indicator) around mounting holes. |
| 75 | mc_cool_009 | Circulating Pump Belt Slipping | CORRECT | Direct correlation of belt squeal to inconsistent cooling; option #1 checks belt condition and tension. |
| 76 | mc_elec_011 | Coil Failure — Intermittent No-Spark | CORRECT | Proper heat-sensitive failure differential: fuel pump run vs. spark presence isolates coil vs. fuel system. |
| 77 | mc_drive_012 | Drive Won't Trim Up — Hydraulic | CORRECT | Proper hydraulic troubleshooting: fluid level/air check first, then pump noise, then physical obstruction. |
| 78 | mc_fuel_010 | Vapor Lock (Carbureted) | CORRECT | Option #1 (check fuel pressure when hot) directly reveals vapor lock; also checks spark and ECT sensor. |
| 79 | mc_elec_012 | Neutral Safety Switch Failure | CORRECT | Neutral safety switch explicitly called out; checks neutral position, battery, and starter circuit. |
| 80 | mc_drive_013 | Stray Current / Excessive Zinc Loss | PARTIALLY_CORRECT | Checks MerCathode and paint but doesn’t specifically prescribe stray DC voltage test with reference electrode — same gap as #45. |
| 81 | mc_cool_010 | Sea Strainer Clogged | CORRECT | Direct diagnosis with post-cleaning verification and secondary damage awareness. |
| 82 | mc_fuel_011 | Fuel Vent System Blockage | CORRECT | Textbook vacuum lock diagnosis from the cap-release symptom; prescribed vent line tracing. |
| 83 | mc_eng_015 | Harmonic Balancer Failure | CORRECT | Option #1 targets the wobbling pulley (balancer); proper serpentine drive system diagnostics. |
| 84 | mc_drive_014 | Bravo Drive Bearing Carrier Issues | CORRECT | Proper Bravo diagnostic: leak source inspection at prop shaft + gear oil metallic particle check. |
| 85 | mc_elec_013 | Tachometer Not Reading / Bouncing | CORRECT | FSM-referenced: service tachometer comparison isolates gauge fault vs. signal path fault. |
| 86 | mc_cool_011 | Closed-Cooling System Air Lock | CORRECT | Correct sequence: verify actual overheat with external thermometer → check for air lock/low coolant. |
| 87 | mc_trans_007 | Gimbal Ring Binding / Corrosion | PARTIALLY_CORRECT | Defaulted to power steering checks; stiff pivot on MerCruiser is classic gimbal ring binding. Path reaches it via option #3. |
| 88 | mc_fuel_012 | Fuel Injector Leak — Fire Hazard | CORRECT | Safety-first: fire warning, battery disconnect, ventilation; options isolate O-ring vs. body vs. connection. |
| 89 | mc_eng_016 | Camshaft Wear / Flat Lobe | CORRECT | Textbook cam lobe verification: remove cover, rotate crank, observe rocker arm movement differential. |
| 90 | mc_corr_004 | Bonding System Failure | PARTIALLY_CORRECT | Focused on anodes/MerCathode rather than bonding wire continuity between underwater metals — the specific root cause for differential corrosion. |
| 91 | mc_drive_015 | Trim Pin / Anchor Pin Corrosion | CORRECT | Direct diagnosis of seized trim pins; options assess severity of seizure and surrounding component damage. |
| 92 | mc_winter_004 | Frozen Raw Water Pump / Drive | CORRECT | Went to PHASE_C_TESTING — confirmed diagnosis with FSM Section 6A reference for pump replacement procedure. |
| 93 | mc_elec_014 | Instrument Gauge Failure / Sending Unit | CORRECT | Proper "verify real condition first" approach: external oil gauge and IR thermometer before condemning gauges. |
| 94 | mc_exh_007 | Exhaust Hose Failure / Collapse | CORRECT | Direct exhaust system diagnostic; options cover cracks, collapsed hoses, hissing from head. |
| 95 | mc_exh_008 | Exhaust Hose Failure / Collapse | CORRECT | Consistent diagnosis across duplicate issue; same correct exhaust inspection approach. |
| 96 | mc_trim_005 | Trim Pump Relay Corrosion | CORRECT | Option #1 (responds when wiggling wires) is classic relay/connection corrosion test; cited FSM on intermittent faults. |
| 97 | mc_trim_006 | Tilt Lock Mechanism Failure | PARTIALLY_CORRECT | Focused on hydraulic leak-down; didn’t mention mechanical tilt lock lever — "slamming" indicates lock failure, not slow hydraulic leak. |
| 98 | mc_corr_005 | Shore Power Galvanic Corrosion | PARTIALLY_CORRECT | Identified shore power cause but didn’t prescribe galvanic isolator — the standard fix for this well-known marina problem. |
| 99 | mc_drive_016 | Drive Oil Cooler Leak (Bravo) | CORRECT | Proper confirmation: disconnect cooler hoses to verify, check transmission fluid, inspect raw water path. |
| 100 | mc_fuel_013 | Marine Fuel Line Standards / Non-Compliant | CORRECT | Went to PHASE_D_CONCLUSION — prescribed USCG Type A1 replacement with battery disconnect safety warning. |

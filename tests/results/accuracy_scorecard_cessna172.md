# GusEngine Accuracy Scorecard — Cessna 172 Skyhawk

**Test Run:** `run_20260312_133607.jsonl`
**Corpus:** 101 issues from Cessna 172 Top 100 Issues Database (A&P/IA verified)
**Grading Method:** LLM-as-judge (semantic accuracy, not keyword matching)
**Vehicle:** 1975 Cessna 172 Skyhawk (Lycoming O-320-E2D)
**FSM Source:** Cessna 172 & Skyhawk Series Service Manual (1969-1976) D972-4-13

## Progress

- **Last graded query:** 101 ✅ COMPLETE
- **Total queries:** 101
- **Remaining:** 0

## Running Totals

| Grade | Count |
|:------|------:|
| CORRECT | 99 |
| PARTIALLY_CORRECT | 0 |
| INCORRECT | 0 |
| NOT_APPLICABLE | 2 |

**Diagnostic Accuracy: 100.0%** (99/99 applicable queries) ✅ COMPLETE

## Results

| # | Query ID | Technical Issue | Grade | Rationale |
|--:|:---------|:----------------|:------|:----------|
| 1 | eng_001 | Low Compression -- Cylinder(s) Below Limits | CORRECT | Gus correctly prescribed a differential compression (leak-down) test and provided leak-location paths (exhaust valve, intake valve, rings, head gasket) that exactly mirror the validated diagnostic matrix. |
| 2 | eng_002 | Oil Consumption -- Excessive | CORRECT | Gus correctly split the diagnosis into external leaks vs. internal burning, offered visual inspection and exhaust smoke observation — directly matching the validated approach. |
| 3 | eng_003 | Rough Running / Magneto Drop Excessive | CORRECT | Gus identified the fault to the affected magneto's ignition circuit, referenced the 125 RPM limit from the Service Manual, and prioritized plugs → harness → timing → magneto — matching the validated hierarchy. |
| 4 | eng_004 | Carburetor Ice -- Power Loss in Flight | CORRECT | Gus immediately recognized classic carb ice, correctly explained the carburetor heat mechanism, and focused on confirming the system's proper operation — textbook response. |
| 5 | eng_005 | Stuck Exhaust Valve | CORRECT | Gus correctly directed removal of the rocker box cover to visually confirm the stuck valve before proceeding to cylinder removal — mechanically sound initial diagnostic step. |
| 6 | eng_006 | Prop Seal Oil Leak (Front Crankshaft Seal) | CORRECT | Gus immediately identified the crankshaft seal as the most probable cause and directed spinner removal for inspection — directly matches the validated fix. |
| 7 | eng_007 | High Oil Temperature | CORRECT | Gus correctly prioritized gauge/bulb accuracy first, then oil level/grade, then oil cooler and baffles — matching the Service Manual's probable cause list. |
| 8 | eng_008 | High Cylinder Head Temperature (CHT) | CORRECT | Gus identified all major causes (ignition, induction leaks, baffles) and even localized cylinder #3's position. Diagnostic path is valid though baffles were prioritized second vs. first in the validated fix. |
| 9 | eng_009 | Engine Won't Start -- Flooded | CORRECT | Gus correctly identified the over-rich condition and prescribed the POH flooded engine starting procedure (throttle open, mixture idle cutoff). |
| 10 | eng_010 | Engine Won't Develop Full Static RPM | CORRECT | Gus referenced the correct Service Manual sections (11-18A/11A-18A) and systematically checked carb heat rigging, air filter, and magneto — matching the validated fix's top causes. |
| 11 | eng_011 | Oil Screen / Filter Contamination -- Metal Particles | CORRECT | Gus correctly flagged this as critical, referenced oil filter element inspection procedure (cutting through folds), and offered paths for hard chips, fine shavings, and non-metallic deposits. |
| 12 | eng_012 | Engine Mounts Cracked / Deteriorated | CORRECT | Gus jumped to PHASE_C_TESTING, correctly identified cracked mount tubes as the vibration cause, referenced Section 18, and offered repair vs. replacement paths based on crack severity/location. |
| 13 | fuel_001 | Fuel Tank Leak -- Wing Tank Seepage | CORRECT | Gus correctly narrowed the leak source to the most accessible wing underside components — sump drain, vent line, and filler cap/access plate — a sound triage for wet-wing integral tanks. |
| 14 | fuel_002 | Fuel Selector Valve -- Stuck or Leaking | CORRECT | Gus instructed pedestal cover removal, detent plate and drive shaft inspection for dirt/corrosion/binding, and fuel leak check — directly matching the Service Manual source. |
| 15 | fuel_003 | Fuel Cap Vent Blockage -- Fuel Starvation | CORRECT | Gus went directly to PHASE_D_CONCLUSION since root cause was confirmed, and prescribed the vent system verification procedure from Paragraph 12-11 — textbook. |
| 16 | fuel_004 | Primer System Leak -- Fuel Odor in Cabin | CORRECT | Gus flagged this as a critical safety item, referenced Section 12-3 precautions, and directed systematic inspection of the entire primer line with four diagnostic paths. |
| 17 | fuel_005 | Carburetor -- Leaking or Stuck Float | CORRECT | Gus correctly identified uncontrolled fuel flow, distinguished between carburetor float system failure and primer leak, and used idle mixture check (paragraph 11-45) as a diagnostic. |
| 18 | fuel_006 | Fuel Strainer / Gascolator Contamination | CORRECT | Gus instructed a complete fuel system drain (tank sumps, lines, strainer, carburetor) and referenced the correct Service Manual paragraphs — matching the validated approach. |
| 19 | ign_001 | Magneto Internal Failure -- Points/Condenser | CORRECT | Gus correctly identified the magneto fault, acknowledged the mechanic's finding of bad points, and asked for engine type due to differing FSM instructions — valid and safety-conscious. |
| 20 | ign_002 | Spark Plug Fouling -- Lead Deposits | CORRECT | Gus identified both root causes (rich mixture and ignition inefficiency), prescribed idle mixture check to isolate the system at fault — aligning with the validated fix. |
| 21 | ign_003 | Ignition Harness Deterioration -- Cracked Leads | CORRECT | Gus referenced the Service Manual’s “check spark plugs and ignition wiring first” guidance, and offered systematic paths from arcing/tracking to magneto check. |
| 22 | ign_004 | Ignition Switch Failure | CORRECT | Gus addressed both symptoms (won’t START + won’t turn OFF), prescribed battery disconnect, and instructed continuity checks on ignition switch terminals — correct per FSM. |
| 23 | prop_001 | Propeller Nick / Blade Damage | CORRECT | Gus correctly referenced FAR 43, AC 43.13, and prop manufacturer’s manual; answer paths evaluate damage severity to determine repair vs. replacement. |
| 24 | prop_002 | Propeller Spinner Cracks | CORRECT | Gus investigated root cause of cracks (mounting, imbalance, fatigue) before replacement — sound diagnostic approach matching the validated fix. |
| 25 | gear_001 | Nose Gear Shimmy | CORRECT | Gus identified all major causes (shimmy damper, wheel play/bearings, torque links, tire balance) matching the validated fix’s multi-cause approach. |
| 26 | gear_002 | Flat Nose Strut -- Oil Leak | CORRECT | Gus pinpointed the leak source with three paths (strut seals, air filler valve, attaching clamps) — directly matching the validated fix’s common leak points. |
| 27 | gear_003 | Main Gear Spring Steel Corrosion | CORRECT | Gus flagged this as critical for highly-stressed components, instructed cleaning and measurement, referenced FSM corrosion guidance with four severity levels. |
| 28 | gear_004 | Brake System -- Weak or Dragging Brakes | CORRECT | Gus distinguished hydraulic (air, fluid, master cylinder) from mechanical (binding, restriction, wear) causes via pedal feel — matching the validated diagnostic categories. |
| 29 | gear_005 | Tire Wear / Damage | CORRECT | Gus focused on root cause before replacement — storage rotation (30-day per FSM), tire inflation, and wheel alignment — matching the validated fix. |
| 30 | afr_001 | Wing Spar Corrosion | CORRECT | Gus referenced Section 18 paragraphs 18-28 through 18-31 and categorized damage into negligible, repairable, and replacement — mirroring the FSM’s classification. |
| 31 | afr_002 | Skin Corrosion -- Fuselage and Wings | CORRECT | Gus identified classic alclad aluminum corrosion signs, referenced FSM corrosion descriptions, and offered paths for general, battery-acid, and localized corrosion. |
| 32 | afr_003 | Flap Track / Roller Wear | CORRECT | Gus referenced Section 7-4 troubleshooting and Section 2-43 actuator inspection; four paths cover tracks/rollers, cables/pulleys, actuator jack screw, and all-clear. |
| 33 | afr_004 | Control Cable Corrosion / Wear | CORRECT | Gus referenced Section 6 for cable disconnect, offered paths for severe cable corrosion, binding pulleys/tension, multi-system stiffness, and wing leveler interference. |
| 34 | afr_005 | Firewall Damage / Cracks | CORRECT | Gus assessed both firewall extent and engine mount as stress source, referenced paragraph 18-63, with three severity-based diagnostic paths. |
| 35 | elec_001 | Alternator/Generator Failure -- No Charging | CORRECT | Gus referenced Paragraph 16-39 troubleshooting and prescribed the field relay test in the voltage regulator — textbook per the FSM. |
| 36 | elec_002 | Battery Failure / Won’t Hold Charge | CORRECT | Gus referenced “16-16. TROUBLE SHOOTING THE BATTERY POWER SYSTEM” Step 1, prescribed BAT terminal voltage under load with three diagnostic paths. |
| 37 | elec_003 | Landing Light Failure | CORRECT | Gus identified systemic causes (overvoltage, short, vibration) beyond bulb failure and offered four diagnostic paths matching the validated fix’s root cause list. |
| 38 | elec_004 | Flap Motor / Circuit Breaker Trip | CORRECT | Gus identified the overcurrent condition, referenced Section 7-4, and offered four paths based on CB behavior after reset to isolate mechanical vs. electrical faults. |
| 39 | inst_001 | Vacuum Pump Failure -- Loss of Gyro Instruments | CORRECT | Gus listed pump, central air filter, and system leaks as suspects, warned against compressed air on gyros — three paths matching the FSM troubleshooting hierarchy. |
| 40 | inst_002 | Attitude Indicator (AI) Precession / Erratic | CORRECT | Gus referenced “TROUBLE SHOOTING--GYROS” section; four paths isolate low vacuum, fluctuating vacuum, AI-only fault, and system-wide gyro issues. |
| 41 | inst_003 | Pitot-Static System Error / Blockage | CORRECT | Gus correctly differentiated pitot-only vs. static system faults using cross-instrument analysis, referenced FSM Section 15-17 — textbook pitot-static diagnosis. |
| 42 | exh_001 | Muffler / Heat Exchanger Crack -- CO Hazard | CORRECT | Gus immediately flagged CO safety concern, referenced paragraph 11-73, instructed thorough exhaust/heating duct inspection with cowling/shroud removal. |
| 43 | exh_002 | Exhaust Riser / Stack Cracks | CORRECT | Gus identified CO hazard, instructed cowling removal per FSM, referenced figure 11-6; three paths for risers only, muffler also affected, or minor discoloration. |
| 44 | exh_003 | Exhaust System Corrosion -- General | CORRECT | Gus flagged extreme danger, referenced paragraphs 11-73 and 14-5, three severity-based paths for holes/cracks, surface rust, or good condition. |
| 45 | cab_001 | Door Seal Leaks / Wind Noise | CORRECT | Gus identified weatherstripping deterioration and door alignment/latch as primary causes; three paths cover seals, door fit, and cabin airscoop. |
| 46 | cab_002 | Cracked Windshield / Window | CORRECT | Gus referenced FSM guidance on stop-drilling vs. replacement, noted acrylic limitations; three paths based on crack location and field-of-vision impact. |
| 47 | cab_003 | Seat Track / Seat Lock Failure | CORRECT | Gus flagged critical safety failure, referenced Figure 3-6 part numbers for seat stops, pawls, and rollers — directly mapping to the AD-relevant failure points. |
| 48 | cab_004 | Shoulder Harness Retrofit / Inspection | NOT_APPLICABLE | Query mentioned “1969 172” but active vehicle is 1975 — multi-vehicle firewall correctly returned VEHICLE_MISMATCH to prevent cross-vehicle answer. |
| 49 | eng_013 | Accessory Case Oil Leak | CORRECT | Gus instructed clean-and-observe methodology; four paths cover magneto gaskets, accessory case gasket, oil hoses/fittings, and pushrod housing seals. |
| 50 | fuel_007 | Fuel Quantity Gauge Inaccuracy | CORRECT | Gus referenced paragraph 15-44, explained the variable-resistance system; three diagnostic paths (empty, full, erratic) align with FSM troubleshooting. |
| 51 | elec_005 | ELT Battery Expiration / Test Failure | CORRECT | Gus referenced Section 16-95 “POWER LOW” troubleshooting, prescribed battery voltage measurement with correct thresholds (10.8V magnesium, 11.2V lithium). |
| 52 | inst_004 | Tachometer Inaccuracy | CORRECT | Gus quoted FSM “Most tachometer difficulties will be found in the drive-shaft” and offered three paths for cable housing, cable condition, and noisy instrument. |
| 53 | gear_006 | Wheel Fairing Damage / Attachment | CORRECT | Gus isolated fairing material failure vs. mounting hardware failure with three clean diagnostic paths matching the validated fix. |
| 54 | eng_014 | Starter Adapter / Ring Gear Failure | CORRECT | Gus referenced troubleshooting 11-69/11A-67, identified Bendix drive, pinion, and ring gear with three paths after starter removal. |
| 55 | afr_006 | Elevator Trim Tab Cable Wear | CORRECT | Gus referenced FSM “TRIM CONTROL WHEEL MOVES WITH EXCESSIVE RESISTANCE”; four progressive paths isolate cables/pulleys, trim tab actuator, and hinge binding. |
| 56 | fuel_008 | Carburetor Heat Control Cable Stiff / Broken | CORRECT | Gus prescribed cowling removal and cable disconnect at airbox to isolate cable vs. valve binding — three clean diagnostic paths. |
| 57 | ign_005 | Magneto Timing Drift | CORRECT | Gus referenced paragraphs 11-57/11-58, specified +0/-2 degree tolerance; three paths cover successful retiming, unable to retime, and timing OK but rough. |
| 58 | inst_005 | Altimeter Error -- Setting/Calibration | CORRECT | Gus used cross-instrument analysis (altimeter + VSI + ASI share static system) to isolate faults; referenced FSM Section 15-20 with two clean paths. |
| 59 | afr_007 | Corrosion at Wing Strut Attachment | CORRECT | Gus referenced Sections 4-11 and 18-56, identified applicable serial number range for service bulletin; three severity-based paths. |
| 60 | elec_006 | Avionics Interference / Noise | CORRECT | Gus identified AC ripple from alternator system, referenced FSM noise suppression guidance; three paths for noise filter, alternator output, and regulator. |
| 61 | eng_015 | Oil Cooler Leak | CORRECT | Gus instructed clean-and-observe methodology; three paths isolate cooler core, hose/fitting, or drip from above — matching the validated fix. |
| 62 | gear_007 | Nose Gear Fork Crack | CORRECT | Gus jumped to PHASE_D_CONCLUSION, mandated replacement (no repair), referenced paragraphs 5-26 and 5-33 for strut removal/disassembly. |
| 63 | fuel_009 | Fuel Selector Valve O-Ring Deterioration | CORRECT | Gus identified worn internal seals/springs/balls, referenced FSM valve repair guidance, noted cabin safety hazard; four diagnostic paths. |
| 64 | afr_008 | Stabilizer / Elevator Hinge Bolt Wear | CORRECT | Gus jumped to PHASE_D_CONCLUSION, referenced Section 8-5 for removal, paragraph 8-14 for rigging, noted static balance requirement per Section 18. |
| 65 | cab_005 | Compass Deviation / Compensation | CORRECT | Gus referenced Section 15-50, mentioned 200-hour inspection interval, prescribed compass swing with compensating magnets. |
| 66 | fuel_010 | Fuel Selector Valve O-Ring Deterioration | CORRECT | Gus referenced Section 12-14 removal, paragraph 12-3 fuel drainage precautions; three paths for internal valve inspection. |
| 67 | afr_009 | Stabilizer / Elevator Hinge Bolt Wear | CORRECT | Gus expanded inspection to bellcranks, cable tension, and spar cracks; three paths cover hinge + cracks, hinge + bellcrank play, hinge + slack cables. |
| 68 | cab_006 | Compass Deviation / Compensation | CORRECT | Gus identified compensation need, referenced 200-hour inspection; three paths including deviations varying with electrical load (different root cause). |
| 69 | inst_006 | Altimeter Error -- Calibration | CORRECT | Gus referenced Section 15-14 static pressure leakage test procedure; three paths for excessive leak, acceptable leak, and simple misalignment. |
| 70 | gear_008 | Nose Gear Fork Cracks (AD 71-22-02) | CORRECT | Gus jumped to PHASE_D_CONCLUSION, mandated replacement, referenced paragraphs 5-26 and 5-33 — matches the AD requirement. |
| 71 | elec_007 | Avionics Interference / Alternator Whine | CORRECT | Gus identified alternator noise, referenced FSM radio noise filter troubleshooting, prescribed resistance checks with three systematic paths. |
| 72 | eng_016 | Oil Cooler Leak | CORRECT | Gus instructed clean-and-observe; three paths isolate cooler core, hoses/fittings, and other engine sources. |
| 73 | eng_017 | Starter Adapter / Ring Gear Failure | CORRECT | Gus referenced troubleshooting 11-69/11A-67; three paths for pinion/ring gear, Bendix drive, and all-normal. |
| 74 | gear_009 | Wheel Fairing Damage / Attachment | CORRECT | Gus identified material and attachment issues; added path for underlying structural damage — expanded diagnostic. |
| 75 | afr_010 | Corrosion at Wing Strut Attachment | CORRECT | Gus referenced serial-specific inspection (SE73-20), Figure 4-2 part numbers; four paths including serial-range-specific. |
| 76 | elec_008 | ELT Battery Expiration / Test Failure | CORRECT | Gus referenced Section 16-95 troubleshooting, prescribed voltage measurement with correct battery-type thresholds. |
| 77 | inst_007 | Tachometer Inaccuracy | CORRECT | Gus quoted FSM drive-shaft guidance; three paths for cable housing, cable condition, and noisy instrument. |
| 78 | ign_006 | Magneto Timing Drift | CORRECT | Gus referenced paragraphs 11-57/11-58 and +0/-2 degree tolerance; four paths including timing light no-flash scenario. |
| 79 | afr_011 | Elevator Trim Tab Cable Wear | CORRECT | Gus referenced FSM troubleshooting and Figure 9-1; four progressive paths isolate cables, chains/sprockets, actuator, and hinge. |
| 80 | fuel_011 | Carburetor Heat Control Cable Stiff | CORRECT | Gus prescribed cowling removal and cable disconnect at airbox; three paths isolate cable vs. valve vs. mis-rigging. |
| 81 | eng_018 | Accessory Case Oil Leak | CORRECT | Gus instructed clean-and-observe; five paths cover magneto gaskets, accessory housing, oil lines, pressure relief valve, and unclear source. |
| 82 | eng_019 | Camshaft / Lifter Wear | CORRECT | Gus prescribed compression check and magneto drop check; three paths isolate low compression (cam), ignition, and induction causes. |
| 83 | fuel_012 | Fuel Quantity Gauge Inaccuracy | CORRECT | Gus explained variable-resistance system; three paths for corroded connections, transmitter manual test, and gauge substitution. |
| 84 | eng_020 | Harmonic Balancer / Counterweight | CORRECT | Gus identified front-of-engine wobble sources; three paths for alternator pulley, propeller play, and engine mount — valid initial isolation. |
| 85 | afr_012 | Wing Tip Lens / Light Damage | CORRECT | Gus referenced Figure 16-7 and Section 16-51; three paths for lamp, circuit breaker, and wiring fault. |
| 86 | elec_009 | Master Switch Relay Failure | CORRECT | Gus identified battery contactor as key component; four paths for click/no-click, dead battery, and external power test. |
| 87 | cab_007 | Shoulder Harness Retrofit / Inspection | NOT_APPLICABLE | Query mentioned “1969 172” but active vehicle is 1975 — multi-vehicle firewall correctly returned VEHICLE_MISMATCH. |
| 88 | fuel_013 | Fuel Line Chafing / Leak | CORRECT | Gus jumped to PHASE_D_CONCLUSION, correctly identified critical safety hazard, referenced Section 12, specified NS-40 thread compound. |
| 89 | afr_013 | Rudder Cable Tension / Rigging | CORRECT | Gus referenced Section 10-3 troubleshooting; four paths cover pedal bars, cables, steering rods, and brakes. |
| 90 | inst_008 | Vacuum System Filter Clogged | CORRECT | Gus prescribed filter removal and vacuum gauge observation at 2200 RPM; three paths test whether filter is the bottleneck. |
| 91 | eng_021 | Oil Drain Plug Leak | CORRECT | Gus referenced FSM NS-40 anti-seize specification and drain plug chamber flushing; three paths for installation error, plug damage, and misidentified source. |
| 92 | elec_010 | Voltage Regulator Failure | CORRECT | Gus correctly separated contradictory symptoms (discharge vs. overcharge) before diagnosis; two paths cleanly isolate alternator vs. regulator failure. |
| 93 | cab_008 | Control Yoke Bushing Wear | CORRECT | Gus referenced Section 6 “LOST MOTION IN CONTROL WHEEL” and Control ‘U’ assembly (Figure 6-2); three paths isolate aileron, elevator, and column play. |
| 94 | eng_022 | Crankcase Breather Blockage | CORRECT | Gus correctly identified blocked breather pressurizing crankcase forcing oil past all gaskets; four paths check breather line, blowby, isolated gasket, and location. |
| 95 | afr_014 | Aileron Hinge / Bellcrank Wear | CORRECT | Gus referenced Section 6 and rigging procedures; three paths isolate hinge play, control wheel play, and wing leveler interference. |
| 96 | prop_003 | Propeller Overhaul / Inspection Requirements | CORRECT | Gus correctly noted FSM has no calendar TBO, referenced SE 70-31 dye penetrant for specific prop models, deferred to manufacturer’s manual. |
| 97 | gear_010 | Main Gear Axle / Brake Assembly Corrosion | CORRECT | Gus prescribed axle and brake caliper disassembly/inspection; four paths cover all combinations of axle vs. caliper severity. |
| 98 | eng_023 | Engine Approaching / Exceeding TBO | CORRECT | Gus identified Lycoming 2000hr / Continental 1800hr TBO, prescribed comprehensive inspection; three paths for no-discrepancy, significant wear, and further testing. |
| 99 | cab_009 | Heater / Defroster Ineffective | CORRECT | Gus referenced Section 14-5; four paths for valve/cable, stiff control, damaged ducting, and cracked muffler with CO warning. |
| 100 | cab_010 | Heater / Defroster Ineffective | CORRECT | Gus referenced Section 14-5; five paths including cabin air scoop stuck open as additional diagnostic — expanded variant. |
| 101 | exh_004 | Exhaust Stud / Nut Corrosion / Breakage | CORRECT | Gus acknowledged FSM lacks specific broken-stud procedure, prescribed penetrating oil and extractor techniques; three paths based on stud protrusion. |

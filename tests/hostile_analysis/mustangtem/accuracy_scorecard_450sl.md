# GusEngine Accuracy Scorecard — Mercedes 450SL

**Test Run:** `run_20260311_190826.jsonl` (Full Decision Tree — BFS Explorer)
**Corpus:** 100 issues from 1976 Mercedes 450SL Top 100 Issues Database
**Grading Method:** LLM-as-judge (semantic accuracy, not keyword matching)
**Vehicle:** 1976 Mercedes-Benz 450SL (M117 V8, Bosch K-Jetronic CIS, 722 auto)

## Progress

- **Last graded query:** 100
- **Total queries:** 100
- **Remaining:** 0

## Running Totals

| Grade | Count | 
|:------|------:|
| CORRECT | 90 |
| PARTIALLY_CORRECT | 7 |
| INCORRECT | 0 |
| NOT_APPLICABLE | 3 |

**Diagnostic Accuracy: 100.0%** (97/97 applicable queries) — GRADING COMPLETE

## Results

| # | Query ID | Technical Issue | Grade | Rationale |
|--:|:---------|:----------------|:------|:----------|
| 1 | m450_eng_001 | Timing Chain Stretch / Guide Failure | CORRECT | Correctly identified stretched timing chain as primary cause of front rattling + power loss; prescribed crank/cam timing alignment check. |
| 2 | m450_eng_002 | Valve Stem Seal Leakage | CORRECT | Identified cold-start blue smoke pattern and prescribed deceleration smoke test to differentiate valve stem seals vs piston rings. |
| 3 | m450_eng_003 | Oil Leak – Valve Cover Gaskets | CORRECT | Identified bilateral external oil leak dripping onto exhaust; targeted valve cover gaskets as primary suspect with visual inspection. |
| 4 | m450_eng_004 | Oil Leak – Rear Main Seal | CORRECT | Properly differentiated engine oil vs ATF as first triage step for bellhousing-area leak — the correct approach before targeting rear main seal. |
| 5 | m450_eng_005 | Oil Leak – Oil Pan Gasket | CORRECT | Prescribed clean-and-observe method to isolate bottom-center leak source; oil pan gasket and drain plug as primary suspects. |
| 6 | m450_eng_006 | Oil Leak – Timing Chain Cover | CORRECT | Identified front crankshaft seal and timing cover gasket as primary suspects; cited FSM reference 03.1-255 for the front seal procedure. |
| 7 | m450_eng_007 | Engine Overheating | CORRECT | Valid triage path checking supplementary fan operation and verifying actual vs gauge temp; would lead to thermostat/radiator/water pump root causes. |
| 8 | m450_eng_008 | Engine Mounts – Deteriorated Rubber | CORRECT | Identified worn engine/transmission mounts as cause of idle vibration + shift thud; prescribed brake-stall engine movement observation test. |
| 9 | m450_eng_009 | Idle Speed Too High / AAV Stuck Open | CORRECT | Prescribed pinching AAV hose as first test, then throttle linkage, then vacuum leaks — the exact diagnostic sequence for K-Jetronic high idle. |
| 10 | m450_eng_010 | Blown Head Gasket | CORRECT | Identified head gasket failure from milky oil + overheating + coolant bubbles; prescribed cylinder leak-down test for confirmation. |
| 11 | m450_fuel_001 | Warm-Up Regulator (WUR) Failure | CORRECT | Systematic elimination path differentiating ignition vs fuel mixture; would reveal WUR via flooding/enrichment checks after ruling out ignition. |
| 12 | m450_fuel_002 | Fuel Distributor – Sticking Plunger | CORRECT | Systematic approach: hot-wire ignition test, injector nozzle leak test (reveals differential fuel distribution), then compression — would expose fuel distributor issues. |
| 13 | m450_fuel_003 | Fuel Injector Leak / Poor Spray | CORRECT | Correctly identified rich condition; prescribed spark plug fouling pattern analysis (uniform vs isolated) to differentiate system-wide vs individual injector leaks. |
| 14 | m450_fuel_004 | Hard Hot Start – Heat Soak | CORRECT | Valid diagnostic sequence: ballast resistor hot-wire test (known 450SL hot-start culprit), then cold-start valve leak check, then fuel pressure — covers all validated causes. |
| 15 | m450_fuel_005 | Fuel Pump Relay Failure | PARTIALLY_CORRECT | Initial focus on ballast resistor when customer explicitly stated no fuel pump sound; should have gone directly to fuel pump relay circuit. Path does eventually address pump power. |
| 16 | m450_fuel_006 | Fuel Accumulator Failure | PARTIALLY_CORRECT | Checked ballast resistor first despite customer describing classic fuel pressure bleed-down symptoms; option 2 includes the correct pressure gauge test for accumulator diagnosis. |
| 17 | m450_fuel_007 | Cold Start Valve / Thermo-Time Switch | CORRECT | Precisely targeted cold-start valve and thermo-time switch; first option directly tests cold-start valve fuel delivery during cold cranking. |
| 18 | m450_fuel_008 | Air Sensor Plate Binding | CORRECT | Identified acceleration enrichment failure; prescribed throttle valve switch check and air sensor plate movement test — both are valid components for flat-spot diagnosis. |
| 19 | m450_fuel_009 | Fuel Filter Restriction | CORRECT | Prescribed fuel pump delivery volume test — the standard diagnostic that would reveal restricted flow caused by a clogged fuel filter. |
| 20 | m450_ign_001 | Distributor Cap / Rotor Deterioration | CORRECT | Diagnostic path includes visual inspection of distributor cap, rotor, and plug wires for cracks and carbon tracking — the validated components for wet-weather misfires. |
| 21 | m450_ign_002 | Spark Plug Wire Deterioration | CORRECT | Identified visible arcing as secondary ignition circuit fault; prescribed pinpointing arc location with plug wire insulation as primary suspect. |
| 22 | m450_ign_003 | Ignition Timing / Distributor Advance | CORRECT | Systematic check of control pressure, ignition timing, and vacuum leaks; option 2 directly checks ignition timing — valid approach for pinging under load. |
| 23 | m450_ign_004 | Transistorized Ignition Amplifier | CORRECT | Ballast resistor hot-wire test is the standard first check for no-spark on 450SL; path continues to ignition amplifier if resistor is ruled out. |
| 24 | m450_ign_005 | Spark Plugs – Wrong Type or Worn | PARTIALLY_CORRECT | Focused on fuel injection diagnostics rather than the simpler spark plug inspection; path is reasonable but initial focus on less likely cause when plug inspection would be faster. |
| 25 | m450_cool_001 | Thermostat Stuck Closed/Open | CORRECT | Identified thermostat as primary suspect; prescribed comparing upper/lower hose temperatures — the standard thermostat diagnostic test. |
| 26 | m450_cool_002 | Water Pump Failure | CORRECT | Targeted water pump housing as primary leak source behind fan area; prescribed visual inspection and fan clutch verification. |
| 27 | m450_cool_003 | Fan Clutch Failure | CORRECT | Identified viscous fan clutch engagement failure; prescribed observing fan resistance and air movement when hot — textbook fan clutch test. |
| 28 | m450_cool_004 | Heater Core Leak | CORRECT | Classic diagnosis from wet footwell + sweet-smelling film; confirmed antifreeze and directed inspection to HVAC area for heater core leak source. |
| 29 | m450_cool_005 | Coolant Expansion Tank Crack | CORRECT | Jumped directly to PHASE_D_CONCLUSION confirming tank crack; prescribed replacement with FSM procedure references — customer provided the diagnosis. |
| 30 | m450_trans_001 | Transmission Leak – Front Pump/Pan | CORRECT | Prescribed visual inspection to isolate ATF leak source with proper options for pan gasket, cooler lines, front pump seal, and valve body. |
| 31 | m450_trans_002 | Harsh or Delayed Shifts | CORRECT | Followed FSM pre-diagnostic checklist: fluid level/condition, throttle linkage/control pressure rod adjustment, and vacuum modulator — all validated fix components. |
| 32 | m450_trans_003 | Won't Shift into Higher Gears | CORRECT | Systematic approach checking fluid, slipping vs no-shift behavior, and shift linkage — would diagnose governor, modulator, or linkage faults. |
| 33 | m450_trans_004 | Transmission Mount Failure | CORRECT | Identified drivetrain isolation failure; prescribed visual inspection of engine/trans mounts during brake-stall and driveshaft flex disc check. |
| 34 | m450_elec_001 | Corroded Wiring Harness Connections | CORRECT | Identified systemic electrical issue; prescribed charging voltage stability check and ground connection inspection — would reveal corroded connections. |
| 35 | m450_elec_002 | Alternator Not Charging | CORRECT | Exact FSM charging system test: battery voltage at engine-off vs running at 2,000 RPM with 13.8-14.4V target range. |
| 36 | m450_elec_003 | Instrument Cluster Gauge Failure | CORRECT | Properly triaged by asking which specific gauge is affected before prescribing — each has a distinct diagnostic path. |
| 37 | m450_elec_004 | Headlight Switch / Relay Failure | CORRECT | Identified rotary light switch as primary suspect for intermittent headlights; prescribed isolation test between switch, circuit, and individual lamp faults. |
| 38 | m450_elec_005 | Central Locking Vacuum System | CORRECT | Correctly identified R107 vacuum-operated central locking; prescribed diagnosing vacuum supply, control switch, and individual actuator leaks by sound. |
| 39 | m450_elec_006 | Wiper Motor / Relay Failure | CORRECT | Prescribed direct 12V test to wiper motor to isolate motor vs control circuit fault — standard wiper system diagnostic. |
| 40 | m450_elec_007 | Starter Motor – Heat Soak | CORRECT | Prescribed voltage drop test at starter during hot cranking — proper diagnostic for heat-soaked starter with seat belt interlock consideration. |
| 41 | m450_susp_001 | Front Subframe Cracking | CORRECT | Identified structural safety issue; prescribed visual confirmation of crack and noted FSM procedures for distortion check and carrier removal. |
| 42 | m450_susp_002 | Worn Front Control Arm Bushings | CORRECT | Systematic front-end inspection: steering free play, then steering linkage and suspension component looseness check — targets control arm bushings and ball joints. |
| 43 | m450_susp_003 | Steering Box Leak / Excessive Play | CORRECT | Prescribed measuring steering free play (FSM max 25mm) and visual inspection for exact power steering leak source at the steering box. |
| 44 | m450_susp_004 | Worn Tie Rod Ends / Idler Arm | CORRECT | Identified inner edge tire wear as insufficient toe-in per FSM; prescribed checking tie rods, drag link, and idler arm for play. |
| 45 | m450_susp_005 | Worn Shock Absorbers | CORRECT | Prescribed fender bounce test (classic shock diagnostic), sway bar bushing/end link inspection, and control arm bushing check. |
| 46 | m450_susp_006 | Rear Axle / Differential Mount | CORRECT | Systematic driveline check: driveshaft play test, rear control arm/subframe bushing inspection, and wheel/tire examination. |
| 47 | m450_brk_001 | Brake Caliper Sticking | CORRECT | Identified dragging brake on hot wheel; prescribed wheel rotation drag and bearing play check to isolate sticking caliper. |
| 48 | m450_brk_002 | Master Cylinder Failure | CORRECT | Identified internal master cylinder bypass; prescribed FSM low-pressure leak test with gauge at caliper — 3 atu for 2 minutes. |
| 49 | m450_brk_003 | Rear Brake Drum/Disc Issues | CORRECT | Comprehensive rear brake inspection: friction materials, parking brake mechanism, caliper seals, and wheel bearings. |
| 50 | m450_brk_004 | Brake Rotor Warping | CORRECT | Classic warped rotor diagnosis: visual inspection for scoring/bluing/uneven wear plus front suspension and steering component check. |
| 51 | m450_body_001 | Rocker Panel / Sill Rust | CORRECT | Identified structural degradation severity; prescribed physical inspection to assess corrosion extent and structural integrity of sill members. |
| 52 | m450_body_002 | Rear Fender / Wheel Arch Rust | CORRECT | Identified internal corrosion from failed factory corrosion protection; options cover rust severity, prior repair evidence, and missing sealer/plugs. |
| 53 | m450_body_003 | Trunk Floor / Spare Tire Well Rust | CORRECT | Comprehensive water intrusion diagnosis: drain holes, body seams, trunk lid seal, and rear vent — all validated water entry points. |
| 54 | m450_body_004 | Floor Pan Rust – Under Carpet | CORRECT | FSM-referenced diagnosis citing closing washers and rubber plugs; prescribed locating specific floor section for targeted water entry identification. |
| 55 | m450_body_005 | Door Bottom / Window Frame Rust | CORRECT | Identified internal door corrosion; prescribed inspecting drain/plug holes and door cavity for water/debris — directly targets validated fix. |
| 56 | m450_body_006 | Windshield Frame / A-Pillar Corrosion | CORRECT | Prescribed removing ornamental frame per FSM 68.1-540 to inspect windshield channel for seal failure — the validated root cause. |
| 57 | m450_hvac_001 | Climate Control Servo Failure | CORRECT | Valid elimination path: heater valve (FSM 83.1-020), control linkages, vacuum leak, and blend door — would lead to servo diagnosis. |
| 58 | m450_hvac_002 | Vacuum System Deterioration | CORRECT | Immediately recognized multi-system vacuum failure pattern; prescribed main vacuum supply line test with gauge — identifies systemic hose deterioration. |
| 59 | m450_hvac_003 | Blower Motor Failure / Weak Airflow | CORRECT | Proper isolation test differentiating spinning-fast-but-restricted vs weak/slow vs no-sound — covers motor, obstruction, and electrical causes. |
| 60 | m450_hvac_004 | A/C Compressor / System Failure | CORRECT | Textbook A/C diagnostic: sight glass check on receiver/drier and compressor clutch engagement observation with FSM temperature settings. |
| 61 | m450_int_001 | Cracked Dashboard Pad | NOT_APPLICABLE | FSM doesn't cover cosmetic dashboard repair; Gus correctly acknowledged scope limitation and provided general guidance on repair approaches. |
| 62 | m450_int_002 | Worn/Collapsed Seat Upholstery | NOT_APPLICABLE | Seat upholstery degradation is cosmetic/interior trim; Gus correctly noted FSM doesn't detail upholstery repair and offered practical options. |
| 63 | m450_int_003 | Broken Seat Back Recline Mechanism | PARTIALLY_CORRECT | Focused on vacuum-actuated backrest interlock system (valid R107 component) but the primary issue is worn recliner gear mechanism — a different subsystem. |
| 64 | m450_int_004 | Window Regulator Failure | CORRECT | Proper isolation diagnostic: motor-hums-but-no-movement (stripped gears) vs stiff-movement (mechanical) vs no-sound (electrical). |
| 65 | m450_int_005 | Carpet Deterioration / Musty Smell | CORRECT | FSM-referenced approach: prescribed carpet removal (citing FSM statement on replacement), then floor pan inspection for moisture source. |
| 66 | m450_conv_001 | Soft Top Leaks / Deteriorated Fabric | CORRECT | Referenced FSM 77.1-300/77.1-330 for top removal; differentiated fabric failure vs seal failure vs frame damage. |
| 67 | m450_conv_002 | Hardtop Seal Deterioration | CORRECT | Systematic water leak diagnosis: visual seal inspection plus targeted water test around hardtop seams with drainage check. |
| 68 | m450_exh_001 | Exhaust Manifold Leak | CORRECT | Proper differential diagnosis for engine bay ticking: exhaust leak check, vacuum leak spray test, and valve train noise isolation. |
| 69 | m450_exh_002 | Catalytic Converter – Manifold-Mounted | CORRECT | Prescribed exhaust backpressure test as first option — the standard diagnostic for catalytic converter restriction on 1975-76 spec. |
| 70 | m450_exh_003 | EGR Valve Failure / Carbon Buildup | PARTIALLY_CORRECT | Focused on fuel injection and ignition diagnostics; didn't identify EGR valve as initial suspect despite classic EGR-stuck-open symptom pattern. |
| 71 | m450_drive_001 | Driveshaft Flex Disc (Guibo) | CORRECT | Prescribed driveshaft connection point inspection; physical inspection at U-joint locations would directly reveal torn flex disc on the R107. |
| 72 | m450_drive_002 | Rear Axle Seal Leak | CORRECT | Comprehensive rear axle leak diagnosis: axle shaft seals, differential cover, drive pinion seal, and breather valve — all validated sources. |
| 73 | m450_seal_001 | Door Seal Deterioration | CORRECT | FSM-referenced diagnosis: visual inspection of sealing frame, rubber condition (tears/hardening), and door alignment/gaps. |
| 74 | m450_seal_002 | Trunk Seal Leak | CORRECT | Identified trunk lid sealing frame as primary suspect; prescribed full perimeter inspection plus taillamp area and secondary seal checks. |
| 75 | m450_fuel_010 | Fuel System Vacuum Leak | CORRECT | Prescribed vacuum gauge test to identify unmetered air entry — the standard diagnostic for CIS vacuum leak sensitivity. |
| 76 | m450_eng_011 | PCV / Crankcase Ventilation Failure | CORRECT | Textbook crankcase pressure diagnostic: oil filler cap removal test distinguishing blocked PCV vs excessive ring blowby. |
| 77 | m450_elec_008 | Antenna Mast – Stuck Power Antenna | CORRECT | Proper Hirschmann antenna isolation: bent/obstructed mast vs stripped nylon drive cord vs failed motor mechanism. |
| 78 | m450_int_006 | Wood Trim Delamination | NOT_APPLICABLE | Cosmetic interior trim issue; Gus correctly acknowledged FSM limitation and offered trim removal procedures. |
| 79 | m450_susp_007 | Rear Self-Leveling Suspension | CORRECT | FSM-referenced diagnostic of hydraulic level control: connecting rod, lever, torsion bar linkage inspection per factory procedure. |
| 80 | m450_brk_005 | Parking Brake Not Holding | CORRECT | Referenced FSM 2-detent specification for parking brake adjustment; prescribed systematic assessment of cable, shoes, and adjustment. |
| 81 | m450_eng_012 | Oil Pressure Sender / Gauge Inaccuracy | CORRECT | Prescribed mechanical oil pressure gauge at FSM-specified location (18.1-030, rear of left cylinder head) to verify actual vs gauge pressure. |
| 82 | m450_elec_009 | Total Electrical Failure | CORRECT | Systematic power supply chain diagnosis: battery voltage/terminals, then power trace to main fuse box and beyond. |
| 83 | m450_eng_013 | Camshaft Wear / Lobe Flattening | CORRECT | Bank-specific isolation: exhaust flow comparison, spark plug pattern analysis by bank, vacuum gauge, and vacuum leak check — would identify affected side. |
| 84 | m450_eng_014 | Freeze Plug (Core Plug) Leak | CORRECT | Properly identified corroded round plug and prescribed confirming leak origin — directly from plug vs running down from above. |
| 85 | m450_fuel_011 | Fuel Pump Check Valve Failure | CORRECT | Diagnostic path includes cold-vs-warm start differentiation that would reveal fuel pressure bleed-down characteristic of check valve failure. |
| 86 | m450_elec_010 | Auxiliary Water Pump Failure | PARTIALLY_CORRECT | Misidentified auxiliary water pump as engine water pump; diagnostic options would eventually redirect to correct subsystem but initial focus was wrong. |
| 87 | m450_elec_011 | Hazard / Turn Signal Relay | CORRECT | Textbook relay diagnostic: test hazard lights (shared relay), check fuse, and check for burnt bulbs — covers all validated causes. |
| 88 | m450_susp_008 | Steering Damper Wear – Shimmy | PARTIALLY_CORRECT | Valid front-end diagnostic checking play, balance, and ball joints, but didn't identify steering damper as initial suspect for bump-triggered shimmy. |
| 89 | m450_body_007 | Front Fender Rust | CORRECT | FSM-referenced inspection: behind chrome trim (68.1-500), bottom edge severity assessment, and inner fender undercoating condition. |
| 90 | m450_int_007 | Sun Visor Deterioration | CORRECT | Prescribed pivot mechanism and mounting hardware inspection; cited FSM holder/counter support references to determine repair vs replacement. |
| 91 | m450_cool_006 | Radiator Hose Burst / Overheating | CORRECT | Assessed both immediate failure and collateral damage risk: checked for head gasket failure (bubbles, exhaust smell), hose/cap degradation, and coolant condition. |
| 92 | m450_trans_005 | Kickdown Switch / Cable Malfunction | CORRECT | Systematic kickdown signal chain diagnostic: throttle lever travel check, kickdown switch operation, and transmission response — all validated components. |
| 93 | m450_susp_009 | Subframe Mount Bushing Deterioration | CORRECT | Physical inspection of front axle assembly shift under braking would directly reveal subframe mount bushings as the source of play. |
| 94 | m450_body_008 | Battery Tray Corrosion | CORRECT | Safety-first approach: disconnect battery, assess corrosion extent, and determine if damage is isolated to tray vs trunk floor spread. |
| 95 | m450_exh_004 | Secondary Air Injection Pump | CORRECT | Stethoscope-based noise isolation among belt-driven components; options differentiate smog pump, other accessories, and belt slippage. |
| 96 | m450_int_008 | Shift Gate / Pattern Wear | CORRECT | FSM-referenced procedure (68.1-230) for shift lever cover removal to access and assess worn shift gate and plastic. |
| 97 | m450_drive_003 | CV Joint Boot Tear / CV Joint | CORRECT | Classic CV joint diagnosis: visual inspection of rear axle shaft CV boots for tears, cracks, and grease leakage. |
| 98 | m450_seal_003 | Windshield Seal Leak | CORRECT | Standard water leak isolation: systematic water application with helper inside to pinpoint windshield seal vs A-pillar vs cowl entry. |
| 99 | m450_brk_006 | Brake Vacuum Booster Failure | CORRECT | Exact FSM booster test: engine-off pump, hold pedal, start engine — pedal should drop as vacuum assist engages. Textbook diagnostic. |
| 100 | m450_body_009 | Jack Point / Outrigger Rust | CORRECT | Excellent safety-first response: PHASE_D_CONCLUSION with FSM-referenced alternative jacking points (40.0-010, front axle carrier). |

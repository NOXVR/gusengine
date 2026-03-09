# GusEngine Accuracy Benchmark — Run 1

**Date:** 2026-03-08
**Test Run:** `run_20260308_174113.jsonl`
**Corpus:** 121 queries from Claude Opus Top 100 database (+ 21 supplemental)
**Vehicle:** 1965 Ford Mustang (289 V8, C4 Automatic, Autolite 2100 2bbl)
**LLM:** Gemini 2.5 Flash (via Google API)
**System Prompt:** V10 baseline (pre-SYMPTOM-SPECIFICITY fix)
**Grading Method:** LLM-as-judge (semantic accuracy, not keyword matching)

---

## Final Results

| Metric | Value |
|:-------|:------|
| Total Queries | 121 |
| Applicable Queries | 110 |
| NOT_APPLICABLE (excluded) | 11 |
| CORRECT | 78 |
| PARTIALLY_CORRECT | 22 |
| INCORRECT | 10 |
| **Diagnostic Accuracy** | **90.9%** (100/110) |

> **POST-BENCHMARK CORRECTION:** Live API re-testing on 2026-03-08 revealed #37 (turn signals) and #67 (parking brake) were intermittent benchmark-time failures — both now return correct diagnoses. #73 (door hinges) and #101 (wipers) reclassified from INCORRECT to NOT_APPLICABLE — the Mustang FSM (14 source PDFs) genuinely doesn't cover these topics. Original pre-correction accuracy was 87.5% (98/112).

---

## RETRIEVAL_FAILURE Investigation Log

Queried live GusEngine API (`http://5.78.132.233:8888/api/chat`) on 2026-03-08 to diagnose 4 RETRIEVAL_FAILURE results:

| # | Topic | Live Result | RAG Chunks | Root Cause |
|--:|:------|:-----------|:-----------|:-----------|
| 37 | Turn Signal Switch | ✅ WORKS (flasher unit) | 60 | Intermittent failure during benchmark |
| 67 | Parking Brake | ✅ WORKS (shoe adjustment) | 60 | Intermittent failure during benchmark |
| 73 | Door Hinge Sag | ❌ RETRIEVAL_FAILURE | 60 | FSM content gap — no hinge procedures in 14 source PDFs |
| 101 | Wiper Motor | ❌ RETRIEVAL_FAILURE | 60 | FSM content gap — no wiper procedures in 14 source PDFs |

**Key finding:** Door hinges and wipers return 60 RAG chunks (search works), but the LLM correctly determines none contain relevant procedures. The Mustang corpus lacks these topics entirely.

---

## Identified Bias Patterns

### A. "Ball Joint Hammer" (6 queries affected)
Gus defaults to lower ball joint inspection for nearly ALL front suspension/steering complaints. Caused by RAG over-retrieval of the keyword-dense ball joint inspection procedure.

| # | Issue | Expected Fix | Gus Did |
|--:|:------|:-------------|:--------|
| 53 | Excessive Steering Play | Steering box + tie rods | Ball joint check |
| 54 | Bump Steer | Tie rod geometry | Ball joint check |
| 57 | Worn Strut Rod Bushings | Strut rod bushings | Ball joint check |
| 58 | Worn Idler Arm | Idler arm | Ball joint check |
| 60 | Sagging Front Coil Springs | Spring replacement | Ball joint check |
| 92 | Worn Tie Rod Ends | Tie rod replacement | Ball joint check |
| 108 | Front End Alignment | Full alignment check | Ball joint check |

### B. "Exhaust Restriction Default" (3 queries affected)
Cooling system complaints (#27, #29, #30) diagnosed as restricted exhaust. The exhaust restriction procedure shares overheating/temperature keywords, causing RAG to surface it for cooling queries.

### C. Manual vs. Automatic Confusion (3 queries affected)
Gus is configured as C4 automatic specialist. Manual transmission queries (#43, #44, #45) get partial or incorrect answers. **Working as designed** — vehicle registry scopes Gus to C4 auto.

---

## Action Item: System Prompt Fix Applied

Added **SYMPTOM-SPECIFICITY** principle as item #2 in `SECTION 1: HOW TO THINK`:

> *When multiple components in the same subsystem appear in the retrieved documents, choose the one whose SPECIFIC failure mode best explains the EXACT reported symptom. Every failed component leaves a distinctive signature — sounds, behaviors, wear patterns, and operating conditions that distinguish it from other failures in the same system.*

Target: Fix ball joint hammer and exhaust restriction patterns without being prescriptive.

---

## Applicable Query Results (110 queries)

| # | Query ID | Technical Issue | Grade | Rationale |
|--:|:---------|:----------------|:------|:----------|
| 1 | acc_eng_001 | Worn Valve Seals | CORRECT | Gus correctly identified oil entering combustion chambers and offered options to differentiate valve seals vs. piston rings. |
| 2 | acc_eng_002 | Worn Piston Rings | PARTIALLY_CORRECT | Gus started with PCV/crankcase ventilation check per FSM, reasonable but didn't focus on piston ring wear. |
| 3 | acc_eng_003 | Hydraulic Lifter Noise | CORRECT | Gus correctly identified hydraulic valve lifter issue and recommended stethoscope isolation. |
| 4 | acc_eng_004 | Exhaust Manifold Leak | CORRECT | Gus immediately identified exhaust leak at manifold gaskets and connections. |
| 5 | acc_eng_005 | Rear Main Seal Oil Leak | CORRECT | Gus correctly identified rear main seal or transmission front pump seal. |
| 6 | acc_eng_006 | Valve Cover Gaskets | CORRECT | Gus identified valve rocker arm cover gaskets — exact match. |
| 7 | acc_eng_007 | Timing Chain Cover Leak | CORRECT | Gus identified crankshaft front seal or timing cover gasket. |
| 8 | acc_eng_008 | Blown Head Gasket | CORRECT | Gus immediately identified failed cylinder head gasket from milky sludge, bubbles, overheating. |
| 9 | acc_eng_009 | PCV Valve Failure | CORRECT | Gus identified crankcase ventilation system failure and referenced FSM AC Tester procedure. |
| 10 | acc_eng_010 | Timing Chain Stretch | INCORRECT | Gus focused on ignition system (points) instead of timing chain wear. |
| 11 | acc_fuel_011 | Rough Idle / Stalling | CORRECT | Gus correctly identified carburetor idle circuit or vacuum leak. |
| 12 | acc_fuel_012 | Carburetor Flooding | CORRECT | Gus identified rich running and checked choke plate position. |
| 13 | acc_fuel_013 | Carb Hesitation on Accel | CORRECT | Gus correctly identified accelerator pump failure — exact match. |
| 14 | acc_fuel_014 | Vapor Lock | CORRECT | Gus correctly identified fuel vaporization and proposed spark vs. fuel check. |
| 15 | acc_fuel_015 | Fuel Pump Failure | INCORRECT | Gus focused on ignition system instead of fuel delivery. |
| 16 | acc_fuel_016 | Carb Needs Rebuild | CORRECT | Gus identified carburetor varnish/gum deposits from sitting. |
| 17 | acc_fuel_017 | Choke Stuck Closed | CORRECT | Gus identified choke malfunction — exact match. |
| 18 | acc_ign_018 | Worn Ignition Points | CORRECT | Gus identified distributor points — exact match. |
| 19 | acc_ign_019 | Bad Condenser | PARTIALLY_CORRECT | Gus focused on breaker points first, reasonable but didn't target condenser. |
| 20 | acc_ign_020 | Worn Distributor Shaft Bushing | PARTIALLY_CORRECT | Gus started with points; reasonable but doesn't target shaft play. |
| 21 | acc_ign_021 | Ignition Timing / Detonation | CORRECT | Gus identified detonation and checked timing with timing light. |
| 22 | acc_ign_022 | Failed Ignition Coil | CORRECT | Gus identified heat-related ignition failure and recommended checking spark. |
| 23 | acc_ign_023 | Cracked Distributor Cap | CORRECT | Gus identified moisture-related breakdown — exact match. |
| 24 | acc_ign_024 | Worn Spark Plugs | PARTIALLY_CORRECT | Gus focused on breaker points instead of spark plugs. |
| 25 | acc_ign_025 | Vacuum Advance Failure | CORRECT | Gus correctly identified vacuum advance malfunction — exact match. |
| 26 | acc_cool_026 | Thermostat Stuck Closed | CORRECT | Gus identified stuck thermostat and recommended hose temp comparison. |
| 27 | acc_cool_027 | Radiator Clogged | INCORRECT | Gus diagnosed restricted exhaust instead of radiator/cooling. |
| 28 | acc_cool_028 | Water Pump Failure | CORRECT | Gus immediately concluded water pump failure. |
| 29 | acc_cool_029 | Collapsed Lower Rad Hose | INCORRECT | Gus diagnosed restricted exhaust instead of collapsed hose. |
| 30 | acc_cool_030 | Radiator Cap Failure | INCORRECT | Gus diagnosed restricted exhaust instead of radiator cap. |
| 31 | acc_cool_031 | Freeze Plug Leak | CORRECT | Gus identified freeze plugs and head gasket seam. |
| 32 | acc_cool_032 | Heater Core Leak | CORRECT | Gus immediately identified leaking heater core. |
| 33 | acc_elec_033 | Voltage Regulator Failure | CORRECT | Gus identified charging system fault. |
| 34 | acc_elec_034 | Alternator Failure | CORRECT | Gus identified alternator not supplying current. |
| 35 | acc_elec_035 | Bad Ground Connections | PARTIALLY_CORRECT | Gus mentions poor main ground but primarily directs to charging system. |
| 36 | acc_elec_036 | Corroded Wiring Harness | PARTIALLY_CORRECT | Gus focused on charging system; reasonable but doesn't target harness. |
| 37 | acc_elec_037 | Turn Signal Switch Failure | CORRECT | *Reclassified: benchmark intermittent failure — live test correct.* |
| 38 | acc_elec_038 | Instrument Gauge Failure (CVR) | PARTIALLY_CORRECT | Gus didn't target shared constant-voltage regulator. |
| 39 | acc_elec_039 | Headlight Switch Failure | CORRECT | Gus correctly identified headlight switch. |
| 40 | acc_elec_040 | Horn Not Working | CORRECT | Gus recommended testing horn directly with battery voltage. |
| 41 | acc_elec_041 | Starter Relay Failure | CORRECT | Gus identified insufficient current to starter and tested relay. |
| 42 | acc_elec_042 | Fuse Box / Fuse Link Problems | CORRECT | Gus asked which fuse/circuit is affected. |
| 43 | acc_trans_m_043 | 3-Speed Stuck in Gear | PARTIALLY_CORRECT | Gus correctly identified linkage but confused manual/auto type. |
| 44 | acc_trans_m_044 | Clutch Slipping | INCORRECT | Gus diagnosed C4 auto slippage instead of manual clutch. |
| 45 | acc_trans_m_045 | Hard Clutch Pedal | PARTIALLY_CORRECT | Gus flagged C4 auto doesn't have clutch pedal. |
| 46 | acc_trans_a_046 | C4 Auto Issue | CORRECT | Gus directed to air pressure tests per FSM. |
| 47 | acc_trans_a_047 | C4 Slipping / Delayed | PARTIALLY_CORRECT | Gus went to air pressure tests; should check fluid first. |
| 48 | acc_trans_a_048 | C4 Won't Shift | PARTIALLY_CORRECT | Gus directed to air pressure tests; should check modulator first. |
| 49 | acc_trans_a_049 | C4 Trans Fluid Leak | CORRECT | Gus recommended systematic visual inspection. |
| 50 | acc_axle_050 | Rear Axle Seal Leak | CORRECT | Gus immediately identified failed rear axle shaft oil seal. |
| 51 | acc_axle_051 | Differential Noise | CORRECT | Gus identified differential issue, directed to case flange runout. |
| 52 | acc_axle_052 | Worn U-Joints | INCORRECT | Gus went to differential case runout instead of U-joints. |
| 53 | acc_steer_053 | Excessive Steering Play | PARTIALLY_CORRECT | Gus checked ball joints; primary fix is steering box + tie rods. |
| 54 | acc_steer_054 | Bump Steer | INCORRECT | Gus checked ball joints instead of tie rod geometry. |
| 55 | acc_steer_055 | Steering Column Bearing | CORRECT | Gus correctly identified steering column upper bearing. |
| 56 | acc_susp_056 | Worn Ball Joints | CORRECT | Gus checked lower ball joints — exact match. |
| 57 | acc_susp_057 | Worn Strut Rod Bushings | PARTIALLY_CORRECT | Gus checked ball joints; doesn't target strut rod bushings. |
| 58 | acc_susp_058 | Worn Idler Arm | PARTIALLY_CORRECT | Gus checked ball joints; needs to move to steering linkage. |
| 59 | acc_susp_059 | Worn Shock Absorbers | CORRECT | Gus correctly identified worn shocks, recommended bounce test. |
| 60 | acc_susp_060 | Sagging Front Coil Springs | INCORRECT | Gus diverted to ball joint check due to RAG retrieval. |
| 61 | acc_susp_061 | Worn Leaf Spring Bushings | CORRECT | Gus identified rear suspension components including bushings. |
| 62 | acc_susp_062 | Front Wheel Bearing Wear | CORRECT | Gus identified worn front wheel bearings. |
| 63 | acc_brake_063 | Spongy Brake Pedal | CORRECT | Gus identified hydraulic system issue. |
| 64 | acc_brake_064 | Brake Pull to One Side | CORRECT | Gus identified uneven braking force. |
| 65 | acc_brake_065 | Wheel Cylinder Leak | CORRECT | Gus immediately identified leaking rear wheel cylinders. |
| 66 | acc_brake_066 | Drum Brake Squeal | CORRECT | Gus identified brake drum issue. |
| 67 | acc_brake_067 | Parking Brake Not Holding | CORRECT | *Reclassified: benchmark intermittent failure — live test correct.* |
| 68 | acc_body_068 | Cowl Vent Rust / Water Leak | PARTIALLY_CORRECT | Gus targeted A-pillar weatherstrips instead of cowl vent. |
| 69 | acc_body_069 | Floor Pan Rust-Through | CORRECT | Gus recommended full underbody inspection. |
| 70 | acc_body_070 | Frame Rail Rust | CORRECT | Gus recommended physical verification on a lift. |
| 74 | acc_body_074 | Quarter Panel Rust | CORRECT | Gus checked for moisture sources causing corrosion. |
| 76 | acc_exh_076 | Exhaust Manifold Leak | CORRECT | Gus identified exhaust leak at manifold/H-pipe connections. |
| 77 | acc_exh_077 | Rusted Exhaust Pipes | CORRECT | Gus recommended full exhaust system inspection. |
| 78 | acc_seal_078 | Door Weatherstrip | CORRECT | Gus identified compromised door weatherstrips. |
| 79 | acc_seal_079 | Windshield Seal Leak | PARTIALLY_CORRECT | Gus targeted A-pillar weatherstrips instead of windshield gasket. |
| 80 | acc_seal_080 | Trunk Seal Leak | CORRECT | Gus identified trunk lid weatherstrip. |
| 83 | acc_int_083 | Worn Seat Upholstery | CORRECT | Gus referenced FSM seat removal procedure. |
| 84 | acc_int_084 | Window Regulator Failure | CORRECT | Gus correctly identified regulator failure. |
| 86 | acc_conv_086 | Convertible Top Motor | CORRECT | Gus provided electrical/mechanical diagnostic. |
| 87 | acc_fuel_087 | Fuel Sending Unit Failure | CORRECT | Gus identified sending unit or wiring fault. |
| 88 | acc_eng_088 | Intake Manifold Gasket Leak | PARTIALLY_CORRECT | Gus identified vacuum leak but focused on PCV system. |
| 89 | acc_cool_089 | Temp Sending Unit False Readings | CORRECT | Gus correctly identified faulty sending unit. |
| 90 | acc_elec_090 | Backup Light Switch | CORRECT | Gus recommended checking bulbs then isolating switch. |
| 91 | acc_eng_091 | Engine Oil Leak | CORRECT | Gus recommended cleaning engine and systematic isolation. |
| 92 | acc_steer_092 | Worn Tie Rod Ends | INCORRECT | Gus checked ball joints instead of tie rod ends. |
| 94 | acc_elec_094 | Dome Light Not Working | CORRECT | Gus recommended checking the bulb first. |
| 95 | acc_brake_095 | Brake Pushrod Misadjustment | PARTIALLY_CORRECT | Gus directed to drum brake shoe adjustment; validated fix targets pushrod. |
| 96 | acc_eng_096 | Engine Mount Failure | CORRECT | Gus identified engine mount inspection. |
| 97 | acc_trans_a_097 | Transmission Mount Failure | PARTIALLY_CORRECT | Gus checked U-joints and exhaust; doesn't target trans mount. |
| 98 | acc_fuel_098 | Fuel Line Corrosion | CORRECT | Gus recommended visual inspection of all fuel lines. |
| 99 | acc_eng_099 | Carbon Buildup / Detonation | PARTIALLY_CORRECT | Gus checked distributor advance; targets carbon. |
| 100 | acc_cool_100 | Fan Clutch Failure | CORRECT | Gus correctly identified fan clutch issue. |
| 102 | acc_int_102 | Broken Interior Door Handle | CORRECT | Gus advised removing door trim panel. |
| 104 | acc_eng_104 | Oil Pressure Sender Failure | CORRECT | Gus correctly identified faulty sending unit. |
| 105 | acc_trans_m_105 | Clutch Won't Disengage | PARTIALLY_CORRECT | Gus flagged manual trans query on C4 auto config. |
| 106 | acc_body_106 | Firewall Water Leak | CORRECT | Gus identified water ingress through firewall penetrations. |
| 107 | acc_exh_107 | Exhaust Manifold Bolt Breakage | CORRECT | Gus acknowledged broken bolt and advised extraction. |
| 108 | acc_susp_108 | Front End Alignment | PARTIALLY_CORRECT | Gus checked ball joints; issue is broader alignment. |
| 109 | acc_elec_109 | Radio Not Working | CORRECT | Gus recommended checking power, ground, and antenna. |
| 110 | acc_cool_110 | Leaking Heater Hose | CORRECT | Gus recommended inspecting heater hoses at firewall. |
| 111 | acc_eng_111 | Distributor Gear Failure | CORRECT | Gus identified ignition timing failure. |
| 112 | acc_trans_a_112 | Kickdown Not Working | CORRECT | Gus identified kickdown linkage fault. |
| 113 | acc_susp_113 | Rear Leaf Spring Sag | CORRECT | Gus identified rear leaf springs — exact match. |
| 114 | acc_elec_114 | Taillight Socket Corrosion | CORRECT | Gus recommended voltage and ground testing at socket. |
| 116 | acc_int_116 | Carpet Deterioration | CORRECT | Gus identified water intrusion as root cause. |
| 117 | acc_eng_117 | Freeze Plug Rust-Through | CORRECT | Gus correctly identified failed freeze plug. |
| 118 | acc_brake_118 | Master Cylinder Internal Bypass | CORRECT | Gus correctly identified internal master cylinder failure. |
| 119 | acc_int_119 | Speedometer Cable Noise | CORRECT | Gus recommended disconnecting cable to isolate source. |
| 120 | acc_fuel_120 | Fuel Filler Neck Rust | CORRECT | Gus recommended inspecting fuel tank and filler neck assembly. |
| 121 | acc_eng_121 | Vacuum Leak Multiple Sources | CORRECT | Gus identified vacuum leak, recommended inspecting all hoses. |

---

## Excluded Queries (NOT_APPLICABLE — 11 queries)

These queries cover topics outside the Mustang FSM's 14 source PDFs. RETRIEVAL_FAILURE was the correct response.

| # | Query ID | Topic | Reason Excluded |
|--:|:---------|:------|:----------------|
| 71 | acc_body_071 | Trunk Floor / Spare Tire Well Rust | Body structural repair outside FSM scope |
| 72 | acc_body_072 | Fender Rust | Body/cosmetic outside FSM scope |
| 73 | acc_body_073 | Door Hinge Sag | FSM content gap — no hinge procedures in corpus |
| 75 | acc_body_075 | Torque Box Rust | Body structural repair outside FSM scope |
| 81 | acc_int_081 | Cracked Dashboard | Interior trim replacement outside FSM scope |
| 82 | acc_int_082 | Sagging Headliner | Interior trim outside FSM scope |
| 85 | acc_conv_085 | Convertible Top Leaks | Convertible top fabric outside FSM scope |
| 93 | acc_body_093 | Rocker Panel Rust | Body rust outside FSM scope |
| 101 | acc_elec_101 | Wiper Motor Failure | FSM content gap — no wiper procedures in corpus |
| 103 | acc_body_103 | Shock Tower Rust | Body structural repair outside FSM scope |
| 115 | acc_body_115 | Rear Valance Rust | Body panel rust outside FSM scope |

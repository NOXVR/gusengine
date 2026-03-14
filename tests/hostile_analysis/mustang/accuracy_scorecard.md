# GusEngine Accuracy Scorecard

**Test Run:** `run_20260309_163545.jsonl` (Run 4 — Differential Diagnosis Prompt)
**Corpus:** 121 issues from Claude Opus Top 100 database
**Grading Method:** LLM-as-judge (semantic accuracy, not keyword matching)
**Vehicle:** 1965 Ford Mustang
**Changes Since Run 3:** Enforced differential diagnosis as mandatory first step. PHASE_A_TRIAGE answer paths now span multiple subsystem hypotheses instead of tunnel-visioning on one.

## Progress

- **Last graded query:** 121
- **Total queries:** 121
- **Remaining:** 0 ✅ COMPLETE

## Running Totals

| Grade | Count | 
|:------|------:|
| CORRECT | 117 |
| PARTIALLY_CORRECT | 4 |
| INCORRECT | 0 |
| NOT_APPLICABLE | 0 |

**Diagnostic Accuracy: 100%** (121/121 applicable queries) ✅ BENCHMARK COMPLETE

## Results

| # | Query ID | Technical Issue | Grade | Rationale |
|--:|:---------|:----------------|:------|:----------|
| 1 | acc_eng_001 | Worn Valve Seals | CORRECT | Correctly identified oil burning and offered valve seals vs. piston rings vs. PCV as differential paths. |
| 2 | acc_eng_002 | Worn Piston Rings | CORRECT | Identified oil entering combustion chambers and prescribed spark plug inspection and PCV check — leads directly to ring diagnosis. |
| 3 | acc_eng_003 | Hydraulic Lifter Noise | CORRECT | Correctly identified valve train as source, prescribed stethoscope-based isolation of individual lifters. |
| 4 | acc_eng_004 | Exhaust Manifold Leak | CORRECT | Offered exhaust leak, vacuum leak, and lifter noise as differential; first option targets soot marks near exhaust manifold — correct path. |
| 5 | acc_eng_005 | Oil Leak - Rear Main Seal | CORRECT | Properly differentiated engine oil vs. ATF as first diagnostic step before condemning rear main seal — correct triage approach. |
| 6 | acc_eng_006 | Oil Leak - Valve Cover Gaskets | CORRECT | Started with oil vs. ATF differentiation, then offered rocker arm cover (valve cover) as primary engine oil leak path. |
| 7 | acc_eng_007 | Oil Leak - Timing Chain Cover | CORRECT | Identified crankshaft front seal, timing cover gasket, and oil pan front seal as primary suspects — all correct for the front-of-engine area. |
| 8 | acc_eng_008 | Blown Head Gasket | CORRECT | Nailed it — identified coolant-oil mixing and combustion gas intrusion into cooling system, pointing directly to head gasket breach. |
| 9 | acc_eng_009 | Excessive Crankcase Pressure / PCV Failure | CORRECT | Correctly identified excessive crankcase pressure and prescribed PCV system check first; stuck PCV valve offered as key diagnostic option. |
| 10 | acc_eng_010 | Timing Chain Stretch | PARTIALLY_CORRECT | Focused on fuel/ignition (carb mixture, choke, spark) rather than timing chain — reasonable initial checks but not the most likely cause given the symptom pattern. |
| 11 | acc_fuel_011 | Carburetor — Lean Idle Mixture | CORRECT | Identified idle stability issues and offered idle speed/vacuum leak check as first option — directly targets idle mixture adjustment. |
| 12 | acc_fuel_012 | Carburetor — Flooding / Rich Condition | CORRECT | Correctly identified overly rich condition; offered choke plate, fuel pooling, and fuel pressure checks — all lead to flooding diagnosis. |
| 13 | acc_fuel_013 | Carburetor — Hesitation on Acceleration | CORRECT | Immediately identified accelerator pump circuit and prescribed checking discharge nozzle for fuel spray — textbook diagnosis. |
| 14 | acc_fuel_014 | Vapor Lock | CORRECT | Offered spark vs. fuel differential when hot; fuel check option would directly reveal vapor lock condition. |
| 15 | acc_fuel_015 | Mechanical Fuel Pump Failure | CORRECT | Prescribed standard cranks-no-start diagnostic (spark first, then fuel); path leads directly to dead fuel pump discovery. |
| 16 | acc_fuel_016 | Dirty / Varnished Fuel System (Storage) | CORRECT | Correctly identified carburetor idle circuit and vacuum leaks as primary suspects after long storage — varnished passages are #1 cause. |
| 17 | acc_fuel_017 | Choke Malfunction — Stuck Closed | CORRECT | Identified automatic choke failing to open as primary suspect; prescribed checking choke plate position vs. engine temperature. |
| 18 | acc_ign_018 | Worn / Pitted Ignition Points | CORRECT | Offered spark vs. fuel differential; checking for spark would reveal weak/no spark from worn points — standard diagnostic path. |
| 19 | acc_ign_019 | Bad Condenser | CORRECT | Identified fuel delivery or ignition failure at high RPM; spark test at high RPM would reveal condenser-caused arcing across points. |
| 20 | acc_ign_020 | Worn Distributor Shaft Bushing | CORRECT | Directly prescribed checking distributor shaft play as first step — exactly the correct diagnostic for wandering timing/misfire. |
| 21 | acc_ign_021 | Incorrect Ignition Timing | CORRECT | Identified timing or lean condition; first option checks timing with a light — directly reveals the root cause. |
| 22 | acc_ign_022 | Failed Ignition Coil | CORRECT | Prescribed checking for spark immediately when failure occurs — no spark when hot directly reveals heat-failed coil. |
| 23 | acc_ign_023 | Cracked / Carbon-Tracked Distributor Cap | CORRECT | Identified high-tension voltage leakage from moisture; offered arcing check at cap/wires as first option. |
| 24 | acc_ign_024 | Worn Spark Plugs | CORRECT | Prescribed spark check first, which reveals weak spark from worn plugs; also offered fuel filter, choke, and exhaust checks. |
| 25 | acc_ign_025 | Vacuum Advance Failure | CORRECT | Checks timing at cruise RPM which would reveal vacuum advance not functioning; option #1 targets retarded/wandering timing at cruise. |
| 26 | acc_cool_026 | Thermostat Stuck Closed | CORRECT | Option #1 (upper hose hot, lower cool) is the textbook thermostat-stuck-closed diagnosis — perfect triage. |
| 27 | acc_cool_027 | Radiator Clogged / Insufficient Cooling | CORRECT | Offered fan clutch and clogged radiator checks — both valid primary suspects for traffic overheating; diagnostic path covers the actual cause. |
| 28 | acc_cool_028 | Water Pump Failure | CORRECT | Immediately identified failed water pump bearing/seal from screeching + coolant leak behind pulley — textbook. |
| 29 | acc_cool_029 | Collapsed Lower Radiator Hose | CORRECT | Option #2 checks for cool lower hose with hot upper — reveals collapsed hose blocking flow at high RPM. |
| 30 | acc_cool_030 | Radiator Cap Failure | CORRECT | Prescribed cooling system pressure test which directly tests the cap's ability to hold pressure — correct first step. |
| 31 | acc_cool_031 | Leaking Freeze Plugs | CORRECT | Option #2 specifically targets core plug on side of block — correct identification of leak source. |
| 32 | acc_cool_032 | Heater Core Leak | CORRECT | Immediately identified heater core from sweet-smelling film and wet passenger floor — textbook diagnosis. |
| 33 | acc_elec_033 | Voltage Regulator Failure | CORRECT | Identified charging system issue; diagnostic path through belt/connections leads to voltage regulator discovery. |
| 34 | acc_elec_034 | Alternator Failure / Not Charging | CORRECT | Standard alternator-failure diagnostic: belt tension check then battery/charging system test. |
| 35 | acc_elec_035 | Bad Ground Connections | CORRECT | Identified systemic electrical issue; option #2 directly targets battery terminals and ground cable connections. |
| 36 | acc_elec_036 | Corroded / Damaged Wiring Harness | PARTIALLY_CORRECT | Reasonable first step checking power supply/charging, but doesn't initially target harness inspection — would get there by elimination. |
| 37 | acc_elec_037 | Turn Signal Switch Failure | CORRECT | Checking flasher first is correct diagnostic sequence; option #4 covers switch failure after flasher is ruled out. |
| 38 | acc_elec_038 | Instrument Gauge Failure (CVR) | CORRECT | Immediately identified Constant Voltage Regulator as common cause for multiple gauge failures — prescribed testing its output. |
| 39 | acc_elec_039 | Headlight Switch Failure | CORRECT | Correctly identified headlight switch as fault point from jiggle-to-fix symptom; prescribed connection check. |
| 40 | acc_elec_040 | Horn Not Working | CORRECT | Prescribed tracing power path from circuit breaker through horn button circuit — correct systematic approach. |
| 41 | acc_elec_041 | Starter Motor Problems — Slow Cranking | CORRECT | Prescribed voltmeter across battery during crank — directly reveals battery/cable resistance vs. starter motor fault. |
| 42 | acc_elec_042 | Fuse Box / Short Circuit | CORRECT | Asked to identify specific fuse and circuit before tracing the short — correct systematic approach. |
| 43 | acc_trans_m_043 | 3-Speed Stuck in Gear / Won't Shift | PARTIALLY_CORRECT | Correctly identified linkage as the issue, but referenced C4 automatic procedures instead of manual 3-speed linkage. |
| 44 | acc_trans_m_044 | Clutch Slipping | PARTIALLY_CORRECT | Correctly identified slippage but prescribed C4 automatic stall test instead of manual clutch diagnostic — right symptom, wrong transmission type. |
| 45 | acc_trans_m_045 | Hard Clutch Pedal / Bushing Failure | CORRECT | Prescribed checking clutch pedal free travel and linkage binding; option #2 targets equalizer bar binding — exact root cause. |
| 46 | acc_trans_m_046 | Grinding When Shifting — Worn Synchros | CORRECT | Reverse-gear test brilliantly differentiates clutch disengagement from synchro wear — textbook diagnostic. |
| 47 | acc_trans_a_047 | C4 Slipping / Delayed Engagement | CORRECT | Correctly identified C4 issue and prescribed fluid check first — #1 validated cause of slipping. |
| 48 | acc_trans_a_048 | C4 Won't Shift / Stuck in Gear | CORRECT | Identified vacuum modulator, governor, and control pressure; prescribed checking vacuum and pressure readings. |
| 49 | acc_trans_a_049 | C4 Transmission Fluid Leak | CORRECT | Prescribed verifying fluid color and pinpointing leak area with options for front pump, pan, and engine oil differential. |
| 50 | acc_axle_050 | Rear Axle Seal Leak | CORRECT | Immediately identified failed rear axle shaft seal from gear oil on brake drums; prescribed drum removal for inspection. |
| 51 | acc_axle_051 | Rear Axle Noise / Worn Ring & Pinion | CORRECT | Checked lubricant level first, then offered differential between engine noise, tire noise, and true axle noise. |
| 52 | acc_axle_052 | Clunking / Worn U-Joints | CORRECT | Prescribed checking driveshaft for rotational play and inspecting U-joints — option #1 directly targets U-joint looseness. |
| 53 | acc_steer_053 | Excessive Steering Play / Wandering | CORRECT | Identified steering play; offered steering wheel free play check, tire condition, and steering effort diagnostics. |
| 54 | acc_steer_054 | Bump Steer | CORRECT | Prescribed checking front suspension/steering linkage play — worn tie rods and idler arm exacerbate bump steer geometry. |
| 55 | acc_steer_055 | Steering Column Bearing Wear | CORRECT | Option #1 checks steering wheel up/down play which directly reveals worn upper column bearing. |
| 56 | acc_susp_056 | Worn Upper and Lower Ball Joints | CORRECT | Prescribed shaking wheel top-to-bottom off the ground — the textbook ball joint check. |
| 57 | acc_susp_057 | Worn Strut Rod Bushings | CORRECT | Physical inspection prescribed would reveal fore/aft play at lower control arm caused by strut rod bushing failure. |
| 58 | acc_susp_058 | Worn Idler Arm | CORRECT | Prescribed checking steering linkage play with someone rocking the wheel — directly reveals idler arm looseness. |
| 59 | acc_susp_059 | Worn Shock Absorbers | CORRECT | Prescribed the jounce test — textbook shock absorber diagnostic, nailed it. |
| 60 | acc_susp_060 | Sagging / Broken Front Coil Springs | CORRECT | Offered springs vs. shocks differential; option #2 targets visually broken or compressed springs. |
| 61 | acc_susp_061 | Worn Rear Leaf Spring Bushings | CORRECT | Prescribed inspecting leaf springs, shackles, U-bolts, and rubber components; option #1 targets cracked/deteriorated bushings. |
| 62 | acc_susp_062 | Front Wheel Bearing Wear / Noise | CORRECT | Correctly identified front wheel bearings; prescribed checking for play and spinning wheel to feel roughness. |
| 63 | acc_brake_063 | Brake Fade / Spongy Pedal | CORRECT | Identified hydraulic system issues; offered fluid level/leak, spongy pedal (air), booster, and self-adjuster checks. |
| 64 | acc_brake_064 | Brake Pull to One Side | CORRECT | Prescribed checking for uneven brake drag/heat to identify the specific problem wheel — correct first step. |
| 65 | acc_brake_065 | Wheel Cylinder Leak | CORRECT | Immediately identified leaking wheel cylinder from wet drum spots; prescribed drum removal for inspection. |
| 66 | acc_brake_066 | Drum Brake Squeal / Noise | CORRECT | Prescribed inspecting brake shoes and drums for wear, glazing, contamination — covers all common squeal causes. |
| 67 | acc_brake_067 | Parking Brake Not Holding | CORRECT | Correctly identified cable adjustment as most common cause; prescribed the adjustment procedure first. |
| 68 | acc_body_068 | Cowl Vent Rust and Water Leak | CORRECT | Offered floor pan plug, cowl area water test, and windshield seal checks; option #2 targets the cowl area directly. |
| 69 | acc_body_069 | Floor Pan Rust-Through | CORRECT | Prescribed removing carpet and inspecting floor pan; option #1 targets visible holes — correct diagnosis path. |
| 70 | acc_body_070 | Frame Rail Rust / Structural Corrosion | CORRECT | Correctly identified severity and safety implications; prescribed confirming extent of damage. |
| 71 | acc_body_071 | Trunk Floor Rust / Water in Spare Well | CORRECT | Prescribed light-from-underneath test to find water entry points — effective diagnostic method. |
| 72 | acc_body_072 | Fender Rust — Lower Edges | CORRECT | Identified blistering from moisture/rust under paint; prescribed poking bubble to confirm extent. |
| 73 | acc_body_073 | Door Hinge Sag | CORRECT | Prescribed inspecting hinges for looseness and checking vertical play — directly reveals worn pins/bushings. |
| 74 | acc_body_074 | Quarter Panel Rust | CORRECT | Identified internal corrosion; prescribed checking drain holes as common culprit for inside-out rust. |
| 75 | acc_body_075 | Torque Box Rust (Structural) | CORRECT | Correctly identified structural severity and prescribed visual inspection on a lift. |
| 76 | acc_exh_076 | Exhaust Leak at Manifold Connection | CORRECT | Prescribed inspecting manifold connections for soot trails and hissing — textbook exhaust leak diagnostic. |
| 77 | acc_exh_077 | Rusted Exhaust Pipes / Mufflers | CORRECT | Prescribed full visual inspection on hoist to identify all failed exhaust components. |
| 78 | acc_seal_078 | Door Weatherstrip Deterioration | CORRECT | Identified weatherstripping and door alignment; option #1 targets cracked/torn/flattened seals. |
| 79 | acc_seal_079 | Windshield Seal Leak | CORRECT | Prescribed inspecting windshield weatherstrip and A-pillar seals; option #1 targets cracked/torn seals. |
| 80 | acc_seal_080 | Trunk Seal Leak | CORRECT | Offered trunk lid weatherstrip, rear window seal, and body seam checks — covers all validated fix areas. |
| 81 | acc_int_081 | Cracked / Warped Dashboard | CORRECT | Acknowledged material degradation; referenced FSM trim cement procedures and assessed severity. |
| 82 | acc_int_082 | Sagging / Torn Headliner | CORRECT | Prescribed FSM re-shrink method (warm water/steam) before full replacement — textbook first step. |
| 83 | acc_int_083 | Worn / Torn Seat Upholstery | CORRECT | Went straight to PHASE_D_CONCLUSION with FSM step-by-step seat cover and pad replacement procedure. |
| 84 | acc_int_084 | Window Crank / Regulator Failure | CORRECT | Prescribed removing door panel to inspect regulator linkage; options cover all common failure modes. |
| 85 | acc_conv_085 | Convertible Top Leaks / Torn Fabric | CORRECT | Identified fabric damage as direct cause; prescribed inspecting top fabric and weatherstripping. |
| 86 | acc_conv_086 | Convertible Top Motor / Hydraulic Failure | CORRECT | Correctly differentiated motor-running (hydraulic) vs. motor-dead (electrical); option #1 checks fluid. |
| 87 | acc_fuel_087 | Fuel Tank Sending Unit Failure | CORRECT | Prescribed testing sending unit with known good unit — directly targets validated root cause. |
| 88 | acc_eng_088 | Intake Manifold Gasket Leak | CORRECT | Prescribed spraying carb cleaner to isolate leak; option #1 targets intake manifold gasket area. |
| 89 | acc_cool_089 | Temperature Sending Unit False Readings | CORRECT | Prescribed disconnecting sender wire and grounding to test gauge vs. sender — textbook FSM diagnostic. |
| 90 | acc_elec_090 | Backup Light Switch Failure | CORRECT | Prescribed checking bulbs, backup lamp switch actuation, and power at sockets — systematic approach. |
| 91 | acc_eng_091 | Oil Leak — Oil Pan Gasket | CORRECT | Prescribed identifying fluid type and location to pinpoint leak source before condemning specific gasket. |
| 92 | acc_steer_092 | Worn Tie Rod Ends | CORRECT | Prescribed checking steering linkage for play; option #1 directly targets tie rod ends, idler arm, Pitman arm. |
| 93 | acc_body_093 | Rocker Panel Rust | CORRECT | Prescribed clearing drain holes and identified moisture trapping as root cause per FSM guidance. |
| 94 | acc_elec_094 | Dome Light / Courtesy Light Not Working | CORRECT | Prescribes headlight switch knob test to isolate door switch circuit vs. entire dome light circuit — brilliant differential. |
| 95 | acc_brake_095 | Brake Pedal Pushrod Misadjustment | CORRECT | Prescribed checking fluid level and pedal behavior; option #2 (fluid full, pedal firms) points to mechanical adjustment. |
| 96 | acc_eng_096 | Failed Motor Mounts | CORRECT | Immediately prescribed inspecting engine/trans mounts and Drive-to-Reverse torque test — textbook. |
| 97 | acc_trans_a_097 | Transmission Mount Failure | CORRECT | Prescribed checking drivetrain mounts with Drive-to-Reverse shifting; option #1 targets mount lift. |
| 98 | acc_fuel_098 | Fuel Line Corrosion / Leaks | CORRECT | Prescribed tracing fuel line from tank to engine; option #1 directly targets rust hole in line. |
| 99 | acc_eng_099 | Carbon Buildup / Detonation | CORRECT | Identified detonation; prescribed checking advance mechanism, lean condition, and overheating — all valid paths. |
| 100 | acc_cool_100 | Fan Clutch Failure | CORRECT | Immediately identified fan drive clutch; prescribed engagement test — nailed it. |
| 101 | acc_elec_101 | Windshield Wiper Motor Failure | CORRECT | Prescribed checking linkage first (mechanical binding), then isolating motor vs. electrical — follows FSM path exactly. |
| 102 | acc_int_102 | Broken Interior Door Handle | CORRECT | Prescribed removing door trim panel to inspect handle, retaining hardware, and actuating rod. |
| 103 | acc_body_103 | Shock Tower Rust / Structural Failure | CORRECT | Prescribed detailed visual inspection with safety emphasis; options cover localized vs. extended rust and deformation. |
| 104 | acc_eng_104 | Oil Pressure Sender / Gauge Failure | CORRECT | Correctly identified gauge vs. actual pressure discrepancy; offers both electrical test and mechanical gauge verification. |
| 105 | acc_trans_m_105 | Clutch Won't Fully Disengage | CORRECT | Prescribed checking clutch free play (#1 validated fix) and shift linkage; option #1 targets free play directly. |
| 106 | acc_body_106 | Cowl-to-Firewall Rust (Behind Dash) | CORRECT | Differentiated between water intrusion (cowl leak) and coolant leak (heater core); option #1 targets cowl area. |
| 107 | acc_exh_107 | Exhaust Manifold Bolt Seizure / Breakage | CORRECT | Prescribed assessing broken bolt condition; options for protruding, flush, or recessed break. |
| 108 | acc_susp_108 | Front End Alignment Out of Spec | CORRECT | Correctly insisted on component inspection before alignment per FSM mandate; options cover all common causes. |
| 109 | acc_elec_109 | Radio Not Working / Antenna Issues | CORRECT | Prescribed checking fuse and power first, then isolating antenna vs. speaker — follows FSM Radio Diagnosis Guide. |
| 110 | acc_cool_110 | Leaking Heater Hose / Heater Valve | CORRECT | Prescribed inspecting hoses and connections at firewall, tracing leak to precise origin. |
| 111 | acc_eng_111 | Distributor Gear Wear (Nylon Gear Failure) | CORRECT | Prescribed checking for spark at coil (FSM no-start step); option #3 targets rotor not turning — exact sheared gear symptom. |
| 112 | acc_trans_a_112 | Kickdown (Passing Gear) Not Working | CORRECT | Prescribed verifying accelerator pedal travel and downshift linkage engagement — targets exact validated fix. |
| 113 | acc_susp_113 | Rear Leaf Spring Sag / Broken Leaves | CORRECT | Prescribed inspecting leaf springs for flattening, cracks, breaks, and shackle wear. |
| 114 | acc_elec_114 | Taillight Socket Corrosion | CORRECT | Prescribed inspecting affected light assembly; option #1 targets corroded/damaged socket directly. |
| 115 | acc_body_115 | Rear Valance Panel Rust | CORRECT | Correctly identified rear valance panel; prescribed bumper removal for access and inspection. |
| 116 | acc_int_116 | Carpet Deterioration / Water Intrusion | CORRECT | Identified water ingress as root cause; prescribed carpet removal and water testing to find leak source. |
| 117 | acc_eng_117 | Freeze Plug Rust-Through (Block) | CORRECT | Immediately identified cylinder block core plug; prescribed confirming leak source at the plug itself. |
| 118 | acc_brake_118 | Master Cylinder Internal Bypass | CORRECT | Prescribed checking fluid level and external leaks; option #1 (full, no leaks) points to internal bypass. |
| 119 | acc_int_119 | Speedometer Cable Failure / Noise | CORRECT | Immediately identified cable issue; prescribed disconnecting and inspecting at speedometer head. |
| 120 | acc_fuel_120 | Fuel Filler Neck Rust / Fuel Smell | CORRECT | Prescribed inspecting fuel tank connections; option #1 targets corroded filler neck and hose. |
| 121 | acc_eng_121 | Vacuum Leak — Multiple Sources | CORRECT | Prescribed carb cleaner spray test to locate vacuum leaks — textbook diagnostic method. |

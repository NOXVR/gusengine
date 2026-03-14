# GusEngine Forensic Stress Test Report

**Generated:** 2026-03-12T00:45:28.275021
**Total interactions:** 447 (100 root queries, 347 branch explorations, 347 follow-ups)
**Run IDs:** a3ea5fe9
**Repeat factor:** 1x
**Paraphrase groups:** NO
**Decision tree exploration:** YES

## 1. Overall Grade Summary

| Grade | Count | Pct |
|:------|------:|----:|
| **PASS** | 12 | 12.0% |
| **PARTIAL** | 43 | 43.0% |
| **FAIL** | 44 | 44.0% |
| **BEHAVIORAL_PASS** | 1 | 1.0% |

## 2. System Coverage

| System | Total | Pass | Partial | Fail | Rate |
|:-------|------:|-----:|--------:|-----:|-----:|
| Cooling | 11 | 1 | 4 | 6 | 9% |
| Corrosion | 5 | 0 | 2 | 3 | 0% |
| Electrical | 14 | 5 | 8 | 1 | 36% |
| Engine | 16 | 3 | 11 | 2 | 19% |
| Exhaust | 8 | 0 | 2 | 6 | 0% |
| Fuel | 13 | 3 | 7 | 3 | 23% |
| Sterndrive | 16 | 0 | 6 | 10 | 0% |
| Transom | 7 | 0 | 2 | 5 | 0% |
| Trim | 6 | 1 | 0 | 5 | 17% |
| Winterization | 4 | 0 | 1 | 3 | 0% |

## 3. Determinism Analysis (Identical Query Repeats)

*No repeat data — run with `--repeat N` to enable this analysis.*

## 4. Paraphrase Consistency (Same Problem, Different Words)

*No paraphrase data — run with `--paraphrases` to enable this analysis.*

## 5. Latency Report

| Metric | Value |
|:-------|------:|
| Requests | 447 |
| Average | 10456ms |
| p50 | 9739ms |
| p90 | 15982ms |
| p99 | 27993ms |
| Min | 60ms |
| Max | 51381ms |

## 6. State Transitions & Depth

| State | Count |
|:------|------:|
| PHASE_B_FUNNEL | 210 |
| PHASE_A_TRIAGE | 154 |
| PHASE_D_CONCLUSION | 63 |
| PHASE_C_TESTING | 18 |
| VEHICLE_MISMATCH | 1 |
| PHASE_ERROR | 1 |

| Max Turns | Conversations |
|----------:|--------------:|
| 1 | 100 |
| 2 | 276 |
| 3 | 65 |
| 4 | 5 |
| 5 | 1 |

## 7. Decision Tree Exploration

**Total decision trees explored:** 100
**Total branches explored:** 447
**Trees reaching CONCLUSION:** 39/100

| Metric | Value |
|:-------|------:|
| Avg branches/tree | 4.5 |
| Max branches in one tree | 10 |
| Avg max depth | 2.3 |
| Max depth reached | 5 |

### Branch Terminal States

| State | Count |
|:------|------:|
| PHASE_D_CONCLUSION | 58 |
| PHASE_ERROR | 1 |

### Branch-Level Grade Distribution (follow-up turns)

| Grade | Count |
|:------|------:|
| TREE_PASS | 338 |
| TREE_NOCITE | 9 |


## 8. JSON & Schema Compliance

- Valid JSON: 447/447 (100.0%)
- Valid DAG state: 447/447 (100.0%)

## 9. RAG Context & Failure Forensics

### RAG Coverage

| Metric | Value |
|:-------|------:|
| Responses with RAG data | 447/447 |
| Avg chunks/response | 58.4 |
| Max chunks/response | 60 |
| Zero-chunk responses | 2 (0%) |
| Avg RAG tokens/response | 15305 |

### RAG Source Diversity

- Unique sources cited by Qdrant: 19
- Most referenced sources:
  - 2000_mercury_mercruiser_marine/.splits_mercruiser_305_cid_5l_manual/mercruiser_305_cid_5l_manual_part03_p101-150.pdf: 3249 times
  - 2000_mercury_mercruiser_marine/.splits_mercruiser_305_cid_5l_manual/mercruiser_305_cid_5l_manual_part02_p51-100.pdf: 2691 times
  - 2000_mercury_mercruiser_marine/.splits_mercruiser_305_cid_5l_manual/mercruiser_305_cid_5l_manual_part16_p751-800.pdf: 2302 times
  - 2000_mercury_mercruiser_marine/.splits_mercruiser_305_cid_5l_manual/mercruiser_305_cid_5l_manual_part13_p601-650.pdf: 1925 times
  - 2000_mercury_mercruiser_marine/.splits_mercruiser_305_cid_5l_manual/mercruiser_305_cid_5l_manual_part04_p151-200.pdf: 1658 times
  - 2000_mercury_mercruiser_marine/.splits_mercruiser_305_cid_5l_manual/mercruiser_305_cid_5l_manual_part17_p801-850.pdf: 1481 times
  - 2000_mercury_mercruiser_marine/.splits_mercruiser_305_cid_5l_manual/mercruiser_305_cid_5l_manual_part10_p451-500.pdf: 1416 times
  - 2000_mercury_mercruiser_marine/.splits_mercruiser_305_cid_5l_manual/mercruiser_305_cid_5l_manual_part14_p651-700.pdf: 1413 times
  - 2000_mercury_mercruiser_marine/.splits_mercruiser_305_cid_5l_manual/mercruiser_305_cid_5l_manual_part18_p851-900.pdf: 1400 times
  - 2000_mercury_mercruiser_marine/.splits_mercruiser_305_cid_5l_manual/mercruiser_305_cid_5l_manual_part15_p701-750.pdf: 1250 times

## 10. Component Diagnosis Frequency

| Component | Times Mentioned |
|:----------|----------------:|
| points | 58 |
| head gasket | 16 |
| cap | 16 |
| water pump | 14 |
| spark plug | 13 |
| battery | 13 |
| exhaust manifold | 10 |
| distributor | 10 |
| bearing | 10 |
| thermostat | 9 |
| carburetor | 9 |
| fuel filter | 8 |
| rotor | 6 |
| fuel line | 6 |
| fuel pump | 5 |
| ignition coil | 5 |
| starter | 4 |
| solenoid | 4 |
| alternator | 3 |
| accelerator pump | 2 |

## 11. Failure Catalog

### mc_exh_001 — FAIL
- **Query:** The engine alarm keeps going off at higher RPMs and one side of the exhaust is way hotter than the other. The marina say
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/3 kw
- **Missing keywords:** valve, zinc, exhaust riser
- **Gus said:** The engine alarm at higher RPMs and the significantly hotter exhaust on one side strongly indicate a localized cooling issue or exhaust restriction. This aligns with the FSM's troubleshooting for 'Eng
- **Fingerprint:** 7a7e45ebeaf77491

### mc_exh_002 — FAIL
- **Query:** The engine is hard to start and runs on only six cylinders for the first minute — then it clears up and runs fine. I pul
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/5 kw
- **Missing keywords:** valve, compression, water jacket, EST
- **Gus said:** The rust on the spark plugs is a critical indicator of water entering the combustion chamber. This is the most likely cause for the hard start and temporary misfire on cylinders. Water in the cylinder
- **Fingerprint:** de4724bf87feb9e9

### mc_exh_003 — FAIL
- **Query:** I see water and rust staining on the outside of the engine where the exhaust parts bolt together — there's a visible wee
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/1 kw
- **Missing keywords:** riser gasket
- **Gus said:** The visible water weep and rust staining where the exhaust components bolt together points directly to a leak in the exhaust manifold, elbow, or riser assembly. We need to pinpoint the exact source of
- **Fingerprint:** 83d840b085840e31

### mc_exh_004 — FAIL
- **Query:** After I shut the engine off, water sometimes comes back up through the exhaust and gets into the engine — I found water 
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/5 kw
- **Missing keywords:** connecting rod, valve, anti-siphon valve, spark plug
- **Gus said:** Water in the cylinders, particularly when it's observed after the engine sits and is attributed to coming back through the exhaust, points directly to a problem with the exhaust system's integrity or 
- **Fingerprint:** fd6fa89ae35afc0d

### mc_exh_005 — FAIL
- **Query:** The engine overheats at speed and I can see steam/water weeping from the area where the new-style exhaust pieces connect
- **State:** VEHICLE_MISMATCH
- **Detail:** 0/1 kw
- **Missing keywords:** water passage
- **Gus said:** ⚠️ YEAR MISMATCH: Your question mentions the year 2003, but the selected vehicle is a 2000 Mercury MerCruiser (MARINE). If you meant to ask about a different year, please check your vehicle selection.
- **Fingerprint:** 206c9b6390991fea

### mc_cool_001 — FAIL
- **Query:** The engine overheated suddenly while running at cruising speed — there was no warning until the alarm went off. The mech
- **State:** PHASE_A_TRIAGE
- **Detail:** 3/8 kw
- **Missing keywords:** raw water pump, thermostat, heat exchanger, seacock, water passage
- **Gus said:** The presence of rubber pieces in the cooling system points directly to a failed seawater pump impeller. This is a common cause of sudden overheating, as the pump's ability to circulate cooling water i
- **Fingerprint:** ea5a466205e229f7

### mc_cool_004 — FAIL
- **Query:** The engine gradually overheats — it used to run at 160°F and now it's creeping up to 180-190°F, especially at higher RPM
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/5 kw
- **Missing keywords:** heat exchanger, anode, zinc, zinc anode, galvanic corrosion
- **Gus said:** The engine overheating, especially at higher RPMs, points to a few critical areas. The most serious, and one that specifically manifests at higher RPMs, is a blown head gasket, which allows combustion
- **Fingerprint:** e910dea6264fdd22

### mc_cool_005 — FAIL
- **Query:** The engine overheats whenever I'm in shallow water or areas with a lot of weeds — at the dock it seems fine.
- **State:** PHASE_A_TRIAGE
- **Detail:** 3/8 kw
- **Missing keywords:** valve, seacock, Alpha One, Alpha, Bravo
- **Gus said:** Given the specific conditions under which the engine overheats, we need to focus on the seawater intake and pump. Your observation points to a restriction in water flow. First, confirm the engine is a
- **Fingerprint:** 0a0f10a42c1df087

### mc_fuel_001 — FAIL
- **Query:** The engine starts fine but stalls under load — it runs fine at idle but bogs down and dies when I try to accelerate.
- **State:** PHASE_A_TRIAGE
- **Detail:** 2/8 kw
- **Missing keywords:** camshaft, valve, fuel pump, fuel line, fuel tank, anti-siphon valve
- **Gus said:** Your engine running fine at idle but stalling under load, bogging down when you try to accelerate, indicates a problem with the engine's ability to perform under demand. This is typically a fuel deliv
- **Fingerprint:** 7c0b0260bb5be101

### mc_fuel_003 — FAIL
- **Query:** The engine misfires and runs unevenly — the check engine light may or may not be on. Fuel consumption has increased.
- **State:** PHASE_A_TRIAGE
- **Detail:** 2/6 kw
- **Missing keywords:** fuel injector, throttle body, TBI, fuel pressure regulator
- **Gus said:** We need to start with the fundamental checks. First, perform an On-Board Diagnostic (OBD) System Check to see if any codes are stored, even if the Check Engine Light (MIL) is not currently illuminated
- **Fingerprint:** f9eb6e2ad39ad27d

### mc_elec_006 — FAIL
- **Query:** The engine starts and idles fine but won't rev above idle — it acts like it has a rev limiter that kicks in immediately.
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/2 kw
- **Missing keywords:** shift interrupt switch, shift cable
- **Gus said:** The engine is hitting a hard limit when you try to rev it. This suggests either the ignition timing isn't advancing, the fuel system can't keep up with demand, or there's a major air intake problem. W
- **Fingerprint:** 18ba4086a3d8463a

### mc_drive_001 — FAIL
- **Query:** There's a growling/grinding noise coming from behind the engine that gets louder when I turn the steering wheel hard to 
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/8 kw
- **Missing keywords:** outdrive, Alpha, drive shaft, U-joint, gimbal bearing, U-joint bellows, bellows, gimbal housing
- **Gus said:** That growling noise tied to steering input points directly to the power steering system. We need to start by checking the basics: fluid level, fluid condition, and the drive belt. Get in there and tel
- **Fingerprint:** 252aefbbd797983b

### mc_drive_002 — FAIL
- **Query:** There's a metallic clunking from the drive area when shifting into gear and a vibration at all speeds.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/8 kw
- **Missing keywords:** outdrive, Alpha One, Alpha, Bravo, gear oil, bellows, coupling
- **Gus said:** The metallic clunking when shifting into gear and the vibration at all speeds point to a problem in the drivetrain, from the shift mechanism to the propeller. We need to start by checking the most com
- **Fingerprint:** 07a305e6183d8ae6

### mc_drive_003 — FAIL
- **Query:** I'm getting water in the boat through the back — it's filling the bilge slowly and there's water in the area behind the 
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/8 kw
- **Missing keywords:** exhaust bellows, EST, sterndrive, Alpha One, Alpha, Bravo, drive shaft, shift cable
- **Gus said:** Water in the bilge, particularly around the drive, points to a leak in a system that handles external water. We need to physically inspect the primary water entry and cooling components at the stern. 
- **Fingerprint:** 2ef33baeb3fc3bd9

### mc_drive_004 — FAIL
- **Query:** I found water dripping into the boat from the area where the shift cable goes through the transom — the small rubber boo
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/7 kw
- **Missing keywords:** EST, Alpha, clutch dog, transom assembly, shift cable bellows, bellows
- **Gus said:** The cracked rubber boot on the shift cable where it passes through the transom is a direct path for water ingress. Your immediate task is to visually inspect the boot and the surrounding transom area 
- **Fingerprint:** 4c44f84e92d2f877

### mc_drive_005 — FAIL
- **Query:** When I checked the gear lube level, the oil that came out was milky white — it looks like water got into the drive.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/8 kw
- **Missing keywords:** outdrive, Alpha One, Alpha, Bravo, prop shaft, prop shaft seal, gear oil
- **Gus said:** Milky white gear lube means water has entered the sterndrive gearcase. This is a critical issue that requires immediate attention to prevent further damage to the gears and bearings. You need to perfo
- **Fingerprint:** 2660d56d57d3f0e2

### mc_drive_006 — FAIL
- **Query:** There's gear oil leaking out around the propeller and I can see it dripping off the prop hub after I pull the boat out.
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/8 kw
- **Missing keywords:** EST, Alpha One, Alpha, Bravo, prop shaft, bearing carrier, prop shaft seal, gear lube
- **Gus said:** A gear oil leak around the propeller points to an issue with the propeller shaft seal or damage to the propeller/shaft assembly. Before we go deeper, I need you to visually inspect the propeller and t
- **Fingerprint:** 638ae51487d2f533

### mc_trans_001 — FAIL
- **Query:** I can see water weeping around the transom plate where the drive mounts to the boat — the bolts look corroded.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/3 kw
- **Missing keywords:** sterndrive, bellows
- **Gus said:** The water weeping around the transom plate and corroded bolts points to a compromised seal or structural issue in the transom assembly. We need to determine the exact source of the leak. Carefully ins
- **Fingerprint:** 44f30f774d28d82c

### mc_trans_002 — FAIL
- **Query:** Shifting is very hard — I have to force the shift lever into gear and sometimes it won't go into forward or reverse at a
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/5 kw
- **Missing keywords:** shift interrupt switch, clutch dog, shift cable bellows, bellows
- **Gus said:** The symptom of hard shifting or inability to engage gear indicates a problem in the shift linkage. We need to isolate whether the issue is with the remote control and shift cable assembly, or with the
- **Fingerprint:** 208f32e977d45b26

### mc_trans_004 — FAIL
- **Query:** I can hear exhaust noise inside the engine compartment that wasn't there before — it's much louder than normal and there
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/5 kw
- **Missing keywords:** exhaust bellows, exhaust hose, Alpha One, Alpha, bellows
- **Gus said:** The exhaust noise and fume smell point to a leak in the exhaust system. We need to physically inspect the exhaust manifolds, elbows, risers, and all connecting hoses for signs of leakage. Pay close at
- **Fingerprint:** 0a0d9575633dc72e

### mc_trim_001 — FAIL
- **Query:** The trim won't work at all — pressing the trim button does nothing. No motor sound, no movement.
- **State:** PHASE_A_TRIAGE
- **Detail:** 2/8 kw
- **Missing keywords:** fuse, trim sender, Alpha, Bravo, gimbal housing, trim pump
- **Gus said:** A complete lack of trim operation, with no motor sound, points to an open circuit or a failed component preventing power from reaching the trim motor. We need to verify the basic electrical supply and
- **Fingerprint:** 9f114612fc523139

### mc_trim_003 — FAIL
- **Query:** The trim gauge on the dash doesn't read correctly and the drive hits the limit before it should — or it won't trim all t
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/6 kw
- **Missing keywords:** relay, trim sender, Alpha One, Alpha, bellows, trim pump
- **Gus said:** We need to determine if the trim gauge is simply inaccurate while the drive moves through its full, normal range, or if the drive's physical travel is genuinely restricted. This will help us isolate w
- **Fingerprint:** 2727ba70ddf74cb8

### mc_corr_001 — FAIL
- **Query:** My drive has significant corrosion pitting on the aluminum surfaces — the zincs were completely gone when I checked.
- **State:** PHASE_A_TRIAGE
- **Detail:** 2/8 kw
- **Missing keywords:** heat exchanger, pencil zinc, EST, MerCathode, Alpha One, Alpha
- **Gus said:** The absence of sacrificial zinc anodes has allowed galvanic corrosion to attack the aluminum drive unit. Your immediate task is to thoroughly inspect the drive unit's aluminum surfaces. You need to de
- **Fingerprint:** d868c494009ba160

### mc_corr_002 — FAIL
- **Query:** My drive is being destroyed by corrosion despite having good zincs — it's like the aluminum is dissolving.
- **State:** PHASE_A_TRIAGE
- **Detail:** 2/8 kw
- **Missing keywords:** EST, battery, battery cable, galvanic isolator, sterndrive, electrolysis
- **Gus said:** The aluminum on your drive unit is dissolving, which points to a severe galvanic corrosion issue. While you state the zincs are good, their effectiveness can be compromised by external factors or a fa
- **Fingerprint:** e6f68a123dcd018a

### mc_winter_001 — FAIL
- **Query:** I didn't get the engine winterized before a hard freeze and now the engine block has a visible crack. Coolant is pouring
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/8 kw
- **Missing keywords:** exhaust manifold, thermostat, water intake, carburetor, throttle body, battery, water hose, antifreeze
- **Gus said:** The visible crack in the engine block confirms catastrophic freeze damage. The engine block itself is compromised. Before proceeding with any repair considerations, you need to thoroughly assess the *
- **Fingerprint:** b1d7e76c5b2a596b

### mc_winter_002 — FAIL
- **Query:** The exhaust manifolds cracked over the winter even though I thought I winterized the engine — now there's coolant leakin
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/5 kw
- **Missing keywords:** exhaust elbow, water jacket, EST, drain plug, antifreeze
- **Gus said:** You've identified cracked exhaust manifolds, which is a common result of improper winterization and freeze damage. Before we proceed with replacing the manifolds, we need to confirm the full extent of
- **Fingerprint:** 8d7113a907bc6519

### mc_winter_003 — FAIL
- **Query:** The freshwater cooling system pump cracked over the winter — coolant leaked out when I opened the engine compartment in 
- **State:** PHASE_C_TESTING
- **Detail:** 1/4 kw
- **Missing keywords:** circulating pump, antifreeze, block drain
- **Gus said:** You've identified the cracked freshwater cooling system pump. Replace the pump. Once the new pump is installed, you must properly fill and air bleed the closed cooling system to prevent engine overhea
- **Fingerprint:** 4646fa6a9e3479ec

### mc_drive_007 — FAIL
- **Query:** The drive makes a horrible grinding noise when I try to go forward — it's like the gears aren't engaging.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/4 kw
- **Missing keywords:** forward gear, clutch dog, gear lube
- **Gus said:** A grinding noise when attempting forward engagement, indicating the gears aren't fully meshing, suggests a problem with the shift mechanism or internal drive components. We need to verify the shift sy
- **Fingerprint:** d15a3e156cf7a054

### mc_drive_008 — FAIL
- **Query:** The prop is dinged up and the boat doesn't perform like it used to — it's slower and uses more fuel.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/5 kw
- **Missing keywords:** Alpha One, Alpha, Bravo, drive shaft
- **Gus said:** A dinged-up propeller is a direct cause of reduced performance and increased fuel consumption. Before we dig deeper, we need to assess the propeller's condition and the boat's hull. We also need to ge
- **Fingerprint:** ec45665e4def710e

### mc_cool_007 — FAIL
- **Query:** The engine overheats intermittently — sometimes it's fine, sometimes the alarm goes off. The mechanic found a hose that 
- **State:** PHASE_D_CONCLUSION
- **Detail:** 1/3 kw
- **Missing keywords:** hose clamp, water hose
- **Gus said:** The collapsing hose is restricting the seawater flow to the engine, causing insufficient cooling and the intermittent overheating. Replace the identified collapsing seawater inlet hose immediately. Af
- **Fingerprint:** 8abc40cfd53132d4

### mc_trans_005 — FAIL
- **Query:** The drive feels loose in the mount and there are visible cracks in the aluminum housing behind the transom.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/3 kw
- **Missing keywords:** gimbal bearing, bellows
- **Gus said:** The visible cracks in the aluminum housing behind the transom are a serious concern. We need to determine the extent of this structural damage and identify if loose engine mounts or improper engine-to
- **Fingerprint:** 8e9bd01cae572dca

### mc_eng_011 — FAIL
- **Query:** The engine has gradually lost power and the timing seems retarded — the chain has stretched.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/4 kw
- **Missing keywords:** oil pump, timing cover, harmonic balancer
- **Gus said:** You've identified a potential timing issue and suspect a stretched timing chain. This is a solid lead, as mechanical timing directly impacts engine performance. However, electronic systems can also ca
- **Fingerprint:** 5cc67a99e7ac07cf

### mc_trim_004 — FAIL
- **Query:** My trim tab on the bottom of the outdrive is broken or corroded away — the boat doesn't track straight.
- **State:** PHASE_A_TRIAGE
- **Detail:** 2/7 kw
- **Missing keywords:** zinc, EST, sacrificial anode, zinc anode, stray current
- **Gus said:** The boat not tracking straight with a broken or corroded trim tab indicates a direct issue with steering stability. The trim tab is designed to counteract propeller torque and keep the boat tracking s
- **Fingerprint:** 3424e5a7304a724a

### mc_drive_010 — FAIL
- **Query:** The drive makes noise and the gear lube was low when I checked — I can't figure out where it went.
- **State:** PHASE_A_TRIAGE
- **Detail:** 2/8 kw
- **Missing keywords:** EST, Alpha One, Alpha, Bravo, drive shaft, prop shaft
- **Gus said:** We need to pinpoint where that gear lube went and confirm the source of the noise.

1.  **Inspect for Gear Lube Leaks:** Thoroughly inspect the entire sterndrive unit for any visible signs of gear lub
- **Fingerprint:** 39e62644bef5d406

### mc_exh_006 — FAIL
- **Query:** The exhaust smells stronger than normal inside the boat and I can see rust and corrosion on the Y-shaped pipe at the bac
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/3 kw
- **Missing keywords:** exhaust bellows, bellows
- **Gus said:** The strong exhaust smell and visible corrosion on the Y-pipe indicate an exhaust leak. You need to physically inspect the Y-pipe and all its connections, including hoses and gaskets, for the source of
- **Fingerprint:** 81ffc9feb908eb35

### mc_cool_009 — FAIL
- **Query:** The engine temperature fluctuates and the cooling doesn't seem consistent — the water pump belt squeals occasionally.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/3 kw
- **Missing keywords:** circulating pump, alternator
- **Gus said:** The occasional squealing of the water pump belt is a critical symptom. This suggests the belt may be slipping, leading to inconsistent operation of the seawater pickup pump and thus fluctuating engine
- **Fingerprint:** e5a2a4eec19887ba

### mc_eng_015 — FAIL
- **Query:** There's a visible wobble at the front of the engine and the drive belt keeps coming off.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/4 kw
- **Missing keywords:** harmonic balancer, front seal, EST
- **Gus said:** The visible wobble and belt coming off indicates a mechanical failure in the serpentine drive system. We need to identify the source of the wobble. This could be a bent or damaged pulley, a worn beari
- **Fingerprint:** 1c482de1de2ab679

### mc_drive_014 — FAIL
- **Query:** My Bravo drive is leaking gear oil from around the rear prop area and making a grinding noise.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/5 kw
- **Missing keywords:** Alpha, prop shaft, bearing carrier, gear lube
- **Gus said:** The gear oil leak and grinding noise from the Bravo drive suggest internal damage. We need to confirm the source of the leak and the condition of the drive unit's internal components. First, visually 
- **Fingerprint:** 408bedf177fdb054

### mc_cool_011 — FAIL
- **Query:** The engine overheats shortly after a coolant change or system repair — the temperature gauge shoots up quickly.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/4 kw
- **Missing keywords:** engine mount, overheat alarm, EST
- **Gus said:** The first step is to verify if the engine is actually overheating or if the temperature gauge or sender is faulty. Use an external temperature measurement tool, like an infrared thermometer, to confir
- **Fingerprint:** fcd8863e7288cafa

### mc_trans_007 — FAIL
- **Query:** The steering is stiff and hard to turn — the drive doesn't pivot smoothly side to side.
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/2 kw
- **Missing keywords:** bellows, gimbal ring
- **Gus said:** The steering being stiff and the drive not pivoting smoothly indicates a problem with the power steering system. We need to start by checking the basics: fluid level and the drive belt. Low fluid, air
- **Fingerprint:** ef743fb4f1664f8b

### mc_corr_004 — FAIL
- **Query:** Individual metal components on the boat are corroding at different rates — some are fine and others are being destroyed.
- **State:** PHASE_A_TRIAGE
- **Detail:** 1/5 kw
- **Missing keywords:** zinc, trim tab, zinc anode, bonding wire
- **Gus said:** The varying rates of corrosion on individual metal components point directly to an issue with the boat's galvanic corrosion protection. Your first step is to physically inspect the sacrificial anodes 
- **Fingerprint:** f01d69924acbb0c0

### mc_trim_005 — FAIL
- **Query:** The trim works intermittently — sometimes it responds and other times nothing happens when I press the button.
- **State:** PHASE_A_TRIAGE
- **Detail:** 0/2 kw
- **Missing keywords:** relay, trim pump
- **Gus said:** An intermittent trim system points directly to an electrical issue, most likely a poor connection or faulty wiring. The fault must be present to locate the problem. Perform a careful visual and physic
- **Fingerprint:** 8b57bfc19a9b692d

### mc_trim_006 — FAIL
- **Query:** The drive slams down when I release the trim button — it won't hold in the tilted-up position for trailering.
- **State:** PHASE_A_TRIAGE
- **Detail:** 2/6 kw
- **Missing keywords:** Alpha, Bravo, trim pump, trim ram
- **Gus said:** The drive unit slamming down when the trim button is released indicates a loss of hydraulic pressure in the trim system. This could be due to an external leak, an internal leak within the trim cylinde
- **Fingerprint:** 0555371de76e3fd1

### mc_fuel_013 — FAIL
- **Query:** The fuel lines on my boat are automotive-grade rubber and are not Coast Guard approved — the surveyor flagged them.
- **State:** PHASE_D_CONCLUSION
- **Detail:** 0/1 kw
- **Missing keywords:** hose clamp
- **Gus said:** The automotive-grade fuel lines must be replaced immediately with Coast Guard approved (USCG Type A1) fuel lines. This is not a diagnostic step, but a mandatory safety and compliance repair. 

Before 
- **Fingerprint:** c762b282e35d9420


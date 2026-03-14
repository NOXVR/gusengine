# Cessna 172 — FSM vs. Gus: Side-by-Side Proof Document

**Authority**: 1975 Cessna 172 & Skyhawk Series Service Manual (1969-1976)
**Test Run**: `20260314_143352` — 60 queries, 0 errors
**Methodology**: Gus's verbatim response compared against FSM troubleshooting tables.
**Reader verifiable**: Open the same PDF, turn to the cited page, read the same table.

---

## Fault 01 — ENGINE WILL NOT START

**FSM Reference**: Section 11-9, Engine Troubleshooting, Part 4 p.4

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | ENGINE WILL NOT START |
| **Probable Cause** | Fuel selector valve not turned on; Fuel tanks empty; Fuel line disconnected or broken; Defective magneto or fouled spark plugs; Primer not functioning |
| **Remedy** | Turn selector valve on; Service with proper grade of fuel; Connect or repair fuel lines; Repair or replace magneto, clean/gap/replace spark plugs; Repair or replace primer |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"I can't get my plane to start. It just cranks and cranks but nothing happens."*
**Response time**: 61.65s

**Gus Diagnosis**:
> We need to systematically check the primary systems required for engine start: fuel, spark, and compression. Start with the most common and easiest to verify:

1.  **Fuel System Check:** Confirm adequate fuel in the tanks. Then, open the fuel strainer drain (refer to Section 12 for location) and check for water or contaminants. Ensure the fuel selector valve is in an 'ON' position to a tank known to contain fuel.
2.  **Ignition System Check (Spark):** Remove a spark plug, ground it, and observe for spark while cranking the engine. Alternatively, perform a magneto check as outlined in paragraph 11-59, noting any absence of RPM drop.
3.  **Ignition System Check (Impulse Coupling):** Listen for the distinct 'clicks' of the impulse coupling engaging during cranking. This indicates the coupling is operating. If no clicks are heard, the impulse coupling may be faulty (refer to paragraph 11-58).
4.  **Fuel System Check (Vent):** Inspect the fuel vent line (protruding beneath the wing) for obstructions. You can attach a rubber tube and blow into it to check for openness, then insert it into water to check the bleed hole for continuous bubbles, as described in paragraph 12-11.
5.  **Engine Mechanical Check (Compression):** If fuel and spark are confirmed to be present and normal, perform an engine compression check on all cylinders. Refer to the engine Manufacturer's Manual for specific procedures, as mentioned in paragraph 11A-18A.4.

**Answer Paths Offered**:
> - Fuel is present in the tanks, the selector valve is ON, and the fuel strainer drain shows clean fuel with no water. However, the engine still won't start.
> - No fuel is reaching the carburetor, or the fuel strainer drain shows significant water/contaminants, or the fuel selector valve was OFF/tanks are empty.
> - There is no spark at the spark plugs when grounded and cranked, or the magneto check shows no RPM drop on either magneto.
> - The impulse coupling does not produce a distinct 'click' sound during engine cranking.
> - The fuel vent line is found to be plugged or restricted when checked per paragraph 12-11.
> - A compression check reveals significantly low compression on one or more cylinders.

#### Expert Pilot
**Query**: *"Engine cranks normally but won't fire. I've verified battery and starter engagement. Suspect fuel delivery issue."*
**Response time**: 63.02s

**Gus Diagnosis**:
> You've confirmed the starter is engaging. Now we need to verify the engine is getting fuel and spark. Let's start with fuel, as you suspect. First, confirm the fuel supply and flow to the carburetor. Then, we'll check for spark.

**Answer Paths Offered**:
> - Fuel tanks are full, selector valve is ON, and fuel flows freely from the carburetor drain.
> - Fuel tanks are full, selector valve is ON, but no fuel or only a trickle comes from the carburetor drain.
> - Fuel tanks are empty or the selector valve is OFF.
> - I've checked for spark at the plugs, and there is no spark on any cylinder.

#### A&P Mechanic
**Query**: *"Engine cranks, no start. What does the FSM troubleshooting table list as probable causes for a no-start condition?"*
**Response time**: 56.44s

**Gus Diagnosis**:
> The engine is cranking but not starting. We need to determine if the issue is with fuel, spark, or air/compression. Start by checking the most common and easily verifiable items first.

**Answer Paths Offered**:
> - Fuel tanks are full, and the fuel selector valve is in the 'ON' position. I've also drained the fuel strainer and found no water or debris.
> - I've removed a spark plug and confirmed there is no spark when cranking the engine.
> - I've removed a spark plug and confirmed there IS spark when cranking the engine, but the plugs appear wet with fuel, indicating flooding.
> - I've removed a spark plug and confirmed there IS spark when cranking the engine, but the plugs appear dry, and I've confirmed fuel flow to the carburetor.

---

## Fault 02 — ENGINE WILL NOT START (Ignition)

**FSM Reference**: Section 11-9, Engine Troubleshooting, Part 4 p.4

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | ENGINE WILL NOT START (Ignition) |
| **Probable Cause** | Defective magneto; Fouled or defective spark plugs; Defective ignition harness or switch |
| **Remedy** | Repair or replace magneto; Clean, gap, or replace spark plugs; Repair or replace harness/switch |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"My plane won't start and it was fine last week. I don't know what's wrong."*
**Response time**: 40.94s

**Gus Diagnosis**:
> We need to determine if the engine is receiving fuel and spark, and if the starter system is functioning correctly. Start by checking the most basic elements. First, confirm the battery has enough charge to crank the engine, then verify fuel supply and check for contamination.

**Answer Paths Offered**:
> - The starter motor engages and cranks the engine normally, but it doesn't catch and start.
> - The starter motor clicks but does not crank the engine, or cranks very slowly.
> - The starter motor does nothing at all when the key is turned.
> - I have confirmed the fuel tanks are full and the selector valve is ON, but I found water in the fuel strainer when I drained it.

#### Expert Pilot
**Query**: *"No start condition. During last mag check before shutdown, I noticed an abnormal RPM drop on the left mag. Now it won't fire at all."*
**Response time**: 42.47s

**Gus Diagnosis**:
> Given the abnormal RPM drop on the left magneto and the current no-start condition, we need to isolate the fault within the left ignition system. First, check the electrical integrity of the left magneto's 'P' lead, then inspect the spark plugs and ignition harness. Finally, if those are clear, we'll look at the magneto itself.

**Answer Paths Offered**:
> - The left magneto 'P' lead shows continuity to ground with the ignition switch in the 'ON' position.
> - Inspection of the spark plugs from the cylinders associated with the left magneto reveals heavy fouling or improper gapping, or the ignition harness shows visible damage.
> - Fuel is not reaching the carburetor, or the carburetor drain shows water/sediment.
> - All spark plugs, ignition harness, and 'P' lead continuity for the left magneto check out as normal.

#### A&P Mechanic
**Query**: *"No-start, good fuel flow confirmed at the gascolator. Suspect ignition system. What are the FSM-listed ignition causes for a no-start?"*
**Response time**: 47.82s

**Gus Diagnosis**:
> For a no-start condition, even with good fuel flow at the gascolator, we need to systematically check for spark, fuel quality at the carburetor, and proper control settings. Start by confirming spark at the cylinders, as this is the most direct way to verify the primary ignition path.

**Answer Paths Offered**:
> - I checked for spark at the spark plugs (removed one, grounded it, and observed while cranking / used an ignition tester), and there IS spark.
> - I checked for spark at the spark plugs, and there is NO spark.
> - I drained the carburetor bowl and found significant water contamination.
> - I verified the mixture control is in the full RICH position, and it was correctly set.
> - I disconnected the magneto 'P' lead at the magneto (with all safety precautions observed) and attempted to start. The engine still did not start.

---

## Fault 03 — ENGINE STARTS BUT DIES

**FSM Reference**: Section 11-9, Engine Troubleshooting, Part 4 p.5

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | ENGINE STARTS BUT DIES |
| **Probable Cause** | Mixture control not in full rich; Idle speed set too low; Fuel contamination |
| **Remedy** | Set mixture to full rich; Adjust idle speed; Drain and service fuel system |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"It starts up but then immediately dies a few seconds later. I have to keep restarting it."*
**Response time**: 65.05s

**Gus Diagnosis**:
> We need to isolate whether the issue is with basic fuel supply, the carburetor's ability to maintain fuel flow, or another system. Start by verifying the fundamental fuel controls and then perform a priming test.

**Answer Paths Offered**:
> - I confirmed the fuel tanks are NOT empty, the fuel selector valve is ON, and the mixture control is in the FULL RICH position. The engine still starts and dies.
> - When I keep the primer active, the engine continues to run, but dies immediately once priming is stopped (with mixture control in FULL RICH).
> - I drained the fuel strainer and found significant water or debris in the fuel.
> - I checked the spark plugs, and they are heavily fouled or improperly gapped.
> - I visually inspected the induction system and found a noticeable air leak, or I disconnected the primer outlet line and found fuel leaking from the primer.

#### Expert Pilot
**Query**: *"Engine fires but won't sustain idle. It catches for 2-3 seconds then quits. Happens consistently."*
**Response time**: 48.76s

**Gus Diagnosis**:
> The engine fires but won't sustain idle, dying after 2-3 seconds. This points to an issue with the engine's ability to maintain combustion without external assistance, likely due to improper fuel-air mixture at idle. We need to determine if the engine is starving for fuel, running too lean, or too rich, or if there's an ignition issue. Your next step is to observe the engine's behavior during and immediately after priming.

**Answer Paths Offered**:
> - Engine starts when primed, but immediately dies when priming is discontinued, even with the mixture control in the full RICH position.
> - Engine starts, but runs very rough and dies, and you can visually identify loose or cracked induction hoses, or hear a distinct hissing sound indicating an air leak around the carburetor or intake manifold.
> - Engine starts, but runs very rough, and a quick check of the spark plugs reveals them to be heavily fouled or improperly gapped.
> - Engine starts, but runs excessively rich (e.g., black smoke, strong fuel smell), and you find fuel leaking from the manual primer outlet line, or suspect a high float level.
> - The issue primarily occurs in hot weather or with a hot engine, and you suspect vapor formation in the fuel system.

#### A&P Mechanic
**Query**: *"Engine starts, runs briefly, dies. Repeatable condition. What does the FSM list for engine starts but dies?"*
**Response time**: 63.78s

**Gus Diagnosis**:
> The engine starts briefly and then dies, which is a classic symptom of a fuel delivery issue preventing sustained operation. We need to determine if the carburetor is capable of maintaining the engine once the initial prime is consumed, or if there's a more fundamental fuel supply, air, or ignition problem. Perform the following checks and report your observations:

**Answer Paths Offered**:
> - The engine starts when primed, but dies immediately when priming is stopped, even with the mixture control in the full RICH position.
> - The engine does not start at all, even with priming, or the fuel strainer drain shows water or significant debris.
> - The engine starts, but runs very rough, and a magneto drop check (per paragraph 11-59) shows an excessive RPM drop on one magneto.
> - A visual inspection reveals obvious induction air leaks (e.g., loose hoses, cracked gaskets) or a compression check shows low readings on one or more cylinders.

---

## Fault 04 — ENGINE ROUGH / RUNS ROUGH AT IDLE

**FSM Reference**: Section 11-9, Engine Troubleshooting, Part 4 p.5

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | ENGINE ROUGH / RUNS ROUGH AT IDLE |
| **Probable Cause** | Idle mixture too rich or too lean; Fouled spark plugs; Defective magneto |
| **Remedy** | Adjust idle mixture; Clean or replace spark plugs; Repair or replace magneto |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"My plane shakes a lot when it's just sitting there running on the ground. Feels rough."*
**Response time**: 53.88s

**Gus Diagnosis**:
> The rough running at idle suggests an issue with combustion or engine vibration isolation. We need to start by checking the ignition system. Perform a magneto check as outlined in paragraph 11-59 of the Service Manual. This will help determine if the issue is related to the magnetos, spark plugs, or ignition harness. Also, visually inspect the engine mounts and carburetor heat control for obvious issues.

**Answer Paths Offered**:
> - The RPM drop on one or both magnetos exceeds 125 RPM, or the differential between magnetos is greater than 50 RPM, or there is no RPM drop.
> - The RPM drop is within limits (not exceeding 125 RPM on either magneto, and less than 50 RPM differential), and the engine mounts appear visually sound with no cracks or excessive play.
> - The carburetor heat control is partially open or improperly rigged, or the induction air filter is visibly restricted.

#### Expert Pilot
**Query**: *"Rough running at idle, RPM fluctuating about 50 RPM. Smooths out above 1200 RPM."*
**Response time**: 62.28s

**Gus Diagnosis**:
> The engine is running rough at idle with RPM fluctuations, but smooths out above 1200 RPM. This indicates a problem with the idle circuit, ignition at low RPM, or an air leak. We need to check the idle speed and mixture adjustment first, as this is a common cause for such symptoms. Perform the idle speed and mixture adjustment procedure as follows:

1.  Start and run the engine until oil and cylinder head temperatures are in the normal operating range.
2.  Advance engine speed to approximately 1000 RPM, then retard the throttle to the idle position. The engine RPM should stabilize at 600 ± 25 RPM. If not, adjust the idle speed screw IN to increase and OUT to decrease RPM. (Refer to paragraph 11-45.c, Source 17)
3.  Once idle speed is stabilized, slowly move the mixture control toward the IDLE CUT-OFF position and observe the tachometer for any minute change. A momentary increase of approximately 25 RPM is desirable. An increase of more than 25 RPM indicates a rich idle mixture, and an immediate decrease (without a momentary increase) indicates a lean idle mixture. (Refer to paragraph 11-45.d, f, Source 14, 17)
4.  Quickly return the mixture control to the FULL RICH position before the engine stops. (Refer to paragraph 11-45.e, Source 14)
5.  If the idle mixture is too rich, turn the idle mixture adjustment center screw one or two notches clockwise. If too lean, turn it one or two notches counterclockwise. After each adjustment, run the engine up to approximately 1800 RPM to clear excess fuel and obtain a correct idle speed, then repeat steps 3 and 4. (Refer to paragraph 11-45.g, h, Source 14, 29, 37)

Report your observations during this process.

**Answer Paths Offered**:
> - I adjusted the idle mixture, and the engine now idles smoothly at 600 RPM with a 25 RPM rise before cut-off.
> - I adjusted the idle mixture, but the engine still runs rough, or the RPM rise during cut-off is incorrect/unstable.
> - I performed the magneto check (paragraph 11-59) and found an RPM drop exceeding 125 RPM on one magneto, or a differential greater than 50 RPM between magnetos, or a sharp RPM drop-off.

#### A&P Mechanic
**Query**: *"Rough idle, stable at higher RPM. Suspect mixture or spark plug issue. What does the FSM troubleshooting say?"*
**Response time**: 54.84s

**Gus Diagnosis**:
> Start by performing a magneto check to assess the ignition system, as this can quickly identify issues with spark plugs, ignition harness, or the magnetos themselves. This procedure is outlined in paragraph 11-59 of the Service Manual. You'll need to run the engine to 1700 RPM and observe the RPM drop when switching to 'R' and 'L' magneto positions. A sharp drop-off or excessive differential indicates an issue.

**Answer Paths Offered**:
> - The RPM drop on one magneto is significantly higher than the other, or exceeds 125 RPM on either side, or the drop is sharp and erratic.
> - The RPM drop is within limits (not exceeding 125 RPM on either magneto, and less than 50 RPM differential), and the engine runs smoothly on both magnetos individually.
> - The engine runs rough even at 1700 RPM, and the magneto check results are inconsistent or difficult to interpret.

---

## Fault 05 — ENGINE LOSES POWER / LOSS OF POWER IN FLIGHT

**FSM Reference**: Section 11-9, Engine Troubleshooting, Part 4 p.5

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | ENGINE LOSES POWER / LOSS OF POWER IN FLIGHT |
| **Probable Cause** | Carburetor icing; Plugged fuel strainer; Defective magneto; Incorrect mixture |
| **Remedy** | Apply carburetor heat; Clean fuel strainer; Replace magneto; Adjust mixture |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"I was flying and the engine just got weaker and weaker. Like it was losing its strength."*
**Response time**: 60.07s

**Gus Diagnosis**:
> The engine losing strength progressively during flight indicates a reduction in power output. We need to narrow down whether this is a fuel delivery issue, an ignition problem, an air intake restriction, or something more severe. To start, observe the engine's response to controls and check for basic system functionality.

**Answer Paths Offered**:
> - When you slowly pull the mixture control to idle cut-off, does the RPM rise slightly before dropping, or does it drop immediately and sharply?
> - During a magneto check (if performed), was there an excessive RPM drop on either magneto, or a rough running condition?
> - Was there any indication of carburetor icing, and did applying carburetor heat have any effect on engine power or smoothness?
> - Were there any unusual engine noises, vibrations, or abnormal gauge readings (oil pressure, oil temperature, cylinder head temperature) when the power loss began?

#### Expert Pilot
**Query**: *"Gradual power loss in cruise at 5,000 feet. Applied carb heat with momentary further power loss then partial recovery. Outside temp around 40F, visible moisture."*
**Response time**: 61.66s

**Gus Diagnosis**:
> The symptoms strongly suggest carburetor icing, but we need to confirm this and rule out other fuel/air system issues. Perform the following checks:

**Answer Paths Offered**:
> - Re-apply carburetor heat and observe the engine RPM and manifold pressure (if equipped). Does the RPM/MP drop further momentarily, then recover or increase?
> - Inspect the fuel tank vent line, especially the portion protruding beneath the wing. Is there any visible ice accumulation or other blockage?
> - Visually inspect the induction air filter for any signs of blockage, dirt, or damage. Is it clean and unobstructed?

#### A&P Mechanic
**Query**: *"Reported power loss in flight. Carb heat partially restored power. What are the FSM-listed causes for in-flight power loss?"*
**Response time**: 56.31s

**Gus Diagnosis**:
> Given that carburetor heat partially restored power, we need to investigate the fuel system, the induction air system, and the integrity of the carburetor heat system itself. Your next step is to physically inspect the fuel and induction systems for obvious issues and verify the functionality of the carburetor heat system. Start by checking for water in the fuel, as this is a common issue that can cause power loss and might be temporarily masked by carb heat.

**Answer Paths Offered**:
> - I drained the fuel strainer and found significant water and sediment.
> - The carburetor heat control moves freely, but the airbox flap does not fully open/close, or the flexible ducting is damaged.
> - The induction air filter is visibly clogged with debris.
> - I performed a magneto check (per 11-59) and found an RPM drop exceeding 125 RPM on one magneto, or a differential greater than 50 RPM between magnetos.

---

## Fault 06 — NO FUEL TO CARBURETOR

**FSM Reference**: Section 12-4, Fuel System Troubleshooting, Part 5 p.36-37

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | NO FUEL TO CARBURETOR |
| **Probable Cause** | Fuel selector valve not turned on; Fuel line disconnected or broken; Plugged fuel strainer; Defective fuel selector valve; Fuel tank outlet strainers plugged |
| **Remedy** | Repair or replace selector valve; Connect or repair fuel lines; Remove and clean strainer and screen; Repair or replace selector valve; Remove and clean strainers, flush fuel tanks |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"The engine stopped getting gas I think. It just quit in the air."*
**Response time**: 61.83s

**Gus Diagnosis**:
> We need to determine if the engine quit due to a lack of fuel, contaminated fuel, or an ignition issue. Your next steps should focus on physical verification of the fuel system and a basic check of engine response.

**Answer Paths Offered**:
> - The fuel selector valve was in the 'BOTH ON' position, and both fuel gauges indicated approximately 1/4 tank each before the engine quit.
> - I drained the fuel strainer and tank sumps. There was some water and sediment in the strainer, and the fuel flow was intermittent.
> - When attempting to restart, the engine cranks normally but shows no signs of combustion (no firing, no sputtering).
> - I attempted to prime the engine. It sputtered briefly but did not start, then went back to no combustion.

#### Expert Pilot
**Query**: *"Engine-out in flight. Fuel selector was confirmed on BOTH. Fuel gauges showed quantity remaining in both tanks."*
**Response time**: 59.21s

**Gus Diagnosis**:
> Given the engine-out in flight, we need to quickly determine the most likely cause to attempt a restart or prepare for a forced landing. Your immediate observations and actions are critical. Consider the following:

**Answer Paths Offered**:
> - When attempting a restart, the engine briefly fires or sputters when the primer is used, but then dies when priming stops.
> - When attempting a restart, the engine does NOT respond at all to the primer, and the propeller windmills freely.
> - When attempting a restart, the engine does NOT respond at all to the primer, and the propeller is seized or very difficult to turn.
> - Before the engine quit, it sputtered or ran rough, and carburetor heat was NOT applied or was applied too late.

#### A&P Mechanic
**Query**: *"Fuel starvation event. Selector valve operative, tanks have fuel. What does the 12-4 troubleshooting table say about no fuel to the carburetor?"*
**Response time**: 44.55s

**Gus Diagnosis**:
> The 12-4 troubleshooting table for 'NO FUEL TO CARBURETOR' lists several probable causes, even with the selector valve operative and tanks full. We need to systematically check for obstructions and contamination. Your next step is to physically inspect the fuel system for these issues. Start by checking for water and sediment, then verify the integrity of the fuel path.

**Answer Paths Offered**:
> - You drain the fuel strainer and tank sumps, finding significant water or sediment.
> - You check the main fuel strainer and find it clean, but blowing into the fuel vent line (per paragraph 12-11) reveals a blockage.
> - You disconnect the fuel line at the carburetor and observe no fuel flow, but the main fuel strainer is clean and the vent line is clear.
> - You disconnect the fuel line at the carburetor and observe good fuel flow, indicating the issue is at or within the carburetor itself.

---

## Fault 07 — STARTING (fuel related)

**FSM Reference**: Section 12-4, Fuel System Troubleshooting, Part 5 p.37

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | STARTING (fuel related) |
| **Probable Cause** | Water in fuel |
| **Remedy** | Drain fuel tank sumps, fuel lines and fuel strainer |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"It starts but sputters and coughs. It rained all week and the plane was outside."*
**Response time**: 65.26s

**Gus Diagnosis**:
> Given the recent rain exposure, we need to systematically check for moisture in the fuel and ignition systems. Start by draining the fuel sumps and strainer to check for water. Then, perform a magneto check to assess the ignition system's performance. Finally, inspect the spark plugs for any signs of fouling or moisture.

**Answer Paths Offered**:
> - When draining the fuel sumps and strainer, I observed significant water contamination.
> - During the magneto check (FSM 11-59), I noted an excessive RPM drop or no drop on one or both magnetos.
> - Upon removing the spark plugs, I found them to be wet, fouled, or improperly gapped.

#### Expert Pilot
**Query**: *"Engine surging and misfiring intermittently. Aircraft sat outside in rain for five days untied down. Suspect contamination."*
**Response time**: 59.95s

**Gus Diagnosis**:
> Given the aircraft's exposure to rain and your suspicion of contamination, the first step is to check for water in the fuel system. Water is denser than fuel and will settle at the lowest points. Open the fuel strainer drain and all fuel tank sumps to collect samples. Observe the samples for any signs of water or sediment.

**Answer Paths Offered**:
> - You find significant water and/or sediment in the fuel drained from the strainer and tank sumps.
> - You find no significant water or sediment in the fuel drained from the strainer and tank sumps, but the engine still surges and misfires.
> - You find no significant water or sediment, and after draining, the engine runs smoothly.

#### A&P Mechanic
**Query**: *"Intermittent misfire and rough running after extended outdoor parking in rain. Suspect water contamination. What is the FSM procedure?"*
**Response time**: 60.73s

**Gus Diagnosis**:
> Given the intermittent misfire and rough running after rain, we need to systematically check for water contamination and ignition system integrity. Start by checking the fuel system for water, then visually inspect the ignition components, and finally perform a magneto check to assess overall ignition performance.

**Answer Paths Offered**:
> - You drain the fuel sumps and carburetor. Do you observe any water or sediment in the drained fuel?
> - You visually inspect the spark plug leads, spark plugs, and ignition harness for signs of moisture, corrosion, or physical damage. What do you find?
> - You perform an engine run-up and magneto check as per Section 11-59. What are the RPM drop readings for each magneto, and do you observe any sharp or smooth drops?

---

## Fault 08 — PRESSURIZED FUEL TANK

**FSM Reference**: Section 12-4, Fuel System Troubleshooting, Part 5 p.37

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | PRESSURIZED FUEL TANK |
| **Probable Cause** | Plugged fuel vent |
| **Remedy** | Check per paragraph 12-13 |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"When I took the fuel cap off it was like opening a soda bottle. There was pressure in there."*
**Response time**: 65.19s

**Gus Diagnosis**:
> The pressurized fuel tank indicates a restriction in the venting system. We need to check the fuel vent line and the bleed hole in the vent valve assembly. Refer to Section 12-11, 'CHECKING' in the Service Manual. (Source 47, page 2; Source 11, page 3)

1.  Attach a rubber tube to the end of the vent line protruding beneath the wing.
2.  Blow into the tube to slightly pressurize the tank. This checks if the vent line is open.
3.  After slightly pressurizing the tank, insert the end of the rubber tube into a container of water and watch for a continuous stream of bubbles. This indicates if the bleed hole in the valve assembly is open and relieving pressure.

What do you observe during this test?

**Answer Paths Offered**:
> - Air can be blown into the tank, but there are no continuous bubbles in the water, or the bubbles stop quickly.
> - Air cannot be blown into the tank at all.
> - Air can be blown into the tank, and there is a continuous stream of bubbles in the water.
> - The vent line is visibly kinked or damaged.

#### Expert Pilot
**Query**: *"Fuel cap difficult to remove, audible pressure release upon opening. Fuel seemed to bulge up when uncapped."*
**Response time**: 44.56s

**Gus Diagnosis**:
> The symptoms indicate a pressurized fuel tank. We need to check the fuel vent system. Refer to Section 12-11, 'CHECKING' in the Service Manual. This procedure will help determine if the vent line, the bleed hole in the vent valve, or the crossover line is obstructed. Begin by accessing the vent line beneath the wing.

**Answer Paths Offered**:
> - Air can be blown into the vent line, but no continuous stream of bubbles appears when the tube is placed in water, or pressure does not escape from the opposite tank's filler cap when loosened. (Indicates plugged bleed hole or crossover line issue)
> - Air cannot be blown into the vent line at all. (Indicates a completely plugged vent line)
> - Air can be blown into the vent line, a continuous stream of bubbles appears in water, and pressure escapes from the opposite tank's filler cap. (Indicates vent system is clear, suggesting an issue with the fuel cap itself or another less common cause)

#### A&P Mechanic
**Query**: *"Pressurized fuel tank condition. What is the FSM-listed probable cause and correction for a pressurized tank?"*
**Response time**: 22.12s

**Gus Diagnosis**:
> For a pressurized fuel tank, the FSM-listed probable cause is a plugged bleed hole in the fuel vent. The correction involves checking the fuel vent and bleed hole for obstructions. Perform the following procedure as outlined in paragraph 12-11 of the Service Manual:

1.  Attach a rubber tube to the end of the vent line beneath the wing.
2.  Blow into the tube to slightly pressurize the tank. If air can be blown into the tank, the vent line is open.
3.  After the tank is slightly pressurized, insert the end of the rubber tube into a container of water and watch for a continuous stream of bubbles. This indicates the bleed hole in the valve assembly is open and relieving pressure.
4.  After completing step 'c', blow into the tube again to slightly pressurize the tank, and loosen (but do not remove) the filler cap on the opposite wing to check the tank crossover line. If pressure escapes from the filler cap, the crossover line is open.
5.  Any fuel vent found plugged or restricted must be corrected prior to returning the aircraft to service.

---

## Fault 09 — NO FUEL QUANTITY INDICATION

**FSM Reference**: Section 12-4 + 15-45, Part 5 p.37

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | NO FUEL QUANTITY INDICATION |
| **Probable Cause** | Open circuit; Defective fuel quantity transmitter |
| **Remedy** | Tighten connections; repair or replace wiring. Refer to Section 15 and 20 |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"The fuel gauge doesn't work. It just sits on empty even though I know there's fuel in there."*
**Response time**: 42.48s

**Gus Diagnosis**:
> The fuel gauge reading empty with fuel in the tank indicates a fault in the fuel quantity indicating system. First, check the circuit breaker for the fuel quantity system. If it's tripped, reset it. If it trips again or is already good, we need to check the electrical path to the fuel quantity transmitter in the tank. This will help us determine if the issue is with the wiring, the transmitter, or the gauge itself.

**Answer Paths Offered**:
> - The fuel quantity circuit breaker was tripped, and resetting it restored the gauge function.
> - The fuel quantity circuit breaker was tripped, but it immediately tripped again after resetting.
> - The fuel quantity circuit breaker is not tripped and appears to be in good condition.
> - I cannot locate a specific circuit breaker for the fuel quantity system.

#### Expert Pilot
**Query**: *"Left fuel quantity gauge reads zero despite confirmed fuel in the tank. Right gauge reads normally."*
**Response time**: 72.37s

**Gus Diagnosis**:
> We need to determine if the issue is electrical continuity, the sensing unit, or the gauge itself. Begin by checking the electrical integrity of the left fuel quantity system.

**Answer Paths Offered**:
> - The fuel quantity circuit breaker for the left tank is tripped (popped out).
> - The electrical lead or ground strap at the left fuel quantity transmitter is visibly loose, corroded, or disconnected.
> - The left fuel quantity gauge needle flickers or moves slightly when the master switch is cycled ON/OFF, or when the gauge is gently tapped.
> - All other electrical instruments and lights on the main bus are functioning normally, with no other electrical anomalies observed.

#### A&P Mechanic
**Query**: *"No fuel quantity indication on left tank gauge. Circuit breaker is in. What does the FSM say about fuel quantity indication failure?"*
**Response time**: 57.37s

**Gus Diagnosis**:
> You have no fuel quantity indication on the left tank gauge, and the circuit breaker is confirmed to be in. We need to systematically check the fuel system and the electrical circuit for the gauge. First, verify the actual fuel level in the left tank. Then, we'll check the electrical supply to the gauge and the integrity of the wiring and components.

**Answer Paths Offered**:
> - The left fuel tank is visually confirmed to be full or partially full.
> - The left fuel tank is visually confirmed to be empty.
> - There is no voltage at the fuel quantity indicator on the instrument panel.
> - There is voltage at the fuel quantity indicator, but the gauge still reads empty/no indication.

---

## Fault 10 — NO OIL PRESSURE

**FSM Reference**: Section 11A-31, Engine Troubleshooting, Part 4 p.34

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | NO OIL PRESSURE |
| **Probable Cause** | Insufficient oil; Defective pressure relief valve; Defective oil pump |
| **Remedy** | Service oil to proper level; Replace relief valve; Replace or repair oil pump |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"There's a red light on the dashboard that came on and I don't know what it means. The needle is all the way down."*
**Response time**: 44.41s

**Gus Diagnosis**:
> Identify the specific red light that is illuminated and the gauge whose needle is 'all the way down.' This will narrow down the potential causes significantly.

**Answer Paths Offered**:
> - The red light is labeled 'HIGH VOLTAGE' and the ammeter needle is all the way to the discharge side.
> - The red light is for 'OIL PRESSURE' and the oil pressure gauge needle is at zero.
> - The red light is for 'LOW FUEL' and the fuel quantity gauge needle is on 'E' (empty).
> - The red light is for something else, or there is no label, and the needle is on a different gauge.

#### Expert Pilot
**Query**: *"Oil pressure gauge dropped to zero in flight. Oil temperature is rising. I'm looking for immediate actions and probable causes."*
**Response time**: 68.0s

**Gus Diagnosis**:
> Zero oil pressure and rising oil temperature in flight is an emergency. Your immediate action should be to reduce power and land as soon as safely possible. Once on the ground, do not restart the engine until a thorough inspection is performed. Your first steps are to physically verify the oil level and inspect for external leaks, then check the oil pressure gauge system.

**Answer Paths Offered**:
> - The oil dipstick shows the oil level is critically low or empty, and I found a significant oil leak.
> - The oil dipstick shows the oil level is normal, and there are no visible external oil leaks.
> - The oil pressure gauge line is congealed or pinched, or the gauge itself is obviously defective (e.g., pointer stuck).

#### A&P Mechanic
**Query**: *"Zero oil pressure indication in flight, oil temp rising. What does the FSM troubleshooting list for a no-oil-pressure condition?"*
**Response time**: 63.67s

**Gus Diagnosis**:
> Given the critical nature of zero oil pressure and rising oil temperature, immediate action is required. We need to determine if this is an actual engine issue or an instrumentation fault. First, verify the actual oil level and check for any external oil leaks. Then, we need to confirm the accuracy of the oil pressure gauge.

**Answer Paths Offered**:
> - I have checked the oil dipstick, and the oil level is critically low or empty. I also see a significant external oil leak.
> - I have checked the oil dipstick, and the oil level is normal. There are no visible external oil leaks.
> - I have substituted a known-good oil pressure gauge, and it also reads zero. The oil temperature gauge still shows rising temperature.

---

## Fault 11 — HIGH OIL TEMPERATURE

**FSM Reference**: Section 11-9 / 11A-31, Part 4 p.34-35

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | HIGH OIL TEMPERATURE |
| **Probable Cause** | Insufficient oil; Defective oil cooler; Clogged oil passages; Incorrect grade of oil |
| **Remedy** | Service oil; Replace oil cooler; Flush oil system; Use correct grade |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"The temperature thing for the oil is really high. Higher than I've ever seen it."*
**Response time**: 58.52s

**Gus Diagnosis**:
> We need to determine if this is a true high oil temperature condition or an instrument malfunction. First, verify the oil level and type. Then, we'll check the oil temperature gauge and the oil cooler's function.

**Answer Paths Offered**:
> - The oil level is correct, the correct grade oil is present, and a known good oil temperature gauge reads normal.
> - The oil level is correct, the correct grade oil is present, and a known good oil temperature gauge also reads high. When feeling the front of the oil cooler core, it is cold.
> - The oil level is correct, the correct grade oil is present, and a known good oil temperature gauge also reads high. When feeling the front of the oil cooler core, it is hot, but the air passages appear clear.
> - The oil level is low, or the oil is not the correct grade/viscosity for the ambient temperature.

#### Expert Pilot
**Query**: *"Oil temp reading above normal limits in cruise. Oil pressure is normal. Outside air temp is moderate."*
**Response time**: 39.93s

**Gus Diagnosis**:
> The reported high oil temperature with normal oil pressure in cruise suggests either a faulty temperature indication or an issue with the oil cooling system. First, we need to verify the accuracy of the oil temperature reading. The FSM recommends checking the gage with a known good unit. This will help distinguish between an actual high temperature and a false reading.

**Answer Paths Offered**:
> - The oil temperature gage reads normal when swapped with a known good unit, or the temperature bulb resistance is within specification when tested.
> - The oil temperature gage still reads high when swapped with a known good unit, and the temperature bulb resistance is also out of specification, indicating a true high temperature.

#### A&P Mechanic
**Query**: *"High oil temperature, pressure within limits. What FSM probable causes and remedies apply to elevated oil temp?"*
**Response time**: 50.04s

**Gus Diagnosis**:
> We need to isolate the cause of the high oil temperature. Given that oil pressure is within limits, we'll start by verifying the temperature reading and then inspect the oil cooling system. What do you observe when performing the following checks?

**Answer Paths Offered**:
> - The oil temperature gauge reads high, but an independent, known-good temperature probe inserted into the oil sump or near the oil temperature bulb confirms the actual oil temperature is normal.
> - The oil cooler core is visibly obstructed with dirt, debris, or the winter baffles are still installed, restricting airflow.
> - With the engine at operating temperature, the oil cooler core feels cold to the touch, indicating oil is bypassing the cooler when it should be flowing through it for cooling.
> - The engine oil currently in the sump is a higher viscosity grade (e.g., SAE 50 in cold weather) than recommended for the current ambient temperature range, or appears unusually thick.

---

## Fault 12 — AIRCRAFT LEANS TO ONE SIDE

**FSM Reference**: Section 5, Landing Gear Troubleshooting, Part 2 p.23+

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | AIRCRAFT LEANS TO ONE SIDE |
| **Probable Cause** | Landing gear attaching parts not tight; Landing gear spring excessively sprung; Incorrect shimming |
| **Remedy** | Tighten loose parts and replace defective parts; Remove and install new parts; Re-shim per FSM |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"My plane sits crooked on the ground. It leans to the left like one side is lower."*
**Response time**: 47.94s

**Gus Diagnosis**:
> First, confirm the aircraft model and year. Assuming a 1975 Cessna 172/Skyhawk, which typically uses tubular spring-steel main gear struts. The lean to the left indicates an issue on that side. We need to systematically check the most common causes. Begin by checking the left main wheel tire pressure and then visually inspect the left main landing gear strut and its attachment points.

**Answer Paths Offered**:
> - The left main tire pressure is significantly lower than specified, or the tire appears visibly deflated.
> - The left main landing gear spring-strut appears visibly bent, cracked, or excessively compressed compared to the right side.
> - The bolts, nuts, or U-bolts securing the left main landing gear strut to the fuselage are loose, or there's visible damage to the attachment points.
> - There is visible structural damage (buckling, cracks, sheared rivets) around the left main landing gear bulkhead or floorboards, indicating a hard landing.

#### Expert Pilot
**Query**: *"Aircraft lists to the left when parked. Left main gear appears to sit lower than right. No recent hard landing."*
**Response time**: 39.2s

**Gus Diagnosis**:
> The aircraft is listing to the left, with the left main gear appearing lower. We need to systematically check the most common causes for this condition. Begin by verifying the tire pressure, then inspect the main gear strut and its attachments.

**Answer Paths Offered**:
> - The left main gear tire pressure is significantly lower than specified, or the tire shows obvious signs of deflation.
> - The left main gear spring strut appears visibly bent, bowed, or compressed more than the right side, indicating it is 'sprung'.
> - The bolts or rivets securing the left main landing gear strut to the fuselage are loose or show signs of movement.
> - The left main gear axle is visibly bent or deformed.

#### A&P Mechanic
**Query**: *"Aircraft leaning to one side on the ground. What does the FSM landing gear troubleshooting table list as probable causes?"*
**Response time**: 54.56s

**Gus Diagnosis**:
> The FSM troubleshooting table for 'AIRCRAFT LEANS TO ONE SIDE' (Source 7, page 24) lists several probable causes. Begin by performing a thorough visual inspection and basic checks of the landing gear and associated components. What do you observe?

**Answer Paths Offered**:
> - I observe one or more main landing gear tires are under-inflated compared to specifications (refer to Figure 1-1 for pressure).
> - I observe loose or damaged landing gear attaching parts, or the landing gear spring-strut appears visibly bent or excessively compressed on one side.
> - I observe a brake dragging on one of the main wheels, or the wheel is difficult to rotate by hand.
> - I observe a visibly bent axle on one of the main wheels, or the wheel bearings feel excessively tight when rotating the wheel off the ground.

---

## Fault 13 — BRAKES DRAG

**FSM Reference**: Section 5, Brake Troubleshooting, Part 2 p.23+

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | BRAKES DRAG |
| **Probable Cause** | Brake disc warped; Return springs weak or broken; Piston stuck in cylinder |
| **Remedy** | Replace disc; Replace springs; Free or replace piston and cylinder |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"It feels like the brakes are always on a little bit. The plane is hard to push on the ground."*
**Response time**: 60.14s

**Gus Diagnosis**:
> We need to determine if the dragging is due to a control input issue, a hydraulic problem, or a mechanical issue at the wheel. Start by checking the brake controls and then the wheels for signs of friction.

**Answer Paths Offered**:
> - With the parking brake released, physically check the parking brake handle and cable for free movement. Then, press and release both rudder/brake pedals. Do they return fully and freely without any binding or resistance?
> - After attempting to push the aircraft, carefully feel the main wheel hubs and brake assemblies. Are they noticeably hot to the touch, and is the heat localized to one wheel or both?
> - Visually inspect the brake master cylinders (located just forward of the pilot rudder pedals) for any signs of external leakage. Also, check the fluid level in both reservoirs. Is the fluid level correct, and are there any visible obstructions around the master cylinder piston rods?

#### Expert Pilot
**Query**: *"Both main wheels exhibit noticeable resistance during ground push-back. Brakes were released. Wheels are warm to touch."*
**Response time**: 34.07s

**Gus Diagnosis**:
> The main wheels are exhibiting resistance during push-back and are warm, even with the brakes released. This indicates a dragging brake condition. First, we need to verify that the brake pedals and parking brake system are fully disengaged and not causing any residual pressure. Inspect the pilot and copilot rudder pedals for any binding or obstruction that might prevent them from returning to their full 'off' position. Then, check the parking brake handle and its cable linkage (refer to Figure 5-14 on page 7 of Source 47) to ensure it is fully released and not applying tension to the master cylinders.

**Answer Paths Offered**:
> - Both brake pedals are free, and the parking brake linkage is fully slack, but the wheels still drag.
> - One or both brake pedals are stiff or not fully returning, or the parking brake linkage is tight even when released.
> - The wheels spin freely with no resistance after jacking the aircraft.

#### A&P Mechanic
**Query**: *"Brake drag on both mains, wheels warm after taxi. What does the FSM say about brake drag probable causes?"*
**Response time**: 60.71s

**Gus Diagnosis**:
> We need to isolate the source of the brake drag affecting both main wheels. Start by checking the most common and easily verifiable external causes that would affect both brakes. Perform the following checks:

**Answer Paths Offered**:
> - The parking brake handle is fully released, but the linkage at the master cylinders appears to be holding the pistons slightly depressed. (Points to Parking Brake System)
> - Both rudder pedals return freely to their full aft position without any binding or stiffness. (Rules out Brake Control Linkage binding)
> - When the brakes are briefly depressed and released, fluid does not visibly return freely to the master cylinder reservoirs, or there's a noticeable delay. (Points to Master Cylinder/Hydraulic Line Restriction)
> - A visual inspection of the main wheel brake assemblies reveals obvious physical damage, excessive dirt, or components that are clearly binding or not fully retracting. (Points to Wheel Brake Assembly mechanical issues)

---

## Fault 14 — LOW OR SLUGGISH AIRSPEED INDICATION

**FSM Reference**: Section 15-17, Pitot Static Troubleshooting, Part 5 p.24

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | LOW OR SLUGGISH AIRSPEED INDICATION |
| **Probable Cause** | Pitot tube obstructed; Pitot line leaking; Defective airspeed indicator |
| **Remedy** | Clear obstruction; Repair or replace pitot line; Replace indicator |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"The speed thing on the dashboard seems wrong. It shows way less speed than I think I'm going."*
**Response time**: 33.92s

**Gus Diagnosis**:
> The airspeed indicator is showing a lower speed than expected. This points to a potential issue with the pitot-static system. We need to determine if the problem is isolated to the pitot system or if it's a broader static system issue affecting multiple instruments. Visually inspect the pitot tube for any obstructions and then check the behavior of the other static instruments.

**Answer Paths Offered**:
> - The pitot tube is visibly obstructed (e.g., by debris, ice, or a cover).
> - The pitot tube is clear, and the altimeter and vertical speed indicator are working normally.
> - The pitot tube is clear, but the altimeter and vertical speed indicator are also showing incorrect or sluggish readings.
> - The pitot tube is clear, and all other static instruments (altimeter, VSI) are working normally, but the airspeed indicator still reads low after a thorough visual inspection of the pitot tube and accessible pitot line.

#### Expert Pilot
**Query**: *"Airspeed indicator reading approximately 20 knots low compared to GPS groundspeed. Sluggish response to power changes."*
**Response time**: 39.13s

**Gus Diagnosis**:
> The airspeed indicator reading low and responding sluggishly suggests a problem in the pitot-static system. We need to isolate whether the issue is with the pitot pressure line, the static pressure line, or the instrument itself. Your first step is to perform a leakage test on the pitot system.

**Answer Paths Offered**:
> - The airspeed indicator registers in the cruise range and holds steady for several minutes, indicating no leak in the pitot system. (Proceed to static system check)
> - The airspeed indicator registers in the cruise range but slowly drops, indicating a leak in the pitot system. (Proceed to pitot line inspection)
> - The airspeed indicator does not register or responds erratically during the test, indicating a significant obstruction or severe leak in the pitot system. (Proceed to pitot line inspection)

#### A&P Mechanic
**Query**: *"Low and sluggish ASI. What does the FSM pitot-static troubleshooting section list for low airspeed indication?"*
**Response time**: 33.88s

**Gus Diagnosis**:
> For a low and sluggish airspeed indication, the FSM points directly to issues within the pitot system. You need to inspect the pitot tube and its associated line for obstructions or leaks. This is a critical flight instrument, so thoroughness is paramount.

First, visually inspect the pitot tube for any obvious blockages (e.g., insects, debris). Then, proceed with a pitot system leakage test as outlined in the FSM, Section 15-14, 'PITOT SYSTEM INSPECTION AND LEAKAGE TEST' on page 23. This involves sealing the pitot tube and applying pressure to check for leaks.

**Answer Paths Offered**:
> - I found an obstruction in the pitot tube or line.
> - I performed the pitot system leakage test and found a leak.
> - I performed the pitot system leakage test and found no leaks or obstructions.

---

## Fault 15 — HIGH SUCTION GAGE READINGS

**FSM Reference**: Section 15-26, Vacuum System Troubleshooting, Part 5 p.29

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | HIGH SUCTION GAGE READINGS |
| **Probable Cause** | Defective suction relief valve; Restricted suction relief valve filter |
| **Remedy** | Replace or adjust suction relief valve; Clean or replace filter |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"One of the round gauges on the dash seems to be reading too high. I think it's the suction one?"*
**Response time**: 44.88s

**Gus Diagnosis**:
> You're reporting a high reading on the suction gauge. This typically indicates an issue with the vacuum system's filtration or regulation, or a faulty gauge. We need to isolate the cause. Start by checking the most common and accessible components.

**Answer Paths Offered**:
> - I removed the instrument air filters, and the suction gauge reading immediately dropped to normal.
> - I inspected the suction relief valve screen, and it was clogged. After cleaning/replacing, the reading is normal.
> - The suction relief valve was improperly adjusted. After adjusting it to 5.3 ± 0.1 inches of mercury at 2200 RPM, the reading is normal.
> - I substituted the suction gauge with a known-good unit, and the new gauge reads correctly. The original gauge is defective.

#### Expert Pilot
**Query**: *"Suction gauge reading above the normal 4.5-5.5 range. Attitude indicator and heading indicator appear to be working but spinning faster than normal."*
**Response time**: 45.05s

**Gus Diagnosis**:
> The reported high suction gauge reading, coupled with the gyros spinning faster than normal, indicates an over-pressure condition in the vacuum system. This could be a faulty gauge or a problem with the suction relief valve. First, we need to confirm the accuracy of the suction gauge. Then, if the reading is confirmed high, we will address the relief valve.

**Answer Paths Offered**:
> - The suction gauge reading is confirmed high when checked with a known good gauge.
> - The suction gauge reading is normal when checked with a known good gauge, indicating the original gauge is faulty.

#### A&P Mechanic
**Query**: *"Suction gauge reads above limits. What are the FSM troubleshooting table probable causes for high suction readings?"*
**Response time**: 37.64s

**Gus Diagnosis**:
> The suction gauge reading above limits indicates an issue within the vacuum system. We need to systematically check the components responsible for vacuum generation and regulation. Start by inspecting the air filters and the suction relief valve, as these are common points of failure for this symptom. The FSM troubleshooting for 'HIGH SUCTION GAGE READINGS' points to these items first.

**Answer Paths Offered**:
> - The instrument air filters are visibly dirty or restricted, or removing them causes the suction reading to drop.
> - The suction relief valve screen is clogged, or the valve itself is stuck/malfunctioning, and adjusting it does not bring the reading within limits (4.6 to 5.4 inches of mercury).
> - There are no obvious issues with the air filters or the relief valve, but there are visible kinks, damage, or loose connections in the vacuum lines between the instruments and the relief valve.
> - A known-good suction gauge reads within normal limits (4.6 to 5.4 inches of mercury) when substituted for the installed gauge.

---

## Fault 16 — ALTERNATOR NOT CHARGING / POWER LOW

**FSM Reference**: Section 16-33, Electrical Troubleshooting, Part 6 p.3, p.33-34

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | ALTERNATOR NOT CHARGING / POWER LOW |
| **Probable Cause** | Defective alternator; Broken or slipping drive belt; Faulty voltage regulator |
| **Remedy** | Replace alternator; Replace or adjust drive belt; Replace voltage regulator |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"A little red light came on while I was flying. I think it says ALT or something. And the radio started getting staticky."*
**Response time**: 36.06s

**Gus Diagnosis**:
> The 'ALT' light and radio static indicate a problem with the charging system. We need to determine if the alternator is producing power or if the system has shut it down. First, check the alternator drive belt and the ammeter indication.

**Answer Paths Offered**:
> - The alternator drive belt is intact and tight, and the ammeter shows a discharge.
> - The alternator drive belt is loose or broken.
> - The ammeter shows a normal charge, but the radio is still staticky.

#### Expert Pilot
**Query**: *"Low voltage annunciator illuminated in flight. Ammeter showing discharge. Bus voltage dropping. I've shed non-essential loads."*
**Response time**: 57.38s

**Gus Diagnosis**:
> We need to determine why the alternator system is not charging. Start by checking the most common and easily verifiable points. Since you're on the ground now, we can perform some basic checks.

**Answer Paths Offered**:
> - The alternator drive belt is intact and properly tensioned.
> - The alternator drive belt is loose or broken.
> - Cycling the master switch (both BAT and ALT portions OFF then ON) restores normal charging (ammeter shows charge, voltage stabilizes).
> - Cycling the master switch has no effect; the ammeter still shows discharge and voltage drops.

#### A&P Mechanic
**Query**: *"Alternator failure light on, ammeter shows discharge. What FSM troubleshooting entries cover the alternator charging system?"*
**Response time**: 55.62s

**Gus Diagnosis**:
> To isolate the fault between the voltage regulator and the alternator, we need to test the alternator's ability to produce a charge independently of the regulator's control. First, ensure the master switch is OFF and the negative lead is disconnected from the battery. Then, remove the cowl and locate the voltage regulator, typically mounted on the left-hand side of the firewall. Disconnect the electrical plug from the regulator. With the regulator plug removed, start the engine. Momentarily jumper the 'A+' and 'F' terminals together on the *regulator plug* (the harness side, not the regulator itself). Observe the ship's ammeter. This test bypasses the regulator, directly energizing the alternator field. Refer to Figure 16-5 on page 8 of Source 27 for regulator wiring context.

**Answer Paths Offered**:
> - The ship's ammeter shows a heavy rate of charge when the 'A+' and 'F' terminals are jumpered.
> - The ship's ammeter does NOT show a heavy rate of charge when the 'A+' and 'F' terminals are jumpered.

---

## Fault 17 — INSTRUMENT LIGHTS WILL NOT LIGHT

**FSM Reference**: Section 16-51, Lighting Troubleshooting, Part 6 p.9-11

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | INSTRUMENT LIGHTS WILL NOT LIGHT |
| **Probable Cause** | Defective bulbs; Open circuit; Defective rheostat/dimmer |
| **Remedy** | Replace bulbs; Repair circuit; Replace rheostat |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"I can't see the gauges at night. The panel lights aren't working at all."*
**Response time**: 42.16s

**Gus Diagnosis**:
> The instrument panel lights are out. For your 1975 model, the instrument flood lighting is controlled by a transistorized dimming assembly with a concentric knob on the lower left side of the pilot's switch panel (Source 52, Source 51). First, check the circuit breaker for the instrument lights. Then, ensure the dimming control is not set to minimum brightness.

**Answer Paths Offered**:
> - The instrument light circuit breaker is tripped (popped out).
> - The instrument light circuit breaker is set (pushed in).
> - The dimming control knob is turned fully counter-clockwise (minimum brightness setting).

#### Expert Pilot
**Query**: *"Instrument panel lighting inoperative. Rheostat rotated to full bright. Circuit breaker checked, appears normal."*
**Response time**: 36.22s

**Gus Diagnosis**:
> The circuit breaker is normal, and the rheostat is at full bright. For 1971 and later models, instrument flood lighting is controlled by a rheostat on the lower, left-hand portion of the instrument panel (Source 9, 23). You need to access the instrument light circuit to measure voltage. With the master switch ON and the rheostat turned full clockwise, measure the voltage at the instrument light assembly.

**Answer Paths Offered**:
> - I measure battery voltage at the instrument light assembly with the master switch ON and the rheostat full clockwise, but the lights are still out.
> - I measure no voltage at the instrument light assembly with the master switch ON and the rheostat full clockwise.
> - I measure voltage, but it drops suddenly as I turn the rheostat counterclockwise, before reaching full dim.

#### A&P Mechanic
**Query**: *"No instrument lighting. Rheostat and circuit breaker checked. What does the FSM troubleshooting say for instrument lights will not light?"*
**Response time**: 40.29s

**Gus Diagnosis**:
> Turn the master switch ON. Set the instrument light rheostat to its full clockwise (brightest) position. Using a voltmeter, check for battery voltage at the instrument light with the rheostat turned full clockwise. Then, slowly turn the rheostat counterclockwise and observe if the voltage decreases smoothly. Refer to the wiring diagrams in Section 20, specifically 'Compass and Instrument Lights' on pages 20-29 or 20-31, and 'Instrument Panel Post Lighting' on pages 20-72 or 20-73, to identify the correct test points. (Source 2, Source 8, Source 13)

**Answer Paths Offered**:
> - I read battery voltage with the rheostat full clockwise, and the voltage decreases smoothly as I turn it counterclockwise.
> - I read no voltage at the instrument light, or the voltage drops suddenly before the rheostat is turned full counterclockwise.
> - I read battery voltage, but the lights still do not illuminate.

---

## Fault 18 — AILERON CONTROL STIFF / RESISTANCE TO CONTROL WHEEL MOVEMENT

**FSM Reference**: Section 6, Aileron Troubleshooting, Part 3 p.8-9

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | AILERON CONTROL STIFF / RESISTANCE TO CONTROL WHEEL MOVEMENT |
| **Probable Cause** | Cable tension too high; Pulleys binding; Bellcrank binding |
| **Remedy** | Adjust cable tension; Lubricate or replace pulleys; Lubricate or replace bellcrank |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"The wheel thing is really hard to turn left and right. It feels stuck."*
**Response time**: 42.42s

**Gus Diagnosis**:
> Clarify what 'wheel thing' refers to. Is the resistance felt when operating the control wheel in the cockpit (for flight control) or when steering the aircraft on the ground (for ground handling)?

**Answer Paths Offered**:
> - The resistance is felt when operating the control wheel in the cockpit, affecting aileron movement.
> - The resistance is felt when steering the aircraft on the ground, affecting nose wheel movement.

#### Expert Pilot
**Query**: *"Aileron control forces noticeably heavier than normal in both directions. Full deflection achievable but requires excessive force."*
**Response time**: 47.85s

**Gus Diagnosis**:
> The aileron control system is experiencing excessive friction. We need to isolate where this friction is occurring. First, disconnect the aileron control cables from the aileron bellcranks in the wings. This will separate the control wheel and internal linkages from the external aileron surfaces and their associated cables and pulleys. Then, check the freedom of movement for both sections.

**Answer Paths Offered**:
> - The control wheels and internal linkages move freely, but the ailerons themselves are stiff when moved by hand.
> - The control wheels and internal linkages are still stiff, but the ailerons move freely when disconnected and moved by hand.
> - Both the control wheels/internal linkages AND the ailerons/external cables are stiff.

#### A&P Mechanic
**Query**: *"Excessive aileron control friction. What are the FSM probable causes for stiff aileron controls?"*
**Response time**: 45.35s

**Gus Diagnosis**:
> The FSM lists 'RESISTANCE TO CONTROL WHEEL MOVEMENT' as a symptom. We need to systematically check the aileron control system for binding or improper adjustment. Begin by checking the control wheel for free movement and then inspect the accessible components for the following:

1.  **Control Cables:** Check for proper tension. Cables that are too tight will cause resistance. Refer to Section 6-18 for rigging specifications (Source 17, 41).
2.  **Pulleys and Brackets:** Inspect all pulleys for binding, damage, or if the cable has come off a pulley. Check pulley brackets for damage.
3.  **Bellcranks:** Inspect aileron bellcranks for distortion, damage, or binding. Access is typically through hand holes on the underside of the wing (Source 3).
4.  **Control 'U' Chains and Sprockets:** Inspect the chains and sprockets within the control 'U' assembly for rust or binding. This is located behind the instrument panel (Source 13, 29).
5.  **Clevis Bolts:** Check all clevis bolts in the system to ensure they are not over-tightened, which can cause binding at pivot points.
6.  **U-joints:** Inspect universal joints for defects, as they can cause resistance in the control column (Source 17).
7.  **Wing Leveler System (if installed):** If the aircraft is equipped with a wing leveler, check its pneumatic servos and connecting cables/hoses for any signs of binding or interference with the main aileron control cables (Source 16, 22, 28). Manual override of the system should allow free movement if the issue is within the wing leveler itself.

**Answer Paths Offered**:
> - The control wheel feels stiff throughout its entire range of motion, and I found one or more control cables are excessively tight or a pulley is visibly binding.
> - The stiffness is primarily felt when initiating movement from neutral, and I found rust or binding in the control 'U' chains or sprockets, or a defective U-joint.
> - The stiffness is intermittent or localized to one aileron, and I found a distorted bellcrank, an over-tightened clevis bolt, or a binding wing leveler servo (if installed).
> - The control system feels generally sluggish, but no specific binding point is obvious; cable tension appears within limits, but movement is not smooth.

---

## Fault 19 — INSUFFICIENT CABIN HEAT

**FSM Reference**: Section 7-4 / 10-3, Heater Troubleshooting, Part 3 p.18

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | INSUFFICIENT CABIN HEAT |
| **Probable Cause** | Heat control cable misadjusted; Heat valve not opening fully; Leaking exhaust shroud |
| **Remedy** | Adjust cable; Repair or replace heat valve; Replace exhaust shroud |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"It's freezing in here when I fly. The heater doesn't seem to do anything even when I pull the knob all the way."*
**Response time**: 41.71s

**Gus Diagnosis**:
> Check the physical operation of the 'CABIN HEAT' control and the associated shut-off valve. The Service Manual indicates that sticking or binding air valves and/or their controls, or damaged air ducting, are common causes for heating system issues. You need to visually confirm the valve's movement and the integrity of the ducts. Also, inspect the exhaust muffler's heat exchange section for any signs of damage or leaks, as this is where the air is heated.

**Answer Paths Offered**:
> - The 'CABIN HEAT' control knob moves freely, and I can see the shut-off valve move through its full range, but there's still no heat. The ducts appear intact.
> - The 'CABIN HEAT' control knob moves freely, but the shut-off valve is stuck or does not move through its full range.
> - The 'CABIN HEAT' control knob is stiff or binds when I try to pull it out, and the shut-off valve does not move fully.
> - I found damaged, disconnected, or obstructed flexible ducting in the heating system.
> - The 'CABIN AIR' control knob is stuck, and the fresh airscoop door is visibly open, even when the 'CABIN AIR' control is pushed in.

#### Expert Pilot
**Query**: *"Cabin heat output minimal with control set to full hot. Defrost seems to work slightly. Outside air temp is 20F."*
**Response time**: 35.91s

**Gus Diagnosis**:
> The most common cause for your symptom is a sticking or binding cabin heat shut-off valve or its control linkage. This valve is located on the right forward side of the firewall. You need to physically verify its operation.

1.  Locate the 'CABIN HEAT' push-pull control on the instrument panel.
2.  Locate the shut-off valve on the right forward side of the firewall, which is connected to this control.
3.  Operate the 'CABIN HEAT' control from full 'IN' (cold) to full 'OUT' (hot).
4.  Observe the shut-off valve's movement. Ensure it moves freely and completely through its full range of travel, from fully closed to fully open. Also, check that the control linkage is not binding or disconnected.

**Answer Paths Offered**:
> - The cabin heat control moves freely, and the shut-off valve on the firewall moves through its full range of travel, from fully closed to fully open, with no binding.
> - The cabin heat control feels stiff or binds, and/or the shut-off valve on the firewall does not move through its full range of travel when the control is operated.
> - The cabin heat control moves freely, but the shut-off valve on the firewall does not move at all, indicating a disconnected linkage.

#### A&P Mechanic
**Query**: *"Insufficient cabin heat output. Control cable travel appears full. What does the FSM list for insufficient heat?"*
**Response time**: 32.51s

**Gus Diagnosis**:
> The FSM indicates that most heating system troubles are caused by sticking air valves, damaged ducting, or defects in the exhaust muffler. Since you've confirmed full control cable travel, we need to verify the physical response of the components the cable operates and the integrity of the air path.

First, inspect the cabin heat shut-off valve, located on the right forward side of the firewall. Manually check its movement to ensure it responds freely to the 'CABIN HEAT' control and moves through its full range of travel, sealing properly when pushed in and fully opening when pulled out. Also, visually inspect the flexible ducting connecting the heating system components for any signs of burning, fraying, crushing, or disconnections.

**Answer Paths Offered**:
> - The cabin heat shut-off valve moves freely and fully, and the ducting appears intact and connected.
> - The cabin heat shut-off valve is sticking or does not move through its full range, or the ducting is visibly damaged/disconnected.
> - The cabin heat shut-off valve moves freely, the ducting is intact, but I hear an exhaust leak or smell exhaust fumes in the cabin.

---

## Fault 20 — NOSE WHEEL SHIMMY

**FSM Reference**: Section 5, Landing Gear Troubleshooting, Part 2 p.23+

### FSM Ground Truth

| Field | FSM Text |
|-------|----------|
| **Trouble** | NOSE WHEEL SHIMMY |
| **Probable Cause** | Shimmy dampener low on fluid; Worn steering components; Tire flat-spotted or worn |
| **Remedy** | Service shimmy dampener; Replace worn steering parts; Replace tire |

### Gus Responses (Verbatim)

#### Vague Owner
**Query**: *"The front wheel shakes like crazy when I'm rolling on the runway. The whole nose vibrates."*
**Response time**: 50.19s

**Gus Diagnosis**:
> We need to isolate the source of this severe nose wheel vibration. Start by physically inspecting the nose gear assembly. This shaking can be caused by several issues, from the wheel itself to the strut's dampening or its structural connections. We'll check the most likely culprits first.

**Answer Paths Offered**:
> - The nose wheel has excessive side-to-side play, or the tire shows uneven wear/damage, or the wheel feels unbalanced when spun by hand.
> - The shimmy dampener is leaking fluid, or the piston rod moves freely with no resistance, indicating a lack of fluid or internal defect.
> - The torque links have noticeable play at their attachment points, or the main nose strut attaching clamps are loose, allowing the strut to shift.

#### Expert Pilot
**Query**: *"Severe nose wheel shimmy on takeoff roll and landing rollout above 30 knots. Shimmy dampener was serviced at last annual."*
**Response time**: 38.39s

**Gus Diagnosis**:
> We need to physically inspect the nose gear assembly. Start by raising the nose of the aircraft to get the nose wheel off the ground. Then, perform the following checks to identify any play or defects in the system components that could be causing the shimmy.

**Answer Paths Offered**:
> - When the nose wheel is off the ground, I can feel significant free play (side-to-side or rotational) in the wheel itself, or the wheel wobbles.
> - I observe hydraulic fluid leaking from the shimmy dampener, or the dampener shaft moves freely with little resistance when compressed/extended by hand.
> - I find noticeable looseness or wear in the nose gear torque links or the nose wheel steering linkage when attempting to move the wheel or linkage by hand.
> - The nose wheel assembly appears visually sound with no obvious play, leaks, or loose components, but the tire shows uneven wear patterns.

#### A&P Mechanic
**Query**: *"Nose wheel shimmy during ground ops. Dampener serviced recently. What does the FSM landing gear troubleshooting say about shimmy?"*
**Response time**: 59.73s

**Gus Diagnosis**:
> The FSM troubleshooting points to several potential causes for nose wheel shimmy. We need to systematically check for mechanical play and wheel integrity. Begin by inspecting the nose wheel assembly for any obvious looseness or damage.

**Answer Paths Offered**:
> - The nose wheel has excessive play when rocked side-to-side, or the tire pressure is incorrect.
> - The nose wheel torque links (Figure 5-12, Source 14) show visible looseness or wear at their attachment points.
> - The nose wheel steering rods or their connections to the steering arm (Figure 5-11, Source 2) have noticeable play.
> - The nose strut itself is loose in its attaching clamps to the firewall (Figure 5-6, Source 41), or the shimmy dampener still feels ineffective despite recent service.

---

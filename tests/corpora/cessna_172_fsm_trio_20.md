# Cessna 172 Skyhawk — FSM-Grounded 20-Fault Trio Corpus

**Authority**: 1975 Cessna 172 & Skyhawk Series Service Manual (1969-1976)  
**Method**: Each fault is a row from the FSM's own troubleshooting tables  
**Variants**: 3 queries per fault — Vague (clueless owner), Expert (experienced pilot), Mechanic (A&P tech)  
**Total Test Cases**: 60 (20 faults × 3 variants)

---

## Fault 1 — ENGINE WILL NOT START (No fuel)

| Field | Value |
|-------|-------|
| **FSM Section** | §11-9, Engine Troubleshooting |
| **FSM Trouble** | ENGINE WILL NOT START |
| **FSM Probable Cause** | Fuel selector valve not turned on / Fuel tanks empty |
| **FSM Remedy** | Turn selector valve on / Service with proper fuel |
| **FSM Page** | Part 4, p.4 |

| Variant | Query |
|---------|-------|
| **Vague** | "I can't get my plane to start. It just cranks and cranks but nothing happens." |
| **Expert** | "Engine cranks normally but won't fire. I've verified battery and starter engagement. Suspect fuel delivery issue." |
| **Mechanic** | "Engine cranks, no start. What does the FSM troubleshooting table list as probable causes for a no-start condition?" |

---

## Fault 2 — ENGINE WILL NOT START (Ignition)

| Field | Value |
|-------|-------|
| **FSM Section** | §11-9, Engine Troubleshooting |
| **FSM Trouble** | ENGINE WILL NOT START |
| **FSM Probable Cause** | Defective magneto / Fouled or defective spark plugs |
| **FSM Remedy** | Repair or replace magneto / Clean, gap, or replace spark plugs |
| **FSM Page** | Part 4, p.4 |

| Variant | Query |
|---------|-------|
| **Vague** | "My plane won't start and it was fine last week. I don't know what's wrong." |
| **Expert** | "No start condition. During last mag check before shutdown, I noticed an abnormal RPM drop on the left mag. Now it won't fire at all." |
| **Mechanic** | "No-start, good fuel flow confirmed at the gascolator. Suspect ignition system. What are the FSM-listed ignition causes for a no-start?" |

---

## Fault 3 — ENGINE STARTS BUT DIES

| Field | Value |
|-------|-------|
| **FSM Section** | §11-9, Engine Troubleshooting (Cont.) |
| **FSM Trouble** | ENGINE STARTS BUT DIES |
| **FSM Probable Cause** | Mixture control not in full rich / Idle speed set too low |
| **FSM Remedy** | Set mixture to full rich / Adjust idle speed |
| **FSM Page** | Part 4, p.5 |

| Variant | Query |
|---------|-------|
| **Vague** | "It starts up but then immediately dies a few seconds later. I have to keep restarting it." |
| **Expert** | "Engine fires but won't sustain idle. It catches for 2-3 seconds then quits. Happens consistently." |
| **Mechanic** | "Engine starts, runs briefly, dies. Repeatable condition. What does the FSM list for 'engine starts but dies'?" |

---

## Fault 4 — ENGINE ROUGH AT IDLE

| Field | Value |
|-------|-------|
| **FSM Section** | §11-9, Engine Troubleshooting |
| **FSM Trouble** | ENGINE ROUGH / RUNS ROUGH AT IDLE |
| **FSM Probable Cause** | Idle mixture too rich or too lean / Fouled spark plugs |
| **FSM Remedy** | Adjust idle mixture / Clean or replace plugs |
| **FSM Page** | Part 4, p.5 |

| Variant | Query |
|---------|-------|
| **Vague** | "My plane shakes a lot when it's just sitting there running on the ground. Feels rough." |
| **Expert** | "Rough running at idle, RPM fluctuating about 50 RPM. Smooths out above 1200 RPM." |
| **Mechanic** | "Rough idle, stable at higher RPM. Suspect mixture or spark plug issue. What does the FSM troubleshooting say?" |

---

## Fault 5 — ENGINE LOSES POWER IN FLIGHT

| Field | Value |
|-------|-------|
| **FSM Section** | §11-9, Engine Troubleshooting |
| **FSM Trouble** | ENGINE LOSES POWER / LOSS OF POWER |
| **FSM Probable Cause** | Carburetor icing / Plugged fuel strainer / Defective magneto |
| **FSM Remedy** | Apply carburetor heat / Clean strainer / Replace magneto |
| **FSM Page** | Part 4, p.5 |

| Variant | Query |
|---------|-------|
| **Vague** | "I was flying and the engine just got weaker and weaker. Like it was losing its strength." |
| **Expert** | "Gradual power loss in cruise at 5,000 feet. Applied carb heat with momentary further power loss then partial recovery. Outside temp around 40°F, visible moisture." |
| **Mechanic** | "Reported power loss in flight. Carb heat partially restored power. What are the FSM-listed causes for in-flight power loss?" |

---

## Fault 6 — NO FUEL TO CARBURETOR

| Field | Value |
|-------|-------|
| **FSM Section** | §12-4, Fuel System Troubleshooting |
| **FSM Trouble** | NO FUEL TO CARBURETOR |
| **FSM Probable Cause** | Fuel selector valve not turned on / Fuel line disconnected or broken / Plugged fuel strainer |
| **FSM Remedy** | Repair or replace selector valve / Connect or repair fuel lines / Clean strainer |
| **FSM Page** | Part 5, p.36-37 |

| Variant | Query |
|---------|-------|
| **Vague** | "The engine stopped getting gas I think. It just quit in the air." |
| **Expert** | "Engine-out in flight. Fuel selector was confirmed on BOTH. Fuel gauges showed quantity remaining in both tanks." |
| **Mechanic** | "Fuel starvation event. Selector valve operative, tanks have fuel. What does the 12-4 troubleshooting table say about no fuel to the carburetor?" |

---

## Fault 7 — WATER IN FUEL

| Field | Value |
|-------|-------|
| **FSM Section** | §12-4, Fuel System Troubleshooting |
| **FSM Trouble** | STARTING (fuel related) |
| **FSM Probable Cause** | Water in fuel |
| **FSM Remedy** | Drain fuel tank sumps, fuel lines and fuel strainer |
| **FSM Page** | Part 5, p.37 |

| Variant | Query |
|---------|-------|
| **Vague** | "It starts but sputters and coughs. It rained all week and the plane was outside." |
| **Expert** | "Engine surging and misfiring intermittently. Aircraft sat outside in rain for five days untied down. Suspect contamination." |
| **Mechanic** | "Intermittent misfire and rough running after extended outdoor parking in rain. Suspect water contamination. What is the FSM procedure?" |

---

## Fault 8 — PRESSURIZED FUEL TANK

| Field | Value |
|-------|-------|
| **FSM Section** | §12-4, Fuel System Troubleshooting |
| **FSM Trouble** | PRESSURIZED FUEL TANK |
| **FSM Probable Cause** | Plugged fuel vent |
| **FSM Remedy** | Check per paragraph 12-13 |
| **FSM Page** | Part 5, p.37 |

| Variant | Query |
|---------|-------|
| **Vague** | "When I took the fuel cap off it was like opening a soda bottle. There was pressure in there." |
| **Expert** | "Fuel cap difficult to remove, audible pressure release upon opening. Fuel seemed to bulge up when uncapped." |
| **Mechanic** | "Pressurized fuel tank condition. What is the FSM-listed probable cause and correction for a pressurized tank?" |

---

## Fault 9 — NO FUEL QUANTITY INDICATION

| Field | Value |
|-------|-------|
| **FSM Section** | §12-4 + §15-45, Fuel/Instrument Troubleshooting |
| **FSM Trouble** | NO FUEL QUANTITY INDICATION |
| **FSM Probable Cause** | Open circuit / Defective fuel quantity transmitter |
| **FSM Remedy** | Tighten connections; repair or replace wiring. Refer to Section 15 and 20 |
| **FSM Page** | Part 5, p.37 |

| Variant | Query |
|---------|-------|
| **Vague** | "The fuel gauge doesn't work. It just sits on empty even though I know there's fuel in there." |
| **Expert** | "Left fuel quantity gauge reads zero despite confirmed fuel in the tank. Right gauge reads normally." |
| **Mechanic** | "No fuel quantity indication on left tank gauge. Circuit breaker is in. What does the FSM say about fuel quantity indication failure?" |

---

## Fault 10 — NO OIL PRESSURE

| Field | Value |
|-------|-------|
| **FSM Section** | §11A-31, Engine Troubleshooting |
| **FSM Trouble** | NO OIL PRESSURE |
| **FSM Probable Cause** | Insufficient oil / Defective pressure relief valve / Defective oil pump |
| **FSM Remedy** | Service oil / Replace relief valve / Replace or repair pump |
| **FSM Page** | Part 4, p.34 |

| Variant | Query |
|---------|-------|
| **Vague** | "There's a red light on the dashboard that came on and I don't know what it means. The needle is all the way down." |
| **Expert** | "Oil pressure gauge dropped to zero in flight. Oil temperature is rising. I'm looking for immediate actions and probable causes." |
| **Mechanic** | "Zero oil pressure indication in flight, oil temp rising. What does the FSM troubleshooting list for a no-oil-pressure condition?" |

---

## Fault 11 — HIGH OIL TEMPERATURE

| Field | Value |
|-------|-------|
| **FSM Section** | §11-9 / §11A-31, Engine Troubleshooting |
| **FSM Trouble** | HIGH OIL TEMPERATURE |
| **FSM Probable Cause** | Insufficient oil / Defective oil cooler / Clogged oil passages |
| **FSM Remedy** | Service oil / Replace cooler / Flush oil system |
| **FSM Page** | Part 4, p.34-35 |

| Variant | Query |
|---------|-------|
| **Vague** | "The temperature thing for the oil is really high. Higher than I've ever seen it." |
| **Expert** | "Oil temp reading above normal limits in cruise. Oil pressure is normal. Outside air temp is moderate." |
| **Mechanic** | "High oil temperature, pressure within limits. What FSM probable causes and remedies apply to elevated oil temp?" |

---

## Fault 12 — AIRCRAFT LEANS TO ONE SIDE

| Field | Value |
|-------|-------|
| **FSM Section** | §5, Landing Gear Troubleshooting |
| **FSM Trouble** | AIRCRAFT LEANS TO ONE SIDE |
| **FSM Probable Cause** | Landing gear attaching parts not tight / Landing gear spring excessively sprung |
| **FSM Remedy** | Tighten loose parts / Remove and install new parts |
| **FSM Page** | Part 2, p.23+ |

| Variant | Query |
|---------|-------|
| **Vague** | "My plane sits crooked on the ground. It leans to the left like one side is lower." |
| **Expert** | "Aircraft lists to the left when parked. Left main gear appears to sit lower than right. No recent hard landing." |
| **Mechanic** | "Aircraft leaning to one side on the ground. What does the FSM landing gear troubleshooting table list as probable causes?" |

---

## Fault 13 — BRAKES DRAG

| Field | Value |
|-------|-------|
| **FSM Section** | §5, Brake Troubleshooting |
| **FSM Trouble** | BRAKES DRAG |
| **FSM Probable Cause** | Brake disc warped / Return springs weak or broken / Piston stuck in cylinder |
| **FSM Remedy** | Replace disc / Replace springs / Free or replace piston |
| **FSM Page** | Part 2, p.23+ |

| Variant | Query |
|---------|-------|
| **Vague** | "It feels like the brakes are always on a little bit. The plane is hard to push on the ground." |
| **Expert** | "Both main wheels exhibit noticeable resistance during ground push-back. Brakes were released. Wheels are warm to touch." |
| **Mechanic** | "Brake drag on both mains, wheels warm after taxi. What does the FSM say about brake drag probable causes?" |

---

## Fault 14 — LOW OR SLUGGISH AIRSPEED INDICATION

| Field | Value |
|-------|-------|
| **FSM Section** | §15-17, Pitot Static System Troubleshooting |
| **FSM Trouble** | LOW OR SLUGGISH AIRSPEED |
| **FSM Probable Cause** | Pitot tube obstructed / Pitot line leaking |
| **FSM Remedy** | Clear obstruction / Repair line |
| **FSM Page** | Part 5, p.24 |

| Variant | Query |
|---------|-------|
| **Vague** | "The speed thing on the dashboard seems wrong. It shows way less speed than I think I'm going." |
| **Expert** | "Airspeed indicator reading approximately 20 knots low compared to GPS groundspeed. Sluggish response to power changes." |
| **Mechanic** | "Low and sluggish ASI. What does the FSM pitot-static troubleshooting section list for low airspeed indication?" |

---

## Fault 15 — HIGH SUCTION GAGE READINGS

| Field | Value |
|-------|-------|
| **FSM Section** | §15-26, Vacuum System Troubleshooting |
| **FSM Trouble** | HIGH SUCTION GAGE READINGS |
| **FSM Probable Cause** | Defective suction relief valve / Restricted suction relief valve filter |
| **FSM Remedy** | Replace or adjust valve / Clean or replace filter |
| **FSM Page** | Part 5, p.29 |

| Variant | Query |
|---------|-------|
| **Vague** | "One of the round gauges on the dash seems to be reading too high. I think it's the suction one?" |
| **Expert** | "Suction gauge reading above the normal 4.5-5.5 range. Attitude indicator and heading indicator appear to be working but spinning faster than normal." |
| **Mechanic** | "Suction gauge reads above limits. What are the FSM troubleshooting table probable causes for high suction readings?" |

---

## Fault 16 — ALTERNATOR NOT CHARGING

| Field | Value |
|-------|-------|
| **FSM Section** | §16-33, Electrical System Troubleshooting |
| **FSM Trouble** | POWER LOW / ALTERNATOR NOT CHARGING |
| **FSM Probable Cause** | Defective alternator / Broken or slipping drive belt / Faulty voltage regulator |
| **FSM Remedy** | Replace alternator / Replace or adjust belt / Replace regulator |
| **FSM Page** | Part 6, p.3 and p.33-34 |

| Variant | Query |
|---------|-------|
| **Vague** | "A little red light came on while I was flying. I think it says ALT or something. And the radio started getting staticky." |
| **Expert** | "Low voltage annunciator illuminated in flight. Ammeter showing discharge. Bus voltage dropping. I've shed non-essential loads." |
| **Mechanic** | "Alternator failure light on, ammeter shows discharge. What FSM troubleshooting entries cover the alternator charging system?" |

---

## Fault 17 — INSTRUMENT LIGHTS WILL NOT LIGHT

| Field | Value |
|-------|-------|
| **FSM Section** | §16-51, Aircraft Lighting Troubleshooting |
| **FSM Trouble** | INSTRUMENT LIGHTS WILL NOT LIGHT |
| **FSM Probable Cause** | Defective bulbs / Open circuit / Defective rheostat |
| **FSM Remedy** | Replace bulbs / Repair circuit / Replace rheostat |
| **FSM Page** | Part 6, p.9-11 |

| Variant | Query |
|---------|-------|
| **Vague** | "I can't see the gauges at night. The panel lights aren't working at all." |
| **Expert** | "Instrument panel lighting inoperative. Rheostat rotated to full bright. Circuit breaker checked — appears normal." |
| **Mechanic** | "No instrument lighting. Rheostat and circuit breaker checked. What does the FSM troubleshooting say for instrument lights will not light?" |

---

## Fault 18 — AILERON CONTROL STIFF

| Field | Value |
|-------|-------|
| **FSM Section** | §6, Aileron Control System Troubleshooting |
| **FSM Trouble** | AILERON CONTROL STIFF / EXCESSIVE FRICTION |
| **FSM Probable Cause** | Cable tension too high / Pulleys binding / Bellcrank binding |
| **FSM Remedy** | Adjust cable tension / Lubricate or replace pulleys / Lubricate or replace bellcrank |
| **FSM Page** | Part 3, p.8-9 |

| Variant | Query |
|---------|-------|
| **Vague** | "The wheel thing is really hard to turn left and right. It feels stuck." |
| **Expert** | "Aileron control forces noticeably heavier than normal in both directions. Full deflection achievable but requires excessive force." |
| **Mechanic** | "Excessive aileron control friction. What are the FSM probable causes for stiff aileron controls?" |

---

## Fault 19 — CABIN HEAT INSUFFICIENT

| Field | Value |
|-------|-------|
| **FSM Section** | §7-4 / §10-3, Heater/Ventilation Troubleshooting |
| **FSM Trouble** | INSUFFICIENT CABIN HEAT |
| **FSM Probable Cause** | Heat control cable misadjusted / Heat valve not opening fully / Leaking exhaust shroud |
| **FSM Remedy** | Adjust cable / Repair valve / Replace shroud |
| **FSM Page** | Part 3, p.18 |

| Variant | Query |
|---------|-------|
| **Vague** | "It's freezing in here when I fly. The heater doesn't seem to do anything even when I pull the knob all the way." |
| **Expert** | "Cabin heat output minimal with control set to full hot. Defrost seems to work slightly. Outside air temp is 20°F." |
| **Mechanic** | "Insufficient cabin heat output. Control cable travel appears full. What does the FSM list for insufficient heat?" |

---

## Fault 20 — NOSE WHEEL SHIMMY

| Field | Value |
|-------|-------|
| **FSM Section** | §5, Landing Gear Troubleshooting |
| **FSM Trouble** | NOSE WHEEL SHIMMY |
| **FSM Probable Cause** | Shimmy dampener low on fluid / Worn steering components / Tire flat-spotted |
| **FSM Remedy** | Service dampener / Replace worn parts / Replace tire |
| **FSM Page** | Part 2, p.23+ |

| Variant | Query |
|---------|-------|
| **Vague** | "The front wheel shakes like crazy when I'm rolling on the runway. The whole nose vibrates." |
| **Expert** | "Severe nose wheel shimmy on takeoff roll and landing rollout above 30 knots. Shimmy dampener was serviced at last annual." |
| **Mechanic** | "Nose wheel shimmy during ground ops. Dampener serviced recently. What does the FSM landing gear troubleshooting say about shimmy?" |

---

## Grading Criteria

Each test case is graded **PASS/FAIL** on three dimensions:

| Criterion | Pass Condition |
|-----------|---------------|
| **System Identification** | Gus identifies the correct system (engine, fuel, electrical, etc.) |
| **Probable Cause Match** | Gus mentions at least ONE of the FSM-documented probable causes |
| **Fix/Remedy Match** | Gus's recommended action aligns with the FSM-documented remedy |

**Overall Score** = (Passes / 60) × 100%  
**Target**: ≥95% (57/60 passes)

> A buyer can open the Cessna 172 Service Manual PDF, turn to the cited page, read the troubleshooting table, and verify every single expected answer independently.

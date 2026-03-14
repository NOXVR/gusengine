"""
Cessna 172 Skyhawk — Quick Validation: 10 Real-World Issues
Sends 10 diagnostic queries to GusEngine, captures responses, and outputs
them for human grading.
"""
import requests, json, sys, time

sys.stdout.reconfigure(encoding='utf-8')

API = "http://5.78.132.233:8888"
VEHICLE_ID = "cessna_172_skyhawk_1970"  # Need to check actual registered ID

# 10 most common real-world Cessna 172 issues
QUERIES = [
    {
        "id": "c172_001",
        "issue": "Carburetor Icing / RPM Drop",
        "system": "Engine / Induction",
        "query": "My Cessna 172 is experiencing a gradual RPM drop during cruise flight, and the engine is running rough. Applying carburetor heat seems to temporarily restore power. What's going on?",
        "ground_truth": "Carburetor icing. The venturi effect in the carburetor causes a temperature drop that can freeze moisture in the air, restricting airflow and fuel flow. Apply full carburetor heat immediately when symptoms appear. The RPM will drop further initially as hot, less dense air enters, then recover as ice melts. Prevention: apply carb heat before reducing power, monitor for conditions conducive to carb ice (high humidity, temperatures 20-70°F). Reference the carburetor heat control procedures in the service manual."
    },
    {
        "id": "c172_002",
        "issue": "Magneto Failure / Rough Running",
        "system": "Ignition",
        "query": "During my run-up, when I switch to the left magneto, the engine runs rough and the RPM drops more than 175 RPM. What should I check?",
        "ground_truth": "Excessive RPM drop on one magneto indicates a problem in that magneto's ignition circuit. Check: (1) Spark plugs on the left magneto circuit — fouled, worn, or improperly gapped plugs are the most common cause. Clean and re-gap to 0.015-0.019 inches. (2) Magneto timing — check and adjust per service manual specifications. (3) Ignition harness leads — check for cracks, chafing, or high resistance. (4) Magneto points and condenser — inspect for wear, pitting, or improper gap. (5) Check for cracked distributor block or rotor. Maximum allowable RPM drop per the POH is typically 125-175 RPM, and differential between magnetos should not exceed 50 RPM."
    },
    {
        "id": "c172_003",
        "issue": "Nose Gear Shimmy",
        "system": "Landing Gear",
        "query": "My Cessna 172 has developed a violent shaking of the nose wheel during landing rollout and taxiing. It's getting progressively worse. What's causing this?",
        "ground_truth": "Nose wheel shimmy. Check: (1) Shimmy dampener — the most common cause. The dampener fluid may be low or the dampener worn/failed. Service or replace the shimmy dampener per the service manual. (2) Nose wheel tire balance and condition — worn or flat-spotted tires cause shimmy. (3) Nose wheel bearings — worn or loose bearings allow lateral play. (4) Torque links (scissors) — check for excessive play in the torque link bolt and bushings. Tighten or replace worn bushings. (5) Nose gear trunnion — check for wear. The service manual specifies inspection intervals and tolerances for all nose gear components."
    },
    {
        "id": "c172_004",
        "issue": "Exhaust System Crack / CO Risk",
        "system": "Exhaust",
        "query": "There's a strong exhaust smell in the cockpit of my Cessna 172 during flight, and I've noticed some black soot stains around the exhaust pipe connections. Is this dangerous?",
        "ground_truth": "CRITICAL SAFETY ISSUE. Exhaust leaks near or forward of the firewall can allow carbon monoxide (CO) into the cabin through the heating system, which draws air over the exhaust muffler/heat shroud. Immediate actions: (1) Open all vents and windows. (2) Turn cabin heat OFF immediately. (3) Land as soon as practicable. Maintenance: Inspect the entire exhaust system — muffler, risers, pipes, clamps, gaskets, and the heater shroud for cracks, holes, or loose connections. The service manual specifies detailed exhaust system inspection procedures including the muffler/heater assembly. Any crack or leak requires immediate repair or replacement. Never fly with a suspected exhaust leak."
    },
    {
        "id": "c172_005",
        "issue": "Low Cylinder Compression",
        "system": "Engine",
        "query": "During the annual inspection, my mechanic found that cylinder #3 on my Cessna 172's Lycoming O-320 has compression of only 42/80. The other cylinders are 68-72/80. What does this mean and what's the fix?",
        "ground_truth": "Low compression on a single cylinder indicates internal engine wear. Common causes: (1) Worn or stuck exhaust valve — the most common cause. Perform a leak-down test: air leaking from the exhaust pipe confirms an exhaust valve not seating properly. (2) Worn piston rings — air leaking past the rings will be heard at the oil filler or breather tube. (3) Worn or damaged cylinder walls. (4) Intake valve not seating. Minimum acceptable compression per Lycoming is 60/80 (or within 15 psi of the highest cylinder). At 42/80, this cylinder is below limits. Typical remedies: valve lapping/resurfacing if the valve seat is the issue, or cylinder removal for inspection and possible overhaul (new rings, hone, valve work). Reference the engine section of the service manual for compression test procedures and limits."
    },
    {
        "id": "c172_006",
        "issue": "Fuel Contamination / Water in Fuel",
        "system": "Fuel",
        "query": "When I sumped the fuel drains on my Cessna 172 this morning, I found water droplets and some sediment in the fuel sample. What should I do?",
        "ground_truth": "Water and sediment contamination in aviation fuel is a serious safety concern. Immediate actions: (1) Continue draining all sump points (wing tank drains, fuel strainer/gascolator drain, lowest point drains) until samples run clear with no visible water or debris. (2) Check fuel cap seals — deteriorated or missing O-ring seals allow rainwater to enter the tanks. Replace damaged seals. (3) Check for condensation — large air spaces in partially filled tanks promote condensation, especially with temperature changes. Keep tanks full when the aircraft is stored. (4) Inspect the fuel strainer/gascolator screen — clean and inspect per the service manual. (5) If contamination is severe, the tanks may need to be drained and flushed. Reference the fuel system inspection and servicing section of the service manual."
    },
    {
        "id": "c172_007",
        "issue": "Alternator Failure",
        "system": "Electrical",
        "query": "In flight, my Cessna 172's ammeter is showing a discharge and the low-voltage warning light came on. What's happening and what should I do?",
        "ground_truth": "The alternator has failed or the voltage regulator has malfunctioned, and the aircraft is now running solely on battery power. Immediate actions: (1) Check the alternator circuit breaker — reset if tripped (one attempt only). (2) Turn off all non-essential electrical equipment to conserve battery. (3) Keep essential items: one radio, transponder if required. (4) Plan to land as soon as practical — battery capacity is limited (30-60 minutes depending on load). Maintenance: Check (1) alternator drive belt — broken or slipping belt is the most common cause. (2) Voltage regulator — faulty regulator prevents proper charging. (3) Alternator brushes — worn brushes lose contact. (4) Alternator field wire and connections. (5) The overvoltage sensor may have tripped. The service manual's electrical system section covers alternator inspection, belt tension specs, and voltage regulator testing."
    },
    {
        "id": "c172_008",
        "issue": "Flap Motor / Flap System Failure",
        "system": "Flight Controls",
        "query": "The flaps on my Cessna 172 are stuck and won't extend or retract when I operate the flap switch. I can hear a clicking sound from the flap motor area but nothing moves. What's wrong?",
        "ground_truth": "The electric flap system has a mechanical or electrical failure. The clicking indicates the relay/solenoid is engaging but the motor can't drive the mechanism. Common causes: (1) Flap motor failure — worn brushes, burned commutator, or internal short. (2) Stripped or worn flap drive screw (jackscrew) — the screw threads wear over time, especially in high-use training aircraft. Inspect the jackscrew for thread damage. (3) Flap transmission/gearbox failure. (4) Bent flap tracks — misalignment prevents flap travel. (5) Flap position limit switches — failed switches prevent motor operation. (6) Corroded or damaged wiring to the flap motor. The service manual covers flap system rigging, motor inspection, jackscrew lubrication, and limit switch adjustment procedures."
    },
    {
        "id": "c172_009",
        "issue": "Engine Oil Leak",
        "system": "Engine / Lubrication",
        "query": "My Cessna 172 is leaving oil drips on the ramp after every flight. There's oil all over the belly and I can see oil on the nose gear tire. Oil consumption has increased noticeably. Where is it coming from?",
        "ground_truth": "Oil leaks on the Lycoming O-320 can originate from multiple sources. Systematic inspection: (1) Rocker cover gaskets — the most common source. Cork gaskets deteriorate and shrink over time. Replace with new gaskets, torque evenly. (2) Oil filler cap and tube — check the O-ring seal. (3) Crankcase through-bolts and parting line — seepage at the case halves indicates deteriorated sealant or case fretting. (4) Pushrod tube seals — O-ring seals on the pushrod housings weep oil as they age. (5) Oil cooler and lines — check fittings and hose connections. (6) Accessory case gasket — rear of engine. (7) Prop governor pad seal. Clean the engine thoroughly, run it, then inspect to identify the source. Oil on the belly typically tracks rearward from the source. The service manual covers engine lubrication system components and inspection procedures."
    },
    {
        "id": "c172_010",
        "issue": "Control Cable Stiffness / Binding",
        "system": "Flight Controls",
        "query": "The elevator controls on my Cessna 172 feel stiff and require more force than normal. There's a notchy, grinding feeling when I move the yoke fore and aft. What could cause this?",
        "ground_truth": "Stiff or binding control cables indicate friction in the control system. Common causes: (1) Control cable pulleys — worn, flat-spotted, or seized pulley bearings create friction and notchiness. Inspect all pulleys in the elevator cable routing for free rotation. (2) Control cables — frayed cables, kinks, or cables rubbing against structure. Inspect cables for broken strands and proper routing through fairleads. (3) Cable tension — incorrect cable tension (too tight) increases friction. Check and adjust per the service manual rigging specifications. (4) Elevator bellcrank — worn bushings or pivot points. (5) Elevator hinge points — worn hinge bearings or corrosion. (6) Foreign object in cable routing — debris can catch in pulleys or fairleads. The service manual covers control system rigging, cable tensions, pulley inspection, and lubrication requirements."
    },
]

# First, check the actual vehicle ID registered on Hetzner
print("Checking registered vehicles...")
r = requests.get(f"{API}/api/vehicles", timeout=10)
vehicles = r.json()["vehicles"]
cessna = None
for v in vehicles:
    if "cessna" in v["id"].lower() or "172" in v["id"].lower() or "skyhawk" in v["id"].lower():
        cessna = v
        break

if not cessna:
    print("ERROR: No Cessna 172 found in vehicle registry!")
    print("Available vehicles:")
    for v in vehicles:
        print(f"  - {v['id']}: {v.get('make','')} {v.get('model','')}")
    sys.exit(1)

VEHICLE_ID = cessna["id"]
print(f"Found vehicle: {VEHICLE_ID} ({cessna.get('make','')} {cessna.get('model','')})")
print(f"Collection: {cessna.get('collection','')}")

# Check stats
r = requests.get(f"{API}/api/stats/{VEHICLE_ID}", timeout=10)
print(f"Stats: {r.json()}")
print()

# Send each query and capture response
results = []
for i, q in enumerate(QUERIES, 1):
    print(f"{'='*70}")
    print(f"[{i}/10] {q['id']}: {q['issue']}")
    print(f"  System: {q['system']}")
    print(f"  Query: {q['query'][:80]}...")
    print()

    try:
        payload = {
            "message": q["query"],
            "vehicle_id": VEHICLE_ID,
            "chat_history": []
        }
        start = time.time()
        r = requests.post(f"{API}/api/chat", json=payload, timeout=120)
        latency = time.time() - start

        if r.status_code == 200:
            data = r.json()
            raw_response = data.get("response", "{}")
            try:
                parsed = json.loads(raw_response)
            except:
                parsed = {"current_state": "PARSE_ERROR", "raw": raw_response[:500]}

            state = parsed.get("current_state", "UNKNOWN")
            instructions = parsed.get("mechanic_instructions", "")
            reasoning = parsed.get("diagnostic_reasoning", "")
            citations = parsed.get("source_citations", [])
            answer_paths = parsed.get("answer_path_prompts", [])

            print(f"  State: {state}")
            print(f"  Latency: {latency:.1f}s")
            print(f"  Citations: {len(citations)}")
            print(f"  Answer paths: {len(answer_paths)}")
            print()
            print(f"  DIAGNOSTIC REASONING:")
            print(f"  {reasoning[:300]}...")
            print()
            print(f"  MECHANIC INSTRUCTIONS:")
            print(f"  {instructions[:400]}...")
            print()
            if answer_paths:
                print(f"  ANSWER PATHS:")
                for j, ap in enumerate(answer_paths, 1):
                    print(f"    {j}. {ap[:80]}")
            print()

            results.append({
                "id": q["id"],
                "issue": q["issue"],
                "system": q["system"],
                "query": q["query"],
                "ground_truth": q["ground_truth"],
                "state": state,
                "latency_s": round(latency, 1),
                "citation_count": len(citations),
                "citations": citations,
                "instructions": instructions,
                "reasoning": reasoning,
                "answer_paths": answer_paths,
            })
        else:
            print(f"  ERROR: HTTP {r.status_code}: {r.text[:200]}")
            results.append({
                "id": q["id"],
                "issue": q["issue"],
                "error": f"HTTP {r.status_code}",
            })
    except Exception as e:
        print(f"  ERROR: {e}")
        results.append({
            "id": q["id"],
            "issue": q["issue"],
            "error": str(e),
        })

    time.sleep(2)

# Save results
import os
out_path = os.path.join("tests", "results", "cessna172_validation.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n{'='*70}")
print(f"VALIDATION COMPLETE — {len(results)} queries processed")
print(f"Results saved to: {out_path}")
print(f"{'='*70}")

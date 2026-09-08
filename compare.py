from storage import get_all_facts
from itertools import combinations

def find_corroborations():
    facts = get_all_facts()
    results = []
    for a, b in combinations(facts, 2):
        if a["document_id"] == b["document_id"]:
            continue
        if a.get("entity") == b.get("entity") and a.get("attribute") == b.get("attribute"):
            if a.get("fact_type") == "numeric" and b.get("fact_type") == "numeric":
                v1 = a.get("value")
                v2 = b.get("value")
                if v1 is not None and v2 is not None and v1 != 0 and v2 != 0:
                    diff = abs(v1 - v2) / max(abs(v1), abs(v2))
                    if diff < 0.10:  
                        results.append({
                            "fact_a": a,
                            "fact_b": b,
                            "explanation": f"{a['entity']} {a['attribute']}: {a['statement']} ≈ {b['statement']}"
                        })
    return results

def find_contradictions():
    facts = get_all_facts()
    results = []
    for a, b in combinations(facts, 2):
        if a["document_id"] == b["document_id"]:
            continue
        if a.get("entity") == b.get("entity") and a.get("attribute") == b.get("attribute"):
            if a.get("fact_type") == "numeric" and b.get("fact_type") == "numeric":
                v1 = a.get("value")
                v2 = b.get("value")
                if v1 is not None and v2 is not None and v1 != 0 and v2 != 0:
                    diff = abs(v1 - v2) / max(abs(v1), abs(v2))
                    if diff > 0.30:
                        results.append({
                            "fact_a": a,
                            "fact_b": b,
                            "explanation": f"Contradiction: {a['statement']} vs {b['statement']} (diff {diff:.0%})"
                        })
    return results

def find_reconciled():
    facts = get_all_facts()
    results = []
    for a, b in combinations(facts, 2):
        if a["document_id"] == b["document_id"]:
            continue
        if a.get("entity") == b.get("entity") and a.get("attribute") == b.get("attribute"):
            if a.get("fact_type") == "numeric" and b.get("fact_type") == "numeric":
                v1 = a.get("value")
                v2 = b.get("value")
                if v1 is not None and v2 is not None and v1 != 0 and v2 != 0:
                    diff = abs(v1 - v2) / max(abs(v1), abs(v2))
                    if diff > 0.15:
                        if a.get("period") != b.get("period") or a.get("year") != b.get("year"):
                            results.append({
                                "fact_a": a,
                                "fact_b": b,
                                "explanation": f"Reconciled by context: {a['statement']} ({a.get('period')}) vs {b['statement']} ({b.get('period')})"
                            })
                        elif a.get("unit") != b.get("unit"):
                            results.append({
                                "fact_a": a,
                                "fact_b": b,
                                "explanation": f"Reconciled by unit: {a['statement']} ({a.get('unit')}) vs {b['statement']} ({b.get('unit')})"
                            })
    return results

def get_failure_example():
    return {
        "description": "Initial extraction failed to detect that '2.8Bn shipments' referred to 'since inception' rather than a single fiscal year.",
        "handling": "Added detection of temporal qualifiers like 'since inception', 'cumulative', 'total'.",
        "improvement": "Implement footnote resolution and context-aware temporal scoping."
    }
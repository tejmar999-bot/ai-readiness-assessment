"""
Scoring logic for Governance-First AI Readiness Framework
"""

from data.dimensions import DIMENSIONS


# ------------------------------------------
# CORE SCORE CALCULATION (WEIGHTED)
# ------------------------------------------

def compute_scores(answers):

    raw_dimension_scores = []
    weighted_dimension_scores = []

    total_weighted_score = 0
    max_possible_weighted = 0

    for dimension in DIMENSIONS:

        dim_total = 0

        for question in dimension["questions"]:
            qid = question["id"]
            dim_total += answers.get(qid, 0)

        raw_dimension_scores.append(dim_total)

        weight = dimension.get("weight", 1.0)

        weighted_score = dim_total * weight
        weighted_dimension_scores.append(weighted_score)

        total_weighted_score += weighted_score
        max_possible_weighted += 15 * weight

    percentage = round((total_weighted_score / max_possible_weighted) * 100, 1)

    readiness_band = get_readiness_band(percentage)

    critical_status = get_critical_dimension_status(raw_dimension_scores)

    governance_index = calculate_governance_index(raw_dimension_scores)

    return {
        "raw_dimension_scores": raw_dimension_scores,
        "dimension_scores": weighted_dimension_scores,
        "total": round(total_weighted_score, 1),
        "max_possible": round(max_possible_weighted, 1),
        "percentage": percentage,
        "readiness_band": readiness_band,
        "critical_status": critical_status,
        "governance_index": governance_index
    }


# ------------------------------------------
# READINESS BANDS (EXECUTIVE TONE)
# ------------------------------------------

def get_readiness_band(percentage):

    if percentage >= 75:
        return {
            "label": "🟢 AI-Ready",
            "description": "Governance, leadership, and operational foundations are sufficiently mature to proceed with structured AI initiatives."
        }

    elif percentage >= 60:
        return {
            "label": "🔵 Conditional Readiness",
            "description": "AI initiatives may proceed cautiously, provided identified weaknesses are remediated in parallel."
        }

    elif percentage >= 45:
        return {
            "label": "🟡 Foundational Exposure",
            "description": "Significant structural gaps exist. AI expansion should pause until foundational controls are strengthened."
        }

    else:
        return {
            "label": "🔴 High Risk – Not Ready",
            "description": "Core governance and operational controls are insufficient. AI initiatives should not proceed."
        }


# ------------------------------------------
# CRITICAL DIMENSION CHECK
# ------------------------------------------

def get_critical_dimension_status(raw_scores):

    below_threshold = []

    for dimension, score in zip(DIMENSIONS, raw_scores):
        if dimension.get("critical", False) and score < 9:
            below_threshold.append((dimension["title"], score))

    if len(below_threshold) >= 2:
        dims = ", ".join([f"{d[0]} ({d[1]}/15)" for d in below_threshold])
        return {
            "severity": "critical",
            "icon": "🛑",
            "title": "Critical Governance Deficiency",
            "message": f"The following critical dimensions are below minimum threshold: {dims}. AI initiatives should not proceed until these exposures are remediated."
        }

    elif len(below_threshold) == 1:
        dim = below_threshold[0]
        return {
            "severity": "warning",
            "icon": "⚠️",
            "title": "Critical Dimension Below Threshold",
            "message": f"{dim[0]} scored {dim[1]}/15 (minimum 9 required). AI expansion should pause until this gap is corrected."
        }

    else:
        return {
            "severity": "info",
            "icon": "✓",
            "title": "Critical Dimensions Satisfied",
            "message": "All governance-critical dimensions meet minimum readiness thresholds."
        }


# ------------------------------------------
# GOVERNANCE RISK INDEX
# ------------------------------------------

def calculate_governance_index(raw_scores):

    governance_score = raw_scores[0]  # Governance is first dimension
    percentage = round((governance_score / 15) * 100)

    return percentage


# ------------------------------------------
# EXECUTIVE SUMMARY (SHARPENED TONE)
# ------------------------------------------

def generate_executive_summary(scores_data):

    raw_scores = scores_data["raw_dimension_scores"]
    readiness_band = scores_data["readiness_band"]
    governance_index = scores_data["governance_index"]

    dimension_results = list(zip(DIMENSIONS, raw_scores))

    # Identify weakest two dimensions
    sorted_dims = sorted(dimension_results, key=lambda x: x[1])
    weakest_two = sorted_dims[:2]

    weakest_text = ", ".join(
        [f"{dim['title']} ({score}/15)" for dim, score in weakest_two]
    )

    summary = (
        f"This evaluation indicates an overall readiness classification of "
        f"{readiness_band['label']}. "
        f"The two most material areas requiring executive attention are "
        f"{weakest_text}. "
        f"These dimensions represent the highest structural exposure to AI-related operational and governance risk. "
    )

    if governance_index < 60:
        summary += (
            "Governance controls are currently insufficient to support scaled AI deployment. "
            "AI initiatives should not expand until governance risk is remediated."
        )
    elif governance_index < 75:
        summary += (
            "Governance maturity is emerging but requires strengthening to support sustainable AI scaling."
        )
    else:
        summary += (
            "Governance maturity is controlled and provides a stable foundation for responsible AI execution."
        )

    summary += (
        " AI amplifies existing strengths and weaknesses. "
        "Proceeding without correcting foundational gaps increases risk rather than value."
    )

    return summary


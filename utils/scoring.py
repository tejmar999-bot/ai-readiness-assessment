from data.dimensions import DIMENSIONS


# ------------------------------------------
# CORE SCORING (NO WEIGHTING)
# ------------------------------------------

def compute_scores(answers):

    raw_dimension_scores = []

    for dimension in DIMENSIONS:
        dim_total = 0
        for question in dimension["questions"]:
            qid = question["id"]
            dim_total += answers.get(qid, 0)

        raw_dimension_scores.append(round(dim_total, 1))

    total_score = sum(raw_dimension_scores)
    percentage = round((total_score / 90) * 100)

    readiness_band = get_readiness_band(percentage)

    critical_status = get_critical_dimension_status(raw_dimension_scores)

    governance_index = calculate_governance_index(raw_dimension_scores)

    # HARD GOVERNANCE OVERRIDE
    if critical_status["severity"] in ["critical", "warning"]:
        if readiness_band["label"] == "🟢 AI-Ready":
            readiness_band = {
                "label": "🔵 Conditional Readiness",
                "color": "#3B82F6",
                "description": "AI scaling restricted due to critical threshold breach."
            }

    return {
        "raw_dimension_scores": raw_dimension_scores,
        "total": total_score,
        "percentage": percentage,
        "readiness_band": readiness_band,
        "critical_status": critical_status,
        "governance_index": governance_index
    }


# ------------------------------------------
# READINESS BAND
# ------------------------------------------

def get_readiness_band(percentage):

    if percentage >= 75:
        return {
            "label": "🟢 AI-Ready",
            "color": "#10B981",
            "description": "Strong governance and operational foundation."
        }

    elif percentage >= 60:
        return {
            "label": "🔵 Conditional Readiness",
            "color": "#3B82F6",
            "description": "AI may proceed cautiously with remediation."
        }

    elif percentage >= 45:
        return {
            "label": "🟡 Foundational Exposure",
            "color": "#F59E0B",
            "description": "Significant structural gaps present."
        }

    else:
        return {
            "label": "🔴 High Risk – Not Ready",
            "color": "#DC2626",
            "description": "Core governance controls insufficient."
        }


# ------------------------------------------
# GOVERNANCE INDEX
# ------------------------------------------

def calculate_governance_index(raw_scores):
    governance_score = raw_scores[0]  # Governance is first dimension
    return round((governance_score / 15) * 100)


# ------------------------------------------
# CRITICAL DIMENSION CHECK
# ------------------------------------------

def get_critical_dimension_status(raw_scores):

    governance = raw_scores[0]
    leadership = raw_scores[1]
    data = raw_scores[2]

    failed = []

    if governance < 9:
        failed.append(f"Governance ({governance}/15)")
    if leadership < 9:
        failed.append(f"Executive Leadership ({leadership}/15)")
    if data < 9:
        failed.append(f"Data Foundations ({data}/15)")

    if len(failed) >= 2:
        return {
            "severity": "critical",
            "icon": "🛑",
            "title": "Critical Threshold Breach",
            "message": ", ".join(failed) + " are below minimum threshold (9.0)."
        }

    elif len(failed) == 1:
        return {
            "severity": "warning",
            "icon": "⚠️",
            "title": "Critical Threshold Warning",
            "message": failed[0] + " is below minimum threshold (9.0)."
        }

    else:
        return {
            "severity": "info",
            "icon": "✓",
            "title": "All Critical Thresholds Met",
            "message": "Governance, Leadership, and Data meet minimum threshold."
        }

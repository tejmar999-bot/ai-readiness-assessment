"""
Recommendation engine for Governance-First AI Readiness Framework
Generates executive-level action directives by dimension.
"""

from data.dimensions import DIMENSIONS


def generate_dimension_recommendations(scores_data):

    raw_scores = scores_data["raw_dimension_scores"]

    dimension_results = list(zip(DIMENSIONS, raw_scores))

    recommendations_output = []

    for dimension, score in dimension_results:

        title = dimension["title"]

        if score >= 12:
            recs = strong_directives(dimension)

        elif score >= 9:
            recs = moderate_directives(dimension)

        else:
            recs = critical_directives(dimension)

        recommendations_output.append({
            "title": title,
            "score": score,
            "recommendations": recs
        })

    return recommendations_output


# ----------------------------------------------------
# DIRECTIVE TIERS
# ----------------------------------------------------

def strong_directives(dimension):
    return [
        "Maintain current governance and oversight standards with periodic executive review.",
        "Benchmark this dimension against industry leaders to prevent complacency.",
        "Document and institutionalize best practices to preserve operational discipline."
    ]


def moderate_directives(dimension):
    return [
        "Strengthen formal controls and executive oversight within this dimension.",
        "Assign accountable ownership for measurable improvement within 90 days.",
        "Implement structured performance tracking to prevent regression."
    ]


def critical_directives(dimension):
    """
    Dimension-specific action directives for scores below threshold.
    """

    if dimension["id"] == "governance":
        return [
            "Establish a formal AI governance framework covering privacy, vendor risk, and model oversight.",
            "Define executive accountability for AI risk and compliance exposure.",
            "Implement structured third-party AI vendor evaluation and monitoring immediately."
        ]

    elif dimension["id"] == "leadership":
        return [
            "Define a formal AI strategy aligned to measurable business objectives.",
            "Assign a named executive accountable for AI performance and risk.",
            "Allocate structured funding tied to governance-approved milestones."
        ]

    elif dimension["id"] == "data":
        return [
            "Implement enforceable data governance standards across core systems.",
            "Remediate known data quality deficiencies before expanding AI use cases.",
            "Establish controlled access frameworks to prevent unauthorized data exposure."
        ]

    elif dimension["id"] == "process":
        return [
            "Document and standardize all mission-critical workflows prior to AI automation.",
            "Introduce KPI tracking to quantify operational stability.",
            "Embed structured continuous improvement discipline."
        ]

    elif dimension["id"] == "technology":
        return [
            "Modernize infrastructure to ensure scalability and secure AI integration.",
            "Eliminate system silos that increase data and operational risk.",
            "Implement formal cybersecurity enforcement tied to AI deployment."
        ]

    elif dimension["id"] == "people":
        return [
            "Launch structured AI literacy and governance training across teams.",
            "Define change-management oversight for AI-driven transformation.",
            "Establish executive-aligned communication to reduce resistance risk."
        ]

    else:
        return [
            "Strengthen controls and executive oversight within this dimension.",
            "Assign accountable ownership and measurable targets.",
            "Conduct structured review within 90 days."
        ]

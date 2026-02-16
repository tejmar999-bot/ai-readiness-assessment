"""
HTML report generator for Governance-First AI Readiness Framework
Executive Risk & Readiness Report
"""

from datetime import datetime
from utils.scoring import generate_executive_summary
from utils.recommendations import generate_dimension_recommendations
from data.dimensions import DIMENSIONS


def generate_html_report(
    scores_data,
    company_name="",
    company_logo_b64=None,
    primary_color="#F97316",
    assessment_date=None,
):

    if not assessment_date:
        assessment_date = datetime.now().strftime("%B %d, %Y")

    total_score = scores_data.get("total", 0)
    max_possible = scores_data.get("max_possible", 100)
    percentage = scores_data.get("percentage", 0)
    readiness_band = scores_data.get("readiness_band", {})
    critical_status = scores_data.get("critical_status", {})
    raw_scores = scores_data.get("raw_dimension_scores", [])
    governance_index = scores_data.get("governance_index", 0)

    dimension_icons = ['⚖️', '🎯', '📊', '⚙️', '💻', '👥']

    def governance_label(index):
        if index >= 80:
            return "Controlled Governance Risk"
        elif index >= 60:
            return "Emerging Governance Exposure"
        elif index >= 40:
            return "Significant Governance Risk"
        return "Critical Governance Deficiency"

    def score_color(score):
        if score < 7:
            return "#DC2626"
        elif score < 9:
            return "#F97316"
        elif score < 12:
            return "#10B981"
        return "#059669"

    exec_summary = generate_executive_summary(scores_data)
    dimension_recommendations = generate_dimension_recommendations(scores_data)

    # -----------------------------
    # CRITICAL ALERT
    # -----------------------------
    critical_alert_html = ""

    if critical_status.get("severity") != "info":
        critical_alert_html = f"""
        <div style="border-left:4px solid #DC2626;background:#FEE2E2;padding:12px;margin:15px 0;">
            <strong>{critical_status.get('icon','')} {critical_status.get('title','')}</strong><br>
            {critical_status.get('message','')}
        </div>
        """

    # -----------------------------
    # DIMENSION BARS
    # -----------------------------
    dimension_bars_html = ""

    for i, dimension in enumerate(DIMENSIONS):
        raw_score = raw_scores[i]
        star = " ⭐" if dimension.get("critical", False) else ""
        width = (raw_score / 15) * 100
        color = score_color(raw_score)

        dimension_bars_html += f"""
        <div style="margin-bottom:10px;">
            <div style="font-weight:600;font-size:12px;">
                {dimension_icons[i]} {dimension['title']}{star}
            </div>
            <div style="height:18px;background:#E5E7EB;border-radius:4px;">
                <div style="width:{width:.0f}%;height:18px;background:{color};color:white;font-size:9px;text-align:right;padding-right:4px;border-radius:4px;">
                    {raw_score:.1f}/15
                </div>
            </div>
        </div>
        """

    # -----------------------------
    # DIMENSION CARDS (Action Directives)
    # -----------------------------
    dimension_cards_html = ""

    for i, (dimension, rec_item) in enumerate(zip(DIMENSIONS, dimension_recommendations)):
        raw_score = raw_scores[i]
        star = " ⭐" if dimension.get("critical", False) else ""

        rec_list = "".join(
            [f"<li>{rec}</li>" for rec in rec_item["recommendations"]]
        )

        dimension_cards_html += f"""
        <div style="margin-bottom:14px;padding:12px;background:#F9FAFB;border-left:4px solid {primary_color};font-size:11px;">
            <strong>{dimension_icons[i]} {dimension['title']}{star}</strong><br>
            <span style="color:#6B7280;">Score: {raw_score:.1f}/15</span>
            <div style="margin-top:6px;font-weight:600;">Executive Action Directives:</div>
            <ul>{rec_list}</ul>
        </div>
        """

    # -----------------------------
    # PRIORITY ACTIONS
    # -----------------------------
    priority_actions = []

    for i, (dimension, rec_item) in enumerate(zip(DIMENSIONS, dimension_recommendations)):
        raw_score = raw_scores[i]

        if raw_score < 9:
            priority_actions.append({
                "dimension": dimension["title"],
                "score": raw_score,
                "action": rec_item["recommendations"][0]
            })

    priority_actions = sorted(priority_actions, key=lambda x: x["score"])[:3]

    priority_html = ""

    for idx, action in enumerate(priority_actions):
        priority_html += f"""
        <div style="margin-bottom:10px;padding:10px;background:#F0F9FF;border:1px solid #BAE6FD;border-radius:4px;font-size:11px;">
            <strong>Priority {idx+1}: {action['dimension']}</strong><br>
            {action['action']}
        </div>
        """

    # -----------------------------
    # HEADER INFO
    # -----------------------------
    company_section = (
        f"<strong>{company_name}</strong><br>Date: {assessment_date}"
        if company_name else f"Date: {assessment_date}"
    )

    logo_html = ""
    if company_logo_b64:
        logo_html = f'<img src="data:image/png;base64,{company_logo_b64}" style="max-width:120px;">'

    # -----------------------------
    # FINAL HTML
    # -----------------------------
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Governance-First AI Readiness Framework</title>
<style>
body {{ font-family: Arial, Helvetica, sans-serif; background:#F9FAFB; color:#1F2937; }}
.report {{ max-width:8.5in; margin:auto; background:white; padding:0.6in; page-break-after:always; }}
.metric-box {{ display:flex; gap:20px; margin:20px 0; }}
.metric {{ flex:1; border:1px solid #E5E7EB; padding:12px; border-radius:6px; text-align:center; }}
</style>
</head>
<body>

<div class="report">

<h1 style="color:{primary_color};">Governance-First AI Readiness Framework</h1>
<div style="font-size:12px;color:#6B7280;margin-bottom:10px;">
Executive Risk & Readiness Report
</div>

<div>{company_section}</div>
{logo_html}

<div class="metric-box">

    <div class="metric">
        <div style="font-size:11px;color:#6B7280;">Weighted Readiness Score</div>
        <div style="font-size:20px;font-weight:bold;color:{primary_color};">
            {total_score:.1f} / {max_possible:.1f}
        </div>
        <div style="font-size:11px;color:#6B7280;">{percentage}%</div>
    </div>

    <div class="metric">
        <div style="font-size:11px;color:#6B7280;">Readiness Classification</div>
        <div style="font-size:18px;font-weight:bold;color:{primary_color};">
            {readiness_band.get('label','N/A')}
        </div>
    </div>

    <div class="metric">
        <div style="font-size:11px;color:#6B7280;">Governance Risk Index</div>
        <div style="font-size:20px;font-weight:bold;color:{primary_color};">
            {governance_index}%
        </div>
        <div style="font-size:11px;color:#6B7280;">
            {governance_label(governance_index)}
        </div>
    </div>

</div>

{critical_alert_html}

<h3>Dimension Performance Overview</h3>
{dimension_bars_html}

<h3>Executive Summary</h3>
<p style="font-size:11px;line-height:1.6;">
{exec_summary}
</p>

</div>

<div class="report">

<h2 style="color:{primary_color};">Executive Action Plan</h2>

{dimension_cards_html}

<h3>Immediate Action Priorities</h3>
{priority_html}

<div style="margin-top:25px;padding:15px;border-top:2px solid {primary_color};background:#F8FAFC;">
<strong>Executive Strategy Consultation</strong><br>
If AI investment or governance exposure is under consideration, 
a structured executive review is recommended to align findings with operational priorities.
</div>

</div>

</body>
</html>
"""

    return html

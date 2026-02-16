"""
Industry Benchmarks for AI Process Readiness Assessment
"""
from db.models import DEFAULT_BASELINE
from data.dimensions import DIMENSIONS

# Industry benchmark scores (average scores across different maturity levels)
INDUSTRY_BENCHMARKS = {

    'Small Business (< 50 employees)': {
        'governance': 6.0,
        'leadership': 6.4,
        'data': 6.8,
        'process': 7.4,
        'technology': 7.0,
        'people': 7.7,
        'total': 41.3,
        'description': 'Small organizations typically have informal governance and limited AI infrastructure.'
    },

    'Mid-Market (50–500 employees)': {
        'governance': 7.6,
        'leadership': 8.1,
        'data': 8.3,
        'process': 8.9,
        'technology': 8.4,
        'people': 9.3,
        'total': 50.6,
        'description': 'Mid-market organizations often have emerging governance structures and are scaling AI capabilities.'
    },

    'Enterprise (500+ employees)': {
        'governance': 9.0,
        'leadership': 9.5,
        'data': 9.9,
        'process': 10.1,
        'technology': 10.3,
        'people': 11.0,
        'total': 59.8,
        'description': 'Large enterprises typically operate structured governance frameworks with active AI programs.'
    },

    'Technology Leaders': {
        'governance': 10.4,
        'leadership': 10.9,
        'data': 11.2,
        'process': 11.5,
        'technology': 11.8,
        'people': 12.3,
        'total': 68.1,
        'description': 'Technology-first organizations with advanced AI governance, data maturity, and execution discipline.'
    },

    'Industry Average': {
        'governance': 9.2,
        'leadership': 9.6,
        'data': 10.2,
        'process': 10.8,
        'technology': 10.5,
        'people': 11.1,
        'total': 61.4,
        'description': 'Average readiness levels across industries and company sizes.'
    }
}


from data.dimensions import DIMENSIONS


# ------------------------------------------
# BENCHMARK COMPARISON
# ------------------------------------------

def get_benchmark_comparison(your_scores, benchmark_name="Industry Average"):

    if benchmark_name not in INDUSTRY_BENCHMARKS:
        benchmark_name = "Industry Average"

    benchmark = INDUSTRY_BENCHMARKS[benchmark_name]
    dimension_scores = your_scores["dimension_scores"]

    comparison = {
        "benchmark_name": benchmark_name,
        "benchmark_description": benchmark["description"],
        "your_total": round(your_scores["total"], 1),
        "benchmark_total": round(benchmark["total"], 1),
        "total_difference": round(your_scores["total"] - benchmark["total"], 1),
        "dimensions": []
    }

    for score_data in dimension_scores:

        dim_id = score_data["id"]
        your_score = round(score_data["score"], 1)
        benchmark_score = round(benchmark.get(dim_id, 0), 1)

        difference = round(your_score - benchmark_score, 1)

        # Color-coded performance label
        if difference >= 1:
            label = "Above Benchmark"
            color = "#10B981"  # Green
        elif difference <= -1:
            label = "Below Benchmark"
            color = "#DC2626"  # Red
        else:
            label = "In Line"
            color = "#F59E0B"  # Amber

        comparison["dimensions"].append({
            "id": dim_id,
            "title": score_data["title"],
            "your_score": your_score,
            "benchmark_score": benchmark_score,
            "difference": difference,
            "performance_label": label,
            "color": color
        })

    return comparison


# ------------------------------------------
# BENCHMARK LIST
# ------------------------------------------

def get_all_benchmarks():
    return ["Moving Average Benchmark"] + list(INDUSTRY_BENCHMARKS.keys())


def get_benchmark_data(benchmark_name):

    if benchmark_name == "Moving Average Benchmark":
        return get_moving_average_benchmark()

    return INDUSTRY_BENCHMARKS.get(
        benchmark_name,
        INDUSTRY_BENCHMARKS["Industry Average"]
    )


# ------------------------------------------
# MOVING AVERAGE BENCHMARK
# ------------------------------------------

def get_moving_average_benchmark():

    try:
        from db.operations import get_current_benchmark

        benchmark_scores = get_current_benchmark()

        benchmark_dict = {}
        total = 0

        # Align strictly to DIMENSIONS order
        for i, dimension in enumerate(DIMENSIONS):
            dim_id = dimension["id"]

            score = benchmark_scores[i] if i < len(benchmark_scores) else 9.0
            score = round(score, 1)

            benchmark_dict[dim_id] = score
            total += score

        benchmark_dict["total"] = round(total, 1)
        benchmark_dict["description"] = (
            "Dynamic moving average benchmark from completed AI Readiness Pro assessments."
        )

        return benchmark_dict

    except Exception as e:
        print(f"Benchmark fetch error: {e}")

        # Fallback baseline aligned to dimension order
        fallback = {dim["id"]: 9.0 for dim in DIMENSIONS}
        fallback["total"] = round(9.0 * len(DIMENSIONS), 1)
        fallback["description"] = "Baseline benchmark (dynamic benchmark unavailable)."

        return fallback

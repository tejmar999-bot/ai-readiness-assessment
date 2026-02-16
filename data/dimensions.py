"""
Dimension and question definitions for Governance-First AI Readiness Framework
"""

PALETTE = [
    '#D7BDE2',  # Governance
    '#9DD0F8',  # Leadership
    '#FFFB4B',  # Data
    '#D17070',  # Process
    '#FDD9B8',  # Technology
    '#B9F0C9',  # People
]

DIMENSIONS = [

    # 1️⃣ GOVERNANCE (FIRST)
    {
        'id': 'governance',
        'title': 'AI Governance & Risk',
        'weight': 1.5,
        'critical': True,
        'color': PALETTE[0],
        'questions': [
            {
                'id': 'gov_privacy',
                'text': 'How formally are AI data privacy, retention, and security policies governed?',
                'answer_choices': {
                    1: 'No AI-specific controls',
                    2: 'Generic IT policies only',
                    3: 'Defined privacy controls for AI',
                    4: 'Formal AI governance oversight',
                    5: 'Enterprise-grade governance with audits'
                }
            },
            {
                'id': 'gov_vendor',
                'text': 'How are AI vendors and third-party models evaluated and monitored?',
                'answer_choices': {
                    1: 'No structured review',
                    2: 'Basic procurement checks',
                    3: 'Security & compliance evaluation',
                    4: 'Formal AI vendor governance framework',
                    5: 'Ongoing third-party AI risk monitoring'
                }
            },
            {
                'id': 'gov_model',
                'text': 'How are AI models monitored for bias, drift, and unintended impact?',
                'answer_choices': {
                    1: 'No monitoring',
                    2: 'Reactive only',
                    3: 'Periodic reviews',
                    4: 'Defined monitoring framework',
                    5: 'Continuous oversight with executive reporting'
                }
            }
        ]
    },

    # 2️⃣ LEADERSHIP
    {
        'id': 'leadership',
        'title': 'Executive Leadership',
        'weight': 1.4,
        'critical': True,
        'color': PALETTE[1],
        'questions': [
            {
                'id': 'leadership_strategy',
                'text': 'How clearly is AI embedded into corporate strategy?',
                'answer_choices': {
                    1: 'No AI strategy',
                    2: 'Exploratory discussion',
                    3: 'Defined AI goals',
                    4: 'Formal AI roadmap',
                    5: 'AI embedded into enterprise strategy'
                }
            },
            {
                'id': 'leadership_funding',
                'text': 'Is dedicated funding allocated to AI initiatives?',
                'answer_choices': {
                    1: 'No budget',
                    2: 'Limited experimentation',
                    3: 'Defined pilot budget',
                    4: 'Strategic funding',
                    5: 'Multi-year AI investment strategy'
                }
            },
            {
                'id': 'leadership_accountability',
                'text': 'Is there executive accountability for AI risk and outcomes?',
                'answer_choices': {
                    1: 'No ownership',
                    2: 'Informal ownership',
                    3: 'Named executive sponsor',
                    4: 'Formal accountability structure',
                    5: 'Board-level AI oversight'
                }
            }
        ]
    },

    # 3️⃣ DATA
    {
        'id': 'data',
        'title': 'Data Foundations',
        'weight': 1.4,
        'critical': True,
        'color': PALETTE[2],
        'questions': [
            {
                'id': 'data_quality',
                'text': 'How reliable and accurate is your operational data?',
                'answer_choices': {
                    1: 'Frequent errors',
                    2: 'Known quality issues',
                    3: 'Generally usable',
                    4: 'High-quality with monitoring',
                    5: 'Trusted and governed'
                }
            },
            {
                'id': 'data_access',
                'text': 'How accessible is data for strategic decisions?',
                'answer_choices': {
                    1: 'Hard to access',
                    2: 'Manual extraction',
                    3: 'Available but slow',
                    4: 'Readily accessible',
                    5: 'Enterprise self-service'
                }
            },
            {
                'id': 'data_governance',
                'text': 'How mature are your data governance standards?',
                'answer_choices': {
                    1: 'No governance',
                    2: 'Informal controls',
                    3: 'Defined standards',
                    4: 'Actively enforced',
                    5: 'Comprehensive governance'
                }
            }
        ]
    },

    # 4️⃣ PROCESS
    {
        'id': 'process',
        'title': 'Process Discipline',
        'weight': 1.0,
        'color': PALETTE[3],
        'questions': [
            {
                'id': 'proc_documented',
                'text': 'How formally are mission-critical workflows documented?',
                'answer_choices': {
                    1: 'Undocumented',
                    2: 'Partially documented',
                    3: 'Key workflows documented',
                    4: 'Documented & followed',
                    5: 'Optimized continuously'
                }
            },
            {
                'id': 'proc_metrics',
                'text': 'How consistently are KPIs tracked?',
                'answer_choices': {
                    1: 'No tracking',
                    2: 'Ad-hoc',
                    3: 'Basic dashboards',
                    4: 'Automated tracking',
                    5: 'Real-time optimization'
                }
            },
            {
                'id': 'proc_improvement',
                'text': 'How structured is continuous improvement?',
                'answer_choices': {
                    1: 'Reactive',
                    2: 'Occasional review',
                    3: 'Periodic cycles',
                    4: 'Defined framework',
                    5: 'Embedded discipline'
                }
            }
        ]
    },

    # 5️⃣ TECHNOLOGY
    {
        'id': 'technology',
        'title': 'Technology Architecture',
        'weight': 1.1,
        'color': PALETTE[4],
        'questions': [
            {
                'id': 'tech_modern',
                'text': 'How modern and scalable is your technology stack?',
                'answer_choices': {
                    1: 'Legacy',
                    2: 'Mixed',
                    3: 'Current systems',
                    4: 'Cloud-based',
                    5: 'API-first architecture'
                }
            },
            {
                'id': 'tech_integration',
                'text': 'How integrated are core systems?',
                'answer_choices': {
                    1: 'Siloed',
                    2: 'Manual integrations',
                    3: 'Partial automation',
                    4: 'Reliable integration',
                    5: 'Real-time integration'
                }
            },
            {
                'id': 'tech_security',
                'text': 'How mature is cybersecurity enforcement?',
                'answer_choices': {
                    1: 'Minimal controls',
                    2: 'Basic policies',
                    3: 'Defined controls',
                    4: 'Audited enforcement',
                    5: 'Enterprise-grade governance'
                }
            }
        ]
    },

    # 6️⃣ PEOPLE
    {
        'id': 'people',
        'title': 'People Capability',
        'weight': 1.2,
        'color': PALETTE[5],
        'questions': [
            {
                'id': 'people_literacy',
                'text': 'How strong is AI literacy across teams?',
                'answer_choices': {
                    1: 'Very limited',
                    2: 'Basic familiarity',
                    3: 'Working knowledge',
                    4: 'Functional proficiency',
                    5: 'Advanced AI fluency'
                }
            },
            {
                'id': 'people_training',
                'text': 'How structured are AI upskilling efforts?',
                'answer_choices': {
                    1: 'None',
                    2: 'Ad-hoc',
                    3: 'Periodic programs',
                    4: 'Defined pathways',
                    5: 'Enterprise-wide strategy'
                }
            },
            {
                'id': 'people_change',
                'text': 'How receptive is the organization to AI-driven change?',
                'answer_choices': {
                    1: 'Resistant',
                    2: 'Skeptical',
                    3: 'Neutral',
                    4: 'Supportive',
                    5: 'Innovation-driven'
                }
            }
        ]
    }

]

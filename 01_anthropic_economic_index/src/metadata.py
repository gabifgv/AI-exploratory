"""
Metadata and data dictionary for the Anthropic Economic Index dataset.
Source: https://huggingface.co/datasets/Anthropic/EconomicIndex
"""

# ---------------------------------------------------------------------------
# Releases
# ---------------------------------------------------------------------------
RELEASES = {
    "release_2025_09_15": {
        "label":        "Ago 2025",
        "reference_dt": "2025-08-07",
        "period":       "2025-08-04 to 2025-08-11",
        "schema":       "enriched",
        "file":         "release_2025_09_15/data/output/aei_enriched_claude_ai_2025-08-04_to_2025-08-11.csv",
        "notes":        "First release with geographic (country-level) data. Enriched schema includes derived per-capita metrics and collaboration classification.",
    },
    "release_2026_01_15": {
        "label":        "Nov 2025",
        "reference_dt": "2025-11-16",
        "period":       "2025-11-13 to 2025-11-20",
        "schema":       "raw",
        "file":         "release_2026_01_15/data/intermediate/aei_raw_claude_ai_2025-11-13_to_2025-11-20.csv",
        "notes":        "Raw schema. Does not include automation_pct, augmentation_pct, or onet_task_pct_index.",
    },
    "release_2026_03_24": {
        "label":        "Fev 2026",
        "reference_dt": "2026-02-08",
        "period":       "2026-02-05 to 2026-02-12",
        "schema":       "raw",
        "file":         "release_2026_03_24/data/aei_raw_claude_ai_2026-02-05_to_2026-02-12.csv",
        "notes":        "Most recent release. Adds new variables: human_only_ability_pct, multitasking_pct, task_success_pct, use_case_pct.",
    },
}

# ---------------------------------------------------------------------------
# Base columns (present in every file)
# ---------------------------------------------------------------------------
BASE_COLUMNS = {
    "geo_id": {
        "type":        "string",
        "description": "Geographic identifier. ISO-3166 alpha-3 for countries (e.g. BRA, USA) or US state FIPS codes for states. 'GLOBAL' for global aggregates.",
        "example":     "BRA",
    },
    "geography": {
        "type":        "categorical",
        "values":      ["country", "state_us", "global"],
        "description": "Level of geographic aggregation.",
        "example":     "country",
    },
    "date_start": {
        "type":        "date",
        "description": "Start date of the data collection window.",
        "example":     "2025-08-04",
    },
    "date_end": {
        "type":        "date",
        "description": "End date of the data collection window.",
        "example":     "2025-08-11",
    },
    "platform_and_product": {
        "type":        "string",
        "description": "Platform that generated the data.",
        "example":     "Claude AI (Free and Pro)",
    },
    "facet": {
        "type":        "categorical",
        "description": "Analysis dimension. Defines what 'cluster_name' represents in each row.",
        "values": {
            "country":               "Geographic usage metrics (usage_pct, per_capita, automation, etc.)",
            "onet_task":             "Usage broken down by O*NET occupational task",
            "collaboration":         "Usage broken down by collaboration pattern (directive, validation, etc.)",
            "request":               "Usage broken down by request cluster (type of work requested)",
            "onet_task::collaboration": "Cross-tabulation: task × collaboration pattern",
        },
    },
    "level": {
        "type":        "integer",
        "description": "Hierarchy level within the facet tree (0 = top level, 1 = subcategory, 2 = leaf).",
        "example":     0,
    },
    "variable": {
        "type":        "categorical",
        "description": "Name of the metric. See VARIABLES dict for full documentation.",
        "example":     "usage_per_capita_index",
    },
    "cluster_name": {
        "type":        "string",
        "description": "Entity within the facet. For onet_task: the task description. For collaboration: pattern name. For request: cluster label. Cross-facets use 'base::sub' format.",
        "example":     "Write reports or other documents",
    },
    "value": {
        "type":        "float",
        "description": "Numeric value of the metric defined by 'variable'.",
        "example":     1.23,
    },
    # Added by our pipeline
    "country_name": {
        "type":        "string",
        "description": "Human-readable country name in English, joined from World Bank population data. NULL for aggregates (AFE, ARB, etc.) and US states.",
        "example":     "Brazil",
        "source":      "Derived — joined from working_age_pop_2024_country_raw.csv",
    },
    "release_label": {
        "type":        "categorical",
        "values":      ["Ago 2025", "Nov 2025", "Fev 2026"],
        "description": "Human-readable label for the data release snapshot. Enables temporal comparison.",
        "source":      "Derived — added during pipeline load",
    },
    "release_date": {
        "type":        "datetime",
        "description": "Reference date (midpoint of collection week) for the release. Use for time-series ordering.",
        "source":      "Derived — added during pipeline load",
    },
}

# ---------------------------------------------------------------------------
# Variables (values of the 'variable' column)
# ---------------------------------------------------------------------------
VARIABLES = {
    # --- Usage ---
    "usage_count": {
        "unit":        "conversations",
        "description": "Raw number of Claude.ai conversations attributed to this facet/cluster.",
        "availability": ["Ago 2025", "Nov 2025", "Fev 2026"],
        "facets":      ["country"],
    },
    "usage_pct": {
        "unit":        "fraction [0-1]",
        "description": "Share of total platform conversations attributed to this geography.",
        "availability": ["Ago 2025", "Nov 2025", "Fev 2026"],
        "facets":      ["country"],
    },
    "usage_per_capita": {
        "unit":        "conversations / working-age person",
        "description": "Raw per-capita usage: usage_count / working_age_population.",
        "availability": ["Ago 2025"],
        "facets":      ["country"],
    },
    "usage_per_capita_index": {
        "unit":        "index (global average = 1.0)",
        "description": "Country's per-capita usage divided by the global average. >1 means above-average adoption. Computed for all releases in our pipeline via usage_pct / pop_share.",
        "availability": ["Ago 2025", "Nov 2025 (computed)", "Fev 2026 (computed)"],
        "facets":      ["country"],
        "interpretation": ">1 = above global average | <1 = below | 2.0 = twice the average",
    },
    "usage_tier": {
        "unit":        "categorical",
        "description": "Binned usage level (Low / Medium / High) relative to global distribution.",
        "availability": ["Ago 2025"],
        "facets":      ["country"],
    },
    # --- O*NET Tasks ---
    "onet_task_count": {
        "unit":        "conversations",
        "description": "Number of conversations classified as involving this O*NET task.",
        "availability": ["Ago 2025", "Nov 2025", "Fev 2026"],
        "facets":      ["onet_task"],
    },
    "onet_task_pct": {
        "unit":        "fraction [0-1]",
        "description": "Share of the country's conversations involving this O*NET task.",
        "availability": ["Ago 2025", "Nov 2025", "Fev 2026"],
        "facets":      ["onet_task"],
    },
    "onet_task_pct_index": {
        "unit":        "index (global average = 1.0)",
        "description": "Specialization index: country's task share divided by the global task share. Reveals which tasks a country over/under-uses vs. the world.",
        "availability": ["Ago 2025"],
        "facets":      ["onet_task"],
        "interpretation": ">1 = country specializes in this task more than globally",
    },
    "soc_pct": {
        "unit":        "fraction [0-1]",
        "description": "Share of usage mapped to this SOC occupational major group.",
        "availability": ["Ago 2025"],
        "facets":      ["country"],
    },
    # --- Collaboration patterns ---
    "collaboration_count": {
        "unit":        "conversations",
        "description": "Conversations exhibiting this collaboration pattern.",
        "availability": ["Ago 2025", "Nov 2025", "Fev 2026"],
        "facets":      ["collaboration"],
    },
    "collaboration_pct": {
        "unit":        "fraction [0-1]",
        "description": "Share of conversations with this collaboration pattern within the geography.",
        "availability": ["Ago 2025", "Nov 2025", "Fev 2026"],
        "facets":      ["collaboration"],
    },
    "collaboration_pct_index": {
        "unit":        "index (global average = 1.0)",
        "description": "Specialization index for collaboration patterns. Shows whether a country over/under-uses a given pattern vs. globally.",
        "availability": ["Ago 2025"],
        "facets":      ["collaboration"],
    },
    "automation_pct": {
        "unit":        "fraction [0-1]",
        "description": "Fraction of classifiable conversations where the model executes tasks autonomously (directive + feedback_loop patterns). High = AI as operator.",
        "availability": ["Ago 2025"],
        "facets":      ["country"],
        "interpretation": "Higher = more autonomous AI use (AI does the work)",
    },
    "augmentation_pct": {
        "unit":        "fraction [0-1]",
        "description": "Fraction of classifiable conversations where the human maintains control (validation + task_iteration + learning patterns). High = AI as assistant.",
        "availability": ["Ago 2025"],
        "facets":      ["country"],
        "interpretation": "Higher = human-in-the-loop use (AI assists the human)",
    },
    # --- Request clusters ---
    "request_count": {
        "unit":        "conversations",
        "description": "Conversations belonging to this request cluster (type of work).",
        "availability": ["Ago 2025", "Nov 2025", "Fev 2026"],
        "facets":      ["request"],
    },
    "request_pct": {
        "unit":        "fraction [0-1]",
        "description": "Share of country's conversations in this request cluster.",
        "availability": ["Ago 2025", "Nov 2025", "Fev 2026"],
        "facets":      ["request"],
    },
    "request_pct_index": {
        "unit":        "index (global average = 1.0)",
        "description": "Specialization index for request clusters.",
        "availability": ["Ago 2025"],
        "facets":      ["request"],
    },
    # --- New in Fev 2026 ---
    "human_only_ability_pct": {
        "unit":        "fraction [0-1]",
        "description": "Share of tasks classified as requiring human-only abilities (judgment, creativity, relationships) — not automatable by current AI.",
        "availability": ["Fev 2026"],
        "facets":      ["onet_task"],
    },
    "multitasking_pct": {
        "unit":        "fraction [0-1]",
        "description": "Share of conversations involving multiple concurrent tasks.",
        "availability": ["Fev 2026"],
        "facets":      ["country", "onet_task"],
    },
    "task_success_pct": {
        "unit":        "fraction [0-1]",
        "description": "Estimated fraction of tasks where the model successfully completed the user's goal.",
        "availability": ["Fev 2026"],
        "facets":      ["onet_task"],
    },
    "use_case_pct": {
        "unit":        "fraction [0-1]",
        "description": "Share of usage belonging to each high-level use case category.",
        "availability": ["Fev 2026"],
        "facets":      ["country", "request"],
    },
    # --- Contextual (enriched only) ---
    "working_age_pop": {
        "unit":        "people",
        "description": "Working-age population (ages 15-64) for the geography. Source: World Bank.",
        "availability": ["Ago 2025"],
        "facets":      ["country"],
    },
    "gdp_per_working_age_capita": {
        "unit":        "USD",
        "description": "GDP divided by working-age population. Proxy for economic development.",
        "availability": ["Ago 2025"],
        "facets":      ["country"],
    },
}

# ---------------------------------------------------------------------------
# Collaboration pattern glossary
# ---------------------------------------------------------------------------
COLLABORATION_PATTERNS = {
    "directive":      "Human gives instructions; model executes with minimal back-and-forth. → Automation signal.",
    "feedback_loop":  "Iterative with model leading, human providing course corrections. → Automation signal.",
    "validation":     "Human reviews and validates model output before acting. → Augmentation signal.",
    "task_iteration": "Human actively refines the task through multiple rounds. → Augmentation signal.",
    "learning":       "Human uses the interaction to build knowledge or skills. → Augmentation signal.",
    "none":           "No clear collaboration pattern detected.",
}

# ---------------------------------------------------------------------------
# Country comparables used in analysis
# ---------------------------------------------------------------------------
BRAZIL = "BRA"
COMPARABLES = ["BRA", "ARG", "MEX", "IND", "ZAF", "COL", "CHL"]
COUNTRY_LABELS = {
    "BRA": "Brasil",       "ARG": "Argentina",    "MEX": "México",
    "IND": "Índia",        "ZAF": "África do Sul", "COL": "Colômbia",
    "CHL": "Chile",        "USA": "EUA",           "GBR": "Reino Unido",
    "FRA": "França",       "DEU": "Alemanha",      "AUS": "Austrália",
    "CAN": "Canadá",       "JPN": "Japão",         "KOR": "Coreia do Sul",
    "SGP": "Singapura",    "NZL": "Nova Zelândia", "SWE": "Suécia",
    "NOR": "Noruega",      "CHE": "Suíça",         "NLD": "Holanda",
    "URY": "Uruguai",      "PER": "Peru",          "VEN": "Venezuela",
    "ECU": "Equador",      "BOL": "Bolívia",       "PRY": "Paraguai",
    "GTM": "Guatemala",    "CRI": "Costa Rica",    "PAN": "Panamá",
    "CUB": "Cuba",
}

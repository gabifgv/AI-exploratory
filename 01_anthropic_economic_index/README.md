# Anthropic Economic Index — Análise Exploratória

## Sobre o dataset

O [Anthropic Economic Index](https://huggingface.co/datasets/Anthropic/EconomicIndex) mapeia como o Claude está sendo usado em ocupações e setores da economia real. Os dados são derivados de uma semana de uso do Claude.ai (Free + Pro), classificados pela taxonomia ocupacional O\*NET.

**Release utilizada:** `release_2025_09_15` — primeira com dados geográficos por país  
**Período dos dados:** 04–11 agosto 2025

---

## Arquivos baixados automaticamente

| Arquivo | Caminho no repo HF | Tamanho |
|---------|--------------------|---------|
| AEI enriquecido (principal) | `release_2025_09_15/data/output/aei_enriched_claude_ai_*.csv` | ~25 MB |
| População por país | `release_2025_09_15/data/input/working_age_pop_2024_country_raw.csv` | ~23 KB |
| Estrutura SOC | `release_2025_09_15/data/input/soc_structure_raw.csv` | ~75 KB |
| Exposição por ocupação | `labor_market_impacts/job_exposure.csv` | ~37 KB |
| Penetração por tarefa | `labor_market_impacts/task_penetration.csv` | ~1.8 MB |

> Os arquivos são baixados via `huggingface_hub` para `data/` (ignorada pelo git).

---

## Schema principal — formato long

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `geo_id` | str | ISO-3 do país (`BRA`, `USA`, …) ou código de estado dos EUA |
| `geography` | str | `country` \| `state_us` \| `global` |
| `facet` | str | Dimensão: `country`, `onet_task`, `collaboration`, `request` |
| `variable` | str | Métrica: `usage_per_capita_index`, `onet_task_pct`, `automation_pct`, `augmentation_pct`, … |
| `cluster_name` | str | Entidade dentro do facet (nome da tarefa O\*NET, padrão de colaboração, etc.) |
| `value` | float | Valor numérico |

---

## Notebooks

| Notebook | Objetivo |
|----------|---------|
| [01_brazil_analysis.ipynb](./notebooks/01_brazil_analysis.ipynb) | Análise exploratória completa: download, exploração, Brasil vs. comparáveis, visualizações |
| [02_presentation.ipynb](./notebooks/02_presentation.ipynb) | Apresentação narrativa — "Hype ou realidade?" — 6 slides com dados reais |

### Como rodar

```bash
pip install -r ../../requirements.txt
jupyter notebook
```

Execute primeiro `01_brazil_analysis.ipynb` para gerar os outputs, depois `02_presentation.ipynb` para a apresentação final.

---

## Países comparáveis usados na análise

`BRA` · `ARG` · `MEX` · `IND` · `ZAF` · `COL` · `CHL`

---

## Estrutura

```
01_anthropic_economic_index/
├── notebooks/
│   ├── 01_brazil_analysis.ipynb   ← análise exploratória
│   └── 02_presentation.ipynb      ← apresentação narrativa
├── data/                          ← arquivos baixados (gitignored)
│   └── .gitkeep
└── outputs/                       ← gráficos e tabelas exportados
    └── .gitkeep
```

## Referências

- Dataset: https://huggingface.co/datasets/Anthropic/EconomicIndex
- Paper: [arxiv:2503.04761](https://arxiv.org/abs/2503.04761)

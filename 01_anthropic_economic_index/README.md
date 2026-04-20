# Anthropic Economic Index — Análise Exploratória

## Sobre o dataset

O [Anthropic Economic Index](https://huggingface.co/datasets/Anthropic/EconomicIndex) é um dataset público que mapeia como o Claude está sendo utilizado em diferentes ocupações e setores da economia. Os dados são derivados de conversas reais (anonimizadas) e classificados por categoria de uso, nível de automação, e código ocupacional (SOC/ISCO).

## Objetivos deste estudo

- Entender a distribuição global de uso de IA por setor e ocupação
- Comparar o Brasil com países de perfil econômico similar (Argentina, México, Índia, África do Sul)
- Identificar quais ocupações brasileiras têm maior exposição à automação via IA
- Gerar visualizações para comunicação dos resultados

## Notebooks

| Notebook | Descrição |
|----------|-----------|
| [01_brazil_analysis.ipynb](./notebooks/01_brazil_analysis.ipynb) | Exploração inicial + análise Brasil vs. países comparáveis |

## Estrutura

```
01_anthropic_economic_index/
├── notebooks/
│   └── 01_brazil_analysis.ipynb
├── data/          # Dataset baixado via huggingface_hub (não versionado)
└── outputs/       # Gráficos e tabelas exportados
```

## Referências

- Dataset: https://huggingface.co/datasets/Anthropic/EconomicIndex
- Artigo original: Anthropic Economic Index (2025)

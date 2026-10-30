# 📚 Pipeline de Dados — Indicador de Alfabetização

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Storage%20%7C%20BigQuery-4285F4?logo=googlecloud&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Arquitetura](https://img.shields.io/badge/Arquitetura-Medallion-CD7F32)

Pipeline híbrida de dados (**batch + streaming**) que integra diferentes fontes relacionadas ao **indicador de alfabetização**, com foco em qualidade, escalabilidade e eficiência de custos em nuvem.

> Projeto desenvolvido na Fase 2 da pós-graduação em Data Science e IA (FIAP).

## 🏗️ Arquitetura

O projeto segue a **arquitetura Medallion**. Este repositório contém a **camada Silver**: tratamento, validação de qualidade e cálculo dos indicadores.

```mermaid
flowchart LR
    subgraph Fontes
        A[Alunos - batch]
        B[Alunos - streaming]
        C[Municípios / UFs]
        D[Metas de alfabetização]
    end

    subgraph Bronze[Bronze - GCS]
        BR[(Parquet bruto)]
    end

    subgraph Silver[Silver - GCS]
        T[transform.py<br/>unifica, deduplica, padroniza]
        Q[quality.py<br/>relatório de qualidade]
        M[metas.py<br/>wide → long]
        I[indicator.py<br/>indicador Brasil / UF / município]
    end

    A --> BR
    B --> BR
    C --> BR
    D --> BR
    BR --> T
    T --> Q
    T --> M
    T --> I
```

## ⚙️ O que cada etapa faz

| Etapa | Script | Responsabilidade |
|---|---|---|
| Transformação | `silver/transform.py` | Une batch + streaming, remove duplicidades por aluno/ano, padroniza tipos, cria a flag de registro válido e recalcula a alfabetização pelo corte de proficiência |
| Qualidade | `silver/quality.py` | Gera relatório com duplicados, nulos, registros válidos, peso nulo, municípios inválidos e divergências no corte |
| Metas | `silver/metas.py` | Converte as tabelas de metas de formato *wide* para *long* e padroniza tipos |
| Indicadores | `silver/indicator.py` | Calcula o percentual de alunos alfabetizados (ponderado pelo peso amostral) por Brasil, UF e município |

### Regras de negócio

- **Registro válido:** aluno presente na avaliação **e** com caderno preenchido.
- **Alfabetizado:** proficiência **≥ 743** pontos.
- **Indicador:** soma dos pesos dos alunos alfabetizados ÷ soma total dos pesos × 100.

## 📁 Estrutura

```
.
├── config.py           # Variáveis de ambiente (projeto, buckets, datasets)
├── utils.py            # Leitura e escrita de Parquet no Cloud Storage
├── silver/
│   ├── transform.py    # Tratamento Bronze → Silver
│   ├── quality.py      # Relatório de qualidade
│   ├── metas.py        # Tratamento das metas
│   └── indicator.py    # Cálculo dos indicadores
├── requirements.txt
└── .env.example
```

## 🚀 Como executar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
cp .env.example .env   # e preencha com os dados do seu projeto GCP

# 3. Autenticar no Google Cloud
gcloud auth application-default login

# 4. Rodar as etapas, a partir da raiz do projeto
python -m silver.transform
python -m silver.quality
python -m silver.metas
python -m silver.indicator
```

## 🛠️ Tecnologias

Python · Pandas · PyArrow · Google Cloud Storage · BigQuery

## 👤 Autor

**Matheus Cadoni** · [LinkedIn](https://www.linkedin.com/in/matheus-cadoni-aab94a208) · [GitHub](https://github.com/Matheus074)

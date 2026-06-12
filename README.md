# Como executar

Garanta que todos os datasets necessários estejam no mesmo diretório dos notebooks e execute-os na ordem em que foram numerados.

## Datasets necessários

Os arquivos podem ser obtidos a partir dos links disponibilizados no README da branch `master`.

---

### 1. `votacao_candidato.csv`

**Colunas obrigatórias:**

```text
Ano de eleição;
Cargo;
Código município;
Cor/raça;
Estado civil;
Faixa etária;
Gênero;
Grau de instrução;
Município;
Nome candidato;
Número candidato;
Ocupação;
Partido;
Região;
Situação totalização;
Turno;
UF;
Zona;
Votos válidos;
Votos nominais;
Data de carga
```

---

### 2. `dados_municipios_panorama.csv`

**Colunas obrigatórias:**

```text
municipio,
municipio_id,
População no último censo,
População estimada,
População quilombola,
População indígena,
Densidade demográfica,
Nome masculino mais popular,
Nome feminino mais popular,
Sobrenome mais popular,
Salário médio mensal dos trabalhadores formais,
Pessoal ocupado em postos de trabalho formais,
Percentual da população com rendimento nominal mensal per capita de até 1/2 salário mínimo,
Taxa de escolarização de 6 a 14 anos de idade,
IDEB – Anos iniciais do ensino fundamental (Rede pública),
IDEB – Anos finais do ensino fundamental (Rede pública),
Matrículas no ensino fundamental,
Matrículas no ensino médio,
Docentes no ensino fundamental,
Docentes no ensino médio,
Número de estabelecimentos de ensino fundamental,
Número de estabelecimentos de ensino médio,
PIB per capita,
Índice de Desenvolvimento Humano Municipal (IDHM),
Total de receitas brutas realizadas,
Transferências correntes (Percentual em relação às receitas correntes brutas realizadas),
Total de despesas brutas empenhadas,
Mortalidade Infantil,
Internações por diarreia pelo SUS,
Estabelecimentos de Saúde SUS,
Área urbanizada,
Esgotamento sanitário por rede geral, rede pluvial ou fossa ligada à rede,
Arborização de vias públicas,
Urbanização de vias públicas,
População exposta ao risco,
Bioma predominante,
Sistema Costeiro-Marinho,
Área da unidade territorial,
Hierarquia urbana,
Região de Influência,
Região intermediária,
Região imediata,
Mesorregião,
Microrregião
```

---

### 3. `municipio_tse_ibge.csv`

**Colunas obrigatórias:**

```text
DT_GERACAO;
HH_GERACAO;
CD_UF_TSE;
CD_UF_IBGE;
SG_UF;
NM_UF;
CD_MUNICIPIO_TSE;
NM_MUNICIPIO_TSE;
CD_MUNICIPIO_IBGE;
NM_MUNICIPIO_IBGE
```

---

## Execução

Após disponibilizar os três arquivos no diretório do projeto, execute os notebooks sequencialmente:

1. `1preprocess.ipynb)`
2. `2candidate_profile.ipynb)`
3. `3candidate_PCA_SDing.ipynb)`

Cada notebook utiliza os arquivos gerados na etapa anterior, portanto a ordem de execução deve ser preservada.

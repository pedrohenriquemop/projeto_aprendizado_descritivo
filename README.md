# Projeto - Aprendizado Descritivo

Este repositório contém o projeto prático desenvolvido para a disciplina de Aprendizado Descritivo..

## Objetivo

O intuito do trabalho foi investigar a influência de indicadores municipais (como IDH, PIB e demografia) sobre fenômenos políticos nacionais através da tarefa de **Mineração de Subgrupos** (_Subgroup Discovery_). A abordagem metodológica baseou-se na exploração autônoma e descentralizada dos dados por cada membro da equipe.

## Fontes de Dados

As análises foram construídas a partir da integração de bases públicas disponibilizadas por órgãos oficiais brasileiros:

Resultados das Eleições (TSE)
Painéis de resultados eleitorais: https://sig.tse.jus.br/ords/dwapr/r/seai/sig-eleicao-resultados/pain%C3%A9is-de-resultados?session=13490862763763

Indicadores Municipais (IBGE)
Panorama dos Municípios Brasileiros: https://cidades.ibge.gov.br/brasil/mg/uba/panorama

Emendas Parlamentares (Portal da Transparência)
Consulta de emendas parlamentares federais: https://portaldatransparencia.gov.br/emendas/consulta?ordenarPor=autor&direcao=asc

Tabela de Correspondência de Municípios (TSE/IBGE)
Códigos oficiais de UF e municípios: https://dadosabertos.tse.jus.br/dataset/codigos-oficiais-de-uf-e-municipios-segundo-o-tse-e-o-ibge

## Estrutura do Repositório

Para manter a independência das análises, os scripts e as bases de dados específicas de cada membro estão estruturados em **branches diferentes**:

- `master`: Contém este README e as bases de dados.
- `vitor`: Análise voltada para o recebimento de emendas parlamentares federais e resultados eleitorais para o cargo de Senador.
- `pedro`: Análise focada na assinatura socioeconômica e demográfica por trás da vitória no pleito Presidencial (2º Turno).
- `joao`: Modelagem avançada com agregação em nível de candidato, redução de dimensionalidade via PCA e mineração do perfil geral dos candidatos eleitos.
- `lucas`: Análise conjunta com dados da pandemia de COVID-19 para trajetória das eleições presidenciais de 2018 e 2022.

## Como Executar

Cada branch possui seu próprio script executável (via CLI ou Notebook). Para replicar os experimentos, alterne para a branch desejada e siga as instruções contidas no arquivo de código correspondente.

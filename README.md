# Projeto - Aprendizado Descritivo

Este repositório contém o projeto prático desenvolvido para a disciplina de Aprendizado Descritivo..

## Objetivo

O intuito do trabalho foi investigar a influência de indicadores municipais (como IDH, PIB e demografia) sobre fenômenos políticos nacionais através da tarefa de **Mineração de Subgrupos** (_Subgroup Discovery_). A abordagem metodológica baseou-se na exploração autônoma e descentralizada dos dados por cada membro da equipe.

## Estrutura do Repositório

Para manter a independência das análises, os scripts e as bases de dados específicas de cada membro estão estruturados em **branches diferentes**:

- `master`: Contém este README e as bases de dados.
- `vitor`: Análise voltada para o recebimento de emendas parlamentares federais e resultados eleitorais para o cargo de Senador.
- `pedro`: Análise focada na assinatura socioeconômica e demográfica por trás da vitória no pleito Presidencial (2º Turno).
- `joao`: Modelagem avançada com agregação em nível de candidato, redução de dimensionalidade via PCA e mineração do perfil geral dos candidatos eleitos.

## Como Executar

Cada branch possui seu próprio script executável (via CLI ou Notebook). Para replicar os experimentos, alterne para a branch desejada e siga as instruções contidas no arquivo de código correspondente.

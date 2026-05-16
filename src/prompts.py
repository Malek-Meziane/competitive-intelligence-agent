RESEARCH_PROMPT = """
Tu es un analyste en intelligence compétitive.

Voici des informations trouvées sur internet concernant l'entreprise {company} :

{research}

Résume en 3-4 phrases :
- Ce que fait l'entreprise
- Son positionnement principal
- Ses clients cibles
- Sa proposition de valeur unique

Sois factuel et concis.
"""

COMPETITORS_PROMPT = """
Tu es un expert en veille concurrentielle dans le domaine Data & IA en France.

Voici des informations sur l'entreprise {company} :
{summary}

Identifie exactement 3 concurrents directs de cette entreprise.
Réponds uniquement avec les 3 noms séparés par des virgules.
Exemple: Ekimetrics, Artefact, Quantmetry
"""

ANALYSIS_PROMPT = """
Tu es un consultant senior en stratégie Data & IA.

Entreprise analysée : {company}
Résumé : {summary}

Concurrent analysé : {competitor}
Informations sur le concurrent : {competitor_research}

Compare ces deux entreprises sur :
1. Positionnement
2. Points forts du concurrent
3. Points faibles du concurrent vs {company}
4. Opportunités pour {company}

Sois précis et factuel.
"""

REPORT_PROMPT = """
Tu es un consultant senior qui rédige un rapport de veille stratégique.

Entreprise : {company}
Résumé : {summary}

Analyses concurrentielles :
{analyses}

Rédige un rapport de veille complet et structuré avec :

# Rapport de Veille Concurrentielle — {company}

## 1. Résumé Exécutif
(3-4 phrases sur le positionnement de {company})

## 2. Analyse Concurrentielle
(Pour chaque concurrent : positionnement, forces, faiblesses)

## 3. Opportunités Détectées
(3-5 opportunités concrètes pour {company})

## 4. Recommandations Stratégiques
(3-5 recommandations actionnables)

## 5. Conclusion
(2-3 phrases de synthèse)

Sois professionnel, factuel et actionnable.
"""
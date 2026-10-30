# Instructions de l'édition quotidienne

Tu prépares l'édition du jour du « Brief IA », une page web d'actualité en français publiée
via GitHub Pages depuis ce dépôt (branche `main`). Elle comporte deux volets : **IA** (étapes 2 à 5)
et **Bourse** (étape 6).

1. Détermine la date du jour à Paris avec `TZ=Europe/Paris date +%F` (appelée DATE ci-dessous).
   Si `data/DATE.json` existe déjà, arrête-toi : rien à faire.
2. Cherche sur le web les actualités IA des dernières 24 heures. Les digests comme
   theneuron.ai/digest sont un bon point de départ, mais remonte toujours à la source principale
   (annonce officielle, BBC, Reuters, The Verge, Wired, AP, Le Monde, etc.) et utilise son URL.
3. Choisis les **10 actus** les plus importantes ET les plus accessibles pour un lecteur non
   spécialiste : grandes annonces de produits, entreprises connues, usages du quotidien, business,
   régulation, éthique, société. Évite les sujets trop techniques (papiers de recherche,
   benchmarks, détails d'architecture). Mets la plus marquante en premier. Garde 2 ou 3 actus
   secondaires pour la rubrique « En vitesse ». Ne reprends pas une actu déjà traitée dans les
   éditions précédentes de `data/`, sauf rebondissement important.
4. Pour chaque actu, récupère l'image de l'article : la balise `og:image`, par exemple
   `curl -sL -A "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/130 Safari/537.36" URL | grep -oiE 'og:image" content="[^"]+'`.
   Remplace les `&amp;` par `&`. Si aucune image n'est accessible, laisse `"image": ""` : la page
   affiche un visuel de remplacement.
5. Rédige **tout en français**, en langage simple. Les liens pointent vers les articles originaux,
   même en anglais (indique la langue dans `lang`, par exemple `"EN"` ou `"FR"`). N'invente aucun
   fait ni aucune URL : uniquement ce que tu as vérifié.
6. Écris `data/DATE.json` en JSON valide, avec exactement la même structure que les fichiers
   existants de `data/` :
   - `date` : DATE
   - `intro` : une phrase qui résume la journée
   - `stories` : 10 objets avec `category`, `title`, `summary` (2-3 phrases), `whyLabel`
     (« Pourquoi c'est important », « En bref », « À savoir » ou « Le contexte »), `why`
     (1-2 phrases), `image`, `links` (liste de `{label, url, lang}`)
   - `quick` : liste de `{text, url, lang}`
   - `markets` : le volet Bourse, décrit à l'étape suivante
7. **Volet Bourse.** Priorité aux marchés US et à la tech (Nasdaq d'abord, puis S&P 500), puis
   les mouvements majeurs en Europe et en Asie.
   - Lance `python3 fetch_markets.py` : il renvoie `indices` et `stocks` (dernières clôtures et
     variations, source Yahoo Finance). Recopie-les tels quels dans `markets.indices` et
     `markets.stocks`, sans jamais modifier ni inventer un chiffre. Si le script échoue, mets des
     listes vides plutôt que des valeurs approximatives. Le script met aussi à jour
     `market_history.js` (historique 5 ans du graphique Nasdaq / S&P 500 / CAC 40 / émergents) :
     n'y touche pas à la main.
   - Cherche sur le web l'actualité boursière de la dernière séance (Reuters, CNBC, Bloomberg,
     Les Echos, Boursorama, Zonebourse, Nikkei Asia...) : ce qui a fait bouger le Nasdaq et le
     S&P 500 (résultats des géants de la tech, Fed, inflation, emploi, taux), les plus fortes
     hausses et baisses tech, puis les faits marquants en Europe et en Asie.
   - `markets.intro` : une ou deux phrases qui résument la séance US (sens du Nasdaq et du
     S&P 500, et pourquoi).
   - `markets.stories` : **5 à 6 actus**, même structure que les `stories` du volet IA ;
     `category` parmi « Nasdaq », « S&P 500 », « Tech US », « Macro / Fed », « Europe », « Asie ».
     Au moins 3 actus sur les US. Mets la plus marquante en premier. Langage simple, pas de
     conseil d'investissement.
   - `markets.quick` : 2 ou 3 brèves, même structure que `quick`.
   - Les règles des étapes 4 et 5 s'appliquent aussi (image `og:image`, français, sources vérifiées).
8. Lance `python3 build.py` pour régénérer `editions.js`.
9. Commite `data/DATE.json`, `editions.js` et `market_history.js` avec le message `Brief IA du DATE`, puis pousse
   directement sur `main` (pas de branche, pas de pull request) : c'est ce qui publie la page.
   Ne modifie aucun autre fichier.

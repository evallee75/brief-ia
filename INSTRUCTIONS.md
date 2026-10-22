# Instructions de l'édition quotidienne

Tu prépares l'édition du jour du « Brief IA », une page web d'actualité IA en français publiée
via GitHub Pages depuis ce dépôt (branche `main`).

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
7. Lance `python3 build.py` pour régénérer `editions.js`.
8. Commite `data/DATE.json` et `editions.js` avec le message `Brief IA du DATE`, puis pousse
   directement sur `main` (pas de branche, pas de pull request) : c'est ce qui publie la page.
   Ne modifie aucun autre fichier.

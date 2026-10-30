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
     `market_history.js` (historique 5 ans des graphiques de chaque zone) :
     n'y touche pas à la main.
   - Cherche sur le web l'actualité boursière de la dernière séance (Reuters, CNBC, Bloomberg,
     Les Echos, Boursorama, Zonebourse, Nikkei Asia...) : ce qui a fait bouger le Nasdaq et le
     S&P 500 (résultats des géants de la tech, Fed, inflation, emploi, taux), les plus fortes
     hausses et baisses tech, puis les faits marquants en Europe et en Asie.
   - `markets.intro` : une ou deux phrases qui résument la séance US (sens du Nasdaq et du
     S&P 500, et pourquoi).
   - `markets.stories` : **6 à 8 actus**, même structure que les `stories` du volet IA, plus un
     champ `region` : « Amérique », « Europe » ou « Asie » (la page les range dans le sous-onglet
     correspondant). Au moins 3 actus Amérique, 1 à 2 Europe, 1 à 2 Asie. `category` parmi
     « Nasdaq », « S&P 500 », « Tech US », « Macro / Fed », « Europe », « Asie », « Émergents ».
     Dans chaque zone, mets la plus marquante en premier. Langage simple, pas de conseil
     d'investissement.
   - `markets.quick` : 2 ou 3 brèves, même structure que `quick` (affichées dans l'onglet Monde).
   - Les règles des étapes 4 et 5 s'appliquent aussi (image `og:image`, français, sources vérifiées).
8. Lance `python3 build.py` pour régénérer `editions.js`.
9. Commite `data/DATE.json`, `editions.js` et `market_history.js` avec le message `Brief IA du DATE`, puis pousse
   directement sur `main` (pas de branche, pas de pull request) : c'est ce qui publie la page.
   Ne modifie aucun autre fichier.

## Mise à jour du soir (vers 18 h, heure de Paris)

Cette section est suivie par une deuxième exécution quotidienne. Elle complète l'édition du jour
au lieu d'en créer une nouvelle (ne pas appliquer l'étape 1 ci-dessus).

1. Détermine DATE comme à l'étape 1. Si `data/DATE.json` n'existe pas, prépare d'abord l'édition
   complète (étapes 2 à 9), puis arrête-toi.
2. Si `intro` contient déjà « Mise à jour du soir », arrête-toi : rien à faire.
3. **IA** : cherche les actus IA parues depuis l'édition du matin. Ajoute **3 à 5 actus** nouvelles,
   jamais déjà traitées dans `data/` (vérifie les titres et les URLs). Insère-les après les 3
   premières actus existantes. Ajoute 1 ou 2 brèves à la fin de `quick`. Complète `intro` avec une
   phrase qui commence par « Mise à jour du soir : ». Mêmes règles qu'aux étapes 2 à 5.
4. **Bourse** : lance `python3 fetch_markets.py` et remplace `markets.indices` et `markets.stocks`
   par sa sortie, telle quelle (l'Europe a clôturé ; Wall Street est encore en séance, ses chiffres
   restent ceux de la veille, c'est normal).
   - Cherche l'actualité de la séance du jour : clôture européenne, Wall Street en séance,
     faits marquants en Asie.
   - Ajoute **4 à 6 actus** en tête de `markets.stories` (même structure, champ `region`), titres
     préfixés du jour de la semaine (« Vendredi : ... »). Au moins 2 Amérique, 1 Europe, 1 Asie
     si l'actualité le permet.
   - Réécris `markets.intro` : la séance du jour d'abord, en précisant que les chiffres de Wall
     Street sont en séance (« vers 18 h, le Nasdaq perdait... »), puis une demi-phrase sur la veille.
   - Ajoute 1 ou 2 brèves en tête de `markets.quick`.
   - Aucun chiffre inventé : uniquement ce que disent les sources.
5. Lance `python3 build.py`, puis commite `data/DATE.json`, `editions.js` et `market_history.js`
   avec le message `Brief IA du DATE : mise à jour du soir` et pousse directement sur `main`.
   Ne modifie aucun autre fichier.

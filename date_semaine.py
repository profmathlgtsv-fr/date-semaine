from datetime import date
from PIL import Image, ImageDraw, ImageFont
import os

# ====================================================
# PARAMÈTRES
# ====================================================

# Définition des chemins d'accès aux ressources
DOSSIER_ASSETS = "assets"
FICHIER_FOND = os.path.join(DOSSIER_ASSETS, "background.png") # Image sans le texte dynamique
FICHIER_POLICE_SERIF = os.path.join(DOSSIER_ASSETS, "times.ttf") # Pour le parchemin
FICHIER_POLICE_SANS = os.path.join(DOSSIER_ASSETS, "DejaVuSans-Bold.ttf")   # Pour la semaine

FICHIER_SORTIE = "date_semaine.png"

# Paramètres de style
COULEUR_DATE = (80, 0, 0)       # Rouge foncé/bordeaux pour le parchemin
COULEUR_SEMAINE_A = (0, 80, 160) # Bleu pour "SEMAINE A"
COULEUR_SEMAINE_B = (0, 100, 50) # Vert pour "SEMAINE B" (adapté de l'illustration)

# Paramètres de police
TAILLE_POLICE_DATE = 60
TAILLE_POLICE_SEMAINE = 80
TAILLE_POLICE_SANS = 80

# Coordonnées (à ajuster selon ton image de fond assets/atrium_background.png)
# Ces valeurs sont des estimations.
POS_Y_DATE = 280      # Position Y sur le parchemin
POS_Y_SEMAINE = 590   # Position Y dans la zone blanche

# Semaine de référence
REFERENCE = date(2026, 8, 31)  # semaine A

# ====================================================
# CALCUL SEMAINE A/B (ton code d'origine)
# ====================================================

aujourdhui = date.today()

nb_semaines = (aujourdhui - REFERENCE).days // 7

semaine = "A" if nb_semaines % 2 == 0 else "B"

# ====================================================
# DATE EN FRANÇAIS
# ====================================================

jours = [
    "lundi",
    "mardi",
    "mercredi",
    "jeudi",
    "vendredi",
    "samedi",
    "dimanche"
]

mois = [
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre"
]

texte_date = (
    f"{jours[aujourdhui.weekday()].capitalize()} "
    f"{aujourdhui.day} "
    f"{mois[aujourdhui.month - 1]} "
    f"{aujourdhui.year}"
)

# Remplacement des "..." par la date du jour
texte_parchemin = f"Nous sommes le \n{texte_date}"
# Pour n'afficher que la semaine active
texte_semaine = f"SEMAINE {semaine}"

# ====================================================
# MODÈLE DE SORTIE EN IMAGE (Modification principale)
# ====================================================

# 1. Charger l'image de fond illustrative
try:
    img = Image.open(FICHIER_FOND).convert("RGB")
    LARGEUR, HAUTEUR = img.size
except FileNotFoundError:
    print(f"Erreur : Impossible de trouver l'image de fond '{FICHIER_FOND}'.")
    exit()

draw = ImageDraw.Draw(img)

# 2. Charger les polices de caractères
try:
    # Police serif pour le parchemin (style 'NOUS SOMMES LE')
    police_date = ImageFont.truetype(
        FICHIER_POLICE_SERIF, TAILLE_POLICE_DATE
    )
    # Police sans-serif pour la semaine active (style 'SEMAINE A')
    police_semaine = ImageFont.truetype(
        FICHIER_POLICE_SANS, TAILLE_POLICE_SANS
    )
except OSError:
    print(f"Erreur : Impossible de charger les polices depuis '{DOSSIER_ASSETS}'. Utilisation des polices par défaut.")
    police_date = ImageFont.load_default()
    police_semaine = ImageFont.load_default()

# ====================================================
# CENTRAGE ET DESSIN DU TEXTE
# ====================================================

# Dessiner la date sur le parchemin
bbox_date = draw.textbbox((0, 0), texte_parchemin, font=police_date)
largeur_date = bbox_date[2] - bbox_date[0]
x_date = (LARGEUR - largeur_date) // 2
draw.text(
    (x_date, POS_Y_DATE),
    texte_parchemin,
    fill=COULEUR_DATE,
    font=police_date,
    align="center" # Centrer le texte multiligne
)

# Dessiner la semaine active
# Sélectionner la couleur de la semaine active
couleur_semaine = COULEUR_SEMAINE_A if semaine == "A" else COULEUR_SEMAINE_B

bbox_semaine = draw.textbbox((0, 0), texte_semaine, font=police_semaine)
largeur_semaine = bbox_semaine[2] - bbox_semaine[0]
x_semaine = (LARGEUR - largeur_semaine) // 2

draw.text(
    (x_semaine, POS_Y_SEMAINE),
    texte_semaine,
    fill=couleur_semaine,
    font=police_semaine
)

# ====================================================
# SAUVEGARDE
# ====================================================

img.save(FICHIER_SORTIE)

print(f"Image illustrative générée : {FICHIER_SORTIE}")

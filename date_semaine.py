from datetime import date
from PIL import Image, ImageDraw, ImageFont

# ====================================================
# PARAMETRES
# ====================================================

LARGEUR = 1200
HAUTEUR = 180

COULEUR_FOND = (255, 255, 255)

COULEUR_DATE = (220, 0, 0)
COULEUR_A = (0, 140, 0)
COULEUR_B = (0, 80, 220)

FICHIER_SORTIE = "date_semaine.png"

# Semaine de référence
REFERENCE = date(2026, 8, 31)  # semaine A

# ====================================================
# CALCUL SEMAINE A/B
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
    f"Aujourd'hui, nous sommes le "
    f"{jours[aujourdhui.weekday()]} "
    f"{aujourdhui.day} "
    f"{mois[aujourdhui.month - 1]} "
    f"{aujourdhui.year}"
)

texte_semaine = f"SEMAINE {semaine}"

# ====================================================
# CREATION IMAGE
# ====================================================

img = Image.new("RGB", (LARGEUR, HAUTEUR), COULEUR_FOND)
draw = ImageDraw.Draw(img)

# ====================================================
# POLICES
# ====================================================

try:
    police_date = ImageFont.truetype(
        "DejaVuSans-Bold.ttf", 34
    )
    police_semaine = ImageFont.truetype(
        "DejaVuSans-Bold.ttf", 52
    )
except:
    police_date = ImageFont.load_default()
    police_semaine = ImageFont.load_default()

# ====================================================
# CENTRAGE
# ====================================================

bbox1 = draw.textbbox((0, 0), texte_date, font=police_date)
largeur1 = bbox1[2] - bbox1[0]

bbox2 = draw.textbbox((0, 0), texte_semaine, font=police_semaine)
largeur2 = bbox2[2] - bbox2[0]

x1 = (LARGEUR - largeur1) // 2
x2 = (LARGEUR - largeur2) // 2

# ====================================================
# DESSIN
# ====================================================

draw.text(
    (x1, 35),
    texte_date,
    fill=COULEUR_DATE,
    font=police_date
)

couleur_semaine = COULEUR_A if semaine == "A" else COULEUR_B

draw.text(
    (x2, 95),
    texte_semaine,
    fill=couleur_semaine,
    font=police_semaine
)

# ====================================================
# SAUVEGARDE
# ====================================================

img.save(FICHIER_SORTIE)

print(f"Image enregistrée : {FICHIER_SORTIE}")

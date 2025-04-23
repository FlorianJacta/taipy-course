import pandas as pd
import random

# Définir manuellement toutes les régions métropolitaines françaises avec leurs départements et villes principales
regions_departements_villes = {
    "Auvergne-Rhône-Alpes": [
        ("Ain", "Bourg-en-Bresse"),
        ("Allier", "Moulins"),
        ("Ardèche", "Privas"),
        ("Cantal", "Aurillac"),
        ("Drôme", "Valence"),
        ("Isère", "Grenoble"),
        ("Loire", "Saint-Étienne"),
        ("Haute-Loire", "Le Puy-en-Velay"),
        ("Puy-de-Dôme", "Clermont-Ferrand"),
        ("Rhône", "Lyon"),
        ("Savoie", "Chambéry"),
        ("Haute-Savoie", "Annecy"),
    ],
    "Bourgogne-Franche-Comté": [
        ("Côte-d'Or", "Dijon"),
        ("Doubs", "Besançon"),
        ("Jura", "Lons-le-Saunier"),
        ("Nièvre", "Nevers"),
        ("Haute-Saône", "Vesoul"),
        ("Saône-et-Loire", "Mâcon"),
        ("Yonne", "Auxerre"),
        ("Territoire de Belfort", "Belfort"),
    ],
    "Bretagne": [
        ("Côtes-d'Armor", "Saint-Brieuc"),
        ("Finistère", "Quimper"),
        ("Ille-et-Vilaine", "Rennes"),
        ("Morbihan", "Vannes"),
    ],
    "Centre-Val de Loire": [
        ("Cher", "Bourges"),
        ("Eure-et-Loir", "Chartres"),
        ("Indre", "Châteauroux"),
        ("Indre-et-Loire", "Tours"),
        ("Loir-et-Cher", "Blois"),
        ("Loiret", "Orléans"),
    ],
    "Corse": [("Corse-du-Sud", "Ajaccio"), ("Haute-Corse", "Bastia")],
    "Grand Est": [
        ("Ardennes", "Charleville-Mézières"),
        ("Aube", "Troyes"),
        ("Marne", "Châlons-en-Champagne"),
        ("Haute-Marne", "Chaumont"),
        ("Meurthe-et-Moselle", "Nancy"),
        ("Meuse", "Bar-le-Duc"),
        ("Moselle", "Metz"),
        ("Bas-Rhin", "Strasbourg"),
        ("Haut-Rhin", "Colmar"),
        ("Vosges", "Épinal"),
    ],
    "Hauts-de-France": [
        ("Aisne", "Laon"),
        ("Nord", "Lille"),
        ("Oise", "Beauvais"),
        ("Pas-de-Calais", "Arras"),
        ("Somme", "Amiens"),
    ],
    "Île-de-France": [
        ("Paris", "Paris"),
        ("Seine-et-Marne", "Melun"),
        ("Yvelines", "Versailles"),
        ("Essonne", "Évry"),
        ("Hauts-de-Seine", "Nanterre"),
        ("Seine-Saint-Denis", "Bobigny"),
        ("Val-de-Marne", "Créteil"),
        ("Val-d'Oise", "Cergy"),
    ],
    "Normandie": [
        ("Calvados", "Caen"),
        ("Eure", "Évreux"),
        ("Manche", "Saint-Lô"),
        ("Orne", "Alençon"),
        ("Seine-Maritime", "Rouen"),
    ],
    "Nouvelle-Aquitaine": [
        ("Charente", "Angoulême"),
        ("Charente-Maritime", "La Rochelle"),
        ("Corrèze", "Tulle"),
        ("Creuse", "Guéret"),
        ("Dordogne", "Périgueux"),
        ("Gironde", "Bordeaux"),
        ("Landes", "Mont-de-Marsan"),
        ("Lot-et-Garonne", "Agen"),
        ("Pyrénées-Atlantiques", "Pau"),
        ("Deux-Sèvres", "Niort"),
        ("Vienne", "Poitiers"),
        ("Haute-Vienne", "Limoges"),
    ],
    "Occitanie": [
        ("Ariège", "Foix"),
        ("Aude", "Carcassonne"),
        ("Aveyron", "Rodez"),
        ("Gard", "Nîmes"),
        ("Haute-Garonne", "Toulouse"),
        ("Gers", "Auch"),
        ("Hérault", "Montpellier"),
        ("Lot", "Cahors"),
        ("Lozère", "Mende"),
        ("Hautes-Pyrénées", "Tarbes"),
        ("Pyrénées-Orientales", "Perpignan"),
        ("Tarn", "Albi"),
        ("Tarn-et-Garonne", "Montauban"),
    ],
    "Pays de la Loire": [
        ("Loire-Atlantique", "Nantes"),
        ("Maine-et-Loire", "Angers"),
        ("Mayenne", "Laval"),
        ("Sarthe", "Le Mans"),
        ("Vendée", "La Roche-sur-Yon"),
    ],
    "Provence-Alpes-Côte d'Azur": [
        ("Alpes-de-Haute-Provence", "Digne-les-Bains"),
        ("Hautes-Alpes", "Gap"),
        ("Alpes-Maritimes", "Nice"),
        ("Bouches-du-Rhône", "Marseille"),
        ("Var", "Toulon"),
        ("Vaucluse", "Avignon"),
    ],
}

secteurs_metiers = {
    "Informatique": ["Ingénieur logiciel", "Analyste de données", "Ingénieur DevOps"],
    "Santé": ["Infirmier", "Médecin", "Technicien de laboratoire"],
    "Éducation": ["Enseignant", "Bibliothécaire", "Chercheur"],
    "Construction": ["Chef de chantier", "Électricien", "Architecte"],
    "Commerce de détail": [
        "Vendeur",
        "Responsable de magasin",
        "Coordinateur logistique",
    ],
    "Finance": ["Comptable", "Analyste financier", "Auditeur"],
}

annees = list(range(2025, 2036))

# Générer des données RH synthétiques
donnees = []
for region, liste_dept_villes in regions_departements_villes.items():
    for departement, ville in liste_dept_villes:
        for secteur, metiers in secteurs_metiers.items():
            for metier in metiers:
                for annee in annees:
                    donnees.append(
                        {
                            "Région": region,
                            "Département": departement,
                            "Ville": ville,
                            "Secteur": secteur,
                            "Métier": metier,
                            "Recrutement": random.randint(50, 500),
                            "Année": annee,
                        }
                    )

# Sauvegarder en CSV
df_rh = pd.DataFrame(donnees)
chemin_csv = "data/hr_data.csv"
df_rh.to_csv(chemin_csv, index=False)
print(
    f"✅ Jeu de données RH complet avec toutes les régions et départements français enregistré dans : {chemin_csv}"
)

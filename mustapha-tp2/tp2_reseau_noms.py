"""
Module tp2_reseau_noms: Recherche dans un réseau d'amis à partir de noms
IFT-1004 Été 2020

Auteur: Mustapha Bouhsen
"""

import tp2_utils
import tp2_reseau_identifiants

def ouvrir_et_lire_fichier_noms():
    """
    Demande à l'utilisateur un nom de fichier contenant le répertoire de nom
    PRÉCONDITION: On considère que le fichier du réseau respecte le format écrit dans l'énoncé du TP.

    Returns:
        liste_noms (list): Une liste de noms (chaque nom est une chaîne de caractères).

    """
    # verifier si l'utilisateur a renter le bon noms du fichier
    while True:
        try:
            nom_fichier = input('Veuillez entrer le nom du fichier: ')
            descripteur_fichier = open(nom_fichier, 'r')
        except FileNotFoundError:
            print("Le fichier n'existe pas. Recommencez!")
            continue
        break

    liste_noms = []   # liste qui va être remplie avec les noms

    # parcourir les noms dans le fichier et les insérer dans la liste
    while True:
        txt = descripteur_fichier.readline()
        if txt == "":
            break
        txt = txt.rstrip("\n")
        liste_noms.append(txt)
    # fermer le fichier en lecture
    descripteur_fichier.close()

    for nom in range(len(liste_noms)):
        liste_noms[nom] = liste_noms[nom].lower()

    return liste_noms

def nom_existe(nom_usager, liste_noms):
    """ fonction qui suggère la personne qui a le plus d'amis en commun avec l'utilisateur

        Args:
            nom_usager : chaine de caractère qui represente un nom
            liste_noms : liste qui contient les noms sur lesquels on compare nom_usager

        Returns:
            bool: True si le noms est dans la liste sinon False

    """
    nom_usager = nom_usager.lower()

    return nom_usager in liste_noms


def creer_dictionnaire_usagers(liste_noms):
    """ fonction crée un dictionnaire des noms d'utilisateur avec leur id comme clê

        Args:
            liste_noms : liste qui contient les noms des usagers

        Returns:
            un dictionnaire des nom et id des utilisateurs

    """

    id = 0    # initialiser la variable id a 0
    dictionnaire_usagers = {}   # initialiser le dictionnaire qui va contenir les cles et valeurs

    # remplir le dictionnaire avec les infos
    for noms in liste_noms:
        dictionnaire_usagers[noms] = id
        id = id + 1

    return dictionnaire_usagers


def recommander(nom_usager, reseau, matrice_similarite, liste_noms, dict_usagers):
    """ fonction qui suggère la personne qui a le plus d'amis en commun avec l'utilisateur

        Args:
            nom_usager: un caractere qui represente le nom de l'utilisateur
            reseau : liste obtenus a partir de la fonction ouvrir_et_lire_fichier_reseau,
            cette derniere retourne une liste des listes des utilisateurs avec leurs amis
            matrice_similarite : matrice des amis en commun
            liste_noms : liste qui contient tous les noms des utilisateurs
            dict_usagers : dictionnaire qui contient les noms des utilisateur et leur id

        Returns:
            srt: un caractere qui represente le noms a suggerer

    """

    # transformer les lettre en miniscul pour matcher avec la liste des utilisateur
    # extraire l'id du dictionnaire
    nom_usager = nom_usager.lower()
    id_usager = dict_usagers[nom_usager]

    # traitement comme avec les id's comme au module tp2_reseau_identifiants (meme logique)
    id = tp2_reseau_identifiants.recommander(id_usager, reseau, matrice_similarite)

    # le nom qui correspond a l'indexe obtenue
    nom = liste_noms[id]

    nom = nom[0].upper() + nom[1:]  # la premiere lettre en majuscule
    return nom

# Tests unitaires (les docstrings ne sont pas exigés pour les fonntions de tests unitaires)

def test_nom_existe():
    assert nom_existe("MoMo", ['momo', 'alex', 'sara']) == True
    assert nom_existe("MomO", ['momo', 'alex', 'sara']) == True
    assert nom_existe("momo", ['adele', 'alex', 'momo']) == True
    assert nom_existe("Momo", ['mom', 'alex', 'sara']) == False
    assert nom_existe("sara", ['momo', 'alex', 'sarah']) == False


def test_creer_dictionnaire_usagers():
    assert creer_dictionnaire_usagers(['abdel', 'momo']) == {'abdel' : 0, 'momo' : 1}
    assert creer_dictionnaire_usagers(['alex', 'abdel']) != {'abdel': 0, 'alex' : 1}
    assert creer_dictionnaire_usagers(['momo', 'abdel']) == {'momo': 0, 'abdel': 1}
    assert creer_dictionnaire_usagers(['abdel', 'momo', 'alex']) == {'abdel': 0, 'momo': 1, 'alex': 2}
    assert creer_dictionnaire_usagers(['abdel', 'alex', 'momo']) == {'abdel': 0, 'alex': 1, 'momo': 2}


if __name__ == "__main__":
    test_nom_existe()
    test_creer_dictionnaire_usagers()
    print('Test unitaires passés avec succès!')


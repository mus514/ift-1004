"""
Module tp2_reseau_identifiants: : Recherche dans un réseau d'amis à partir d'identifiants (nombre unique)
IFT-1004 Été 2020

Auteur: Mustapha Bouhsen
"""
import tp2_utils


def ouvrir_et_lire_fichier_reseau():
    """
    Demande à l'utilisateur un nom de fichier contenant un réseau d'amis et charge le réseau en mémoire.
    PRÉCONDITION: On considère que le fichier du réseau respecte le format écrit dans l'énoncé du TP

    Returns:
        reseau (list): le réseau extrait du fichier (une liste de listes d'index d'usgers).

    """

    descripteur_fichier = tp2_utils.ouvrir_fichier()

    # La première ligne du fichier contient le nombre total d'usagers
    nb_usagers = int(descripteur_fichier.readline())
    print("Le réseau contient {} usagers".format(nb_usagers))

    # Création d'un réseau vide (c-a-d une liste de listes vides)
    reseau = []
    for i in range(nb_usagers):
        reseau.append([])

    # Chaque ligne du fichier (sauf la première) contient un coupe "d'amis"
    for ligne in descripteur_fichier.readlines():
        couple_usagers = ligne.split(' ')
        id_usager_1 = int(couple_usagers[0])
        id_usager_2 = int(couple_usagers[1])
        reseau[id_usager_1].append(id_usager_2)
        reseau[id_usager_2].append(id_usager_1)

    # Fermeture du fichier
    descripteur_fichier.close()
    print("Lecture du fichier terminé.")

    return reseau


def trouver_nombre_elements_communs_entre_listes(liste1, liste2):
    """Calcule le nombre d'element en commun des deux liste entrees en argument

        Args:
            liste1 : la liste a comparer
            liste2 : la liste a comparer avec liste1

        Returns:
            int: Le nombre total d'elements en commun des deux liste

    """

    compteur = 0  # variable qui va sommer le nombre d'element en commun
    for element in liste1:
        if element in liste2:
            compteur = compteur + 1

    return compteur



def calculer_scores_similarite(reseau):
    """Calcule le nombre d'amis en commun avec chaque deux paire d'utilisateurs

        Args:
            reseau : obtenus a partir de la fonction ouvrir_et_lire_fichier_reseau,
            cette derniere retourne une liste des listes des utilisateurs avec leurs amis

        Returns:
            int: une liste des listes des amis en commun avec chaque paire


    """

    compteur1 = 0     # compteur1 sert comme index pour les listes
    compteur2 = 0     # compteur2 sert comme index pour les listes

    # cree la matrice des zeros
    matrice_similarite = tp2_utils.initialiser_matrice_carre(len(reseau))

    for liste1 in reseau:       # iterer sur les n listes de la matrice

        for liste2 in reseau:   # iterer sur les element chaques element de la liste
            # remplir la matrice des zeros
            matrice_similarite[compteur1][compteur2] = trouver_nombre_elements_communs_entre_listes(liste1, liste2)
            compteur2 = compteur2 + 1

        compteur2 = 0               # reinitialiser le compteur
        compteur1 = compteur1 + 1   # incrementer le conteur de +1

    return matrice_similarite



def recommander(id_usager, reseau, matrice_similarite):
    """ fonction qui suggere la personne qui a le plus d'amis en commun avec l'utilisateur

        Args:
            id_usager : un entier qui represente l'identifiant de l'utilisateur
            reseau : liste obtenus a partir de la fonction ouvrir_et_lire_fichier_reseau,
            cette derniere retourne une liste des listes des utilisateurs avec leurs amis
            matrice_similarite : matrice des amis en commun

        Returns:
            int: l'id de la personne a suggerer

    """

    # sortir de la liste indexee de la matrice similarite
    liste = matrice_similarite[id_usager]

    # donner a l'usager -1 pour qu'il ne soit pas selectionner
    liste[id_usager] = -1

    # verifier si la personne suggerer est deja ami avec l'usager et lui attribuer -1 pour qu'il ne soit
    # selectionner
    for ami in liste:
        if liste.index(ami) in reseau[id_usager]:
            liste[liste.index(ami)] = -1

    # La valeur maximal dans la liste des usagers qu'ils ne
    # sont pas deja ami avec l'utilisateur
    maximum = max(liste)

    # l'ami a suggerer
    resultat = liste.index(maximum)

    return resultat



# Tests unitaires (les docstrings ne sont pas exigés pour les fonntions de tests unitaires)

def test_trouver_nombre_elements_communs_entre_listes():
    assert trouver_nombre_elements_communs_entre_listes([1, 2, 4], [1, 2, 4]) == 3
    assert trouver_nombre_elements_communs_entre_listes(['a', 'b', 4], [1, 'a', 7]) == 1
    assert trouver_nombre_elements_communs_entre_listes([1, 2, 3], [4, 5, 6]) == 0
    assert trouver_nombre_elements_communs_entre_listes([1, 1, 1], [1, 1, 1]) == 3
    assert trouver_nombre_elements_communs_entre_listes([-1, 2.7, 4, 9], [-1, 2, 2.7]) == 2


def test_scores_similarite():
    assert calculer_scores_similarite([[1, 2], [0], [0]]) == [[2, 0, 0], [0, 1, 1], [0, 1, 1]]
    assert calculer_scores_similarite([[3, 4], [6, 2], [6, 9]]) == [[2, 0, 0], [0, 2, 1], [0, 1, 2]]
    assert calculer_scores_similarite([[7, 3], [9], [10]]) == [[2, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert calculer_scores_similarite([[], [], []]) == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert calculer_scores_similarite([[], [0], []]) == [[0, 0, 0], [0, 1, 0], [0, 0, 0]]


if __name__ == "__main__":
    test_trouver_nombre_elements_communs_entre_listes()
    test_scores_similarite()
    print('Test unitaires passés avec succès!')



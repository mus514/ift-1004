"""
Programme intéractif pour le TP2 (Partie 2)
IFT-1004 Été 2020

Auteur: Mustapha Bouhsen
"""

import tp2_reseau_identifiants
import tp2_reseau_noms


print('--- Chargement du réseau (identifiants) ---')
reseau = tp2_reseau_identifiants.ouvrir_et_lire_fichier_reseau()
nb_usagers = len(reseau)

print('--- Chargement des noms ---')
liste_noms = tp2_reseau_noms.ouvrir_et_lire_fichier_noms()

if nb_usagers != len(liste_noms):
    print("ERREUR: Le nombre d'usager est différents dans les deux fichiers.")
    fin_du_programme = True

else:
    matrice = tp2_reseau_identifiants.calculer_scores_similarite(reseau)
    dict_usagers = tp2_reseau_noms.creer_dictionnaire_usagers(liste_noms)
    fin_du_programme = False

while not fin_du_programme:

    nom_usager = input("Entrer le nom de l'usager pour lequel vous voulez une recommandation: " )
    nom_usager = nom_usager.strip() # Enlève les espaces superflus au début et à la fin de la chaîne de caractères

    # verifier si le nom entree existe dans la liste des noms
    nom_valide = tp2_reseau_noms.nom_existe(nom_usager, liste_noms)

    # si le noms n'existe pas dans la liste
    if not nom_valide:
        print("Erreur: l'usager {} n'existe pas".format(nom_usager))
        print("")

    # si le nom existe dans la liste
    elif nom_valide:
        nom_recommandation = tp2_reseau_noms.recommander(nom_usager, reseau, matrice, liste_noms, dict_usagers)
        print("Pour {}, nous recommandons l'ami(e) {}".format(nom_usager, nom_recommandation) )

        # demander à l'utilisateur s'il veut contunier ou quitter
        reponse = ['oui', 'non']
        print("")
        demande = input("Voulez-vous une autre recommandation (oui/non)? ").lower()

        # s'execute tant que la reponse est differente de oui ou non
        while demande not in reponse:
            print("Error: il faut repondre par oui ou non")
            demande = input("Voulez-vous une autre recommandation (oui/non)? ").lower()

        if demande == 'oui':
           continue
        else:
           break



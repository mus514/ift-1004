"""
Programme intéractif pour le TP2 (Partie 1)
IFT-1004 Été 2020

Auteur: Mustapha Bouhsen
"""

import tp2_reseau_identifiants

print('--- Chargement du réseau (identifiants) ---')
reseau = tp2_reseau_identifiants.ouvrir_et_lire_fichier_reseau()
nb_usagers = len(reseau)

matrice = tp2_reseau_identifiants.calculer_scores_similarite(reseau)

arret = False

while not arret :

    # verifier si l'entrée est un entier entre 0 et n-1
    while True:
        try:
            id_usager = int(input("Entrer l'id de l'usager pour lequel vous voulez une recommandation (entre 0 et {}):".format(nb_usagers-1)))
            if id_usager not in range(nb_usagers):
                print("Erreur : l'usager doit être un nombre entier entre 0 et 9 inclusivement")
                print("")
                continue
        except ValueError:
            print("")
            print("Erreur : l'usager doit être un nombre entier entre 0 et 9 inclusivement")
            continue

        break

    id_recommandation = tp2_reseau_identifiants.recommander(id_usager, reseau, matrice)
    print("Pour la personne {}, nous recommandons l'ami {}.".format(id_usager, id_recommandation) )

    # demander à l'utilisateur s'il veut recommencer ou quiter
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

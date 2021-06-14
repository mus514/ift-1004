# Auteur: Mustapha Bouhsen, 910201346
# Description: TP1, L'aire sous la courbe de la fonction x^3 + 1 sur l'interval [0, 1]


# On demande à l'utilisateur de renter le nombre de rectangles
nombre_rectangle = int(input("Enter un nombre positif inférieur ou égale à 10000 ou (0 pour terminer): "))

while nombre_rectangle != 0:
    # On répète la procédure tant que le nombre
    # entré est different de 0 sinon on quitte la boucle
    if nombre_rectangle < 0:          # tester si le nombre est négatif
        print("Erreur, entrer un nombre positif")
        print("")
        nombre_rectangle = int(input("Enter un nombre positif inférieur ou égale à 10000 ou (0 pour terminer): "))

    elif nombre_rectangle > 10000:    # tester si le nombre dépasse 10000
        print("Erreur, le nombre est trop grand, enter un nombre inférieur ou égale a 10000")
        print("")
        nombre_rectangle = int(input("Enter un nombre positif inférieur ou égale à 10000 ou (0 pour terminer): "))

    else:
        largeur = 1/nombre_rectangle
        aire_rectangle = 0   # variable qui sert à additionner les aires calculés

        for i in range(nombre_rectangle):
            # On calcule l'aire de chaque rectangle allant  de 0 jusqu'à
            # le nombre total des rectangles moins 1 et on les additionnent
            limite_gauche = i * largeur
            limite_droite = (i * largeur) + largeur
            hauteur_gauche = limite_gauche**3 + 1
            hauteur_droite = limite_droite**3 + 1
            hauteur = (hauteur_gauche + hauteur_droite)/2     # Calculer la moyenne des deux hauteur
            aire_rectangle = aire_rectangle + hauteur*largeur  # Addition des aires calculées
        # Afficher les résultats à l'écran
        print("La valeur de A calculée par le programme est: ", aire_rectangle)
        print("La valeur réel de A calculée analytiquement est: ", 1.25)
        print("")
        # On demande de nouveau d'enter le nombre de rectangles
        nombre_rectangle = int(input("Enter un nombre positif inférieur ou égale a 10000 ou (0 pour terminer): "))







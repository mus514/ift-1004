# Auteurs: Mustapha Bouhsen, Sofiane Dris

from damier import Damier
from position import Position


class Partie:
    """Gestionnaire de partie de dames.

    Attributes:
        damier (Damier): Le damier de la partie, contenant notamment les pièces.
        couleur_joueur_courant (str): Le joueur à qui c'est le tour de jouer.
        doit_prendre (bool): Un booléen représentant si le joueur actif doit absolument effectuer une prise
            de pièce. Sera utile pour valider les mouvements et pour gérer les prises multiples.
        position_source_selectionnee (Position): La position source qui a été sélectionnée. Utile pour sauvegarder
            cette information avant de poursuivre. Contient None si aucune pièce n'est sélectionnée.
        position_source_forcee (Position): Une position avec laquelle le joueur actif doit absolument jouer. Le
            seul moment où cette position est utilisée est après une prise: si le joueur peut encore prendre
            d'autres pièces adverses, il doit absolument le faire. Ce membre contient None si aucune position n'est
            forcée.

    """

    def __init__(self):
        """Constructeur de la classe Partie. Initialise les attributs à leur valeur par défaut. Le damier est construit
        avec les pièces à leur valeur initiales, le joueur actif est le joueur blanc, et celui-ci n'est pas forcé
        de prendre une pièce adverse. Aucune position source n'est sélectionnée, et aucune position source n'est forcée.

        """
        self.damier = Damier()
        self.couleur_joueur_courant = "blanc"
        self.doit_prendre = False
        self.position_source_selectionnee = None
        self.position_source_forcee = None


    def position_source_valide(self, position_source):
        """Vérifie la validité de la position source, notamment:
            - Est-ce que la position contient une pièce?
            - Est-ce que cette pièce est de la couleur du joueur actif?
            - Si le joueur doit absolument continuer son mouvement avec une prise supplémentaire, a-t-il choisi la
              bonne pièce?

        Cette méthode retourne deux valeurs. La première valeur est Booléenne (True ou False), et la seconde valeur est
        un message d'erreur indiquant la raison pourquoi la position n'est pas valide (ou une chaîne vide s'il n'y a pas
        d'erreur).

        ATTENTION: Utilisez les attributs de la classe pour connaître les informations sur le jeu! (le damier, le joueur
            actif, si une position source est forcée, etc.

        ATTENTION: Vous avez accès ici à un attribut de type Damier. vous avez accès à plusieurs méthodes pratiques
            dans le damier qui vous simplifieront la tâche ici :)

        Args:
            position_source (Position): La position source à valider.

        Returns:
            bool, str: Un couple où le premier élément représente la validité de la position (True ou False), et le
                 deuxième élément est un message d'erreur (ou une chaîne vide s'il n'y a pas d'erreur).

        """

        # initialiser le resultat
        resultat = False

        # verifier si la piece se trouve dans le dictionnaire
        if position_source in self.damier.cases:

            # verifier si c'est le tour de la couleur
            if self.damier.recuperer_piece_a_position(position_source).couleur == self.couleur_joueur_courant:

                # verifier si la piece peut faire une prise
                if self.damier.piece_peut_faire_une_prise(position_source):
                    # on l'oblige a continuer de jouer
                    self.doit_prendre = True
                    # devienne la piece qu'il faut bouger
                    self.position_source_forcee = position_source
                    resultat = True
                    print("")

                # sinon si la piece peut juste bouger
                elif self.damier.piece_peut_se_deplacer(position_source):
                    # on selectionne cette piece
                    self.position_source_selectionnee = position_source
                    resultat = True
                    print("")

                # verifier si la piece ne peux pas bouger
                elif not (self.damier.piece_peut_se_deplacer(position_source)
                      and ((self.damier.piece_peut_faire_une_prise(position_source)) or
                           (not self.damier.piece_peut_faire_une_prise(position_source)))):
                    print("Erreur: La piece ne peut pas se deplacer")
                    print("")

            # si ce n'est pas le tour de jouer de la couleur
            else:
                print("""Erreur: Ce n'est pas le tour du {}
                """.format(self.damier.recuperer_piece_a_position(position_source).couleur))
                print("")

        # si la piece n'existe pas
        else:
            print("Erreur: Position source invalide: aucune pièce à cet endroit")
            print("")

        return resultat



    def position_cible_valide(self, position_cible):
        """Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide (utilisez les méthodes que vous avez programmées dans le Damier!), mais
        également si le joueur a respecté la contrainte de prise obligatoire.

        Returns:
            bool, str: Deux valeurs, la première étant Booléenne et indiquant si la position cible est valide, et la
                seconde valeur est une chaîne de caractères indiquant un message d'erreur (ou une chaîne vide s'il n'y
                a pas d'erreur).

        """

        # initialiser le resultat
        resultat = False

        # verifier s'il y a une prise obligatoire
        if self.doit_prendre:

            # verifier si on se joue avec la piece qui doit faire une prise et qu'elle peut faire une prise
            if self.damier.piece_peut_sauter_vers(self.position_source_forcee, position_cible):
                print("")
                resultat = True

            # si la piece bouge ailleur que la cible ou qu'on selectionne une autre piece
            elif self.damier.piece_peut_se_deplacer_vers(self.position_source_forcee, position_cible) or \
                    self.damier.piece_peut_se_deplacer_vers(self.position_source_selectionnee, position_cible):

                print("Le déplacement demandé n'est pas une prise alors qu'une prise est possible")
                print("")

            # verifier si on bouge la piece au mauvais endroit
            elif not self.damier.piece_peut_se_deplacer_vers(self.position_source_forcee, position_cible) or \
                    not self.damier.piece_peut_se_deplacer_vers(self.position_source_selectionnee, position_cible):

                print("Position cible invalide")
                print("")

        # s'il n y a aucune piece qui doit prendre
        else:
        # verifier si la piece peut se deplacer a la position cible
            if self.damier.piece_peut_se_deplacer_vers(self.position_source_selectionnee, position_cible):
                print("")
                resultat = True

            else:
                print("Position cible invalide")
                print("")


        return resultat



    def demander_positions_deplacement(self):
        """Demande à l'utilisateur les positions sources et cible, et valide ces positions. Cette méthode doit demander
        les positions à l'utilisateur tant que celles-ci sont invalides.

        Cette méthode ne doit jamais planter, peu importe ce que l'utilisateur entre.

        Returns:
            Position, Position: Un couple de deux positions (source et cible).

        """
        # initialiser la condition de sortie
        arret = False

        while not arret:

            # tant que les positions entrees ne sont pas acceptees , on reste dans la boucle
            while True:

            # verifier si les entrees de l'utilisateur sont correcte
                try:
                    self.source_ligne = int(input("(Position source) Numéro de ligne "))
                    self.source_colonne = int(input("(Position source) Numéro de colonne "))

                    if not self.position_source_valide(Position(self.source_ligne, self.source_colonne)):
                        continue

                except ValueError:
                    continue

                try:
                    self.cible_ligne = int(input("(Position cible) Numéro de ligne "))
                    self.cible_colonne = int(input("(Position cible) Numéro de colonne "))

                    if not self.position_cible_valide(Position(self.cible_ligne, self.cible_colonne)):
                        continue

                except ValueError:
                    continue

                # une fois les les entrees sont acceptees, on sort de la boucle
                break

            arret = True

        self.source = Position(self.source_ligne, self.source_colonne) # coordonees position source
        self.cible = Position(self.cible_ligne, self.cible_colonne) # coordonees position cible

        # retourner le couble de position source et cible
        return self.source, self.cible



    def tour(self):
        """Cette méthode effectue le tour d'un joueur, et doit effectuer les actions suivantes:
        - Assigne self.doit_prendre à True si le joueur courant a la possibilité de prendre une pièce adverse.
        - Affiche l'état du jeu
        - Demander les positions source et cible (utilisez self.demander_positions_deplacement!)
        - Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        - Si une pièce a été prise lors du déplacement, c'est encore au tour du même joueur si celui-ci peut encore
          prendre une pièce adverse en continuant son mouvement. Utilisez les membres self.doit_prendre et
          self.position_source_forcee pour forcer ce prochain tour!
        - Si aucune pièce n'a été prise ou qu'aucun coup supplémentaire peut être fait avec la même pièce, c'est le
          tour du joueur adverse. Mettez à jour les attributs de la classe en conséquence.

        """

        # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.
        if self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.doit_prendre = True

        # Affiche l'état du jeu
        print(self.damier)
        print("")
        print("Tour du joueur", self.couleur_joueur_courant, end=".")
        if self.doit_prendre:
            if self.position_source_forcee is None:
                print(" Doit prendre une pièce.")
            else:
                print(" Doit prendre avec la pièce en position {}.".format(self.position_source_forcee))
        else:
            print("")

        # Demander les positions
        self.position = self.demander_positions_deplacement()

        # Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
        self.damier.deplacer(self.position[0], self.position[1])

        # Mettre à jour les attributs de la classe
        # si on doit absolument faire une prise
        if self.doit_prendre:

            # si la piece ne peut plus faire des  prise additionnelles on modifie les attributs
            if not self.damier.piece_peut_faire_une_prise(self.position[1]):
                self.doit_prendre = False
                self.position_source_forcee = None

            # on change le joueur
                if self.damier.recuperer_piece_a_position(self.position[1]).couleur == 'blanc':
                    self.couleur_joueur_courant = 'noir'

                else:
                    self.couleur_joueur_courant = 'blanc'

            # si la piece peut encore faire une prise on modifie sa position
            else:
                self.position_source_forcee = self.position[1]

        # s'il n y a aucune prise obligatoire
        else:
        # on change le joueur
            if self.damier.recuperer_piece_a_position(self.position[1]).couleur == 'blanc':
                self.couleur_joueur_courant = 'noir'

            else:
                self.couleur_joueur_courant = 'blanc'

    def jouer(self):
        """Démarre une partie. Tant que le joueur courant a des déplacements possibles (utilisez les méthodes
        appriopriées!), un nouveau tour est joué.

        Returns:
            str: La couleur du joueur gagnant.
        """

        while self.damier.piece_de_couleur_peut_se_deplacer(self.couleur_joueur_courant) or \
                self.damier.piece_de_couleur_peut_faire_une_prise(self.couleur_joueur_courant):
            self.tour()

        # ajout: pour afficher le damier a la fin du jeu
        print(self.damier)

        if self.couleur_joueur_courant == "blanc":
            return "noir"
        else:
            return "blanc"



if __name__ == "__main__":
    # Point d'entrée du programme. On initialise une nouvelle partie, et on appelle la méthode jouer().
    partie = Partie()

    gagnant = partie.jouer()

    print("------------------------------------------------------")
    print("Partie terminée! Le joueur gagnant est le joueur", gagnant)

# Auteurs: Mustapha Bouhsen & Andreanne Lapointe

from tkinter import Tk, Label, NSEW, Button, Toplevel, Frame, E, W, Spinbox
from tkinter import messagebox
from canvas_damier import CanvasDamier
from damier import Damier
from partie import Partie
from position import Position
from piece import Piece


class BoutonVert(Button):
    """Création d'un bouton pour garder le même style de bouton à différents endroits"""

    def __init__(self,boss,**Arguments):
        Button.__init__(self,boss,bg="green",fg="white",font="Verdana 8 bold",**Arguments)

class FenetrePartie(Tk):
    """Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme
        listes: listes contenant les positions des cliques
        boutons (BoutonVert):Un widget graphique de type Button pour annuler le dernier déplacement, pour recommencer,
                             afficher les réglements du jeu, pour quitter la partie et pour redimensionner
        statistiques (Frame): Affichant les statistiques de jeu
        dimension (Spinbox): Widget pour choisir une nouvelle dimenssion du damier
        messagebox (messagebox): Pose une question à l'utilisateur à savoir s'il veut reprendre une partie sauvegardé

    """

    def __init__(self):
        """Constructeur de la classe FenetrePartie. On initialise une partie en utilisant la classe Partie du TP3 et
        on dispose les «widgets» dans la fenêtre.
        """

        # Appel du constructeur de la classe de base (Tk)
        super().__init__()

        # La partie
        self.partie = Partie()

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(sticky=NSEW)
        self.canvas_damier.bind('<Button-1>', self.selectionner)

        # Ajout pour organiser les autres widgets
        self.frame_bouton = Frame(self)
        self.frame_bouton.grid()

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # liste qui contient les positions des cliques
        self.liste_position = []
        self.liste_mouvements = []
        self.liste_deplacement = []

        # Bouton afin de faire un retour en arrière et annuler le dernier mouvement
        self.annuler = BoutonVert(self.frame_bouton, text='Annuler dernier mouvement')
        self.annuler.grid(row=0, column=1, pady=10)
        self.annuler.bind('<Button-1>', self.annuler_mouvement)

        # Bouton afin de remettre les pièces en position de départ
        self.recommancer_bouton = BoutonVert(self.frame_bouton, text='Recommencer')
        self.recommancer_bouton.grid(row=1, column=0, padx=10)
        self.recommancer_bouton.bind('<Button-1>', self.recommencer)

        # Bouton pour ouvrir une fenêtre qui explique les reglements
        self.bouton_reglement = BoutonVert(self.frame_bouton, text="Règlements")
        self.bouton_reglement.grid(row = 1, column = 1)
        self.bouton_reglement.bind('<Button-1>', self.popup_reglements)

        # Bouton qui permet de quitter la partie et de la sauvegarder avant de quitter
        self.bouton_quitter = BoutonVert(self.frame_bouton, text = "Quitter")
        self.bouton_quitter.grid(row = 1, column = 3, padx=10)
        self.bouton_quitter.bind('<Button-1>', self.popup_sauvegarder)

        # Message qui avise c'est le tour de quel joueur
        self.messages['foreground'] = 'black'
        self.messages['font'] = "Verdana 10"
        self.messages['text'] = "C'est le tour du joueur {}.".format(self.partie.couleur_joueur_courant)

        # Spinbox pour choisir la dimension du damier avec bouton pour redimensionner
        self.dimension = Label(self,text= "Changer la dimension du damier\n", font= "Verdana 8" )
        self.dimension.grid(row = 3, column = 1)
        self.ma_dimension = Spinbox(self, values =(8, 10, 12))
        self.ma_dimension.grid(row=4, column=1)
        self.redimensionner =BoutonVert(self,text="Redimensionner")
        self.redimensionner.grid(row=5, column=1)
        self.redimensionner.bind('<Button-1>', self.dimension_damier)

        # Organisation des statistiques
        self.satistique = Frame(self)
        self.satistique.grid(row = 0, column = 1)

        self.pion_blanc = Label(self.satistique, text = 'Joueur Blanc',bg="white",fg="black", font= "Verdana 12 bold")
        self.pion_blanc.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.pion_blanc = Label(self.satistique, text='Joueur Noir',bg="black",fg="white",font= "Verdana 12 bold")
        self.pion_blanc.grid(row=0, column=1,  padx = 10, pady = 10)

        self.joueur_blanc = Frame(self.satistique)
        self.joueur_blanc.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.joueur_noir = Frame(self.satistique)
        self.joueur_noir.grid(row=1, column=1, padx = 10, pady = 10)

        Label(self.joueur_blanc, text = "Pions: ",bg="white",
              fg="black",font= "Verdana 10 bold").grid(row = 0, column = 0, padx = 10, pady = 10, sticky = E)

        Label(self.joueur_blanc, text = "Dames: ",
              bg="white",fg="black",font= "Verdana 10 bold").grid(row=1, column=0, padx=10, pady=10, sticky = E)

        Label(self.joueur_blanc, text = "Chance de gagner: ",
              bg="white",fg="black",font= "Verdana 10 bold").grid(row=2, column=0, padx=10, pady=10, sticky = E)

        Label(self.joueur_noir, text="Pions: ",
              bg="black",fg="white", font="Verdana 10 bold").grid(row=0, column=0, padx=10, pady=10, sticky = E)

        Label(self.joueur_noir, text="Dames: ",
              bg="black",fg="white", font="Verdana 10 bold").grid(row=1, column=0, padx=10, pady=10, sticky = E)

        Label(self.joueur_noir, text="Chance de gagner: ",
              bg="black",fg="white",font="Verdana 10 bold").grid(row=2, column=0, padx=10, pady=10, sticky = E)

        self.b_pion = Label(self.joueur_blanc, text='12',bg="white",fg="black",font="Verdana 10")
        self.b_pion.grid(row=0, column=1, sticky = E)

        self.b_dame = Label(self.joueur_blanc, text='0',bg="white",fg="black",font="Verdana 10")
        self.b_dame.grid(row=1, column=1, sticky = E)

        self.b_stat = Label(self.joueur_blanc, text='50%',bg="white",fg="black",font="Verdana 10")
        self.b_stat.grid(row=2, column=1, sticky = E)

        self.n_pion = Label(self.joueur_noir, text='12',bg="black",fg="white",font="Verdana 10")
        self.n_pion.grid(row=0, column=1, sticky = E)

        self.n_dame = Label(self.joueur_noir, text='0',bg="black",fg="white",font="Verdana 10")
        self.n_dame.grid(row=1, column=1, sticky = E)

        self.n_stat = Label(self.joueur_noir, text='50%',bg="black",fg="white",font="Verdana 10")
        self.n_stat.grid(row=2, column=1, sticky = E)

        # Message convivial
        Label(text=" Bonne partie! ",fg = "blue",
              font="Verdana 8 bold").grid(row=5, column=0, padx=10, pady=10, sticky=E)

        # Message qui demande à l'utilisateur s'il veut reprendre une partie sauvegardée
        message = messagebox.askquestion ("Information","Souhaitez-vous reprendre la partie sauvegardée?")
        if message == 'yes':
            self.reprendre_partie_sauvegarder()



    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_damier.n_pixels_par_case
        colonne = event.x // self.canvas_damier.n_pixels_par_case
        position = Position(ligne, colonne)

        # On récupère l'information sur la pièce à l'endroit choisi.
        piece = self.partie.damier.recuperer_piece_a_position(position)

        # a chaque clique, on ajoute la position aux listes
        self.liste_position.append(position)     # liste utilisée pour déplacer les pions
        self.liste_mouvements.append(position)   # liste utilisée pour annuler le dernier déplacement

        # On vérifie que la pièce est dans le dictionnaire
        if self.liste_position[0] in self.partie.damier.cases:

            if len(self.liste_position) > 1:

                # si la couleur du joueur courant et de la pièce est la même
                if self.partie.couleur_joueur_courant == \
                        self.partie.damier.recuperer_piece_a_position(self.liste_position[0]).couleur:

                    # on vérifie si la pièce doit faire une prise
                    if self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
                        self.partie.doit_prendre = True

                    # si la pièce doit faire une prise
                    if self.partie.doit_prendre:

                        # si le deuxième clique correspond à une prise, on déplace la pièce source
                        if self.partie.damier.piece_peut_faire_une_prise(self.liste_position[0]) and \
                                self.partie.damier.piece_peut_sauter_vers(self.liste_position[0],
                                                                          self.liste_position[1]):

                            self.partie.damier.deplacer(self.liste_position[0], self.liste_position[1])

                        else:   # si le deuxième clique n'est pas une prise on affiche un message d'erreur
                            self.messages['foreground'] = 'red'
                            self.messages['text'] = "Erreur! le joueur {}, doit faire une prise".format(
                                self.partie.couleur_joueur_courant)

                        # si la pièce déplacée ne peut pas faire une seconde prise
                        if not self.partie.damier.piece_peut_faire_une_prise(self.liste_position[1]):
                            # il n'y a pas de second tour possible pour ce joueur
                            self.partie.doit_prendre = False
                            self.partie.position_source_forcee = None

                            # on verifie que la pièce a bougé de la position source, donc le joueur a joué son tour
                            if self.liste_position[0] not in self.partie.damier.cases:

                                if self.partie.couleur_joueur_courant == "blanc":  # si c'était le tour du joueur blanc
                                    self.partie.couleur_joueur_courant = "noir"     # ça devient le tour du joueur noir

                                else:                                  # autrement c'est encore le tour du joueur blanc
                                    self.partie.couleur_joueur_courant = "blanc"

                                # on affiche un message pour aviser c'est le tour de quel joueur
                                self.messages['foreground'] = 'black'
                                self.messages['text'] = "C'est le tour du joueur {}.".format(
                                    self.partie.couleur_joueur_courant)

                    # si le joueur n'a pas de prise possible, on déplace la pièce source à la position cible
                    else:
                        self.partie.damier.deplacer(self.liste_position[0], self.liste_position[1])

                        # on verifie que la pièce a bougé de la position source, donc le joueur a joué son tour
                        if self.liste_position[0] not in  self.partie.damier.cases:

                            if self.partie.couleur_joueur_courant == "blanc":      # si c'était le tour du joueur blanc
                                self.partie.couleur_joueur_courant = "noir"         # ça devient le tour du joueur noir

                            else:                                      # autrement c'est encore le tour du joueur blanc
                                self.partie.couleur_joueur_courant = "blanc"

                        # on affiche un message pour aviser c'est le tour de quel joueur
                        self.messages['foreground'] = 'black'
                        self.messages['text'] = "C'est le tour du joueur {}.".format(self.partie.couleur_joueur_courant)

                else:  # on affiche un message d'erreur pour aviser que ce n'est pas le bon joueur
                    self.messages['foreground'] = 'red'
                    self.messages['text'] = "Erreur! C'est le tour du joueur {}."\
                        .format(self.partie.couleur_joueur_courant)

                # si le joueur blanc n'a plus de pièce à déplacer le joueur noir a gagné
                if not self.partie.damier.piece_de_couleur_peut_se_deplacer('blanc'):
                    self.messages['foreground'] = 'green'
                    self.messages['text'] = "Le joueur  Noir a gagné le jeu !"

                # si le joueur noir n'a plus de pièce à déplacer le joueur blanc a gagné
                elif not self.partie.damier.piece_de_couleur_peut_se_deplacer('noir'):
                    self.messages['foreground'] = 'green'
                    self.messages['text'] = "Le joueur Blanc a gagné le jeu !"

                # On vide la liste de ses positions et on met à jour le damier
                self.liste_position.clear()
                self.canvas_damier.actualiser()

        # si la position source n'est pas dans le dictionnaire
        # ou si les positions ne sont pas dans le damier on vide la liste de ses positions
        elif (self.liste_position[0] not in self.partie.damier.cases) or \
                ((self.liste_position[0] and self.liste_position[1]) not in self.partie.damier.cases):

            self.liste_position.clear()

        # section pour les calculer les statistiques de la partie
        p_noir = 0
        p_blanc = 0
        d_blanc = 0
        d_noir =0

        for i in self.partie.damier.cases.values():  # on compte le nombre de pièce de chaque type et couleur sur le jeu

            if i.couleur =='blanc' and i.type_de_piece == 'pion':
                p_blanc += 1

            if i.couleur == 'blanc' and i.type_de_piece == 'dame':
                d_blanc += 1

            if i.couleur == 'noir' and i.type_de_piece == 'pion':
                p_noir += 1

            if i.couleur == 'noir' and i.type_de_piece == 'dame':
                d_noir += 1

        somme = p_blanc + d_blanc + p_noir + d_noir   # total de toutes les pièces sur le jeu
        total_blanc = p_blanc + d_blanc               # total des pièces blanches sur le jeu
        total_noir = p_noir + d_noir                  # total des pièces noires sur le jeu

        self.b_pion['text'] = str(p_blanc)            # nombre de pion blanc sur le jeu
        self.b_dame['text'] = str(d_blanc)            # nombre de dame blanche sur le jeu
        self.b_stat['text'] = str(round((total_blanc/somme) * 100)) + "%"  # pourcentage de pièces blanches
        self.n_pion['text'] = str(p_noir)             # nombre de pion noir sur le jeu
        self.n_dame['text'] = str(d_noir)             # Nombre de dame noir sur le jeu
        self.n_stat['text'] = str(round((total_noir/somme) * 100)) + "%"   # pourcentage de pièce noires


    def dimension_damier(self,_):
        """ Méthode qui redimensionne le damier avec le choix de l'utilisateur

                """

        # on récupère le choix de l'utilisateur de la Spinbox pour les dimensions
        self.nouvelle_dimension = int(self.ma_dimension.get())

        # on assigne le choix de l'utilisateur pour la nouvelle dimension du damier
        self.partie.damier.n_lignes = self.nouvelle_dimension
        self.partie.damier.n_colonnes = self.nouvelle_dimension

        self.n = self.nouvelle_dimension
        self.dam_dict = {}

        # Construction du dictionnaire qui vas centenir les nouvelles pieces et positions:
        # Pour les pieces noires
        for j in range(int((self.n - 2)/2)):
            for i in range(int((self.n / 2))):
                if j % 2 == 0:
                    self.dam_dict[Position(j, 2*i + 1)] = Piece("noir", "pion")
                else:
                    self.dam_dict[Position(j, i*2)] = Piece("noir", "pion")

        # Pour les pieces blanches
        for j in range(int((self.n -1)), int((self.n / 2)), -1):
            for i in range(int((self.n / 2))):
                if j % 2 == 0:
                    self.dam_dict[Position(j, 2 * i + 1)] = Piece("blanc", "pion")

                else:
                    self.dam_dict[Position(j, i * 2)] = Piece("blanc", "pion")

        self.canvas_damier.damier.cases = self.dam_dict

        # pour redimension de la fentere
        if  self.n == 12:
            self.canvas_damier.n_pixels_par_case = 40

        if self.n == 10:
            self.canvas_damier.n_pixels_par_case = 48

        if self.n == 8:
            self.canvas_damier.n_pixels_par_case = 60

        # remettre le blanc comme si c'est une nouvelle partie
        self.partie.couleur_joueur_courant = 'blanc'

        # affichier la couleur du joueur courant
        self.messages['text'] = "C'est le tour du joueur {}.".format(self.partie.couleur_joueur_courant)

        # actualiser le damier
        self.canvas_damier.actualiser()


    def annuler_mouvement(self,_):
        """ Méthode qui annule le dernier déplacement en retournant la pièce à la position source

        """

        # pour faire un retour et annuler le dernier déplacement on récupère dans la liste les deux dernières positions
        position_annuler = self.liste_mouvements[-1] # on récupère la position à annuler dans la liste
        position_retour = self.liste_mouvements[-2] # on récupère la position source dans la liste

        # on détermine la direction du déplacement si prise autrement on aura (0,0)
        case = Position(int((position_annuler.ligne - position_retour.ligne) / 2),
                        int((position_annuler.colonne - position_retour.colonne) / 2))

       # on détermine la position de la pièce adverse (si prise)
        piece_milieu = Position(int(position_retour.ligne + case.ligne),
                                int(position_retour.colonne + case.colonne))

        # on met à jour le dictionnaire et on retire la position qui a été annulée
        self.partie.damier.cases[position_retour] = self.partie.damier.cases[position_annuler]
        del self.partie.damier.cases[position_annuler]

        # on détermine la couleur du joueur courant et on remplace par l'autre pour qu'il puisse continuer son tour
        if self.partie.couleur_joueur_courant == "blanc":
            self.partie.couleur_joueur_courant = "noir"
            # si case est (0,0) ce n'était pas une prise, on actualise le damier et le joueur peut reprendre son tour
            if case == Position(0,0):
                self.messages['text'] = "C'est le tour du joueur {}.".format(self.partie.couleur_joueur_courant)

                self.canvas_damier.actualiser()
            # autrement c'était une prise donc il faut remettre une pièce adverse sur la case
            else:
                piece_adverse_couleur = "blanc"
                piece_adverse_type = "pion"
                self.partie.damier.cases.update({Position(piece_milieu.ligne, piece_milieu.colonne):
                                                 Piece(piece_adverse_couleur, piece_adverse_type)})
        else:
            self.partie.couleur_joueur_courant = "blanc"

            if case == Position(0,0):
                self.messages['text'] = "C'est le tour du joueur {}.".format(self.partie.couleur_joueur_courant)

                self.canvas_damier.actualiser()
            else:
                piece_adverse_couleur = "noir"
                piece_adverse_type = "pion"
                self.partie.damier.cases.update({Position(piece_milieu.ligne,piece_milieu.colonne):
                                                 Piece(piece_adverse_couleur, piece_adverse_type)})

        # une fois la pièce adverse remise on actualise le damier et le joueur peut reprendre son tour
        self.messages['text'] = "C'est le tour du joueur {}.".format(self.partie.couleur_joueur_courant)
        self.canvas_damier.actualiser()


    def recommencer(self,_):
        """ Méthode qui permet de recommencer une partie.

        """

        # pour pouvoir recommencer le jeu on remet les pièces dans le dictionnaire à leur position initiale
        self.partie.damier.cases = \
            {
            Position(7, 0): Piece("blanc", "pion"),
            Position(7, 2): Piece("blanc", "pion"),
            Position(7, 4): Piece("blanc", "pion"),
            Position(7, 6): Piece("blanc", "pion"),
            Position(6, 1): Piece("blanc", "pion"),
            Position(6, 3): Piece("blanc", "pion"),
            Position(6, 5): Piece("blanc", "pion"),
            Position(6, 7): Piece("blanc", "pion"),
            Position(5, 0): Piece("blanc", "pion"),
            Position(5, 2): Piece("blanc", "pion"),
            Position(5, 4): Piece("blanc", "pion"),
            Position(5, 6): Piece("blanc", "pion"),
            Position(2, 1): Piece("noir", "pion"),
            Position(2, 3): Piece("noir", "pion"),
            Position(2, 5): Piece("noir", "pion"),
            Position(2, 7): Piece("noir", "pion"),
            Position(1, 0): Piece("noir", "pion"),
            Position(1, 2): Piece("noir", "pion"),
            Position(1, 4): Piece("noir", "pion"),
            Position(1, 6): Piece("noir", "pion"),
            Position(0, 1): Piece("noir", "pion"),
            Position(0, 3): Piece("noir", "pion"),
            Position(0, 5): Piece("noir", "pion"),
            Position(0, 7): Piece("noir", "pion")
            }

        # on met à jour les attributs de la partie avec les attributs de départ
        self.partie.couleur_joueur_courant = "blanc"
        self.partie.doit_prendre = False
        self.partie.position_source_selectionnee = None
        self.partie.position_source_forcee = None

        # on vide les listes
        self.liste_position.clear()
        self.liste_deplacement.clear()
        self.liste_mouvements.clear()

        # message indiquant que le joueur courant (blanc) doit commencer
        self.messages['foreground'] = 'black'
        self.messages['text'] = "C'est le tour du joueur {}.".format(self.partie.couleur_joueur_courant)

        # On remet les lignes est colonnes du damier a leur etat initial
        self.partie.damier.n_lignes = 8
        self.partie.damier.n_colonnes = 8

        #On remet la dimension original
        self.canvas_damier.n_pixels_par_case = 60

        # on met le damier à jour
        self.canvas_damier.actualiser()


    def sauvegarder_partie(self):
        """ Méthode qui sauvegarde la partie dans un fichier texte.

        """
        fichier = open("sauvegarde.txt", "w")  # en mode écriture on ouvre un fichier text qu'on nomme sauvegarde

        fichier.write("{}\n".format(self.partie.couleur_joueur_courant)) # on sauvegarde c'est le tour de quel joueur

        fichier.write("{}\n".format(self.partie.damier.n_colonnes))



        for i in self.partie.damier.cases.keys():       # on sauvegarde les positions de la partie en cours

            text = "{} {} {} {} \n".format(i.ligne, i.colonne, self.partie.damier.cases[i].couleur,
                                   self.partie.damier.cases[i].type_de_piece )
            fichier.write(text)

        fichier.close()  # on ferme le fichier text créé


    def reprendre_partie_sauvegarder(self):
        """ Méthode qui permet de reprendre la partie sauvegardée dans un fichier texte.

        """

        cases_damier = {}

        try: # si l'utilisateur souhaite reprendre une partie on vérifie qu'il y a bien une partie de sauvegardé

            fichier = open("sauvegarde.txt", "r")  # on ouvre le fichier texte sauvegarde
            couleur = fichier.readline() # on récupère la couleur du joueur à qui s'était le tour

            self.partie.couleur_joueur_courant = couleur.rstrip('\n')   # on met à jour la couleur du joueur courant

            ligne = fichier.readline()
            self.partie.damier.n_lignes = int(ligne.rstrip('\n'))
            self.partie.damier.n_colonnes = int(ligne.rstrip('\n'))


            for i in fichier.readlines(): # on récupère l'état des positions au moment de la sauvegarde

                y = i.split(" ")    # on enlève les espaces

                # Remplir de nouveau dictionnaire par le dictionnaire sauvegarder
                cases_damier[Position(int(y[0]), int(y[1]))] = Piece(y[2], y[3].lstrip("\n"))
                fichier.close()  # on ferme le fichier texte

            self.partie.damier.cases = cases_damier  # on met à jour le dictionnaire avec les positions sauvegardées

            # on informe c'est le tour de quel joueur
            self.messages['text'] = "C'est le tour du joueur {}.".format(self.partie.couleur_joueur_courant)

            # pour redimension de la fentere
            if self.partie.damier.n_lignes == 12:
                self.canvas_damier.n_pixels_par_case = 40

            if self.partie.damier.n_lignes == 10:
                self.canvas_damier.n_pixels_par_case = 48

            if self.partie.damier.n_lignes == 8:
                self.canvas_damier.n_pixels_par_case = 60


            # on met à jour le damier
            self.canvas_damier.actualiser()

        except: # s'il n'a a pas de partie sauvegardé on passe par dessus
            pass



    def popup_reglements(self,_):
        """
        Apelle la fonction pop_règlements uniquement lorsque le bouton est cliqué
        """
        # En attente du clique du bouton règlements
        Reglements(self)
        self.wait_window()

    def popup_sauvegarder(self,_):
        """
        Apelle la fonction popup_sauvegarder uniquement lorsque le bouton est cliqué
        """
        # En attente du clique du bouton sauvegarder
        Sauvegarder(self)
        self.wait_window()


class Reglements(Toplevel):
    """
    Fenêtre pop-up montrant les réglements du jeu de dame

    Attributes:
        cadre (Frame): pour organiser la fenêtre
        règlements (Label) : message avec les règlements de jeu
        bouton (BoutonVert) : un widget graphique de style bouton pour fermer la fenêtre

    """

    def __init__(self,master):
        super().__init__(master)
        # Nom de la fenêtre
        self.title("Réglements du jeu de dames")

        # oragnisation de la fenêtre
        self.cadre = Frame(self)
        self.cadre.grid()

        # messages incluant les règlements de jeu
        Label(self.cadre, text = "Règlements:").grid(pady = 5)
        Label(self.cadre,
              text="#1- Le joueur avec les pions blancs commence en premier").grid(row=1, sticky = W, pady = 5)

        Label(self.cadre,
              text="#2- Les pions peuvent se déplacer en diagonale vers l'avant").grid(row=2, sticky = W, pady = 5)

        Label(self.cadre,
              text="#3- Une case doit être libre pour s'y déplacer").grid(row=3, sticky = W, pady = 5)

        Label(self.cadre,
              text="#4- Lorsqu'un pion atteint le côté opposé il devient une dame").grid(row=4, sticky = W, pady = 5)

        Label(self.cadre,
              text="#5- Une dame peut se déplacer en diagonale vers l'avant et vers l'arrière").grid(row=5,
                                                                                                 sticky = W, pady = 5)

        Label(self.cadre,
              text="#6- Un pion peut effectuer une prise en sautant par dessus un pion adverse").grid(row=6,
                                                                                                sticky = W, pady = 5)

        Label(self.cadre,
              text="#7- Pour effectuer une prise la case d'arrivée doit être libre").grid(row=7,
                                                                                          sticky = W, pady = 5)
        Label(self.cadre,
              text="#8- Après une prise un joueur doit continuer son tour tant qu'il peut faire des prises").grid(row=8,
                                                                                                sticky = W, pady = 5)

        Label(self.cadre,
              text="#9- Lors du tour d'un joueur s'il peut faire une prise il doit absolument le faire").grid(row=9,
                                                                                            sticky = W, pady = 5)

        Label(self.cadre,
              text="#10- Un joueur gagne la partie si son adversaire n'a plus de pièce à déplacer").grid(row=10,
                                                                                                 sticky = W, pady = 5)

        # widget bouton pour fermer la fenêtre
        self.bouton_ok = BoutonVert(self, text="Fermer")
        self.bouton_ok.grid(pady = 10)
        self.bouton_ok.bind('<Button-1>', self.popup_ok)

    # commande associé au bouton pour détruire la fenêtre
    def popup_ok(self,_):
        self.destroy()


class Sauvegarder(Toplevel):
    """ Fenêtre pop-up demandant aux joueurs s'ils veulent sauvegarder la partie en cours

        Attributes:
            Label: message à l'utilisateur
            boutons (BoutonVert): widgets graphiques de style bouton pour sauvegarder ou quitter la partie

    """

    def __init__(self,master):
        super().__init__(master)
        # Nom de la fenêtre
        self.title("Quitter la partie")

        # message à l'utilisateur
        Label(self, text="Avant de quitter, souhaitez-vous sauvegarder la partie?").grid()

        # un widget bouton pour sauvegarder la partie, lorsque cliqué associé à save qui appelle la méthode sauvegarder
        self.bouton_oui = BoutonVert(self, text="Sauvegarder")
        self.bouton_oui.grid(row = 2, column = 0)
        self.bouton_oui.bind('<Button-1>',self.save)

        # un widget bouton pour quitter la partie, lorsque cliqué associé à quitter qui détruit les fenêtres
        self.bouton_non = BoutonVert(self, text="Quitter")
        self.bouton_non.grid(row = 3, column = 0, padx = 10, pady=10)
        self.bouton_non.bind('<Button-1>', self.quitter)

    # commande associé au bouton pour quitter
    def quitter(self,_):
        self.destroy()
        fenetre.destroy()

    # commande associé au bouton pour sauvegarder la partie
    def save(self,_):
        fenetre.sauvegarder_partie()
        # une fois sauvergardé on détruit les fenêtre
        self.destroy()
        fenetre.destroy()


if __name__ == '__main__':
    # Point d'entrée principal du TP4.
    fenetre = FenetrePartie()
    fenetre.mainloop()








# Importation des bibliothèques nécessaires
import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk, ImageFilter  # Bibliothèque pour gérer les images

# Configuration des dimensions de la fenêtre et des cartes
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 100, 140  # Dimensions des cartes
CARD_SPACING = 15  # Espacement entre les cartes

# Classe principale du jeu de Blackjack
class BlackjackGame:
    def __init__(self, root):
        # Initialisation de la fenêtre de jeu et des variables de base
        self.root = root
        self.root.title("BlackJack ALPHA 0.1")
        
        # Charger et flouter l'image de fond
        self.background_image = Image.open("C:/Users/Riyad/Desktop/Jeu PYTHON/Assets/FondVert.jpg")
        self.background_image = self.background_image.resize((WIDTH, HEIGHT))
        self.background_image = self.background_image.filter(ImageFilter.GaussianBlur(10))  # Appliquer un flou
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Création du canvas pour dessiner les éléments graphiques
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        
        # Chargement des images de cartes dans un dictionnaire
        self.card_images = {}
        self.load_card_images()  # Charge les images des cartes

        # Initialisation du deck de cartes, des mains de joueur et croupier, et des variables de jeu
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
        self.result_message = ""
        self.state = "menu"  # État actuel du jeu ("menu", "playing", "game_over")
        
        # Liste pour stocker les boutons
        self.buttons = []

        # Charger l'image de la carte masquée pour le croupier
        self.hidden_card_image = Image.open("C:/Users/Riyad/Desktop/Jeu PYTHON/Assets/Point_d'interrogation.png").resize((CARD_WIDTH, CARD_HEIGHT))
        self.hidden_card_photo = ImageTk.PhotoImage(self.hidden_card_image)
        
        # Mise à jour de l'interface utilisateur en fonction de l'état
        self.update_ui()

    # Fonction pour créer un deck de cartes mélangé
    def create_deck(self):
        ranks = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Fou", "Reine", "Roi"]
        suits = ["Pic", "Trefle", "Coeur", "Carreaux"]
        deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    # Fonction pour charger les images de chaque carte
    def load_card_images(self):
        suits = ["Pic", "Trefle", "Coeur", "Carreaux"]
        ranks = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Fou", "Reine", "Roi"]
        for suit in suits:
            for rank in ranks:
                card_name = f"{rank}{suit}"  # Nom de la carte
                for extension in ['png', 'jpg']:
                    image_path = f"C:/Users/Riyad/Desktop/Jeu PYTHON/Assets/{card_name}.{extension}"  # Chemin de l'image
                    try:
                        img = Image.open(image_path).resize((CARD_WIDTH, CARD_HEIGHT))
                        self.card_images[card_name] = ImageTk.PhotoImage(img)
                        break  # Si l'image est trouvée, arrêter la recherche
                    except FileNotFoundError:
                        continue

    # Fonction pour distribuer une carte à une main spécifique
    def deal_card(self, hand):
        card = self.deck.pop()
        hand.append(card)
        return card

    # Fonction pour démarrer une nouvelle partie
    def start_game(self):
        self.deck = self.create_deck()
        self.player_hand = [self.deal_card(self.player_hand), self.deal_card(self.player_hand)]
        self.dealer_hand = [self.deal_card(self.dealer_hand), self.deal_card(self.dealer_hand)]
        self.game_over = False
        self.result_message = ""
        self.state = "playing"
        self.update_ui()

    # Fonction pour calculer le score d'une main
    def calculate_score(self, hand):
        values = {'As': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Fou': 10, 'Reine': 10, 'Roi': 10}
        score = 0
        num_aces = 0
        for card in hand:
            for i in range(len(card)):
                if card[i].isupper() and i != 0:
                    card_name = card[:i]
                    break
            else:
                card_name = card
            if card_name in values:
                score += values[card_name]
                if card_name == 'As':
                    num_aces += 1

        # Ajuster la valeur des As si le score dépasse 21
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1

        return score

    # Fonction pour ajouter une carte à la main du joueur
    def player_hit(self):
        if not self.game_over:
            card = self.deal_card(self.player_hand)
            player_score = self.calculate_score(self.player_hand)
            if player_score > 21:
                self.result_message = "Vous avez perdu !"
                self.game_over = True
            elif player_score == 21 and len(self.player_hand) == 2:
                self.result_message = "BLACK JACK ! VOUS AVEZ GAGNÉ !"
                self.game_over = True
            self.update_ui()

    # Fonction pour gérer le tour du croupier
    def dealer_play(self):
        dealer_score = self.calculate_score(self.dealer_hand)
        while dealer_score < 17:
            self.deal_card(self.dealer_hand)
            dealer_score = self.calculate_score(self.dealer_hand)
        if not self.game_over:
            player_score = self.calculate_score(self.player_hand)
            if dealer_score > 21 or player_score > dealer_score:
                self.result_message = "Vous avez gagné !"
            elif dealer_score == player_score:
                self.result_message = "Égalité !"
            else:
                self.result_message = "Vous avez perdu !"
        self.game_over = True
        self.update_ui()

    # Fonction pour afficher le menu de démarrage
    def show_menu(self):
        self.clear_buttons()
        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)
        self.canvas.create_text(WIDTH // 2, HEIGHT // 4, text="Bienvenue au BlackJack !", fill="white", font=("Arial", 24))
        
        start_button = tk.Button(self.root, text="Commencer une nouvelle partie", command=self.start_game)
        start_button.pack(pady=20)
        self.buttons.append(start_button)
        
        quit_button = tk.Button(self.root, text="Quitter", command=self.root.quit)
        quit_button.pack(pady=20)
        self.buttons.append(quit_button)

    # Fonction pour afficher l'état de jeu en cours
    def show_playing(self):
        self.clear_buttons()
        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)

        # Afficher les cartes du joueur
        for i, card in enumerate(self.player_hand):
            self.canvas.create_image(200 + i * (CARD_WIDTH + CARD_SPACING), HEIGHT - CARD_HEIGHT - 50, image=self.card_images[card])

        player_score = self.calculate_score(self.player_hand)
        self.canvas.create_text(200, HEIGHT - CARD_HEIGHT - 100, text=f"Score du Joueur: {player_score}", fill="white", font=("Arial", 18))

        # Afficher les cartes du croupier
        self.canvas.create_image(200, 50, image=self.hidden_card_photo)  # Carte cachée
        for i, card in enumerate(self.dealer_hand[1:], start=1):  # Afficher la carte visible
            self.canvas.create_image(200 + i * (CARD_WIDTH + CARD_SPACING), 50, image=self.card_images[card])

        dealer_score = self.calculate_score(self.dealer_hand)
        self.canvas.create_text(200, 20, text=f"Score du Croupier: {dealer_score}", fill="white", font=("Arial", 18))

        # Afficher les boutons pour le joueur
        hit_button = tk.Button(self.root, text="Tirer une carte", command=self.player_hit)
        hit_button.pack(pady=10)
        self.buttons.append(hit_button)

        stand_button = tk.Button(self.root, text="Se coucher", command=self.stand)
        stand_button.pack(pady=10)
        self.buttons.append(stand_button)

    # Fonction pour afficher l'écran de fin de partie
    def show_game_over(self):
        self.clear_buttons()
        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)
        self.canvas.create_text(WIDTH // 2, HEIGHT // 4, text=self.result_message, fill="white", font=("Arial", 24))

        replay_button = tk.Button(self.root, text="Rejouer", command=self.start_game)
        replay_button.pack(pady=20)
        self.buttons.append(replay_button)

        quit_button = tk.Button(self.root, text="Quitter", command=self.root.quit)
        quit_button.pack(pady=20)
        self.buttons.append(quit_button)

    # Supprimer tous les boutons affichés
    def clear_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []

    # Mettre à jour l'interface utilisateur en fonction de l'état du jeu
    def update_ui(self):
        if self.state == "menu":
            self.show_menu()
        elif self.state == "playing":
            self.show_playing()
        elif self.state == "game_over":
            self.show_game_over()

    # Fonction pour que le joueur choisisse de "se coucher"
    def stand(self):
        self.dealer_play()
        self.state = "game_over"
        self.update_ui()

# Fonction principale pour démarrer l'application
def main():
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

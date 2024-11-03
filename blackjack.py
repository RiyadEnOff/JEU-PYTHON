import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk  # Assurez-vous que Pillow est installé

# Configuration des dimensions et couleurs
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = "#006400"  # Vert foncé pour la table
CARD_WIDTH, CARD_HEIGHT = 100, 140  # Dimensions des cartes
CARD_SPACING = 15  # Espacement entre les cartes

class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("BlackJack ALPA 0.1")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()
        
        self.card_images = {}  # Dictionnaire pour stocker les images des cartes
        self.load_card_images()  # Charge les images des cartes
        self.deck = self.create_deck()  # Crée un nouveau deck
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
        self.result_message = ""
        self.state = "menu"  # "menu", "playing", "game_over"
        
        self.buttons = []  # Liste pour stocker les boutons
        
        self.update_ui()

    def create_deck(self):
        ranks = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Fou", "Reine", "Roi"]
        suits = ["Pic", "Trefle", "Coeur", "Carreaux"]
        deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def load_card_images(self):
        suits = ["Pic", "Trefle", "Coeur", "Carreaux"]
        ranks = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Fou", "Reine", "Roi"]
        for suit in suits:
            for rank in ranks:
                card_name = f"{rank}{suit}"  # Adapté au format sans espace
                for extension in ['png', 'jpg']:
                    image_path = f"C:/Users/Riyad/Desktop/Jeu PYTHON/Assets/{card_name}.{extension}"  # Chemin complet
                    try:
                        img = Image.open(image_path).resize((CARD_WIDTH, CARD_HEIGHT))
                        self.card_images[card_name] = ImageTk.PhotoImage(img)
                        break  # Sortir de la boucle si l'image est chargée
                    except FileNotFoundError:
                        continue  # Continuer à essayer les autres formats
                else:
                    print(f"Image non trouvée pour la carte: {card_name}")

    def deal_card(self, hand):
        card = self.deck.pop()
        hand.append(card)
        return card

    def start_game(self):
        self.deck = self.create_deck()
        self.player_hand = [self.deal_card(self.player_hand), self.deal_card(self.player_hand)]
        self.dealer_hand = [self.deal_card(self.dealer_hand), self.deal_card(self.dealer_hand)]
        self.game_over = False
        self.result_message = ""
        self.state = "playing"
        self.update_ui()

    def calculate_score(self, hand):
        values = {'As': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Fou': 10, 'Reine': 10, 'Roi': 10}
        score = 0
        num_aces = 0
        for card in hand:
            # Extraire le nom de la carte en prenant tout sauf le dernier caractère majuscule (la couleur)
            for i in range(len(card)):
                if card[i].isupper() and i != 0:
                    card_name = card[:i]
                    break
            else:
                card_name = card  # Au cas où quelque chose se passe mal, utilisez la carte entière

            if card_name in values:
                score += values[card_name]
                if card_name == 'As':
                    num_aces += 1

        # Ajuster la valeur des As si le score dépasse 21
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1

        return score

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

    def show_menu(self):
        self.clear_buttons()
        self.canvas.create_text(WIDTH // 2, HEIGHT // 4, text="Bienvenue au BlackJack !", fill="white", font=("Arial", 24))
        
        start_button = tk.Button(self.root, text="Commencer une nouvelle partie", command=self.start_game)
        start_button.pack(pady=20)
        self.buttons.append(start_button)
        
        quit_button = tk.Button(self.root, text="Quitter", command=self.root.quit)
        quit_button.pack(pady=20)
        self.buttons.append(quit_button)

    def show_playing(self):
        self.clear_buttons()
        self.canvas.delete("all")

        # Texte de la main du joueur
        self.canvas.create_text(WIDTH // 2, HEIGHT // 7, text="Votre main", fill="white", font=("Arial", 18))
        x_start_player = WIDTH // 2 - (len(self.player_hand) * (CARD_WIDTH + CARD_SPACING)) // 2
        y_pos_player = HEIGHT // 5.2  # Ajuster la position verticale des cartes du joueur

        # Afficher les cartes du joueur
        for card in self.player_hand:
            if card in self.card_images:
                self.canvas.create_image(x_start_player, y_pos_player, image=self.card_images[card], anchor=tk.NW)
                x_start_player += CARD_WIDTH + CARD_SPACING  # Espacement entre les cartes

        # Texte de la main du croupier
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2.1, text="Main du croupier", fill="white", font=("Arial", 18))
        x_start_dealer = WIDTH // 2 - (len(self.dealer_hand) * (CARD_WIDTH + CARD_SPACING)) // 2
        y_pos_dealer = HEIGHT // 1.9  # Ajuster la position verticale des cartes du croupier

        # Afficher les cartes du croupier
        for card in self.dealer_hand:
            if card in self.card_images:
                self.canvas.create_image(x_start_dealer, y_pos_dealer, image=self.card_images[card], anchor=tk.NW)
                x_start_dealer += CARD_WIDTH + CARD_SPACING  # Espacement entre les cartes

        # Scores
        self.canvas.create_text(WIDTH // 2, HEIGHT // 1.2, text=f"Score Joueur: {self.calculate_score(self.player_hand)}", fill="white", font=("Arial", 18))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 1.15, text=f"Score Croupier: {self.calculate_score(self.dealer_hand)}", fill="white", font=("Arial", 18))

        # Boutons de jeu
        hit_button = tk.Button(self.root, text="Tirer", command=self.player_hit)
        hit_button.pack(side=tk.LEFT, padx=20)
        self.buttons.append(hit_button)
        
        stand_button = tk.Button(self.root, text="Se coucher", command=self.stand)
        stand_button.pack(side=tk.RIGHT, padx=20)
        self.buttons.append(stand_button)

    def show_game_over(self):
        self.clear_buttons()
        self.canvas.delete("all")
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=self.result_message, fill="red", font=("Arial", 24))
        
        replay_button = tk.Button(self.root, text="Rejouer", command=self.start_game)
        replay_button.pack(side=tk.LEFT, padx=20)
        self.buttons.append(replay_button)
        
        quit_button = tk.Button(self.root, text="Quitter", command=self.root.quit)
        quit_button.pack(side=tk.RIGHT, padx=20)
        self.buttons.append(quit_button)

    def clear_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []

    def update_ui(self):
        if self.state == "menu":
            self.show_menu()
        elif self.state == "playing":
            self.show_playing()
        elif self.state == "game_over":
            self.show_game_over()

    def stand(self):
        self.dealer_play()
        self.state = "game_over"
        self.update_ui()

def main():
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

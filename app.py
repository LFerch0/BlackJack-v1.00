import random

# Función para generar una carta aleatoria
def randomizeCard():
    simbols = ['♠', '♥', '♦', '♣']
    numberCards = [('A', 10), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('J', 10), ('Q', 10), ('K', 10)]
    
    def createCard(simbols, numberCards):
        simbol = random.choice(simbols)
        number, value = random.choice(numberCards)
        card = (simbol, number, value)  # simbolo, numero, valor
        return card
    
    return createCard(simbols, numberCards)

# Función para verificar que no se repita la carta
def comprobationCard(card, usedCards):
    attempts = 0
    while card in usedCards and attempts < 6:
        card = randomizeCard()
        attempts += 1
    return card

def comprobationA(hand):
    new_hand = []
    
    for card in hand:
        if card[1] == 'A' and card[2] == 11:  # Si el rango es 'A' y el valor es 11
            # Cambiamos el valor de 11 a 1
            new_card = (card[0], card[1], 1)
            new_hand.append(new_card)
        else:
            # Mantenemos la carta sin cambios
            new_hand.append(card)

    return new_hand 

# Generar cartas
def generateCards(num_cards):
    cards = []
    usedCards = set()
    
    for _ in range(num_cards):
        card = randomizeCard()
        card = comprobationCard(card, usedCards)
        cards.append(card)  # Se agrega la carta completa
        usedCards.add(card)
    
    return cards

# Imprimir las cartas (solo símbolo y número)
def printCards(cards):
    return [f"{number}{symbol}" for symbol, number, _ in cards]

# Generar la primera mano
def firstHands():
    dealer_hand = generateCards(2)
    player_hand = generateCards(1)
    
    print("Dealer's cards:", printCards(dealer_hand))
    print("Player's cards:", printCards(player_hand))
    
    return player_hand, dealer_hand

# Pedir una nueva carta
def askForNewCard():
    while True:
        response = input("Do you want to take a new card? (yes/no): ").strip().lower()

        if response == 'yes':
            return True  # El jugador toma otra carta
        elif response == 'no':
            return False  # El jugador detiene su turno
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Turno del jugador
def playerTurn(player_hand, money, bet):
    while True:

        # Pregunta si el jugador quiere tomar más cartas
        if not askForNewCard():
            return money  # El jugador decide detenerse sin perder

        new_card = generateCards(1)[0]
        player_hand.append(new_card)
        print("Player's new card:", printCards([new_card])[0])
        print("Player's cards:", printCards(player_hand))
        
        # Sumar el valor total de las cartas del jugador
        total_value = sum(card[2] for card in player_hand)

        if total_value > 21:
            if any(card[1] == 'A' for card in player_hand):
                player_hand = comprobationA(player_hand)
                total_value = sum(card[2] for card in player_hand)
            else:
                print(f"Player's lost with a total value of {total_value}")                
                print("Player's cards:", printCards(player_hand))
                return money - bet  # El jugador pierde, se resta la apuesta
        elif total_value == 21:
            print("Player wins with a total value of 21!")
            print("Player's cards:", printCards(player_hand))
            return money + bet * 2  # El jugador gana, se duplica la apuesta

        print(f"Player's total value: {total_value}")

# Turno del dealer
def dealerTurn(dealer_hand, money, bet):
    print("Dealer's cards:", printCards(dealer_hand))

    # El dealer sigue tomando cartas mientras su valor total sea menor que 17
    while sum(card[2] for card in dealer_hand) < 17:
        new_card = generateCards(1)[0]
        dealer_hand.append(new_card)
        print("Dealer's new card:", printCards([new_card])[0])
        print("Dealer's cards:", printCards(dealer_hand))

    total_value = sum(card[2] for card in dealer_hand)
    
    if total_value > 21:
        if any(card[1] == 'A' for card in dealer_hand):  # Corregido: buscar en dealer_hand
            dealer_hand = comprobationA(dealer_hand)
            total_value = sum(card[2] for card in dealer_hand)
        elif total_value == 21:
            print("Dealer wins with a total value of 21!")
            return money - bet  # El dealer gana, se resta la apuesta
        else:
            print(f"Dealer's lost with a total value of {total_value}")
            return money + bet * 2  # El dealer pierde, se duplica la apuesta
    else:
        print("Dealer's final cards:", printCards(dealer_hand))
        print(f"Dealer's total value: {total_value}")
        return money

# Comparar manos
def compareHands(dealer_hand, player_hand, money, bet):
    dealer_score = sum(card[2] for card in dealer_hand)
    player_score = sum(card[2] for card in player_hand)

    if player_score > dealer_score:
        print("Player wins")
        return money + bet * 2
    elif player_score < dealer_score:
        print("Dealer wins")
        return money - bet
    else:
        print("It's a tie")
        return money  # Empate, no cambia el dinero

# Flujo principal del juego
def game():
    money = int(input("How much money are you willing to lose today? "))  # Convertir a número
    bet = int(input("How much money do you want to bet? "))  # Convertir a número
    
    player_hand, dealer_hand = firstHands()

    # Ejecutar el turno del jugador
    money = playerTurn(player_hand, money, bet)

    # Si el jugador no ha perdido todo, ejecutar el turno del dealer
    if money > 0:
        money = dealerTurn(dealer_hand, money, bet)

        # Comparar las manos si el dealer no pierde
        money = compareHands(dealer_hand, player_hand, money, bet)

    print(f"Final money: {money}")

# Iniciar el juego
game()

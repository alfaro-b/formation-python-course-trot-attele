import random


def ask_user():
    horse_nbr = int(input("Combien de chevaux participent à la course? (Entre 12 et 20 chevaux) "))

    while horse_nbr < 12 or horse_nbr > 20:
        print("Une course comporte entre 12 et 20 chevaux.")
        horse_nbr = int(input("Combien de chevaux participent à la course?"))

    race_type = int(input("Choisissez un type de course? 3(Tiercé), 4(Quarté), 5(Quinté) "))
    while race_type not in (3, 4, 5):
        print("Choisissez 3,4 ou 5 pour le type de course.")
        race_type = int(input("Choisissez un type de course? 3(Tiercé), 4(Quarté), 5(Quinté) "))

    return horse_nbr, race_type


def create_horses(horse_nbr):
    horses = []
    for n in range(horse_nbr):
        horse = {
            "numéro": n + 1,
            "vitesse": 0,
            "distance": 0,
            "disqualified": False
        }
        horses.append(horse)
    return horses


def roll_dice():
    dice_nbr = random.randint(1, 6)
    return dice_nbr


speed_changes = [
    [0, 1, 1, 1, 2, 2],  # vitesse à 0
    [0, 0, 1, 1, 1, 2],  # vitesse à 1
    [0, 0, 1, 1, 1, 2],  # vitesse à 2
    [-1, 0, 0, 1, 1, 1],  # vitesse à 3
    [-1, 0, 0, 1, 1, 1],  # vitesse à 4
    [-2, -1, 0, 0, 0, 1],  # vitesse à 5
    [-2, -1, 0, 0, 0, "DQ"]  # vitesse à 6
    ]


def calculate_new_speed(dice_nbr, horse):
    actual_speed = horse["vitesse"]
    change = speed_changes[actual_speed][dice_nbr - 1]
    if change == "DQ":
        horse["disqualified"] = True
        return actual_speed

    actual_speed += change
    horse["vitesse"] = actual_speed
    return actual_speed


distance = [0, 23, 46, 69, 92, 115, 138]  # Distance parcourue en fonction de la vitesse 0,1,2,3,4,5,6


def calculate_distance(actual_speed):
    distance_traveled = distance[actual_speed]
    return distance_traveled


def is_end_game(horses):
    for horse in horses:
        if not (horse["disqualified"]) and horse["distance"] < 2400:
            return False

    print("Course terminée")
    return True


def display_winner(horses, race_type):
    sorted_horses = sorted(
        [horse for horse in horses if not horse["disqualified"]],
        key=lambda horse: horse["distance"],
        reverse=True
    )  # permet de trier liste en fonction de la distance
    return sorted_horses[:race_type]
    # race_type ne contenant que 3, 4, 5, permet de retourner podium en fonction du type de course


if __name__ == "__main__":
    horse_nbr, race_type = ask_user()
    horses = create_horses(horse_nbr)

    round = 0

    while not is_end_game(horses):
        round += 1
        passed_time = round * 10
        print(f"Tour : {round}, Temps écoulé = {passed_time} secondes")

        for horse in horses:
            if horse["disqualified"]:
                continue
            dice_nbr = roll_dice()
            new_speed = calculate_new_speed(dice_nbr, horse)
            distance_traveled = calculate_distance(new_speed)
            horse["distance"] += distance_traveled
            print(
                f"Cheval {horse['numéro']} : "
                f"vitesse = {horse['vitesse']}, "
                f"distance parcourue = {horse['distance']}m, "
                f"statut = {horse['disqualified']}"
            )

    print(f"La course s'est terminée en {round} tours.")

    print(horses)
    podium = display_winner(horses, race_type)
    print(f"Les {race_type} premiers sont :")
    for place, horse in enumerate(podium, start=1): # enumerate permet d'obtenir l'indice, mais en commençant à 1
        print(
            f"En position {place} : Cheval {horse["numéro"]} "
            f"avec une ditance de {horse['distance']}"
        )

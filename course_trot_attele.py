import random


def ask_user():
    """
    Demande à l'utilisateur de choisir le nombre de chevaux et le type de course
    :return: Nombre de chevaux entre 12 et 20 et
    type de course 3 pour tiercé, 4 pour quarté ou 5 pour quinté
    """
    horse_number = int(input("Combien de chevaux participent à la course? (Entre 12 et 20 chevaux) "))

    while horse_number < 12 or horse_number > 20:
        print("Une course comporte entre 12 et 20 chevaux.")
        horse_number = int(input("Combien de chevaux participent à la course?"))

    race_category = int(input("Choisissez un type de course? 3(Tiercé), 4(Quarté), 5(Quinté) "))
    while race_category not in (3, 4, 5):
        print("Choisissez 3,4 ou 5 pour le type de course.")
        race_category = int(input("Choisissez un type de course? 3(Tiercé), 4(Quarté), 5(Quinté) "))

    return horse_number, race_category


def create_horses(horse_number):
    """
    Crée une liste de chevaux en fonction du nombre de chevaux participant à la course
    :param horse_number: Nombre de chevaux participant à la course
    :return: Liste de chevaux, un dictionnaire pour chaque cheval avec ses informations
    """
    horses_list = []
    for n in range(horse_number):
        racehorse = {
            "numéro": n + 1,
            "vitesse": 0,
            "distance": 0,
            "disqualified": False,
            "finished": False,
            "arrival_round": None
        }
        horses_list.append(racehorse)
    return horses_list


def roll_dice():
    """
    simule un lancer de dé
    :return: Chiffre entre 1 et 6
    """
    die_nbr = random.randint(1, 6)
    return die_nbr


speed_changes = [
    [0, 1, 1, 1, 2, 2],  # vitesse à 0
    [0, 0, 1, 1, 1, 2],  # vitesse à 1
    [0, 0, 1, 1, 1, 2],  # vitesse à 2
    [-1, 0, 0, 1, 1, 1],  # vitesse à 3
    [-1, 0, 0, 1, 1, 1],  # vitesse à 4
    [-2, -1, 0, 0, 0, 1],  # vitesse à 5
    [-2, -1, 0, 0, 0, "DQ"]  # vitesse à 6
    ]


def calculate_new_speed(die_nbr, racehorse):
    """
    Calcule la nouvelle vitesse du cheval en fonction du chiffre obtenu au lancer de dé
    :param die_nbr: Chiffre entre 1 et 6
    :param racehorse: Dictionnaire du cheval
    :return: Vitesse du cheval
    """
    actual_speed = racehorse["vitesse"]
    change = speed_changes[actual_speed][die_nbr - 1]
    if change == "DQ":
        racehorse["disqualified"] = True
        return actual_speed

    actual_speed += change
    racehorse["vitesse"] = actual_speed
    return actual_speed


distance = [0, 23, 46, 69, 92, 115, 138]  # Distance parcourue en fonction de la vitesse 0,1,2,3,4,5,6


def calculate_distance(actual_speed):
    """
    Calcule la distance parcourue en fonction de la vitesse du cheval
    :param actual_speed: Vitesse du cheval
    :return: Distance parcourue
    """
    distance_covered = distance[actual_speed]
    return distance_covered


def is_end_game(horses_list):
    """
    Vérifie si la course est terminée, c'est-à-dire si tous les chevaux sont arrivés ou disqualifiés
    :param horses_list: Liste des chevaux
    :return: False si course pas terminée et True si course terminée
    """
    for racehorse in horses_list:
        if not (racehorse["disqualified"]) and not racehorse["finished"]:
            return False

    print("Course terminée")
    return True


def display_winner(horses_list, race_category):
    """
    Trie la liste des chevaux en fonction du tour d'arrivée et de la distance parcourue
    :param horses_list: Liste des chevaux
    :param race_category: Type de course
    :return: Retourne la liste des chevaux triée,
    uniquement les 3, 4 ou 5 premiers en fonction du type de course
    """
    sorted_horses = sorted(
        [racehorse for racehorse in horses_list if not racehorse["disqualified"]],
        key=lambda racehorse: (racehorse["arrival_round"], -racehorse["distance"]),
    )
    # permet de trier liste en fonction du tour d'arrivée et
    # de la distance mis en négatif pour avoir ordre inverse (décroissant)
    return sorted_horses[:race_category]
    # race_type ne contenant que 3, 4, 5, permet de retourner podium en fonction du type de course


def calculate_time(time):
    """
    Convertit secondes en minutes et secondes
    :param time: Temps en secondes
    :return: Retourne les minutes et les secondes
    """
    minutes = time // 60
    seconds = time % 60
    return minutes, seconds


if __name__ == "__main__":
    horse_nbr, race_type = ask_user()
    horses = create_horses(horse_nbr)

    turn = 0

    while not is_end_game(horses):
        turn += 1
        passed_time = turn * 10
        convert_time = calculate_time(passed_time)
        print(f"Tour : {turn}, Temps écoulé = {convert_time[0]} minutes {convert_time[1]} secondes")

        for horse in horses:
            if horse["disqualified"] or horse["finished"]:
                continue
            dice_nbr = roll_dice()
            new_speed = calculate_new_speed(dice_nbr, horse)
            distance_traveled = calculate_distance(new_speed)
            horse["distance"] += distance_traveled
            if horse["distance"] > 2400:
                horse["finished"] = True
                horse["arrival_round"] = turn
            print(
                f"Cheval {horse['numéro']} : "
                f"vitesse = {horse['vitesse']}, "
                f"distance parcourue = {horse['distance']}m, "
                f"disqualifié = {horse['disqualified']}, "
                f"arrivé = {horse['finished']}"
            )

    print(f"La course s'est terminée en {turn} tours.")

    podium = display_winner(horses, race_type)

    print(f"Les {race_type} premiers sont :")
    for place, horse in enumerate(podium, start=1):  # enumerate permet d'obtenir l'indice, mais en commençant à 1
        arrival_time = horse["arrival_round"] * 10
        arrival_time_converted = calculate_time(arrival_time)
        print(
            f"En position {place} : Cheval {horse['numéro']} "
            f"en {horse['arrival_round']} tours "
            f"en {arrival_time_converted[0]} minutes et {arrival_time_converted[1]} secondes "
            f"avec une distance de {horse['distance']}. "
        )

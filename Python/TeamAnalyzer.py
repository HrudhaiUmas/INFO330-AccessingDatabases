import sqlite3  # This is the package for all sqlite3 access in Python
import sys  # This helps with command-line parameters

connection = sqlite3.connect('pokemon.sqlite')
cursor = connection.cursor()

# All the "against" column suffixes:
types = ["bug", "dark", "dragon", "electric", "fairy", "fight",
         "fire", "flying", "ghost", "grass", "ground", "ice", "normal",
         "poison", "psychic", "rock", "steel", "water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    # Getting pokemon name based on the pokedex number that is passed in the terminal.
    # EXTRA CREDIT: FLEXIBLE INPUT: Accepts either Pokedex numbers or Pokemon names at the command line
    if arg.isdigit():
        getName = """SELECT name FROM pokemon WHERE pokedex_number = """ + arg + """;"""
        cursor.execute(getName)
        result = cursor.fetchone()
    else:
        result = [arg]

    # If the pokemon exists, starts analyzing and prints the name of the pokemon.
    if result is not None:
        pokemon_name = result[0]
        print("Analyzing", i)
        print(pokemon_name, end=" ")
    else:
        print("Pokemon not found!")
        continue

    # Getting pokemon type1 based on the pokemon name.
    getType1 = """SELECT type1 FROM pokemon_types_view WHERE name='""" + pokemon_name + """';"""
    cursor.execute(getType1)
    typeCounts = cursor.fetchone()

    # If the pokemon type1 exists, type1 is printed.
    if typeCounts is not None:
        pokemon_type1 = typeCounts[0]
        print("(" + pokemon_type1, end="")
    else:
        print("Pokemon type 1 not found!")
        continue

    # Getting pokemon type2 based on the pokemon name.
    getType2 = """SELECT type2 FROM pokemon_types_view WHERE name='""" + pokemon_name + """';"""
    cursor.execute(getType2)
    type2Counts = cursor.fetchone()

    # If the pokemon type2 exists, type2 is printed.
    if type2Counts is not None:
        pokemon_type2 = type2Counts[0]
        print(" " + pokemon_type2 + ")", end="")
    else:
        print(")", end="")

    # Getting the pokemon against_NNN stats based on the pokemon types.
    getTypeStats = """SELECT against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM pokemon_types_battle_view WHERE type1name = '""" + pokemon_type1 + """' AND type2name = '""" + pokemon_type2 + """';"""
    cursor.execute(getTypeStats)
    typeStats = cursor.fetchone()

    # Checking which types are "good" and "bad" against another type.
    if typeStats is not None:
        pokemon_against_stats = typeStats
        strong_against = []
        weak_against = []
        for indexOfAgainst_NNN, nameOfAgainst in enumerate(types):
            if pokemon_against_stats[indexOfAgainst_NNN] > 1:
                strong_against.append(nameOfAgainst)
            elif pokemon_against_stats[indexOfAgainst_NNN] < 1:
                weak_against.append(nameOfAgainst)
        print(" is strong against", strong_against, "but weak against", weak_against)
    else:
        print("Pokemon stats not found!")
        continue

# Close the connection.
connection.close()

# Option to save the team.
answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")


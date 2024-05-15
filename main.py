import csv
from random import randint

from colorama import Back, Fore, Style, init  #package for colored text in terminal

init(autoreset=True)  #resets Colorama between each line

with open('Pokemon.csv', 'r') as pokedex:
  reader = csv.reader(pokedex)

  #header formatting
  def header():
    row = Fore.WHITE + Back.BLACK + Style.BRIGHT + "\n"
    row += f"{'NO':6}"
    row += f"{'NAME':28}"
    row += f"{'TYPE 1':11}"
    row += f"{'TYPE 2':11}"
    row += f"{'TOTAL':8}"
    row += f"{'HP':6}"
    row += f"{'ATTACK':9}"
    row += f"{'DEFENSE':10}"
    row += f"{'SP. ATK':10}"
    row += f"{'SP. DEF':10}"
    row += f"{'SPEED':8}"
    row += f"{'GENERATION':13}"
    row += f"{'LEGENDARY':9}"
    return row

  #table formatting
  def formatting(r):
    row = ''
    row += f'{r[0]:6}'
    row += f'{r[1]:28}'
    row += f'{r[2]:11}'
    row += f'{r[3]:11}'
    row += f'{r[4]:8}'
    row += f'{r[5]:6}'
    row += f'{r[6]:9}'
    row += f'{r[7]:10}'
    row += f'{r[8]:10}'
    row += f'{r[9]:10}'
    row += f'{r[10]:8}'
    row += f'{r[11]:13}'
    row += f'{r[12]:9}'
    return (row)

  #error message formatting
  def errorf(message):
    return Fore.RED + Back.BLACK + Style.BRIGHT + message

  types = [
      "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison",
      "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark",
      "Steel", "Fairy", "Normal", ""
  ]  #list of all types including an option for blank

  #-------------------------------------------

  #Display entries until specified threshold
  def display_until(threshold):
    if threshold < 1 or threshold > 800:
      print(
          errorf(
              '\nInvalid threshold. Try entering a number between 1 and 800.'))
    else:
      print(header())
      rowtotal = 0
      pokedex.seek(0)
      for r in reader:
        print(formatting(r))
        rowtotal += 1
        if rowtotal == threshold:
          break

  #Display first entry with specified type
  def display_type(type):
    print(header())
    pokedex.seek(0)
    for r in reader:
      if r[2] == type or r[3] == type:
        print(formatting(r))
        break

  #Display entries with specified total base stat
  def display_totalstat(total):
    total = int(total)

    found = False
    print_header = False

    pokedex.seek(0)
    for r in reader:
      if int(r[4]) == total:
        if not print_header:
          print(header())
          print_header = True

        print(formatting(r))
        found = True
    if not found:
      print(errorf(f'\nNo Pokemon found with a total base stat of {total}'))

  #Display entries that satisfy minimum stat requirements, able to specify one or more stats at a time
  def display_minstat(min_hp, min_atk, min_def, min_spatk, min_spdef,
                      min_speed):

    print_header = False
    found = False

    pokedex.seek(0)
    for r in reader:

      if int(r[5]) >= min_hp and int(r[6]) >= min_atk and int(
          r[7]) >= min_def and int(r[8]) >= min_spatk and int(
              r[9]) >= min_spdef and int(r[10]) >= min_speed:

        if not print_header:
          print(header())
          print_header = True

        print(formatting(r))
        found = True

    if not found:
      print(errorf("\nNo Pokemon found with the minimum required base stats."))

  #Display legendaries with specified types
  def display_legendary(type1, type2):
    print_header = False
    found_pokemon = False

    pokedex.seek(0)
    for r in reader:

      #scenario for when the first type is left blank
      if type1 == "":
        if (r[2] == type2 or r[3] == type2) and r[12] == "TRUE":
          if not print_header:
            print(header())
            print_header = True

          print(formatting(r))
          found_pokemon = True

      #scenario for when the second type is left blank
      elif type2 == "":
        if (r[2] == type1 or r[3] == type1) and r[12] == "TRUE":
          if not print_header:
            print(header())
            print_header = True

          print(formatting(r))
          found_pokemon = True

      #scenario for when both types are specified
      elif ((r[2] == type1 and r[3] == type2) or
            (r[2] == type2 and r[3] == type1)) and r[12] == 'TRUE':

        if not print_header:
          print(header())
          print_header = True

        print(formatting(r))
        found_pokemon = True

    if not found_pokemon:
      print(errorf("\nNo legendaries found"))

  #Return a random entry
  def random_entry(reader):
    randrow = randint(1, 800)
    pokedex.seek(0)
    for i, row in enumerate(reader):
      if i == randrow - 1:
        return row

#-----------------------------------------------------------------

#welcome message

  print(Fore.WHITE + Back.BLACK + Style.BRIGHT + '''
__________         __           ________                    
\\______   \\ ____  |  | __  ____ \\____   \\    ____  ___  ___ 
 |   ____/ / __ \\ |  |/ /_/ __ \\ |   \\   \\ _/ __ \\ \\  \\/  / 
 |   |    | |__| ||    ( \\  ___/ |  __\\   \\\\  ___/ /     /  
 |___|     \\____/ |__|__\\ \\____/ \\________/ \\____//__/\\__\\  
''')

  #mainloop
  running = True

  while running:

    #main menu
    print(Fore.WHITE + Back.BLACK + Style.BRIGHT + "\nMAIN MENU")
    print('''
1. Display selected number of Pokemon with their types and statistics
2. Display the first Pokemon of a Type of the trainer’s choice
3. Display all Pokemon with Total Base stat of the trainer’s choice
4. Display all Pokemon with a minimum set of stats
5. Display all legendary Pokemon of Types of the trainer’s choice
6. Display a random Pokemon
7. Who's That Pokemon?''')
    print(Fore.RED + '8. Quit')

    #prompts
    choice = input(Style.BRIGHT + '\nEnter choice: ')
    if choice == '1':
      try:
        threshold = int(input(Style.NORMAL + '\nEnter threshold: '))
        display_until(threshold)
      except ValueError:
        print(errorf("\nInvalid threshold. Please enter a valid integer."))

    elif choice == '2':
      type = input('\nEnter type: ').capitalize()
      if type not in types or type == "":
        print(errorf("\nInvalid type"))
      else:
        display_type(type)

    elif choice == '3':
      total = input('\nEnter total base stat: ')
      if total.isdigit():
        display_totalstat(total)
      else:
        print(
            errorf(
                "\nInvalid total base stat, try entering a valid positive integer"
            ))

    elif choice == '4':
      min_hp, min_atk, min_def, min_spatk, min_spdef, min_speed = 0, 0, 0, 0, 0, 0  #sets default min stats to 0
      choosing = True
      while choosing:
        print(Fore.WHITE + Back.BLACK + Style.BRIGHT + "\nSTATS")
        print('''
1. HP
2. Attack
3. Defense
4. Special Attack
5. Special Defense
6. Speed''')
        print(Fore.RED + "7. Exit")
        choice = input('\nEnter choice: ')
        try:
          if choice == '1':
            min_hp = int(input('\nEnter minimum HP: '))
            print(f"Minimum HP set to {min_hp}")
            display_minstat(min_hp, min_atk, min_def, min_spatk, min_spdef,
                            min_speed)
          elif choice == '2':
            min_atk = int(input('\nEnter minimum Attack: '))
            print(f"Minimum Attack set to {min_atk}")
            display_minstat(min_hp, min_atk, min_def, min_spatk, min_spdef,
                            min_speed)
          elif choice == '3':
            min_def = int(input('\nEnter minimum Defense: '))
            print(f"Minimum Defense set to {min_def}")
            display_minstat(min_hp, min_atk, min_def, min_spatk, min_spdef,
                            min_speed)
          elif choice == '4':
            min_spatk = int(input('\nEnter minimum Special Attack: '))
            print(f"Minimum Special Attack set to {min_spatk}")
            display_minstat(min_hp, min_atk, min_def, min_spatk, min_spdef,
                            min_speed)
          elif choice == '5':
            min_spdef = int(input('\nEnter minimum Special Defense: '))
            print(f"Minimum Special Defense set to {min_spdef}")
            display_minstat(min_hp, min_atk, min_def, min_spatk, min_spdef,
                            min_speed)
          elif choice == '6':
            min_speed = int(input('\nEnter minimum Speed: '))
            print(f"Minimum Speed set to {min_speed}")
            display_minstat(min_hp, min_atk, min_def, min_spatk, min_spdef,
                            min_speed)
          elif choice == '7':
            choosing = False
          else:
            print(
                errorf(
                    '\nInvalid choice, please enter an integer from 1 to 7'))

        except ValueError:
          print(errorf('\nInvalid input'))

    elif choice == '5':
      type1 = input('\nEnter type 1: ').capitalize()
      type2 = input('\nEnter type 2: ').capitalize()
      if type1 in types and type2 in types:
        display_legendary(type1, type2)
      else:
        print(errorf("\nInvalid type(s)"))

    elif choice == '6':
      print(header())
      print(formatting(random_entry(reader)))

    elif choice == '7':
      print(Style.NORMAL)
      print('''Congratulations, you have found the Pokemon Guessing Game!
A random Pokemon will be selected. You will have 5 tries to guess this Pokemon
Each wrong guess will reveal a hint that may help you guess correctly.''')

      answer = random_entry(reader)
      guessed = False
      count = 0
      if answer is not None:
        print(Fore.YELLOW + Back.BLACK + Style.BRIGHT +
              f"\nHint #1: Generation {answer[11]}")
        while not guessed:
          print(Fore.WHITE + Back.BLACK + Style.BRIGHT +
                f"\nGuess #{count + 1}")
          print(Fore.BLUE + "Who's That Pokemon?")
          guess = input().capitalize()
          if guess == "":
            print(
                errorf(
                    "\nPlease enter the name of a Pokemon in the space below.")
            )
          else:
            if guess == answer[1]:
              print(Fore.GREEN + Back.BLACK + Style.BRIGHT +
                    f"\n...it's {answer[1]}!")
              guessed = True
            else:
              print(errorf(f"\n{guess} is incorrect"))
              count += 1
              if count == 1:
                print(Fore.YELLOW + Back.BLACK + Style.BRIGHT +
                      f"Hint #2: Legendary Pokemon: {answer[12].capitalize()}")
              elif count == 2:
                print(Fore.YELLOW + Back.BLACK + Style.BRIGHT +
                      f"Hint #3: The Pokemon's Type 1 is {answer[2]}")
              elif count == 3:
                print(
                    Fore.YELLOW + Back.BLACK + Style.BRIGHT +
                    f"Hint #4: The first letter of its name is {answer[1][0]}")
              elif count == 4:
                print(
                    Fore.YELLOW + Back.BLACK + Style.BRIGHT +
                    f"Hint #5: The length of its name is {len(answer[1])} characters"
                )
              else:
                print(Fore.RED + Back.BLACK + Style.BRIGHT +
                      f"Too bad, the answer was {answer[1]}")
                guessed = True

    elif choice == '8':
      print(Fore.GREEN + Back.BLACK + Style.BRIGHT + '\nSee you next time')
      running = False
    else:
      print(errorf('\n' + str(choice) + ' is not a valid choice.'))

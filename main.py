################################################################################
# Written by Daniel Narciso                                                    #
# 06/05/2018                                                                   #
# Version 1.0                                                                  #
################################################################################

import sys
import requests
import csv
import re #regular expressions
from bs4 import BeautifulSoup
import numpy as np

def howmany(rolls, target):
    i = 0
    for roll in rolls:
        if roll >= target:
            i = i + 1
    return i

def scrape_data(monster, n, attack, AC):
    #url = f"https://roll20.net/compendium/dnd5e/Monsters:{monster}"
    url = "https://roll20.net/compendium/dnd5e/Monsters:%s" %monster
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    alldiv = soup.findAll('div')
    stralldiv = str(alldiv)
    start = stralldiv.find('data-pageid')

    id_begin = start + 13
    id_end = start + 18

    mon_id = stralldiv[int(id_begin):int(id_end)]

    rolls = np.random.randint(1,21,int(n)) #nd20 roll
    if attack == 'ranged':
        monster_tag = soup.find('div', attrs={'data-pageid': mon_id})
        monster_ranged = monster_tag.text.split("Ranged Weapon Attack: +")[1].strip()
        monst_ranged_bonus = int(monster_ranged[0])
        rolls = rolls + monst_ranged_bonus
    elif attack == 'melee':
        monster_tag = soup.find('div', attrs={'data-pageid': mon_id})
        monster_melee = monster_tag.text.split("Melee Weapon Attack: +")[1].strip()
        monst_melee_bonus = int(monster_melee[0])
        rolls = rolls + monst_melee_bonus
    else:
        rolls = rolls

    rolls_list = list(rolls)

    hits = howmany(rolls,AC)

    result_dict = {"Hits: ": hits, "Rolls: ": rolls_list}

    return result_dict

if __name__=='__main__':
    while True:
        try:
            monster = raw_input("Monster: ")
            n = raw_input("How many? ")
            attack = raw_input("Ranged or Melee? ")
            AC = raw_input("Defender AC (0 if N/A)? ")

            answer = scrape_data(monster,n,attack,AC)
            print(answer)
            print(' ')

            again = raw_input('Again? (y/n) ')
            if again.upper() == 'Y':
                print('')
                continue
            if again.upper() not in ('Y', 'N'):
                print("Nice try bro.")
                continue
            if again.upper() == 'N':
                print("Later.")
                break
            else:
                continue
        except:
            print('')
            print("Something wasn't right.")
            print('')

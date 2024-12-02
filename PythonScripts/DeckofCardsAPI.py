##########################################################################################################################
# Script Name: DeckofCards
# Author: Joe Smith
# Date: 2021-10-10
# Description: This script utilizes the deck of cards API. this was some fun script i made when i was learning to play with APIs
##########################################################################################################################

import requests
import json

deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1").json()

deckId = deck['deck_id']

deckId = "https://deckofcardsapi.com/api/deck/" + deckId + "/draw/?count=5"

whileTrue = True

i = 1


hand = requests.get(deckId).json()

# if hand['remaining'] > 40:
#     print(hand['remaining'])


while whileTrue == True:

    if hand['remaining'] == 0:
        whileTrue = False

    print("This is hand " + str(i))
    print()

    for hands in hand['cards']:
        print(hands['value'] + " of " + hands['suit'])
        
    print()

    i += 1
    hand = requests.get(deckId).json()


    
    
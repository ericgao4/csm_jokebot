import csv
import sys
import json
import time
import requests

# I would like to thank the VPN Betternet for making this project possible as I had
# had to code this bot in China where the Great FireWall tried everything in its power
# to end my productivity.
# Betternet > China FireWall

# Takes in prompt (String) and punchline (String)
# Prints prompt, waits 2 seconds, then prints punchline
# Returns null/None


def deliver_joke(prompt, punchline):
    print(prompt)
    time.sleep(2)
    print(punchline)

# Reads user input
# return True if input is string "next"
# return False if input is "quit"
# if user input is anything else, print error message:
# "I don't understand" and then wait for more user input


def check_user_input():
    user_input = input()
    if user_input == "next":
        return True
    elif user_input == "quit":
        return False
    else:
        print("I don't understand")
        return check_user_input()

# Reads jokes in form of prompt,punchline from a csv file
# Returns a list of these jokes in form [[prompt, punchline]]
# filename must contain .csv, ex: jokes.csv


def read_jokes_from_csv(filename):
    if ".csv" not in filename:
        print("Error: Please make sure to include .csv in filename")
        return []
    try:
        csvfile = open(filename)
    except IOError:
        print("Error: File could no be opened")
    # csvreader returns [prompt, punchline] after each iteration
    csvreader = csv.reader(csvfile)
    joke_list = []
    for row in csvreader:
        joke_list = joke_list + [row]
    return joke_list

# Gets a list of Reddit posts from /r/dadjokes
# Returns this list in the same format as csv funct


def read_jokes_from_reddit():
    req = requests.get('https://www.reddit.com/r/dadjokes.json', headers={'User-agent': 'your bot 0.1'})
    if not req.status_code == requests.codes.ok:
        print("Bad HTTPS Request" + str(req.status_code))
    else:
        try:
            dic_data = req.json()
            posts = dic_data['data']['children']
            joke_list = []
            for post in posts:
                not_suitable = post['data']['over_18']
                is_question = post['data']['title'].startswith(('Why', 'What', 'How'))
                if not not_suitable and is_question:
                    title = post['data']['title']
                    body = post['data']['selftext']
                    joke_list = joke_list + [[title, body]]
            return joke_list
        except ValueError:
            print("Https Response to Reddit's /r/dadjokes contains invalid JSON")

# Main function for jokebot procedure
# Checks how many arguments were given to the bot.


def main(args):
    if len(args) == 1:
        joke_list = read_jokes_from_reddit()
    elif len(args) == 2:
        joke_list = read_jokes_from_csv(args[1])
    else:
        print("Error: Too many arguments, Please type the name of the csv file containing jokes "
              "followed by .csv or no arguements for some dad jokes from reddit's /r/dadjokes")
        return
    row_number = 0
    for joke_row in joke_list:
        prompt = joke_row[0]
        punchline = joke_row[1]
        deliver_joke(prompt, punchline)
        row_number += 1
        if row_number == len(joke_list) or not check_user_input():
                break


if __name__ == "__main__":
    main(sys.argv)


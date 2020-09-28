import sys
from argparse import ArgumentParser

import markovify
import pandas as pd
import twint


def build_model(username, limit):
    c = twint.Config()
    c.Username = username
    c.Store_csv = True
    c.Limit = limit
    c.Output = "data"
    twint.run.Search(c)
    print("Model created.")


def generate_tweet():
    try:
        data = pd.read_csv("data/tweets.csv")
    except FileNotFoundError:
        sys.exit("Data model not found. Run python generator.py --build-model username")
    text_model = markovify.NewlineText(data.tweet, state_size=2)
    print(text_model.make_short_sentence(max_chars=180))


if __name__ == "__main__":
    parser = ArgumentParser(prog="tweet-generator")
    parser.add_argument(
        "--build-model",
        help="Pass this flag to generate a new data model.",
        dest="build_model",
        action="store_true",
    )
    parser.add_argument(
        "--generate-tweet",
        help="Pass this flag to generate a new tweet.",
        dest="tweet",
        action="store_true",
    )
    parser.add_argument(
        "username", help="The username to generate tweets for.", nargs="?",
    )
    parser.add_argument(
        "--limit",
        help="The number of tweets to scrape. Default is 1000.",
        nargs="?",
        default=1000,
    )
    args = parser.parse_args()

    if args.build_model:
        if not args.username:
            sys.exit(
                "Username not found. Run python generator.py --build-model username"
            )
        else:
            build_model(args.username, args.limit)

    if args.tweet:
        generate_tweet()

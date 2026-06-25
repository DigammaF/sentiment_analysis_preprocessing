
import csv
import string
import statistics

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from dataclasses import dataclass, field

STOP_WORDS = set(stopwords.words('english'))

ROWS = (
    "Year", "Month", "Day", "Time of Tweet", "text", "sentiment", "Platform"
)
TEXT_INDEX = ROWS.index("text")
SENTIMENT_INDEX = ROWS.index("sentiment")

SENTIMENT_CODE: dict[str, int] = {
    "positive": 1, "negative": -1,
    "neutral": 0
}

WORDS: set[str] = set()

def main():
    pure_texts: list[str] = []
    sentiments: dict[str, str] = {}

    with open("sentiment_analysis.csv", "r", newline="") as input_file:
        with open("sentiment.csv", "w", newline="") as output_file:
            reader = csv.reader(input_file, delimiter=",")
            writer = csv.writer(output_file, delimiter=",")

            next(reader)

            for row in reader:
                text = row[TEXT_INDEX]
                sentiment = row[SENTIMENT_INDEX]
                pure_text = "".join(tuple(c if c in string.ascii_lowercase else " " for c in text.lower()))
                words = word_tokenize(pure_text.lower())
                words = [word for word in words if word not in STOP_WORDS]

                if not words:
                    continue

                pure_text = " ".join(words)
                pure_texts.append(pure_text)
                sentiments[pure_text] = sentiment

                for word in words:
                    WORDS.add(word)

            WORDS_TUPLE = list(WORDS)
            WORDS_TUPLE.sort()
            WORDS_TUPLE = tuple(WORDS_TUPLE)

            writer.writerow(
                (
                    "word_count", "average_word_length", "median_word_length"
                ) + WORDS_TUPLE + ("sentiment",)
            )

            print("---")

            for pure_text in pure_texts:
                words = pure_text.split()
                word_lengths = tuple(len(word) for word in words)

                average_word_length = sum(word_lengths) / len(words)
                median_word_length = statistics.median(word_lengths)
                word_count = tuple(
                    words.count(word)
                    for word in WORDS_TUPLE
                )
                writer.writerow(
                    (
                        len(words), average_word_length, median_word_length,
                    ) + word_count + (SENTIMENT_CODE[sentiments[pure_text]],)
                )

if __name__ == "__main__":
    main()

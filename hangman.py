import random

WORD_BANK = {
    "Fruits": (
        "mango", "orange", "papaya", "grape", "lychee", "rambutan",
        "pineapple", "watermelon", "strawberry", "blueberry", "kiwi", "pomegranate"
    ),
    "Animals": (
        "zebra", "giraffe", "panda", "kangaroo","cheetah", 
        "leopard", "rhinoceros", "crocodile"
    ),
    "City": (
        "london", "madrid", "mumbai", "paris", "tokyo", "bangkok",
        "newyork", "berlin", "moscow", "dubai", "singapore", "toronto"
    ),
    "Countries": (
         "brazil", "germany", "france","malaysia","argentina",
        "australia", "egypt", "russia", "china", "spain","morocco"
    ),

    "Birds": (
        "sparrow", "peacock", "pigeon", "flamingo",
        "penguin", "ostrich", "swan", "crow", "falcon", "woodpecker"
    ),
}


def choose_word():
    category = random.choice(list(WORD_BANK.keys()))
    word = random.choice(WORD_BANK[category])
    return category, word


def display_word(word, guessed_letters):
    display_chars = []
    for letter in word:
        if letter in guessed_letters:
            display_chars.append(letter)
        else:
            display_chars.append('_')
    return ' '.join(display_chars)


def is_word_complete(word, guessed_letters):
    for letter in word:
        if letter not in guessed_letters:
            return False
    return True


def play_hangman():
    print("")
    print("WELCOME TO HANGMAN")
    print("")

    category, word = choose_word()
    max_tries = len(word) + 3      # total tries = word length + 3
    tries_left = max_tries
    guessed_letters = set()
    wrong_letters = set()

    print(f"\nCategory: {category}")
    print(f"The word has {len(word)} letters.")
    print(f"You have {max_tries} total tries (word length + 3).\n")

    while tries_left > 0:
        print(f"Category: {category}")
        print("Word: " + display_word(word, guessed_letters))
        print(f"Tries left: {tries_left}")
        if wrong_letters:
            print("Wrong guesses :", ', '.join(sorted(wrong_letters)))

        guess = input("\nGuess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.\n")
            continue

        if guess in guessed_letters or guess in wrong_letters:
            print("You already guessed that letter. Try another.\n")
            continue

        if guess in word:
            guessed_letters.add(guess)
            print(f"Good guess! '{guess}' is in the word.\n")
        else:
            wrong_letters.add(guess)
            tries_left -= 1
            print(f"Wrong! '{guess}' is not in the word.\n")

        if is_word_complete(word, guessed_letters):
            print("")
            print(f"YOU WIN! The word was: {word.upper()}")
            print("")
            return

    print("")
    print("GAME OVER! You ran out of tries.")
    print(f"The word was: {word.upper()}")
    print("")


def main():
    play_again = 'y'
    while play_again == 'y':
        play_hangman()
        play_again = input("\nPlay again? (y/n): ").strip().lower()
    print("\nBye :)")


if __name__ == "__main__":
    main()


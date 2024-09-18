import random

def display_word_state(word, guessed_letters):
    """Display the current state of the word with guessed letters and blanks."""
    return ''.join([letter if letter in guessed_letters else '_' for letter in word])

def hangman(words, max_guesses):
    """Main hangman game logic."""
    word = random.choice(words).lower()
    guessed_letters = set()
    attempts_left = max_guesses + len(word)  
    
    print(f"The word has {len(word)} letters.")
    
    while attempts_left > 0:
        print(f"\nWord: {display_word_state(word, guessed_letters)}")
        print(f"Guesses left: {attempts_left}")
        
        guess = input("Enter a letter: ").lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input! Please enter a single alphabetic character.")
            continue
        
        if guess in guessed_letters:
            print("You already guessed that letter! Try a different one.")
            continue
        
        guessed_letters.add(guess)
        
        if guess in word:
            print("Good guess!")
        else:
            print(f"Wrong guess! '{guess}' is not in the word.")
            attempts_left -= 1
        
        # Check if the user has guessed the entire word
        if set(word) <= guessed_letters:
            print(f"Congratulations! You guessed the word: {word}")
            return
    
    print(f"YOU FAILED! The word was: {word}")

def main():
    input_words = input("Input the words you would like to guess, separated by commas: ")
    words = [word.strip().lower() for word in input_words.split(",")]
    print(words)
    try:
        guess_amount = int(input("Enter the base number of guesses you'd like (this scales with word length): "))
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        return
    
    if guess_amount <= 0:
        print("You need to have at least 1 guess!")
        return
    
    hangman(words, guess_amount)

if __name__ == "__main__":
    while True:
        main()
        play_again = input("Would you like to play again? (yes/no): ").lower()
        if play_again != 'yes':
            break

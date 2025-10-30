import json
import random

def _load_words():
    try:
        with open("words.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_words(data):
    with open("words.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_word():
    word = input("Enter a word to add: ").strip()
    if not word:
        print("No word entered.")
        return
    definition = input("Enter its definition: ").strip()
    data = _load_words()

    if any(item.get("word", "").lower() == word.lower() for item in data):
        print(f'Word "{word}" already exists in words.json')
        return

    data.append({"word": word, "definition": definition})
    _save_words(data)
    print(f'Word "{word}" added to words.json')

def remove_word():
    word = input("Enter a word to remove: ").strip()
    if not word:
        print("No word entered.")
        return
    data = _load_words()
    new_data = [item for item in data if item.get("word", "").lower() != word.lower()]

    if len(new_data) == len(data):
        print(f'Word "{word}" not found in words.json')
        return

    _save_words(new_data)
    print(f'Word "{word}" removed from words.json')

def view_words():
    data = _load_words()
    if not data:
        print("No words in words.json")
        return
    for item in data:
        print(f'{item.get("word", "")} - {item.get("definition", "")}')

def flashcards():
    data = _load_words()
    if not data:
        print("No words in words.json to practice.")
        return
    for item in data:
        input(item.get("definition", ""))
        print(f'   - {item.get("word", "")}')

def practice_words():

    data = _load_words()
    if not data:
        print("No words in words.json to practice.")
        return

    queue = list(data)
    attempts = {}

    while queue:
        random.shuffle(queue)
        next_queue = []
        for item in queue:
            word = item.get("word", "")
            definition = item.get("definition", "")
            attempts[word] = attempts.get(word, 0) + 1

            answer = input(f'What is the word for: "{definition}"? ').strip()
            if answer.lower() == word.lower():
                print("Correct!")
            else:
                print(f'Incorrect! The correct word is: "{word}"')
                next_queue.append(item)

        if next_queue:
            print(f'\nRepeating {len(next_queue)} word(s) you got wrong...\n')
        queue = next_queue

    print("\nAll done! Summary of attempts:")
    for w, cnt in attempts.items():
        print(f'  {w}: {cnt} attempt(s)')

def quiz():
    data = _load_words()
    if not data:
        print("No words in words.json to practice.")
        return

    questions = random.sample(data, len(data))
    score = 0

    for idx, item in enumerate(questions, start=1):
        correct_word = item.get("word", "")
        definition = item.get("definition", "")

        num_choices = min(4, len(data))
        pool = [d for d in data if d.get("word", "").lower() != correct_word.lower()]
        distractors = random.sample(pool, num_choices - 1) if pool else []
        options = [correct_word] + [d.get("word", "") for d in distractors]
        random.shuffle(options)

        print(f'\nQuestion {idx}/{len(questions)}:')
        print(f'What is the word for: "{definition}"?')
        for i, opt in enumerate(options, start=1):
            print(f'  {i}. {opt}')

        choice = input(f'Enter choice (1-{len(options)}) or type the word: ').strip()
        selected = None
        if choice.isdigit():
            n = int(choice)
            if 1 <= n <= len(options):
                selected = options[n - 1]
        else:
            selected = choice

        if selected is None:
            print("Invalid choice. Marked as incorrect.")
            print(f'Incorrect! The correct word is: "{correct_word}"')
            continue

        if selected.lower().strip() == correct_word.lower():
            print("Correct!")
            score += 1
        else:
            print(f'Incorrect! The correct word is: "{correct_word}"')

    print(f"\nQuiz finished. Score: {score}/{len(questions)}")


if __name__ == "__main__":
    print("Welcome to FlashLearn!\n")
    print("Choose an option:")
    print("1. Add a word")
    print("2. Remove a word")
    print("3. View all words")
    print("4. Flashcards")
    print("5. Practice words")
    print("6. Quiz")
    choice = input("Enter your choice (1-6): ").strip()
    if choice == "1":
        add_word()
    elif choice == "2":
        remove_word()
    elif choice == "3":
        view_words()
    elif choice == "4":
        flashcards()
    elif choice == "5":
        practice_words()
    elif choice == "6":
        quiz()
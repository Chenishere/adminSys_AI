import json
from difflib import get_close_matches
import subprocess

def load_data_ai(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
        return data

def save_data_ai(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2) 

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, data_ai: dict) -> str | None: 
    for q in data_ai["questions"]:
        if q["questions"] == question:
            return q["answer"]
    return None

def execute_command(command: str):
    subprocess.run(command, shell=True)

def create_user(name: str):
    # Créer l'utilisateur
    subprocess.run(f'sudo useradd {name}', shell=True)

    # Afficher un message pour demander le mot de passe
    print(f"Please set a password for the user '{name}'")
    subprocess.run(f'sudo passwd {name}', shell=True)

def chat_bot():
    data_ai: dict = load_data_ai('data_ai.json')

    while True:
        user_input: str = input('Vous: ').strip()  # Strip leading and trailing whitespace
        
        if user_input.lower() == 'quit':
            break

        # Check if user input is empty or contains only whitespace
        if not user_input.strip():
            continue

        # Check if the user wants to create a user
        if "creer un user" in user_input.lower():
            # Ask for the username
            name = input("Entrez le nom de l'utilisateur à créer: ")
            create_user(name)
            print(f"L'utilisateur '{name}' a bien été créé.")
            continue
    
        best_match: str | None = find_best_match(user_input, [q["questions"] for q in data_ai["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, data_ai)
            print(f'Bot: {answer}')
            if answer:
                execute_command(answer)
        else:
            print(f'Bot: Je ne connais pas la réponse. Pouvez-vous m\'enseigner ?')
            new_answer: str = input('Tapez la réponse ou "skip" pour ignorer : ')

            if new_answer.lower() != 'skip':
                data_ai['questions'].append({"questions": user_input, "answer": new_answer})
                save_data_ai('data_ai.json', data_ai)
                print('Bot: Merci, j\'ai appris une nouvelle réponse !')

if __name__ == '__main__':
    chat_bot()

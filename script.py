import json
from difflib import get_close_matches
import subprocess

def load_data_ai(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

def save_data_ai(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list) -> str or None:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, data_ai: dict) -> str or None:
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

def delete_user(name: str, data_ai: dict):
    # Supprimer l'utilisateur
    subprocess.run(f'sudo userdel -r {name}', shell=True)
    print(f"L'utilisateur '{name}' a bien été supprimé.")
    # Ajouter la réponse dans le fichier JSON
    data_ai['questions'].append({"questions": f"supprime l'utilisateur {name}", "answer": f"L'utilisateur '{name}' a bien été supprimé."})
    save_data_ai('data_ai.json', data_ai)

def add_user_to_group(user: str, group: str, data_ai: dict):
    # Ajouter l'utilisateur au groupe
    subprocess.run(f'sudo usermod -aG {group} {user}', shell=True)
    print(f"L'utilisateur '{user}' a bien été ajouté au groupe '{group}'.")
    # Ajouter la réponse dans le fichier JSON
    data_ai['questions'].append({"questions": f"ajoute l'utilisateur {user} au groupe {group}", "answer": f"sudo usermod -aG {group} {user}"})
    save_data_ai('data_ai.json', data_ai)

def remove_user_from_group(user: str, group: str, data_ai: dict):
    # Retirer l'utilisateur du groupe
    subprocess.run(f'sudo deluser {user} {group}', shell=True)
    print(f"L'utilisateur '{user}' a bien été supprimé du groupe '{group}'.")
    # Ajouter la réponse dans le fichier JSON
    data_ai['questions'].append({"questions": f"supprime l'utilisateur {user} du groupe {group}", "answer": f"sudo deluser {user} {group}"})
    save_data_ai('data_ai.json', data_ai)

def create_group_with_permissions(permissions: str, data_ai: dict):
    # Créer le groupe avec les permissions spécifiées
    subprocess.run(f'sudo addgroup {permissions}', shell=True)
    print(f"Le groupe avec les permissions '{permissions}' a bien été créé.")
    # Ajouter la réponse dans le fichier JSON
    data_ai['questions'].append({"questions": f"crée un groupe avec certaines permissions", "answer": f"sudo addgroup {permissions}"})
    save_data_ai('data_ai.json', data_ai)

def chat_bot():
    data_ai = load_data_ai('data_ai.json')

    while True:
        user_input = input('Vous: ').strip()  # Strip leading and trailing whitespace

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

        # Check if the user wants to delete a user
        if "supprime un user" in user_input.lower():
            # Ask for the username to delete
            name = input("Quel utilisateur voulez-vous supprimer ? ")
            delete_user(name, data_ai)
            continue

        # Check if the user wants to add a user to a group
        if "ajoute un user au groupe" in user_input.lower():
            # Ask for the user and group names
            user = input("Quel utilisateur voulez-vous ajouter au groupe ? ")
            group = input("Dans quel groupe voulez-vous l'ajouter ? ")
            add_user_to_group(user, group, data_ai)
            continue

        # Check if the user wants to remove a user from a group
        if "supprime un user de son groupe" in user_input.lower():
            # Ask for the user and group names
            user = input("Quel utilisateur voulez-vous supprimer de son groupe ? ")
            group = input("De quel groupe voulez-vous le supprimer ? ")
            remove_user_from_group(user, group, data_ai)
            continue

        # Check if the user wants to create a group with certain permissions
        if "crée un groupe avec certaines permissions" in user_input.lower():
            # Ask for the permissions
            permissions = input("Quelles permissions voulez-vous attribuer à ce groupe ? ")
            create_group_with_permissions(permissions, data_ai)
            continue

        best_match = find_best_match(user_input, [q["questions"] for q in data_ai["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, data_ai)
            print(f'Bot: {answer}')
            if answer:
                execute_command(answer)
        else:
            print(f'Bot: Je ne connais pas la réponse. Pouvez-vous m\'enseigner ?')
            new_answer = input('Tapez la réponse ou "skip" pour ignorer : ')
            
            if new_answer.lower() != 'skip':
                data_ai['questions'].append({"questions": user_input, "answer": new_answer})
                save_data_ai('data_ai.json', data_ai)
                print('Bot: Merci, j\'ai appris une nouvelle réponse !')

if __name__ == '__main__':
    chat_bot()

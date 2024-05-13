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

def create_group(group_name: str):
    # Créer le groupe
    subprocess.run(f'sudo groupadd {group_name}', shell=True)
    print(f"Le groupe '{group_name}' a bien été créé.")

def add_user_to_group():
    # Ajouter un utilisateur à un groupe
    user_name = input("Quel utilisateur voulez-vous ajouter au groupe ? ")
    group_name = input("À quel groupe voulez-vous l'ajouter ? ")
    subprocess.run(f'sudo usermod -aG {group_name} {user_name}', shell=True)
    print(f"L'utilisateur '{user_name}' a bien été ajouté au groupe '{group_name}'.")

def remove_user_from_group():
    # Retirer un utilisateur d'un groupe
    user_name = input("Quel utilisateur voulez-vous supprimer du groupe ? ")
    group_name = input("De quel groupe voulez-vous le supprimer ? ")
    subprocess.run(f'sudo deluser {user_name} {group_name}', shell=True)
    print(f"L'utilisateur '{user_name}' a bien été supprimé du groupe '{group_name}'.")

def install_package(package_name: str, data_ai: dict):
    # Installer le paquet
    subprocess.run(f'sudo apt install {package_name}', shell=True)
    print(f"Le paquet '{package_name}' a bien été téléchargé et installé.")
    # Ajouter la réponse dans le fichier JSON
    data_ai['questions'].append({"questions": f"telecharge le paquet {package_name}", "answer": f"sudo apt install {package_name}"})
    save_data_ai('data_ai.json', data_ai)

def remove_package(package_name: str, data_ai: dict):
    # Supprimer le paquet
    subprocess.run(f'sudo apt remove {package_name}', shell=True)
    print(f"Le paquet '{package_name}' a bien été supprimé.")
    # Ajouter la réponse dans le fichier JSON
    data_ai['questions'].append({"questions": f"supprime le paquet {package_name}", "answer": f"sudo apt remove {package_name}"})
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

        # Check if the user wants to create a group
        if "creer un groupe" in user_input.lower():
            # Ask for the group name
            group_name = input("Nom du groupe que voulez-vous créer ? ")
            create_group(group_name)
            continue

        # Check if the user wants to add a user to a group
        if "ajoute un user au groupe" in user_input.lower():
            add_user_to_group()
            continue

        # Check if the user wants to remove a user from a group
        if "supprime un user de son groupe" in user_input.lower():
            remove_user_from_group()
            continue

        # Check if the user wants to install a package
        if "telecharge un paquet" in user_input.lower():
            # Ask for the package name
            package_name = input("Quel paquet voulez-vous télécharger ? ")
            install_package(package_name, data_ai)
            continue

        # Check if the user wants to remove a package
        if "supprime un paquet" in user_input.lower():
            # Ask for the package name to remove
            package_name = input("Quel paquet voulez-vous supprimer ? ")
            remove_package(package_name, data_ai)
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

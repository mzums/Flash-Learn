import requests
from typing import Dict, Optional


class QuizletClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def login(self, username: str) -> bool:
        """Logowanie poprzez wysłanie istniejącego username"""
        response = self.session.post(
            f"{self.base_url}/login",
            json={"username": username}
        )
        return response.status_code == 200

    def create_user(self, username: str, email: str) -> Optional[Dict]:
        response = self.session.post(
            f"{self.base_url}/users",
            json={"username": username, "email": email}
        )
        return response.json() if response.status_code == 200 else None

    def create_set(self, name: str, is_public: bool = True) -> Optional[Dict]:
        response = self.session.post(
            f"{self.base_url}/sets",
            json={"name": name, "is_public": is_public}
        )
        return response.json() if response.status_code == 200 else None

    def add_term(self, set_id: int, word: str, definition: str) -> Optional[Dict]:
        response = self.session.post(
            f"{self.base_url}/sets/{set_id}/terms",
            json={"word": word, "definition": definition}
        )
        return response.json() if response.status_code == 200 else None

    def get_my_sets(self) -> Optional[Dict]:
        response = self.session.get(f"{self.base_url}/users/me/sets")
        return response.json() if response.status_code == 200 else None

    def logout(self):
        self.session.cookies.clear()


if __name__ == "__main__":
    client = QuizletClient()
    
    try:
        # 1. Create user
        user = client.create_user("test_user16", "test16@example.com")
        if not user:
            print("Error creating user!")
            exit()
        print("Created user:", user)

        # 2. Login
        if not client.login(user["username"]):
            print("Login error!")
            exit()
        print("Login successful!")

        # 3. Create set
        new_set = client.create_set("My flashcards", is_public=True)
        if not new_set:
            print("Error creating set!")
            exit()
        print("Created set:", new_set)

        # 4. Add flashcard
        term = client.add_term(new_set["set_id"], "Hello", "Cześć")
        if not term:
            print("Error adding flashcard!")
            exit()
        print("Added flashcard:", term)

        # 5. Get sets
        sets = client.get_my_sets()
        print("Set list:", sets)

    except Exception as e:
        print("Error occurred:", e)
    finally:
        client.logout()
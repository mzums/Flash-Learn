import requests
from typing import Dict, Optional


class QuizletClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.logged_user_id = None

    def _debug_request(self, response):
        """Funkcja pomocnicza do debugowania żądań"""
        print(f"[DEBUG] URL: {response.url}")
        print(f"[DEBUG] Status code: {response.status_code}")
        print(f"[DEBUG] Response: {response.text}\n")

    def create_user(self, username: str, email: str) -> Optional[Dict]:
        response = self.session.post(
            f"{self.base_url}/api/users/",
            json={"username": username, "email": email}
        )
        self._debug_request(response)
        try:
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Create user: {str(e)}")
            return None

    def login(self, username: str) -> bool:
        response = self.session.post(
            f"{self.base_url}/api/users/login",
            json={"username": username}
        )
        self._debug_request(response)
        if response.status_code == 200:
            try:
                user_data = response.json()
                self.logged_user_id = user_data["user_id"]
                return True
            except KeyError:
                print("[ERROR] Brak user_id w odpowiedzi serwera")
        return False

    def create_set(self, name: str, is_public: bool = True) -> Optional[Dict]:
        response = self.session.post(
            f"{self.base_url}/api/v1/sets",
            json={
                "name": name,
                "is_public": is_public,
                "creator_id": self.logged_user_id
            }
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
    print("=== Rozpoczynam test ===")
    
    try:
        print("\n--- Creating user ---")
        user = client.create_user("test_user32", "test32@example.com")
        if not user:
            print("!!! Error creating user !!!")
            exit()
        print(f"Created user: {user}")

        print("\n--- Login ---")
        if not client.login(user["username"]):
            print("!!! Login error !!!")
            exit()
        print(f"Logged in! User ID: {client.logged_user_id}")

        print("\n--- creating set ---")
        new_set = client.create_set("My flashcards", is_public=True)
        if not new_set:
            print("!!! Error creating set !!!")
            exit()
        print(f"Created set: {new_set}")

    except Exception as e:
        print(f"\n### Critic error: {str(e)} ###")
    finally:
        client.logout()
        print("\n=== Test completed ===")
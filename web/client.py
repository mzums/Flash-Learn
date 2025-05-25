import requests
from typing import Dict, Optional


class QuizletClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.logged_user_id = None

    def _debug_request(self, response):
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
        try:
            response = self.session.post(
                f"{self.base_url}/api/users/login",
                json={"username": username}
            )
            self._debug_request(response)
            
            if response.status_code == 200:
                self.logged_user_id = response.json()["user_id"]
                return True
                
            return False
        except Exception as e:
            print(f"Login error: {str(e)}")
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
    
    def fork_set(self, parent_set_id: int, name: str, is_public: bool = False) -> Optional[Dict]:
        if not self.logged_user_id:
            print("Error: User not logged in")
            return None
            
        response = self.session.post(
            f"{self.base_url}/api/v1/sets/{parent_set_id}/fork",
            json={
                "name": name,
                "is_public": is_public,
                "creator_id": self.logged_user_id
            }
        )
        
        print(f"[FORK] Status code: {response.status_code}")
        print(f"[FORK] Response content: {response.text}")
    
        return response.json() if response.status_code == 200 else None
    
    def get_set_forks(self, set_id: int):
        response = self.session.get(f"{self.base_url}/api/v1/sets/{set_id}/forks")
        return response.json()

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
        user = client.create_user("test_user8", "test8@example.com")
        if not user:
            print("!!! Error creating user !!!")
            exit()
        print(f"Created user: {user}")

        print("\n--- Login ---")
        if not client.login("test_user1"):
            print("!!! Login error !!!")
            exit()
        print(f"Logged in! User ID: {client.logged_user_id}")

        print("\n--- creating set ---")
        new_set = client.create_set("My flashcards", is_public=True)
        if not new_set:
            print("!!! Error creating set !!!")
            exit()
        print(f"Created set: {new_set}")

        print("\n--- creating fork ---")
        forked_set = client.fork_set(
            parent_set_id=1,
            name="My fork",
            is_public=False
        )

        print("Fork created:", forked_set)

        forks = client.get_set_forks(set_id = 1)

    except Exception as e:
        print(f"\n### Critic error: {str(e)} ###")
    finally:
        client.logout()
        print("\n=== Test completed ===")
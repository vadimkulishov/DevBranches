import requests
from typing import List, Dict, Optional

class TodoModel:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000/todos"
        
    def get_all_todos(self) -> List[Dict]:
        response = requests.get(self.base_url)
        return response.json()
        
    def create_todo(self, title: str, description: Optional[str] = None) -> Dict:
        data = {"title": title}
        if description:
            data["description"] = description
        response = requests.post(self.base_url, json=data)
        return response.json()
        
    def update_todo(self, todo_id: int, title: Optional[str] = None, 
                   description: Optional[str] = None, completed: Optional[bool] = None) -> Dict:
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if completed is not None:
            data["completed"] = completed
            
        response = requests.put(f"{self.base_url}/{todo_id}", json=data)
        return response.json()
        
    def delete_todo(self, todo_id: int) -> bool:
        response = requests.delete(f"{self.base_url}/{todo_id}")
        return response.status_code == 204
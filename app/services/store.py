from typing import Any, Dict, List, Optional
from uuid import uuid4
from datetime import datetime, timezone


class Store:
    def __init__(self) -> None:
        self.users: Dict[str, Dict[str, Any]] = {}
        self.athletes: Dict[str, Dict[str, Any]] = {}
        self.biometrics: Dict[str, List[Dict[str, Any]]] = {}
        self.predictions: Dict[str, List[Dict[str, Any]]] = {}
        self.wearables: Dict[str, Dict[str, Any]] = {}

    def now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def create_user(self, name: str, email: str, password_hash: str, role: str) -> Dict[str, Any]:
        user_id = str(uuid4())
        self.users[user_id] = {"id": user_id, "name": name, "email": email, "password_hash": password_hash, "role": role}
        return self.users[user_id]

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        for u in self.users.values():
            if u["email"].lower() == email.lower():
                return u
        return None

    def create_athlete(self, coach_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        athlete_id = str(uuid4())
        payload = {"id": athlete_id, "coach_id": coach_id, **data}
        self.athletes[athlete_id] = payload
        return payload

    def list_athletes_for_coach(self, coach_id: str) -> List[Dict[str, Any]]:
        return [a for a in self.athletes.values() if a["coach_id"] == coach_id]

    def get_athlete(self, athlete_id: str) -> Optional[Dict[str, Any]]:
        return self.athletes.get(athlete_id)

    def update_athlete(self, athlete_id: str, patch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        a = self.athletes.get(athlete_id)
        if not a:
            return None
        a.update({k: v for k, v in patch.items() if v is not None})
        return a

    def add_biometrics(self, athlete_id: str, item: Dict[str, Any]) -> Dict[str, Any]:
        self.biometrics.setdefault(athlete_id, [])
        self.biometrics[athlete_id].append(item)
        return item

    def get_biometrics(self, athlete_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        return list(self.biometrics.get(athlete_id, []))[-limit:]

    def add_prediction(self, athlete_id: str, item: Dict[str, Any]) -> Dict[str, Any]:
        self.predictions.setdefault(athlete_id, [])
        self.predictions[athlete_id].append(item)
        return item

    def get_latest_prediction(self, athlete_id: str) -> Optional[Dict[str, Any]]:
        items = self.predictions.get(athlete_id, [])
        return items[-1] if items else None

    def get_prediction_history(self, athlete_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        return list(self.predictions.get(athlete_id, []))[-limit:]

    def wearable_connect(self, user_id: str, provider: str) -> Dict[str, Any]:
        self.wearables[user_id] = {"connected": True, "provider": provider, "last_sync": None}
        return self.wearables[user_id]

    def wearable_status(self, user_id: str) -> Dict[str, Any]:
        return self.wearables.get(user_id, {"connected": False, "provider": None, "last_sync": None})

    def wearable_sync(self, user_id: str) -> Dict[str, Any]:
        s = self.wearables.get(user_id, {"connected": False, "provider": None, "last_sync": None})
        s["last_sync"] = self.now()
        self.wearables[user_id] = s
        return s


store = Store()
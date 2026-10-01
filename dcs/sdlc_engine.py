"""Generative SDLC engine: derive process execution from the manifest."""
import json
from pathlib import Path

REQUIRED_FIELDS = [
    "id", "name", "category", "identity", "inputs", "outputs",
    "controls", "dependencies", "evidence", "metrics", "state",
    "exit_criteria", "test",
]
BELNAP_STATES = {"UNKNOWN", "TRUE", "FALSE", "CONFLICT"}


class SDLCEngine:
    def __init__(self, manifest_path):
        self.manifest_path = Path(manifest_path)
        self.data = None

    def load(self):
        self.data = json.loads(self.manifest_path.read_text())
        return self.data

    def validate(self):
        if self.data is None:
            self.load()
        for req in self.data["requirements"]:
            for field in REQUIRED_FIELDS:
                if field not in req:
                    raise ValueError(f"{req.get('id')} missing {field}")
            if req["state"] not in BELNAP_STATES:
                raise ValueError(f"{req['id']} invalid state {req['state']}")
        return True

    def process_all(self):
        if self.data is None:
            self.load()
        self.validate()
        return [req["id"] for req in self.data["requirements"]]

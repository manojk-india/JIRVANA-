import yaml
import os
from pathlib import Path

# Get correct config path
config_path = Path(__file__).parent / "config/tasks.yaml"

try:
    with open(config_path, "r") as f:
        tasks_config = yaml.safe_load(f) or {}  # Ensure dict fallback
except Exception as e:
    print(f"Config load error: {e}")
    tasks_config = {}

# Validate structure
if not tasks_config.get("Splitter1"):
    print("Invalid tasks.yaml structure")

print(f"Config type: {type(tasks_config)}")  # Should be <class 'dict'>
print(f"Splitter1 type: {type(tasks_config.get('Splitter1'))}")  # Should be <class 'dict'>


from pathlib import Path
from typing import Any, Optional

import yaml


class PromptLoader:
    """Load and render versioned YAML prompts from backend/prompts."""

    def __init__(self, prompt_dir: Optional[str] = None):
        backend_dir = Path(__file__).resolve().parent.parent
        self.prompt_dir = Path(prompt_dir) if prompt_dir else backend_dir / "prompts"
        self._cache: dict[str, dict[str, Any]] = {}

    def load_prompt(self, prompt_name: str) -> dict[str, Any]:
        if prompt_name in self._cache:
            return self._cache[prompt_name]

        prompt_path = self.prompt_dir / f"{prompt_name}.yaml"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

        prompt_data = yaml.safe_load(prompt_path.read_text(encoding="utf-8")) or {}
        self._cache[prompt_name] = prompt_data
        return prompt_data

    def render_prompt(self, prompt_name: str, **variables: Any) -> str:
        prompt_data = self.load_prompt(prompt_name)
        required_variables = prompt_data.get("input_variables", [])
        missing = [name for name in required_variables if name not in variables]
        if missing:
            raise ValueError(f"Missing prompt variables for '{prompt_name}': {', '.join(missing)}")

        template = prompt_data.get("template", "")
        return template.format(**variables)
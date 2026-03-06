import os
from dataclasses import dataclass, field
from pathlib import Path


def _parse_csv_list(raw_value: str | None, default: list[str]) -> list[str]:
    if not raw_value:
        return default.copy()
    values = [item.strip() for item in raw_value.split(",") if item.strip()]
    return values or default.copy()


@dataclass(slots=True)
class AppConfig:
    backend_dir: Path
    app_title: str = "Schema Rag"
    app_version: str = "1.0.0"
    cors_origins: list[str] = field(default_factory=lambda: ["*"])
    prompt_dir: Path = field(default_factory=Path)
    schema_file: Path = field(default_factory=Path)
    business_db_path: Path = field(default_factory=Path)
    qdrant_host: str = "localhost"
    qdrant_port: int = 6334
    qdrant_collection: str = "schema_metadata"

    @classmethod
    def from_env(cls) -> "AppConfig":
        backend_dir = Path(__file__).resolve().parent.parent
        return cls(
            backend_dir=backend_dir,
            app_title=os.getenv("APP_TITLE", "Schema Rag"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
            cors_origins=_parse_csv_list(os.getenv("CORS_ALLOW_ORIGINS"), ["*"]),
            prompt_dir=backend_dir / "prompts",
            schema_file=backend_dir / "data" / "erp_schema_dump.sql",
            business_db_path=backend_dir / "data" / "erp_data.db",
            qdrant_host=os.getenv("QDRANT_HOST", "localhost"),
            qdrant_port=int(os.getenv("QDRANT_PORT", "6334")),
            qdrant_collection=os.getenv("QDRANT_COLLECTION", "schema_metadata"),
        )


def load_app_config() -> AppConfig:
    return AppConfig.from_env()
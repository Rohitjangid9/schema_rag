from dataclasses import dataclass
from typing import Optional

from config.app_config import AppConfig
from core.graph_logic import GraphLogic
from core.prompt_builder import PromptBuilder
from core.prompt_loader import PromptLoader
from core.qdrant_manager import QdrantManager
from core.query_executor import QueryExecutor
from core.reranker import Reranker
from core.result_formatter import ResultFormatter
from core.sql_generator import SQLGenerator


@dataclass
class AppRuntime:
    qdrant_manager: Optional[QdrantManager] = None
    graph_logic: Optional[GraphLogic] = None
    prompt_builder: Optional[PromptBuilder] = None
    sql_generator: Optional[SQLGenerator] = None
    query_executor: Optional[QueryExecutor] = None
    result_formatter: Optional[ResultFormatter] = None
    reranker: Optional[Reranker] = None
    initialization_error: Optional[str] = None

    def has_search(self) -> bool:
        return all([self.qdrant_manager, self.graph_logic])

    def has_phase2(self) -> bool:
        return all([self.qdrant_manager, self.graph_logic, self.prompt_builder, self.sql_generator])

    def has_chat(self) -> bool:
        return all([
            self.qdrant_manager,
            self.graph_logic,
            self.prompt_builder,
            self.sql_generator,
            self.query_executor,
            self.result_formatter,
        ])


def create_runtime(config: AppConfig) -> AppRuntime:
    try:
        prompt_loader = PromptLoader(str(config.prompt_dir))
        runtime = AppRuntime(
            qdrant_manager=QdrantManager(
                host=config.qdrant_host,
                port=config.qdrant_port,
                collection_name=config.qdrant_collection,
            ),
            graph_logic=GraphLogic(),
            prompt_builder=PromptBuilder(schema_file=str(config.schema_file), prompt_loader=prompt_loader),
            sql_generator=SQLGenerator(),
            query_executor=QueryExecutor(db_path=str(config.business_db_path)),
            result_formatter=ResultFormatter(prompt_loader=prompt_loader),
            reranker=Reranker(),
        )
        print("✓ All managers initialized (Phase 1 foundation + Phase 2/3 runtime)")
        return runtime
    except Exception as exc:
        print(f"⚠️  Warning: Could not initialize managers: {exc}")
        return AppRuntime(initialization_error=str(exc))
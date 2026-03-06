"""
Generate table summaries using NVIDIA Llama API
Optimized for RAG retrieval - summaries are designed to match user queries
"""
import os
import json
import time
from typing import Dict, Any, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class NVIDIASummarizer:
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables")

        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )
        self.model = "meta/llama-3.1-8b-instruct"

    def _identify_key_columns(self, columns: List[Dict]) -> Dict[str, List[str]]:
        """Identify important columns by type for better context"""
        key_columns = {
            "amounts": [],      # Money/numeric columns
            "dates": [],        # Date/time columns
            "references": [],   # Foreign keys / ID references
            "status": [],       # Status/state columns
            "descriptive": []   # Text/description columns
        }

        for col in columns:
            name = col["name"].lower()
            col_type = col["type"].upper()

            # Amounts/Money
            if any(term in name for term in ["amount", "price", "cost", "total", "balance", "salary", "rate", "fee"]):
                key_columns["amounts"].append(col["name"])
            # Dates
            elif any(term in name for term in ["date", "time", "created", "updated", "at"]) or "TIMESTAMP" in col_type or "DATE" in col_type:
                key_columns["dates"].append(col["name"])
            # References/IDs
            elif name.endswith("_id") or name == "id" or "ref" in name:
                key_columns["references"].append(col["name"])
            # Status
            elif any(term in name for term in ["status", "state", "type", "is_", "has_"]):
                key_columns["status"].append(col["name"])
            # Descriptive
            elif any(term in name for term in ["name", "description", "title", "comment", "note", "address"]):
                key_columns["descriptive"].append(col["name"])

        return key_columns

    def format_table_info(self, metadata: Dict[str, Any]) -> str:
        """Format table metadata into a readable string with key column analysis"""
        table_name = metadata["table_name"]
        module = metadata["module"]
        entity = metadata["entity"]
        columns = metadata["columns"]
        row_count = metadata["row_count"]

        # Get key columns
        key_cols = self._identify_key_columns(columns)

        columns_str = ", ".join([f"{col['name']} ({col['type']})" for col in columns])

        key_cols_str = ""
        if key_cols["amounts"]:
            key_cols_str += f"\n  Amount/Money columns: {', '.join(key_cols['amounts'])}"
        if key_cols["dates"]:
            key_cols_str += f"\n  Date columns: {', '.join(key_cols['dates'])}"
        if key_cols["references"]:
            key_cols_str += f"\n  Reference/ID columns: {', '.join(key_cols['references'])}"
        if key_cols["status"]:
            key_cols_str += f"\n  Status columns: {', '.join(key_cols['status'])}"
        if key_cols["descriptive"]:
            key_cols_str += f"\n  Descriptive columns: {', '.join(key_cols['descriptive'])}"

        return f"""Table: {table_name}
Module: {module} (Entity: {entity})
Record Count: {row_count}
All Columns: {columns_str}
Key Columns Analysis:{key_cols_str if key_cols_str else ' None identified'}"""

    def generate_summary(self, metadata: Dict[str, Any], include_foreign_keys: Optional[List[str]] = None) -> str:
        """
        Generate a RAG-optimized summary for a table using NVIDIA Llama API
        The summary is designed to match how users will ask questions
        """
        table_info = self.format_table_info(metadata)
        table_name = metadata["table_name"]
        module = metadata["module"]

        # Add foreign key info if available
        fk_context = ""
        if include_foreign_keys and len(include_foreign_keys) > 0:
            fk_context = f"\nRelated Tables (via Foreign Keys): {', '.join(include_foreign_keys)}"

        prompt = f"""You are a database documentation expert. Your task is to write a summary that helps users FIND this table when they search with natural language questions.

{table_info}{fk_context}

Write a 2-3 sentence summary following this EXACT format:
1. First sentence: What specific data this table stores (mention key column types like amounts, dates, names)
2. Second sentence: What business questions can be answered using this table (be specific with examples)
3. Third sentence: Related keywords and concepts users might search for

IMPORTANT: Include searchable terms like "revenue", "sales", "inventory", "customers", "orders", "employees", "payments" etc. that match the table's purpose.

Example good summary:
"This table stores sales order transactions including order amounts, dates, customer references, and order status. Use it to answer questions about revenue trends, order volumes, sales by region, and customer purchase history. Related to: invoices, billing, sales reports, revenue analysis, order tracking."

Now write the summary for {table_name}:"""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a database expert who writes concise, search-optimized table descriptions. Always include business terms and potential user query keywords."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent output
                top_p=0.9,
                max_tokens=300,
                stream=False
            )

            summary = completion.choices[0].message.content.strip()

            # Clean up any quotes or extra formatting
            summary = summary.strip('"').strip("'")

            return summary

        except Exception as e:
            print(f"Error generating summary for {metadata['table_name']}: {e}")
            # Enhanced fallback summary
            return self._generate_fallback_summary(metadata)

    def _generate_fallback_summary(self, metadata: Dict[str, Any]) -> str:
        """Generate a better fallback summary without API"""
        table_name = metadata["table_name"]
        module = metadata["module"]
        entity = metadata["entity"]
        columns = metadata["columns"]

        key_cols = self._identify_key_columns(columns)

        # Build descriptive parts
        parts = [f"Table {table_name} in the {module} module stores {entity.replace('_', ' ')} data"]

        if key_cols["amounts"]:
            parts.append(f"with financial fields ({', '.join(key_cols['amounts'][:3])})")
        if key_cols["dates"]:
            parts.append(f"tracking dates ({', '.join(key_cols['dates'][:2])})")

        summary = " ".join(parts) + "."
        summary += f" Use for queries about {module} {entity.replace('_', ' ')} records."
        summary += f" Related to: {module}, {entity.replace('_', ' ')}, {', '.join([c['name'] for c in columns[:5]])}."

        return summary

    def generate_summaries_batch(
        self,
        metadata_list: list,
        output_file: str = "data/table_summaries.json",
        foreign_keys: Optional[Dict[str, List[str]]] = None,
        delay_between_calls: float = 0.1
    ) -> Dict[str, str]:
        """
        Generate summaries for all tables with optional foreign key context

        Args:
            metadata_list: List of table metadata dictionaries
            output_file: Path to save summaries JSON
            foreign_keys: Optional dict mapping table_name -> list of related table names
            delay_between_calls: Delay between API calls to avoid rate limiting
        """
        summaries = {}
        total = len(metadata_list)

        print(f"\n{'='*60}")
        print(f"GENERATING RAG-OPTIMIZED SUMMARIES")
        print(f"{'='*60}")
        print(f"Tables to process: {total}")
        print(f"Model: {self.model}")
        print(f"Output: {output_file}")
        print(f"{'='*60}\n")

        for i, metadata in enumerate(metadata_list, 1):
            table_name = metadata["table_name"]

            # Get foreign keys for this table if available
            table_fks = foreign_keys.get(table_name, []) if foreign_keys else None

            print(f"  [{i}/{total}] {table_name}...", end=" ", flush=True)

            try:
                summary = self.generate_summary(metadata, table_fks)
                summaries[table_name] = summary
                print(f"✓")
                print(f"           → {summary[:80]}...")
            except Exception as e:
                print(f"✗ Error: {e}")
                summaries[table_name] = self._generate_fallback_summary(metadata)

            # Small delay to avoid rate limiting
            if delay_between_calls > 0 and i < total:
                time.sleep(delay_between_calls)

        # Save summaries to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*60}")
        print(f"✓ Summaries saved to {output_file}")
        print(f"✓ Total tables processed: {len(summaries)}")
        print(f"{'='*60}\n")

        return summaries


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate RAG-optimized table summaries")
    parser.add_argument("--input", default="data/table_metadata.json", help="Input metadata file")
    parser.add_argument("--output", default="data/table_summaries.json", help="Output summaries file")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of tables (for testing)")
    args = parser.parse_args()

    # Load metadata
    print(f"Loading metadata from {args.input}...")
    with open(args.input, 'r') as f:
        metadata_list = json.load(f)

    if args.limit:
        metadata_list = metadata_list[:args.limit]
        print(f"Limited to {args.limit} tables for testing")

    # Generate summaries
    summarizer = NVIDIASummarizer()
    summaries = summarizer.generate_summaries_batch(metadata_list, args.output)

    print(f"\n✓ Generated {len(summaries)} RAG-optimized summaries")


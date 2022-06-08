from pathlib import Path
from textwrap import dedent

from dbt_osmosis.core.osmosis import DbtOsmosis


def inject_macros(dbt: DbtOsmosis):
    macro_path = Path(dbt.config.macro_paths[0]) / "dbt_osmosis"
    macro_path.mkdir(parents=True, exist_ok=True)
    (macro_path / "dbt_osmosis_compare.sql").write_text(
        dedent(
            """
    {% macro dbt_osmosis_compare(a_query, b_query, primary_key=none) }

    {% set audit_query = compare_queries(
        a_query=query_A,
        b_query=query_B,
        primary_key=pk,
    ) %}

    {% set audit_results = run_query(audit_query) %}

    {% if execute %}
        {% do audit_results.print_table() %}
    {% endif %}
    {% endmacro %}
    """
        )
    )

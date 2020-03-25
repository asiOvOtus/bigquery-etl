"""clients_daily_histogram_aggregates query generator."""
import argparse
from jinja2 import Environment, PackageLoader

from bigquery_etl.format_sql.formatter import reformat


def render_main(**kwargs):
    """Create a SQL query for the clients_daily_histogram_aggregates dataset."""
    env = Environment(loader=PackageLoader("bigquery_etl", "glam/templates"))
    main_sql = env.get_template("clients_histogram_aggregates_v1.sql")
    return reformat(main_sql.render(**kwargs))


def render_init(**kwargs):
    """Create a SQL init."""
    env = Environment(loader=PackageLoader("bigquery_etl", "glam/templates"))
    template = env.get_template("clients_histogram_aggregates_v1.init.sql")
    return reformat(template.render(**kwargs))


def glean_variables():
    """Variables for templated SQL."""
    attributes_list = [
        "sample_id",
        "client_id",
        "ping_type",
        "os",
        "app_version",
        "app_build_id",
        "channel",
    ]
    return dict(
        attributes_list=attributes_list,
        attributes=",".join(attributes_list),
        metric_attributes="""
            latest_version,
            metric,
            metric_type,
            key,
            agg_type
        """,
    )


def main():
    """Print a rendered query to stdout."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-parameterize",
        action="store_true",
        help="Generate a query without parameters",
    )
    parser.add_argument(
        "--init", action="store_true", help="Generate the table creation DDL"
    )
    args = parser.parse_args()

    module = "bigquery_etl.glam.clients_histogram_aggregates"
    header = (
        f"-- Query generated by: python3 -m {module} "
        + (" --no-parameterize" if args.no_parameterize else "")
        + (" --init" if args.init else "")
    )

    render = render_init if args.init else render_main
    print(
        render(
            header=header, parameterize=not args.no_parameterize, **glean_variables()
        )
    )


if __name__ == "__main__":
    main()
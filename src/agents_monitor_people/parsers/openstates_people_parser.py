"""
parsers/openstates_people_parser.py

Queries OpenStates GraphQL for basic people counts.

MIT License — Civic Interconnect
"""

import asyncio

import pandas as pd
from civic_lib_core import graphql_utils, log_utils
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

logger = log_utils.logger

# GraphQL query for people data
PEOPLE_QUERY = gql("""
query PeopleSummary($first: Int, $after: String) {
  people(first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        name
        jurisdiction { name }
      }
    }
  }
}
""")


async def fetch_people(api_key: str, config: dict) -> pd.DataFrame:
    url = config["openstates_graphql_url"]
    headers = {"Authorization": f"Bearer {api_key}"}

    transport = AIOHTTPTransport(url=url, headers=headers, ssl=True)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    people = []
    after = None

    while True:
        variables = {"first": 100, "after": after}
        response = await client.execute_async(PEOPLE_QUERY, variable_values=variables)
        edges = response["people"]["edges"]
        for edge in edges:
            person = edge["node"]
            people.append({
                "id": person["id"],
                "name": person["name"],
                "jurisdiction": person["jurisdiction"]["name"],
            })
        page = response["people"]["pageInfo"]
        if not page["hasNextPage"]:
            break
        after = page["endCursor"]

    logger.info(f"Fetched {len(people)} people total")
    return pd.DataFrame(people)


def run(storage_path: str, config: dict, api_key: str) -> list | str:
    """
    Entry point to pull and summarize OpenStates people data.
    """
    logger.info("Pulling OpenStates people summary...")

    try:
        df = asyncio.run(fetch_people(api_key, config))
        grouped = df.groupby("jurisdiction").size().reset_index(name="person_count")
        summary = grouped.to_dict(orient="records")
        logger.info(f"Summary: {summary}")
        return summary

    except Exception as e:
        return graphql_utils.handle_transport_errors(e, resource_name="OpenStates People Monitor")

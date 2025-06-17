"""
parsers/openstates_people_parser.py

Queries OpenStates GraphQL for basic people counts.
"""

import asyncio
import pandas as pd
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import (
    TransportServerError,
    TransportQueryError,
    TransportProtocolError,
)
from loguru import logger

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


async def fetch_people(api_key, config):
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
            people.append(
                {
                    "id": person["id"],
                    "name": person["name"],
                    "jurisdiction": person["jurisdiction"]["name"],
                }
            )
        page = response["people"]["pageInfo"]
        if not page["hasNextPage"]:
            break
        after = page["endCursor"]

    logger.info(f"Fetched {len(people)} people total")
    return pd.DataFrame(people)


def run(storage_path, config, api_key):
    logger.info("Pulling OpenStates people summary...")

    try:
        df = asyncio.run(fetch_people(api_key, config))
        grouped = df.groupby("jurisdiction").size().reset_index(name="person_count")
        summary = grouped.to_dict(orient="records")
        logger.info(f"Summary: {summary}")
        return summary

    except TransportServerError as e:
        if "403" in str(e):
            logger.warning(
                "OpenStates people access not yet enabled (received 403 Forbidden)."
            )
            return "People data access not yet granted"
        else:
            logger.error(f"Server error: {e}")
            raise

    except TransportQueryError as e:
        logger.error(f"GraphQL query error: {e}")
        raise

    except TransportProtocolError as e:
        logger.error(f"Transport protocol error: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

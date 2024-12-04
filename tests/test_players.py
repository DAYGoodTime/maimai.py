import pytest

from maimai_py.maimai import MaimaiClient
from maimai_py.providers import LXNSProvider
from tests import secrets


@pytest.mark.asyncio()
async def test_players_fetching():
    maimai = MaimaiClient()
    lxns_provider = LXNSProvider(developer_token=secrets.lxns_developer_token)
    player = await maimai.players(lxns_provider, friend_code=664994421382429)
    assert player.rating > 10000

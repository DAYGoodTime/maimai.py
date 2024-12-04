from httpx import AsyncClient, AsyncHTTPTransport
from maimai_py.enums import RecordKind
from maimai_py.models import DivingFishPlayer, LXNSPlayer, PlayerIdentifier, Song, SongAlias
from maimai_py.providers import IAliasProvider, IPlayerProvider, ISongProvider, DivingFishProvider, LXNSProvider, YuzuProvider


class MaimaiSongs:
    _song_id_dict: dict[int, Song]  # song_id: song
    _alias_entry_dict: dict[str, int]  # alias_entry: song_id

    def __init__(self, songs: list[Song], aliases: list[SongAlias] | None) -> None:
        self._song_id_dict = {song.id: song for song in songs}
        self._alias_entry_dict = {}
        for alias in aliases:
            target_song = self._song_id_dict.get(alias.song_id)
            if target_song:
                target_song.aliases = alias.aliases
            for alias_entry in alias.aliases:
                self._alias_entry_dict[alias_entry] = alias.song_id

    @property
    def songs(self):
        return self._song_id_dict.values()

    def by_id(self, id: int) -> Song | None:
        """
        Get a song by its ID, if it exists, otherwise return None

        Parameters
        ----------
        id: int
            the ID of the song, always smaller than 10000, should (% 10000) if necessary
        """
        return self._song_id_dict.get(id, None)

    def by_title(self, title: str) -> Song | None:
        """
        Get a song by its title, if it exists, otherwise return None

        Parameters
        ----------
        title: str
            the title of the song
        """
        return next((song for song in self.songs if song.title == title), None)

    def by_alias(self, alias: str) -> Song | None:
        """
        Get song by one possible alias, if it exists, otherwise return None

        Parameters
        ----------
        alias: str
            one possible alias of the song
        """
        song_id = self._alias_entry_dict.get(alias, 0)
        return self.by_id(song_id)

    def by_artist(self, artist: str) -> list[Song]:
        """
        Get songs by their artist, case-sensitive, return an empty list if no song is found

        Parameters
        ----------
        artist: str
            the artist of the songs
        """
        return [song for song in self.songs if song.artist == artist]

    def by_genre(self, genre: str) -> list[Song]:
        """
        Get songs by their genre, case-sensitive, return an empty list if no song is found

        Parameters
        ----------
        genre: str
            the genre of the songs
        """
        return [song for song in self.songs if song.genre == genre]

    def by_bpm(self, minimum: int, maximum: int) -> list[Song]:
        """
        Get songs by their BPM, return an empty list if no song is found

        Parameters
        ----------
        minimum: int
            the minimum (inclusive) BPM of the songs
        maximum: int
            the maximum (inclusive) BPM of the songs
        """
        return [song for song in self.songs if minimum <= song.bpm <= maximum]

    def filter(self, **kwargs) -> list[Song]:
        """
        Filter songs by their attributes, all conditions are connected by AND, return an empty list if no song is found

        Parameters
        ----------
        kwargs: dict
            the attributes to filter the songs by=
        """
        return [song for song in self.songs if all(getattr(song, key) == value for key, value in kwargs.items())]


class MaimaiClient:
    client: AsyncClient

    def __init__(self, retries: int = 3, **kwargs) -> None:
        """
        Initialize the maimai.py client

        Parameters
        ----------

        retries: int
            the number of retries to attempt on failed requests, defaults to 3
        """
        self.client = AsyncClient(transport=AsyncHTTPTransport(retries=retries), **kwargs)

    async def songs(
        self,
        provider: ISongProvider = LXNSProvider(),
        alias_provider: IAliasProvider = YuzuProvider(),
    ) -> MaimaiSongs:
        """
        Fetch all maimai songs from the provider, returning a wrapper of the song list, for easier access and filtering

        Parameters
        ----------
        provider: ISongProvider (DivingFishProvider | LXNSProvider)
            the data source to fetch the player from, defaults to LXNSProvider

        alias_provider: IAliasProvider (YuzuProvider | LXNSProvider)
            the data source to fetch the song aliases from, defaults to YuzuProvider
        """
        aliases = await alias_provider.get_aliases(self.client) if alias_provider else None
        songs = await provider.get_songs(self.client)
        maimai_songs = MaimaiSongs(songs, aliases)
        return maimai_songs

    async def players(
        self,
        identifier: PlayerIdentifier,
        provider: IPlayerProvider = DivingFishProvider(),
    ) -> DivingFishPlayer | LXNSPlayer:
        """
        Fetch player data from the provider, using the given one identifier

        Parameters
        ----------

        identifier: PlayerIdentifier
            the identifier of the player to fetch, e.g. PlayerIdentifier(username="turou")
        provider: IPlayerProvider (DivingFishProvider | LXNSProvider)
            the data source to fetch the player from, defaults to DivingFishProvider
        """
        return await provider.get_player(identifier, self.client)

    async def scores(
        self,
        identifier: PlayerIdentifier,
        kind: RecordKind = RecordKind.BEST,
        provider: IPlayerProvider = DivingFishProvider(),
    ):
        pass
from typing import Literal, TypedDict

MediaType = Literal["tv"] | Literal["movie"]


class MediaConfig(TypedDict):
    download_path: str
    movie_path: str
    tv_path: str


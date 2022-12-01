from pydantic import BaseModel, validator


class User(BaseModel):
    user_id: int
    n_items: int

    @validator("user_id")
    def user_id_must_be_positive(cls, value):
        if value < 0 or value >= 6040:
            raise ValueError(
                f"Expected userid>=0 and less than 6040, but recieved {value}"
            )
        return value

    @validator("n_items")
    def n_items_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError(
                f"Expected at least 1 recommendation, but recieved {value}"
            )
        return value


class Response(BaseModel):
    MovieID: str
    Title: str
    Genres: str

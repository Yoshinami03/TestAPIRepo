from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from enum import Enum

app = FastAPI()

CardNumber = Annotated[int, Field(ge=1, le=13)]


class Suit(str, Enum):
    spades   = "spades"
    hearts   = "hearts"
    diamonds = "diamonds"
    clubs    = "clubs"
    joker    = "joker"


class CardRequest(BaseModel):
    value: Optional[CardNumber] = None
    suit: Suit


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/cards")
def post_card(cards: list[CardRequest]):
    for card in cards:
        if card.suit == Suit.joker and card.value is not None:
            raise HTTPException(status_code=400, detail="Joker must not have a value")
        if card.suit != Suit.joker and card.value is None:
            raise HTTPException(status_code=400, detail="Non-Joker cards must have a value")
    return [{"suit": card.suit, "value": card.value} for card in cards]
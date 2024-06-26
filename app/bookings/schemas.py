from datetime import date

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int


class SBookingAdvancedData(SBooking):
    room_name: str
    hotel_name: str
    location: str


class SBookingWithRoomData(SBooking):
    image_id: int
    name: str
    description: str
    services: list

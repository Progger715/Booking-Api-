import datetime
import json
from typing import Iterable

from app.bookings.dao import BookingDAO
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.dao import RoomsDAO
from app.logger import logger

TABLE_MODEL_MAP = {
    "hotels": HotelsDAO,
    "rooms": RoomsDAO,
    "bookings": BookingDAO,
}


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    try:
        data = []
        for row in csv_iterable:
            for k, v in row.items():
                if v.isdigit():
                    row[k] = int(v)
                elif k == "services":
                    row[k] = json.loads(v.replace("'", '"'))
                elif "date" in k:
                    row[k] = datetime.datetime.strptime(v, "%d.%m.%Y")
            data.append(row)
        return data
    except Exception:
        logger.error("Cannot convert CSV into DB format", exc_info=True)

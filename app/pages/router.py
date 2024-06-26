from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.bookings.router import add_bookings, get_bookings
from app.hotels.rooms.router import get_rooms
from app.hotels.router import get_one_hotel, get_hotels
from app.pages.utils import format_number_thousand_separator, get_month_days

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_page(
        request: Request,
        hotels=Depends(get_hotels)
):
    return templates.TemplateResponse(
        name="Hotels.html",
        context={"request": request, "hotels": hotels})


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "now": datetime.now,
        "timedelta": timedelta
    })


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {
        "request": request,
        "now": datetime.now,
        "timedelta": timedelta
    })


@router.get("/hotels/{location}", response_class=HTMLResponse)
async def get_hotels_page(
        request: Request,
        location: str,
        date_to: date,
        date_from: date,
        hotels=Depends(get_hotels),
):
    dates = get_month_days()
    if date_from > date_to:
        date_to, date_from = date_from, date_to
    date_from = max(datetime.today().date(), date_from)  # ставим дату заезда позже текущей даты
    date_to = min((datetime.today() + timedelta(days=99)).date(),
                  date_to)  # ставим дату выезда не позже, чем через 99 дней
    return templates.TemplateResponse(
        "hotels_and_rooms/hotels.html",
        {
            "request": request,
            "hotels": hotels,
            "location": location,
            "date_to": date_to.strftime("%Y-%m-%d"),
            "date_from": date_from.strftime("%Y-%m-%d"),
            "dates": dates,
            "now": datetime.now,
            "timedelta": timedelta
        },
    )


@router.get("/hotels/{hotel_id}/rooms", response_class=HTMLResponse)
async def get_rooms_page(
        request: Request,
        date_from: date,
        date_to: date,
        rooms=Depends(get_rooms),
        hotel=Depends(get_one_hotel),
):
    date_from_formatted = date_from.strftime("%d.%m.%Y")
    date_to_formatted = date_to.strftime("%d.%m.%Y")
    booking_length = (date_to - date_from).days
    return templates.TemplateResponse(
        "hotels_and_rooms/rooms.html",
        {
            "request": request,
            "hotel": hotel,
            "rooms": rooms,
            "date_from": date_from,
            "date_to": date_to,
            "booking_length": booking_length,
            "date_from_formatted": date_from_formatted,
            "date_to_formatted": date_to_formatted,
            "format_number_thousand_separator": format_number_thousand_separator,
            "now": datetime.now,
            "timedelta": timedelta
        },
    )


@router.get("/bookings", response_class=HTMLResponse)
async def get_bookings_page(
        request: Request,
        bookings=Depends(get_bookings),
):
    return templates.TemplateResponse(
        "bookings/bookings.html",
        {
            "request": request,
            "bookings": bookings,
            "format_number_thousand_separator": format_number_thousand_separator,
            "now": datetime.now,
            "timedelta": timedelta
        },
    )

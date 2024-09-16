import uvicorn
from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from trip_model import TripPlan, TripRequest, TripLocation
from trip_repository import TripRepository
from plan_trip_usecase import PlanTripUseCase

app = FastAPI()
templates = Jinja2Templates(directory="./templates")
app.mount("/statics", StaticFiles(directory="./templates/statics"), name="statics")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/hotels")
def get_hotels():
    trip_repository = TripRepository()
    plan_trip_usecase = PlanTripUseCase(trip_repository)

    return [
        {"id": hotel[0], "name": hotel[1], "latitude": hotel[2], "longitude": hotel[3]}
        for hotel in plan_trip_usecase.show_all_hotels()
    ]


@app.get("/tags")
def get_tags():
    trip_repository = TripRepository()
    plan_trip_usecase = PlanTripUseCase(trip_repository)

    return plan_trip_usecase.show_all_tags()


@app.post("/plan_trip", response_model=TripPlan)
def plan_trip(request: TripRequest):
    trip_repository = TripRepository()
    plan_trip_usecase = PlanTripUseCase(trip_repository)
    itinerary = plan_trip_usecase.plan_trip(hotel_id=request.hotel_id, tag=request.tag)

    return TripPlan(
        itinerary=[TripLocation(id=loc[0], name=loc[1], latitude=loc[2], longitude=loc[3]) for loc in itinerary[0]],
        distances=itinerary[1],
        total_distance=sum(itinerary[1])
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

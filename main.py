import uvicorn
from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from plan_trip_usecase import PlanTripUseCase
from trip_model import TripPlan, TripRequest
from trip_repository import TripRepository

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

    return plan_trip_usecase.show_all_hotels()


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

    destinations = itinerary[0]
    distances = itinerary[1]
    total_distance = itinerary[2]

    return TripPlan(
        destinations=destinations,
        distances=distances,
        total_distance=total_distance
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)

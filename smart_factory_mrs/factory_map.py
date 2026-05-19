from smart_factory_mrs.models import Location


FACTORY_MAP = {
    "W1": Location("W1", 0.0, 0.0),
    "W2": Location("W2", 0.0, 6.0),
    "S1": Location("S1", 8.0, 0.0),
    "S2": Location("S2", 8.0, 3.0),
    "S3": Location("S3", 8.0, 6.0),
}


def travel_distance(start: str, pickup: str, dropoff: str) -> float:
    start_loc = FACTORY_MAP[start]
    pickup_loc = FACTORY_MAP[pickup]
    dropoff_loc = FACTORY_MAP[dropoff]
    return start_loc.distance_to(pickup_loc) + pickup_loc.distance_to(dropoff_loc)

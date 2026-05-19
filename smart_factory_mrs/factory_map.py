from smart_factory_mrs.models import Location

OBSTACLE_PENALTY = 10.0
OBSTACLE_X = 4.0
OBSTACLE_Y_MIN = 1.0
OBSTACLE_Y_MAX = 5.0


FACTORY_MAP = {
    "W1": Location("W1", 0.0, 0.0),
    "W2": Location("W2", 0.0, 6.0),
    "S1": Location("S1", 8.0, 0.0),
    "S2": Location("S2", 8.0, 3.0),
    "S3": Location("S3", 8.0, 6.0),
}


def travel_distance(start: str, pickup: str, dropoff: str, obstacle_active: bool = False) -> float:
    start_loc = FACTORY_MAP[start]
    pickup_loc = FACTORY_MAP[pickup]
    dropoff_loc = FACTORY_MAP[dropoff]
    base_distance = start_loc.distance_to(pickup_loc) + pickup_loc.distance_to(dropoff_loc)
    if not obstacle_active:
        return base_distance
    return base_distance + obstacle_penalty(start_loc, pickup_loc) + obstacle_penalty(pickup_loc, dropoff_loc)


def obstacle_penalty(start: Location, end: Location) -> float:
    if not _segment_crosses_obstacle_zone(start, end):
        return 0.0
    return OBSTACLE_PENALTY


def _segment_crosses_obstacle_zone(start: Location, end: Location) -> bool:
    if (start.x < OBSTACLE_X and end.x < OBSTACLE_X) or (start.x > OBSTACLE_X and end.x > OBSTACLE_X):
        return False
    if start.x == end.x:
        return abs(start.x - OBSTACLE_X) < 0.001 and _ranges_overlap(start.y, end.y)

    ratio = (OBSTACLE_X - start.x) / (end.x - start.x)
    if ratio < 0.0 or ratio > 1.0:
        return False
    crossing_y = start.y + (end.y - start.y) * ratio
    return OBSTACLE_Y_MIN <= crossing_y <= OBSTACLE_Y_MAX


def _ranges_overlap(start_y: float, end_y: float) -> bool:
    low = min(start_y, end_y)
    high = max(start_y, end_y)
    return not (high < OBSTACLE_Y_MIN or low > OBSTACLE_Y_MAX)

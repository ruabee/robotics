from smart_factory_mrs.models import Location

OBSTACLE_PENALTY = 10.0
OBSTACLE_X = 4.0
OBSTACLE_Y_MIN = 1.0
OBSTACLE_Y_MAX = 5.0
LOWER_DETOUR_Y = 0.0
UPPER_DETOUR_Y = 6.0
MAIN_AISLE_X_LEFT = 2.4
MAIN_AISLE_X_RIGHT = 5.6
AISLE_LEVELS = [0.0, 3.0, 6.0]


FACTORY_MAP = {
    "W1": Location("W1", 0.0, 0.0),
    "W2": Location("W2", 0.0, 6.0),
    "S1": Location("S1", 8.0, 0.0),
    "S2": Location("S2", 8.0, 3.0),
    "S3": Location("S3", 8.0, 6.0),
}


def travel_distance(start: str, pickup: str, dropoff: str, obstacle_active: bool = False) -> float:
    points = route_points(start, pickup, dropoff, obstacle_active)
    return path_distance(points)


def route_points(start: str, pickup: str, dropoff: str, obstacle_active: bool = False) -> list[Location]:
    points = [FACTORY_MAP[start]]
    points.extend(_segment_points(FACTORY_MAP[start], FACTORY_MAP[pickup], obstacle_active)[1:])
    points.extend(_segment_points(points[-1], FACTORY_MAP[dropoff], obstacle_active)[1:])
    return _deduplicate_points(points)


def path_distance(points: list[Location]) -> float:
    return sum(start.distance_to(end) for start, end in zip(points, points[1:]))


def obstacle_penalty(start: Location, end: Location) -> float:
    if not _segment_crosses_obstacle_zone(start, end):
        return 0.0
    return OBSTACLE_PENALTY


def _segment_points(start: Location, end: Location, obstacle_active: bool) -> list[Location]:
    if not obstacle_active:
        return _aisle_route(start, end)

    points = _aisle_route(start, end)
    if any(_segment_crosses_obstacle_zone(a, b) for a, b in zip(points, points[1:])):
        detour_y = LOWER_DETOUR_Y if (start.y + end.y) / 2.0 <= 3.0 else UPPER_DETOUR_Y
        points = [
            start,
            Location("detour_start", start.x, detour_y),
            Location("detour_left", MAIN_AISLE_X_LEFT, detour_y),
            Location("detour_right", MAIN_AISLE_X_RIGHT, detour_y),
            Location("detour_end", end.x, detour_y),
            end,
        ]
    return _deduplicate_points(points)


def _aisle_route(start: Location, end: Location) -> list[Location]:
    if abs(start.x - end.x) < 0.001 or abs(start.y - end.y) < 0.001:
        return [start, end]

    aisle_y = _nearest_aisle_y((start.y + end.y) / 2.0)
    left_x = MAIN_AISLE_X_LEFT if start.x <= end.x else MAIN_AISLE_X_RIGHT
    right_x = MAIN_AISLE_X_RIGHT if start.x <= end.x else MAIN_AISLE_X_LEFT
    return [
        start,
        Location("aisle_start_y", start.x, aisle_y),
        Location("aisle_left", left_x, aisle_y),
        Location("aisle_right", right_x, aisle_y),
        Location("aisle_end_y", end.x, aisle_y),
        end,
    ]


def _nearest_aisle_y(value: float) -> float:
    return min(AISLE_LEVELS, key=lambda aisle_y: abs(aisle_y - value))


def _deduplicate_points(points: list[Location]) -> list[Location]:
    result = []
    for point in points:
        if result and abs(result[-1].x - point.x) < 0.001 and abs(result[-1].y - point.y) < 0.001:
            continue
        result.append(point)
    return result


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

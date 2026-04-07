SCHEDULE_TEMPLATE = {
    "blacksmith": {
        "dawn": "at home, sleeping",
        "morning": "at the forge, working",
        "midday": "at the forge, working",
        "afternoon": "at the forge, finishing work",
        "evening": "at the tavern, drinking",
        "night": "at home, sleeping"
    },
    "merchant": {
        "dawn": "at market, setting up stall",
        "morning": "at market stall, trading",
        "midday": "at market stall, trading",
        "afternoon": "at market, packing up",
        "evening": "at inn or home",
        "night": "at home or inn, sleeping"
    },
    "guard": {
        "dawn": "on patrol, north gate",
        "morning": "on patrol, main street",
        "midday": "at barracks, resting",
        "afternoon": "on patrol, south gate",
        "evening": "on patrol, town square",
        "night": "at guard post, watching"
    },
}


def get_schedule(profession: str) -> dict[str, str]:
    return SCHEDULE_TEMPLATE.get(profession, {
        "dawn": "preparing for the day",
        "morning": "carrying out daily tasks",
        "midday": "resting briefly",
        "afternoon": "returning to work",
        "evening": "winding down",
        "night": "sleeping",
    })

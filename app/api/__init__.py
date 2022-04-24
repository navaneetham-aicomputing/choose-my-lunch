from . import restaurant, user, vote_v1, vote_v2

REGISTERED_ROUTES = (
    user.rt,
    restaurant.rt,
    vote_v1.rt,
    vote_v2.rt
)

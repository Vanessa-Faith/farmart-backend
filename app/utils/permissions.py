def is_farmer(user):
    return user.role == "farmer"


def owns_order(order, user):
    return order.buyer_id == user.id

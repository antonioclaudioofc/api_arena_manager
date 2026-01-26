from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    owner = "owner"
    client = "client"


class ReservationStatus(str, Enum):
    active = "active"
    cancelled = "cancelled"
    finished = "finished"
    cancel_requested = "cancel_requested"

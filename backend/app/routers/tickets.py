from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services import ticket_service as svc
from app.services import void_service

router = APIRouter(prefix="/tickets", tags=["tickets"])


class TicketLineIn(BaseModel):
    sku_code: str
    new_price: float


class TicketCreateIn(BaseModel):
    title: str
    effective_at: str
    note: str | None = None
    lines: list[TicketLineIn] = Field(default_factory=list)


class TicketVoidIn(BaseModel):
    # Default empty so a missing/blank reason reaches the service and returns the
    # domain-level 400「作废原因必填，需留痕」instead of a framework 422.
    reason: str = ""


@router.get("")
def list_tickets():
    return svc.list_tickets()


@router.get("/void-policy")
def get_void_policy():
    """The one global, mutually exclusive fate policy for applied tickets."""
    return void_service.policy()


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int):
    return svc.get_ticket(ticket_id)


@router.post("")
def create_ticket(body: TicketCreateIn):
    return svc.create_ticket(body.model_dump())


@router.post("/{ticket_id}/void", status_code=200)
def void_ticket(ticket_id: int, body: TicketVoidIn):
    return void_service.void_ticket(ticket_id, body.model_dump())

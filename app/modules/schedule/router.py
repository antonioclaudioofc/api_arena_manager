from fastapi import APIRouter, Depends
from app.modules.auth.dependencies import get_current_user
from app.modules.schedule.dependencies import get_schedule_service
from app.schemas.schedule import RequestScheduleBatch, UpdateSchedule
from app.modules.schedule.service import ScheduleService
from starlette import status
from app.shared.schemas import MessageResponse

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"]
)


@router.post("/batch", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
def create_batch(
    data: RequestScheduleBatch,
    user=Depends(get_current_user),
    schedule_service=Depends(get_schedule_service),
):
    schedule_service.create_batch(user, data)

    return {
        "message": "Horários criados com sucesso"
    }


@router.put("/{schedule_id}", response_model=MessageResponse)
def update(
    schedule_id: int,
    data: UpdateSchedule,
    user=Depends(get_current_user),
    schedule_service=Depends(get_schedule_service),
):
    schedule_service.update(user, data, schedule_id)

    return {
        "message": "Horário atualizado com sucesso"
    }


@router.delete("/{schedule_id}", response_model=MessageResponse)
def delete(
    schedule_id: int,
    user=Depends(get_current_user),
    schedule_service: ScheduleService = Depends(get_schedule_service),
):
    schedule_service.delete(user, schedule_id)

    return {
        "message": "Horário deletado com sucesso"
    }

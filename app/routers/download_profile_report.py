from fastapi import FastAPI, APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.celery.tasks.pdf_tasks import generate_user_profile_pdf
from io import BytesIO
import base64
from app.dependencies.user_deps import get_current_user

router = APIRouter(prefix="/user-profile", tags=["Profile Report"])

@router.get("/download", response_class=StreamingResponse)
async def download_profile(current_user=Depends(get_current_user)):
    user_id = current_user.id
    task_result = generate_user_profile_pdf.delay(user_id)
    base64_pdf = task_result.get(timeout=5)

    pdf_bytes = base64.b64decode(base64_pdf)
    buffer = BytesIO(pdf_bytes)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": f"inline; filename={current_user.username}_profile.pdf"})

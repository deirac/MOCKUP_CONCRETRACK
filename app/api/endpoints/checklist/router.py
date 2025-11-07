from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.api.endpoints.checklist.handlers import (
    checklist_page,
    get_checklists_data,
    get_checklist_details,
    create_checklist,
    update_checklist_item,
    complete_checklist
)

router = APIRouter()

# Register routes
router.get("/checklist", response_class=HTMLResponse, summary="Checklist Page")(checklist_page)
router.get("/api/checklists", summary="Get checklists data")(get_checklists_data)
router.get("/api/checklists/{checklist_id}", summary="Get checklist details")(get_checklist_details)
router.post("/api/checklists", summary="Create new checklist")(create_checklist)
router.put("/api/checklists/{checklist_id}/items/{item_id}", summary="Update checklist item")(update_checklist_item)
router.put("/api/checklists/{checklist_id}/complete", summary="Complete checklist")(complete_checklist)
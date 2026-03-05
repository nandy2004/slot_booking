from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import datetime

from database import get_db, engine
import models, schemas

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Seed initial slots (run once)
def seed_slots(db: Session):
    if db.query(models.Slot).count() == 0:
        times = [
            "09:00 AM - 09:30 AM",
            "09:30 AM - 10:00 AM",
            "10:00 AM - 10:30 AM",
            "10:30 AM - 11:00 AM",
            "11:00 AM - 11:30 AM",
            "11:30 AM - 12:00 PM",
            "02:00 PM - 02:30 PM",
            "02:30 PM - 03:00 PM",
        ]
        for t in times:
            db.add(models.Slot(slot_time=t))
        db.commit()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    seed_slots(db)
    slots = db.query(models.Slot).all()
    return templates.TemplateResponse("index.html", {"request": request, "slots": slots})


@app.post("/book")
def book_slot(
    slot_id: int = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    slot = db.query(models.Slot).filter(models.Slot.id == slot_id).first()
    if slot and not slot.is_booked:
        slot.is_booked = True
        slot.booked_by = name
        slot.booked_at = datetime.datetime.now()
        db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/cancel/{slot_id}")
def cancel_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = db.query(models.Slot).filter(models.Slot.id == slot_id).first()
    if slot and slot.is_booked:
        slot.is_booked = False
        slot.booked_by = None
        slot.booked_at = None
        db.commit()
    return RedirectResponse(url="/", status_code=303)
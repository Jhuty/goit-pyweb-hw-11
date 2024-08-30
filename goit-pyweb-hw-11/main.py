from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import db
from schemas import Contact, ContactCreate
from typing import List, Optional
from datetime import datetime, timedelta

models.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contacts API"}

@app.post("/contacts/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(db.get_db)):
    return crud.create_contact(db=db, contact=contact)

@app.get("/contacts/", response_model=List[Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts

@app.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(db.get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(db.get_db)):
    db_contact = crud.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(db.get_db)):
    db_contact = crud.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.get("/contacts/search", response_model=List[Contact])
def search_contacts(
    name: Optional[str] = None,
    surname: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(db.get_db)
):
    query = db.query(Contact)
    if name:
        query = query.filter(Contact.first_name.ilike(f"%{name}%"))
    if surname:
        query = query.filter(Contact.last_name.ilike(f"%{surname}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    
    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="Contacts not found")
    return results

@app.get("/contacts/upcoming-birthdays", response_model=List[Contact])
def get_upcoming_birthdays(db: Session = Depends(db.get_db)):
    today = datetime.today()
    upcoming = today + timedelta(days=7)
    
    contacts = db.query(Contact).filter(
        Contact.birthday.between(today, upcoming)
    ).all()
    
    if not contacts:
        raise HTTPException(status_code=404, detail="No upcoming birthdays found")
    
    return contacts

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from enum import Enum
import json

from app.db import get_db
from app.schemas import FacultyOut

app = FastAPI(title="Faculty API")


JSON_FIELDS = {
    "phone",
    "email",
    "teaching",
    "publications",
    "website_links",
}


def parse_row(row: dict) -> dict:
    data = dict(row)

    for field in JSON_FIELDS:
        value = data.get(field)
        if value is None:
            data[field] = None
        else:
            try:
                data[field] = json.loads(value)
            except Exception:
                data[field] = None

    return data


@app.get("/faculty", response_model=List[FacultyOut])
def get_all_faculty(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM faculty"))
    rows = result.mappings().all()
    return [parse_row(row) for row in rows]


@app.get("/faculty/{faculty_id}", response_model=FacultyOut)
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM faculty WHERE id = :id"),
        {"id": faculty_id}
    )
    row = result.mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return parse_row(row)


@app.get("/faculty/name/{faculty_name}", response_model=List[FacultyOut])
def get_by_name(faculty_name: str, db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            SELECT * FROM faculty
            WHERE LOWER(name) LIKE LOWER(:name)
        """),
        {"name": f"%{faculty_name}%"}
    )
    rows = result.mappings().all()
    return [parse_row(row) for row in rows]


class FacultyType(str, Enum):
    faculty = "faculty"
    adjunct_faculty = "adjunct-faculty"
    adjunct_faculty_international = "adjunct-faculty-international"
    distinguished_professor = "distinguished-professor"
    professor_practice = "professor-practice"


@app.get("/faculty/type/{faculty_type}", response_model=List[FacultyOut])
def get_by_type(
    faculty_type: FacultyType,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("SELECT * FROM faculty WHERE faculty_type = :t"),
        {"t": faculty_type.value}
    )
    rows = result.mappings().all()
    return [parse_row(row) for row in rows]


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

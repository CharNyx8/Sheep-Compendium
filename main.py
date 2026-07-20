from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep

app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    sheep = db.get_sheep(id)
    if sheep is None:
        raise HTTPException(status_code=404, detail="Sheep with this ID does not exist")
    return sheep

@app.post("/sheep", response_model=Sheep, status_code=status.HTTP_201_CREATED) # Status code 201
def add_sheep(sheep: Sheep):
    # Check if the sheep ID already exists to avoid duplicates
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")

    # Add the new sheep to the database
    db.data[sheep.id] = sheep
    return sheep # Return the newly added sheep data

@app.get("/sheep", response_model=list[Sheep])
def read_all_sheep():
    # Return every sheep currently stored in the database
    return list(db.data.values())

@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, sheep: Sheep):
    # Check that the sheep exists before trying to update it
    if id not in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID does not exist")

    # Update the sheep record
    db.data[id] = sheep
    return sheep

@app.delete("/sheep/{id}", response_model=list[Sheep])
def delete_sheep(id: int):
    # Check that the sheep exists before trying to delete it
    if id not in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID does not exist")

    # Remove the sheep from the database
    db.data.pop(id)

    # Return the full remaining list of sheep
    return list(db.data.values())
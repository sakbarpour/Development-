from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from HyperMin import load_hyperspectral_data, detect_mineral_hotspots

class UserInput(BaseModel):
    datacollection: str
    date: str
    mineral_signature: float

app = FastAPI()

@app.post("/detect-hotspots/")
async def detect_hotspots(user_input: UserInput):
    try:
        data_collection = load_hyperspectral_data(user_input.datacollection, user_input.date)
        hotspots = detect_mineral_hotspots(data_collection, user_input.mineral_signature)
        return {"hotspots": hotspots.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

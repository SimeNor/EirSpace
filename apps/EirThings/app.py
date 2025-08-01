import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv, find_dotenv

# Load the environment variables
load_dotenv(find_dotenv())

# Import the scales
from api_utils import load_scales, check_scale_exists
import uvicorn

scales = load_scales(vault_root=os.getenv("VAULT_ROOT"))

# Create a FastAPI app
app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Welcome to the scale API",
        "endpoints": {
            "/status/{scale_id}": "Get the status of the scale",
            "/tare/{scale_id}": "Tare the scale",
            "/calibrate/{scale_id}": "Calibrate the scale",
            "/read/{scale_id}": "Read the scale",
        },
        "loaded_scales": list(scales.keys()),
        "scale_status": {scale_id: scales[scale_id].status() for scale_id in scales},
    }


@app.get("/status/{scale_id}")
async def get_status(scale_id: str):
    check_scale_exists(scale_id, scales)
    return {"scale_id": scale_id, "status": scales[scale_id].status()}


@app.post("/tare/{scale_id}")
async def tare_scale(scale_id: str):
    check_scale_exists(scale_id, scales)

    if scales[scale_id].tare():
        return {"scale_id": scale_id, "status": "tared"}
    else:
        raise HTTPException(status_code=400, detail="Tare failed")


@app.post("/calibrate/{scale_id}")
async def calibrate_scale(scale_id: str, weight: float, unit: str | None = "kg"):
    check_scale_exists(scale_id, scales)

    if scales[scale_id].calibrate(weight, unit):
        return {"scale_id": scale_id, "status": "calibrated"}
    else:
        raise HTTPException(status_code=400, detail="Calibration failed")


@app.get("/read/{scale_id}")
async def read_scale(scale_id: str, unit: str | None = "kg"):
    check_scale_exists(scale_id, scales)
    result = scales[scale_id].read(unit)

    # Add the scale_id to the result
    return {"scale_id": scale_id, "weight": result, "unit": unit}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

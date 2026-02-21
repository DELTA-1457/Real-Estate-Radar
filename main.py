from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import engine_core  # <--- เรียกใช้ไฟล์สมองกล

app = FastAPI()

# ตั้งค่า CORS ให้ GitHub Pages เข้าถึงได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PropertyData(BaseModel):
    price_per_sqm: float
    zone: str
    distance: float
    age: int

@app.post("/api/scan")
async def scan_property(data: PropertyData):
    try:
        # สมองกลต้องการ 4 ค่า เราก็ดึงจากหน้าเว็บ (data) ส่งไปให้ครบ 4 ค่า!
        final_score = engine_core.calculate_secret_score(
            data.price_per_sqm,
            data.zone,
            data.distance,
            data.age
        )
        
        return {
            "status": "success",
            "score": final_score,
            "version": engine_core.get_version(),
            "note": "Calculated by Encrypted Engine"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
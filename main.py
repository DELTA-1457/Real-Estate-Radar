from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import engine_core  # <--- เรียกใช้ไฟล์ลับ .pyd ของคุณ

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
        # ใช้สมองกลจาก engine_core.pyd คำนวณ (คนอื่นจะดูสูตรข้างในไม่ได้)
        # หมายเหตุ: ชื่อฟังก์ชันต้องตรงกับที่มีใน .pyd (อ้างอิงจาก test.py ของคุณ)
        final_score = engine_core.calculate_secret_score(data.price_per_sqm)
        
        # คุณสามารถเพิ่มตรรกะพื้นฐานอื่นๆ ประกอบได้ในนี้ 
        # เพื่อให้หน้าเว็บแสดงผลได้ครบถ้วน
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
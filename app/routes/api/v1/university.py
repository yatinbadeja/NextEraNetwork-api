from fastapi import APIRouter
from typing import List
from fastapi.responses import ORJSONResponse
from app.utils.cloudinary_client import cloudinary_client
from app.database.repositories.university import university_repo
from fastapi import File,UploadFile
import app.http_exception as excpetion
from app.database.models.university import UniversityBase,UniversityDB

university = APIRouter()

@university.post("/university/create",response_class=ORJSONResponse)
async def universityCreate(
    university_name : str = "",
    university_image : UploadFile = File(...),
    university_address: str = ""
):
    universityExists = await university_repo.findOne({
        "universityName":university_name
    })
    if universityExists is not None:
        raise excpetion.ResourceConflictException()
    
    universityProfileUrl = cloudinary_client.upload_file(university_image)
    
    universityDict = {
        "universityName":university_name,
        "universityImage":universityProfileUrl,
        "address":university_address
    }
    
    await university_repo.new(UniversityBase(**universityDict))
    
    return {
        "success":True,
        "message":"University created Successfully",
        "status_code":200
    }
    
@university.get("/get/university",response_class=ORJSONResponse)
async def getUniversityCollege():
    UniversityList = await university_repo.collection.aggregate([
        {"$project":{
            "created_at":0,
            "updated_at":0    
        }}
    ]).to_list(None)
    
    return {
        "success":True,
        "message":"Data Fetched Successfully",
        "data" :UniversityList
    } 


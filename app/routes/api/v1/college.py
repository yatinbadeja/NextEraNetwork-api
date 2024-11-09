from fastapi import APIRouter
from typing import List
from fastapi.responses import ORJSONResponse
from app.utils.cloudinary_client import cloudinary_client
from app.database.repositories.college import college_repo
from app.database.repositories.university import university_repo
from fastapi import File,UploadFile
from app.database.repositories.branch import branch_repo
from app.database.repositories.courses import course_repo
import app.http_exception as excpetion
from app.schema.inputModel import experienceCreate
# from app.schema.inputModel import ProfileCreate
from app.database.models.branch import BranchBase
from app.database.models.department import DepartmentBase,DepartmentDB
from app.database.repositories.department import department_repo
from app.database.models.college import CollegeBase,CollegeDB
from app.schema.enums import DepartmentType,CourseType,BranchType
from app.database.models.course import CourseBase,CourseDB
from app.database.repositories.profile import profile_repo
from app.database.repositories.user import user_repo
from app.database.models.profile import ProfileBase
from app.database.repositories.courses import course_repo
from app.schema.token import TokenData
import app.http_exception as http_exception
from app.database.models.profile import ProfileBase
from app.oauth2 import get_current_user
from fastapi import Depends
import datetime
from app.database.repositories.experience import experience_repo
from app.database.models.experience import ExperienceBase
college = APIRouter()

@college.post("/college/create",response_class=ORJSONResponse)
async def collegeCreate(
    college_name : str = "",
    college_image : UploadFile = File(...),
    university_id: str = "",
    city : str = ""
):
    universityExists = await university_repo.findOne({
        "_id":university_id
    })
    if universityExists is None:
        return {
            "success":False,
            "message":"university not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    collegeExists = await college_repo.findOne({
        "collegeName":college_name
    })
    if collegeExists is not None:
        return {
            "success":False,
            "message":"college not found",
            "status_code":excpetion.ResourceConflictException()
        }
        
    college_image_url = cloudinary_client.upload_file(college_image)
    collegeDict = {
        "collegeName":college_name,
        "college_image":college_image_url,
        "university_id":university_id,
        "city":city
    }
    
    await college_repo.new(CollegeBase(**collegeDict))
    
    return {
        "success":True,
        "message":"College created Successfully",
        "status_code":200
    }
    
@college.get("/university/college/{university_id}",response_class=ORJSONResponse)
async def getUniversityCollege(
    university_id : str = "",
):
    universityExists = await university_repo.findOne({
        "_id":university_id
    })
    
    if universityExists is None:
        return {
            "success":False,
            "message":"university not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    
    pipeline = [
       {
            "$match":{
                "_id":university_id
            },
            
        },
        {
            "$lookup":{
                "from":"college",
                "localField":"_id",
                "foreignField":"university_id",
                "as":"college"
            }
        },
        {
            "$project":{
                "created_at":0,
                "updated_at":0,
                "college.created_at":0,
                "college.updated_at":0
            }
        } 
    ]
        
    collegeUniversity = await university_repo.collection.aggregate(pipeline=pipeline).to_list(None)

    return {
        "success":True,
        "message":"Data Fetched Successfully",
        "data":collegeUniversity
    }
    
@college.post("/create/department",response_class = ORJSONResponse)
async def departmentCreate(
    university_id : str = "",
    college_id : str = "",
    dept_name : DepartmentType = DepartmentType.ai
):
    universityExists = await university_repo.findOne({
        "_id":university_id
    })
    if universityExists is None:
        return {
            "success":False,
            "message":"University not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    collegeExists = await college_repo.findOne({
        "_id":college_id,
        "university_id":university_id
    })
    if collegeExists is None:
        return {
            "success":False,
            "message":"college not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    
    dept_dict = {
        "university_id":university_id,
        "college_id":college_id,
        "departmentName":dept_name
    }
    await department_repo.new(DepartmentBase(**dept_dict))
        
@college.get("/college/department",response_class=ORJSONResponse)
async def getCollegeDept(
    college_id : str = "",
    university_id : str = ""
):
    deptExists = await college_repo.findOne({
        "_id":college_id,
        "university_id":university_id
    })
    if deptExists is None:
        raise excpetion.ResourceNotFoundException()
    
    data = await university_repo.collection.aggregate([
        {
            "$match":{
                "_id":university_id
            }
        },
        {
            "$lookup":{
                "from":"college",
                "let":{"university_id":"$_id"},
                "pipeline":[
                    {
                        "$match":{
                            "$expr":{
                                "$and":[
                                    {"$eq":["$$university_id","$university_id"]},
                                    {"$eq":["$_id",college_id]}
                                ]
                            }
                        }
                    }
                ],
                "as":"collegeData"
            }
        },
        {
            "$set":{
                "college":{"$first":"$collegeData"}
            }
        },
        {
            "$project":{
                "collegeData":0
            }
        },
        {
            "$set":{
                "college_id":"$college._id",
                "college_name":"$college.collegeName",
                "college_city":"$college.city",
                "college_image":"$college.college_image"
            }
        },
        {
            "$project":{
                "college":0,  
                "created_at":0,
                "updated_at":0
            }
        },
        {
            "$lookup":{
                "from":"department",
                "let":{"university_id":"$_id","college_id":"$college_id"},
                "pipeline":[
                    {
                        "$match":{
                            "$expr":{
                                "$and":[
                                    {"$eq":["$$university_id","$university_id"]},
                                    {"$eq":["$$college_id","$college_id"]}
                                ]
                            }
                        }
                    }
                ],
                "as":"dept"
            }
        },
        {
            "$project":{
                "dept.university_id":0,
                "dept.created_at":0,
                "dept.updated_at":0,
                "dept.college_id":0,
            }
        }
    ]).to_list(None)
    return {
        "success":True,
        "message":"Data Fetched Successfully",
        "data":data
    }

@college.post("/create/courses",response_class = ORJSONResponse)
async def coursesCreate(
    university_id : str = "",
    college_id : str = "",
    dept_id : str = "",
    courses_name : CourseType =CourseType.Btech
):
    universityExists = await university_repo.findOne({
        "_id":university_id
    })
    if universityExists is None:
        return {
            "success":False,
            "message":"University not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    collegeExists = await college_repo.findOne({
        "_id":college_id,
        "university_id":university_id
    })
    if collegeExists is None:
        return {
            "success":False,
            "message":"college not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    deptExists = await department_repo.findOne({
        "_id":dept_id,
        "university_id":university_id,
        "college_id":college_id
    })
    if deptExists is None:
        return {
            "success":False,
            "message":"Dept not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    
    courses_dict = {
        "university_id":university_id,
        "college_id":college_id,
        "department_id":dept_id,
        "courseName":courses_name
    }
    await course_repo.new(CourseBase(**courses_dict))
 
@college.get("/college/course",response_class=ORJSONResponse)
async def getDeptCouses(
    college_id : str = "",
    university_id : str = "",
    dept_id : str = ""
):
    deptExists = await department_repo.findOne({
        "_id":dept_id,
        "university_id":university_id,
        "college_id":college_id
    })
    if deptExists is None:
        raise excpetion.ResourceNotFoundException()
    
    data = await university_repo.collection.aggregate([
        {
            "$match":{
                "_id":university_id
            }
        },
        {
            "$lookup":{
                "from":"college",
                "let":{"university_id":"$_id"},
                "pipeline":[
                    {
                        "$match":{
                            "$expr":{
                                "$and":[
                                    {"$eq":["$$university_id","$university_id"]},
                                    {"$eq":["$_id",college_id]}
                                ]
                            }
                        }
                    }
                ],
                "as":"collegeData"
            }
        },
        {
            "$set":{
                "college":{"$first":"$collegeData"}
            }
        },
        {
            "$project":{
                "collegeData":0
            }
        },
        {
            "$set":{
                "college_id":"$college._id",
                "college_name":"$college.collegeName",
                "college_city":"$college.city",
                "college_image":"$college.college_image"
            }
        },
        {
            "$project":{
                "college":0,  
                "created_at":0,
                "updated_at":0
            }
        },
        {
            "$lookup":{
                "from":"department",
                "let":{"university_id":"$_id","college_id":"$college_id"},
                "pipeline":[
                    {
                        "$match":{
                            "$expr":{
                                "$and":[
                                    {"$eq":["$$university_id","$university_id"]},
                                    {"$eq":["$$college_id","$college_id"]},
                                    {"$eq":["$_id",dept_id]}
                                ]
                            }
                        }
                    }
                ],
                "as":"dept"
            }
        },
        {
            "$set":{
                "department":{"$first":"$dept"}
            }
        },
        {
            "$project":{
                "dept":0
            }
        },
        {
            "$set":{
                "dept_id":"$department._id",
                "dept_name":"$department.departmentName",
            }
        },
        {
            "$project":{
                "dept.university_id":0,
                "dept.created_at":0,
                "dept.updated_at":0,
                "dept.college_id":0,
                "department":0
            }
        },
        {
            "$lookup":{
                "from":"courses",
                "let":{
                    "university_id":"$_id",
                    "college_id":"$college_id",
                    "department_id":"$dept_id"
                },
                "pipeline":[
                    {
                        "$match":{
                            "$expr":{
                                "$and":[
                                    {"$eq":["$$university_id","$university_id"]},
                                    {"$eq":["$$college_id","$college_id"]},
                                    {"$eq":["$department_id","$$department_id"]}
                                ]
                            }
                        }
                    }
                ],
                "as":"Courses"
            }
        },
        {
            "$project":{
                "Courses.university_id":0,
                "Courses.college_id":0,
                "Courses.department_id":0,
                "Courses.created_at":0,
                "Courses.updated_at":0
            }
        }
    ]).to_list(None)
    return {
        "success":True,
        "message":"Data Fetched Successfully",
        "data":data
    }

@college.post("/create/branch",response_class = ORJSONResponse)
async def branchCreate(
    university_id : str = "",
    college_id : str = "",
    dept_id : str = "",
    course_id : str = "",
    branch_name : BranchType = BranchType.ai
):
    universityExists = await university_repo.findOne({
        "_id":university_id
    })
    if universityExists is None:
        return {
            "success":False,
            "message":"University not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    collegeExists = await college_repo.findOne({
        "_id":college_id,
        "university_id":university_id
    })
    if collegeExists is None:
        return {
            "success":False,
            "message":"college not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    deptExists = await department_repo.findOne({
        "_id":dept_id,
        "university_id":university_id,
        "college_id":college_id
    })
    if deptExists is None:
        return {
            "success":False,
            "message":"Dept not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    
    coursesExists = await course_repo.findOne({
        "_id":course_id,
        "university_id":university_id,
        "college_id":college_id,
        "department_id":dept_id
    })
    if coursesExists is None:
        return {
            "success":False,
            "message":"courses not found",
            "status_code":excpetion.ResourceNotFoundException()
        }
    
    branchDict = {
        "university_id":university_id,
        "college_id":college_id,
        "department_id":dept_id,
        "course_id":course_id,
        "branchName":branch_name
    }
    await branch_repo.new(BranchBase(**branchDict))

    return {
        "success":True,
        "message":"branch created successfully"
    }

@college.get("/college/branch",response_class=ORJSONResponse)
async def getDeptCouses(
    college_id : str = "",
    university_id : str = "",
    dept_id : str = "",
    course_id : str = ""
):
    deptExists = await department_repo.findOne({
        "_id":dept_id,
        "university_id":university_id,
        "college_id":college_id
    })
    if deptExists is None:
        raise excpetion.ResourceNotFoundException()
    
    data = await university_repo.collection.aggregate([
        {
            "$match":{
                "_id":university_id
            }
        },
        {
            "$lookup":{
                "from":"college",
                "let":{"university_id":"$_id"},
                "pipeline":[
                    {
                        "$match":{
                            "$expr":{
                                "$and":[
                                    {"$eq":["$$university_id","$university_id"]},
                                    {"$eq":["$_id",college_id]}
                                ]
                            }
                        }
                    }
                ],
                "as":"collegeData"
            }
        },
        {
            "$set":{
                "college":{"$first":"$collegeData"}
            }
        },
        {
            "$project":{
                "collegeData":0
            }
        },
        {
            "$set":{
                "college_id":"$college._id",
                "college_name":"$college.collegeName",
                "college_city":"$college.city",
                "college_image":"$college.college_image"
            }
        },
        {
            "$project":{
                "college":0,  
                "created_at":0,
                "updated_at":0
            }
        },
        {
            "$lookup":{
                "from":"department",
                "let":{"university_id":"$_id","college_id":"$college_id"},
                "pipeline":[
                    {
                        "$match":{
                            "$expr":{
                                "$and":[
                                    {"$eq":["$$university_id","$university_id"]},
                                    {"$eq":["$$college_id","$college_id"]},
                                    {"$eq":["$_id",dept_id]}
                                ]
                            }
                        }
                    }
                ],
                "as":"dept"
            }
        },
        {
            "$set":{
                "department":{"$first":"$dept"}
            }
        },
        {
            "$project":{
                "dept":0
            }
        },
        {
            "$set":{
                "dept_id":"$department._id",
                "dept_name":"$department.departmentName",
            }
        },
        {
            "$project":{
                "dept.university_id":0,
                "dept.created_at":0,
                "dept.updated_at":0,
                "dept.college_id":0,
                "department":0
            }
        },
        {
            "$lookup":{
                "from":"courses",
                "let":{
                    "university_id":"$_id",
                    "college_id":"$college_id",
                    "department_id":"$dept_id",
                },
                "pipeline":[
                    {
                        "$match":{
                            "$expr":{
                                "$and":[
                                    {"$eq":["$$university_id","$university_id"]},
                                    {"$eq":["$$college_id","$college_id"]},
                                    {"$eq":["$department_id","$$department_id"]},
                                    {"$eq":["$_id",course_id]}
                                ]
                            }
                        }
                    }
                ],
                "as":"Courses"
            }
        },
        {
            "$set":{
                "coursesFirst":{"$first":"$Courses"}
            }
        },
        {
            "$project":{
                "Courses":0
            }
        },
        {
            "$lookup":{
                "from":"branch",
                "let":{
                    "university_id":"$_id",
                    "college_id":"$college_id",
                    "department_id":"$dept_id",
                    "course_id":"$coursesFirst._id"
                },
                "pipeline":[
                    {
                        "$match":{
                            "$expr":{
                                "$and":[
                                    {"$eq":["$$university_id","$university_id"]},
                                    {"$eq":["$$college_id","$college_id"]},
                                    {"$eq":["$department_id","$$department_id"]},
                                    {"$eq":["$course_id","$$course_id"]}
                                ]
                            }
                        }
                    }
                ],
                "as":"branch"
            }
        },
        {
            "$project":{
                "coursesFirst":0,
                "branch.university_id":0,
                "branch.created_at":0,
                "branch.updated_at":0,
                "branch.college_id":0,
                "branch.department_id":0  
            }
        }
    ]).to_list(None)
    return {
        "success":True,
        "message":"Data Fetched Successfully",
        "data":data
    }

@college.post('/profile/create',response_class = ORJSONResponse)
async def profileCreate(
    data : ProfileBase,
    current_user : TokenData = Depends(get_current_user),
):
    if current_user.user_type != "Student":
        raise http_exception.CredentialsInvalidException()
    
    userProfileID = current_user.profile_id
    print(userProfileID)
    print(data)
    profileDict = {
        "firstname": data.firstname,
        "middlename":data.middlename,
        "lastname":data.lastname,
        "gender" : data.gender,
        "abcID" : data.abcID,
        "category" : data.category.value,
        "profession" : data.profession,
        "position": data.position,
        "state" : data.state,
        "about" : data.about,
        "passOut_Year" : data.passOut_Year,
        "skills": data.skills,
        "hobbies": data.hobbies,
        "links": data.links,
        "languages": data.languages,
        "university" : data.university,
        "college": data.college,
        "department" : data.department,
        "courses" : data.courses,
        "branch" : data.branch,
        "enrollmentNumber": data.enrollmentNumber,
        "enrollmentID" : data.enrollmentID,
    }
    
    profile = await profile_repo.new(ProfileBase(**profileDict))
    print("Profile Created")
    print(profile)
    print(type(profile))
    await user_repo.update_one(
        {"profileID":userProfileID},
        {
            "$set":{
                "profileID":profile
            }
        }
    )
    return {
        "success":True,
        "message":"Data Fetched Successfully"
    }

@college.get('/student/profile',response_class = ORJSONResponse)
async def studentProfile(
    current_user : TokenData = Depends(get_current_user)
):
    if current_user.user_type != "Student":
        raise http_exception.CredentialsInvalidException()
    print(current_user.profile_id)
    userExists = await user_repo.findOne({
        "_id":current_user.user_id
    })
    if userExists is None:
        raise http_exception.ResourceNotFoundException()
    profileExists = await profile_repo.findOne({
        "_id":userExists["profileID"]
    })
    if profileExists is None:
        raise http_exception.ResourceNotFoundException()
    
    return {
        "success":True,
        "message":"Data Fetched SuccessFully",
        "data":profileExists
    }

@college.post("/create/experience",response_class=ORJSONResponse)
async def createExprience(
    experience : experienceCreate,
    current_user : TokenData = Depends(get_current_user)
):
    if current_user.user_type != "Student":
        raise http_exception.CredentialsInvalidException()
    
    profileID = await user_repo.findOne({
        "_id":current_user.user_id
    })
    if profileID is None:
        raise http_exception.ResourceNotFoundException()
    
    if experience.start_date != "":
        start_date = datetime.datetime.strptime(experience.start_date, "%Y-%m-%d")
    if experience.end_date != "":
        end_date = datetime.datetime.strptime(experience.end_date, "%Y-%m-%d")
    profileID = profileID["profileID"]
    
    experienceDict = {
        "profile_id":profileID,
        "jobTitle":experience.jobTitle,
        "experienceType":experience.experienceType,
        "companyName":experience.companyName,
        "description":experience.description,
        "jobMode":experience.jobMode.value,
        "location":experience.location,
        "start_date": start_date,
        "end_date":end_date,
        "continuing":experience.continuing
    }
    
    await experience_repo.new(ExperienceBase(**experienceDict))
    
    return {
        "success":True,
        "message":"Data Inserted Successfully"
    }
    

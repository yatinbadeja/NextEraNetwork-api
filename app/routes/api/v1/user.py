from fastapi import APIRouter, status, Response, Depends,Form,File,UploadFile
from fastapi.responses import ORJSONResponse
from app.schema.inputModel import userCreate
from app.database.repositories.user import user_repo
import app.http_exception as http_expection
from app.utils.password import generatePassword
from app.utils.mailer_module import mail,template
from app.database.models.user import UserBase,UserDB
from app.schema.token import TokenData
from app.database.models.education import EducationBase,EducationDB
from app.oauth2 import get_current_user
import datetime
from app.schema.inputModel import ProjectCreate
from app.database.repositories.experience import experience_repo
from typing import List
from app.database.models.project import ProjectBase
from app.database.repositories.project import project_repo
from app.database.models.experience import ExperienceBase,ExperienceDB
from app.database.repositories.education import education_repo
from app.schema.inputModel import EducationCreate,AchievementCreate
from app.database.models.certification import CertificationBase
from app.schema.inputModel import CertificationCreate
from app.database.repositories.certification import certification_repo
from app.utils.cloudinary_client import cloudinary_client
from typing import Optional
from app.database.models.achievement import AchievementBase
from app.database.repositories.achievements import achievement_repo
user =  APIRouter()

@user.post("/auth/create",response_class=ORJSONResponse)
async def userCreateAPI(
    user: userCreate
):
    userExists = await user_repo.findOne({"email":user.email,"accountType":user.accountType})
    if userExists is not None:
        raise http_expection.ResourceConflictException()
    password = generatePassword.createPassword()
    mail.send(
        "Welcome to NextEraNetwork",
        user.email,
        template.Onboard(user.accountType.value, user.email, password),
    )  
    print(password)
    print("Mail sent")
    userInstance = {
        "username" :user.username,
        "password" : password,
        "email" : user.email,
        "accountType" : user.accountType.value,
        "profileID" : None
    }
    await user_repo.new(UserBase(**userInstance))
    
    return {
        "Success":True,
        "message":"User created successfully"
    }
    
@user.put("/user/edit/{user_id}",response_class=ORJSONResponse)
async def userEdit(
    current_user :TokenData = Depends(get_current_user),
    user_id : str = "",
    username : str = "",
    useremail : str = ""
):
    if current_user.user_type != "Student":
        raise http_expection.CredentialsInvalidException()
    
    userExists = await user_repo.findOne({"_id":user_id})
    if not userExists:
        raise http_expection.ResourceNotFoundException()
    
    keys = ["username","useremail"]
    values = [username,useremail]
    
    updatedValues = {}
    
    for key,value in zip(keys,values):
        if value != "":
            updatedValues[key] = value
            
    await user_repo.update_one({"_id":user_id},{"$set":updatedValues})
    
    return {
        "success":True,
        "message":"User data successfully..."
    }
   
@user.post("/create/education",response_class=ORJSONResponse)
async def createStudentEducation(
    experience : EducationCreate,
    current_user: TokenData = Depends(get_current_user)
):
    print(current_user.user_type)
    if current_user.user_type != "Student":
        raise http_expection.CredentialsInvalidException()
    create = {
        "profile_id":current_user.profile_id
    }
    if current_user.profile_id != None:
        for keys,values in dict(experience).items():
            if keys in ["start_date","end_date"]:
                create[keys] = datetime.datetime.strptime(getattr(experience,keys), "%Y-%m-%d")
            else:
                create[keys] = values
    
    print(create)
    
    await education_repo.new(EducationBase(**create))
    
    return {
        "success":True,
        "message":"Experience Created Successfully"
    }
    
@user.post("/create/certification",response_class=ORJSONResponse)
async def createStudentCertification(
    certificationName : Optional[str] = Form(None),
    issuingOrganization : Optional[str] = Form(None),
    certificateURL : UploadFile = File(None),
    issue_date : Optional[str] = Form(None),
    expiry_date : Optional[str] = Form(None),
    description : Optional[str] = Form(None),
    current_user: TokenData = Depends(get_current_user)
):
    print(current_user.user_type)
    if current_user.user_type != "Student" and current_user.user_type != "University":
        raise http_expection.CredentialsInvalidException()
    if certificateURL is not None:
        certificateURL = cloudinary_client.upload_file(certificateURL)

    create = {
        "profile_id":current_user.profile_id,
        "certificateURL":certificateURL
    }
    
    value = [certificationName,issuingOrganization,issue_date,expiry_date,description]
    key = ["certificationName","issuingOrganization","issue_date","expiry_date","description"]
    if current_user.profile_id != None:
        for keys,values in zip(key,value):
            if values == None:
                create[keys] = None
            elif keys in ["issue_date","expiry_date"]:
                create[keys] = datetime.datetime.strptime(values, "%Y-%m-%d")
            else:
                create[keys] = values

    print(create)
    
    await certification_repo.new(CertificationBase(**create))
    
    return {
        "success":True,
        "message":"Certification Created Successfully"
    }

@user.post("/create/achievement",response_class=ORJSONResponse)
async def createStudentAchievement(
    achievement : AchievementCreate,
    current_user: TokenData = Depends(get_current_user)
):
    print(current_user.user_type)
    if current_user.user_type != "Student" and current_user.user_type != "University":
        raise http_expection.CredentialsInvalidException()


    create = {
        "profile_id":current_user.profile_id,
    }
    
    if current_user.profile_id != None:
        for keys,values in dict(achievement).items():
            if values == None:
                create[keys] = None
            elif keys in ["date_achieved"]:
                create[keys] = datetime.datetime.strptime(getattr(achievement,keys), "%Y-%m-%d")
            else:
                create[keys] = values

    print(create)
    
    await achievement_repo.new(AchievementBase(**create))
    
    return {
        "success":True,
        "message":"Certification Created Successfully"
    }

@user.post("/create/project",response_class=ORJSONResponse)
async def createStudentProject(
    project : ProjectCreate,
    current_user: TokenData = Depends(get_current_user)
):
    print(current_user.user_type)
    if current_user.user_type != "Student" and current_user.user_type != "University":
        raise http_expection.CredentialsInvalidException()
    if projectURL is not None:
        projectURL = cloudinary_client.upload_file(projectURL)

    create = {
        "profile_id":current_user.profile_id,
    }
    
    key = ["description","technology","projectName","start_date","end_date","projectURL"]
    if current_user.profile_id != None:
        for values in key:
            if getattr(project,values) == None:
                create[values] = None
            elif values in ["start_date","end_date"]:
                create[values] = datetime.datetime.strptime(getattr(project,values), "%Y-%m-%d")
            else:
                create[values] = getattr(project,values)

    print(create)
    
    await project_repo.new(ProjectBase(**create))
    
    return {
        "success":True,
        "message":"Project Created Successfully"
    }

@user.delete("/delete/user/details",response_class=ORJSONResponse)
async def deleteUserDetails(
    current_user: TokenData = Depends(get_current_user),
    experienceList : List[str] = [],
    educationList : List[str] = [],
    projectList : List[str] = [],
    certificationList : List[str] = [],
    achievementList : List[str] = [],
):
    if current_user.user_type != "Student" and current_user.user_type != "University":
        raise http_expection.CredentialsInvalidException()
    
    repoList = [experience_repo,education_repo,project_repo,certification_repo,achievement_repo]
    Listing = {
        "experienceList":experienceList,
        "educationList":educationList,
        "projectList":projectList,
        "certificationList":certificationList,
        "achievementList":achievementList
    }
    count = 0
    for keys,values in Listing.items():
        if len(values) != 0:
            for element in values:
                repo = repoList[count]
                await repo.deleteAllById(values)
        count = count + 1   
        
    return {
        "success":True,
        "message":"Document Updated Successfully..."
    } 
    
@user.get("/user/experience",response_class=ORJSONResponse)
async def userExperience(
    current_user : TokenData = Depends(get_current_user)
):
    if current_user.user_type != "Student" and current_user.user_type != "University":
        raise http_expection.CredentialsInvalidException()
    
    experience = await experience_repo.collection.aggregate(
        [
            {
                "$match":{
                    "profile_id":current_user.profile_id
                }
            },
            {
                "$project":{
                    "created_at":0,
                    "updated_at":0
                }
            }
        ]
    ).to_list(None)
    
    return {
        "success":True,
        "message":"Data Fetched Successfully",
        "data":experience
    }

@user.get("/user/project",response_class=ORJSONResponse)
async def userProject(
    current_user : TokenData = Depends(get_current_user)
):
    if current_user.user_type != "Student" and current_user.user_type != "University":
        raise http_expection.CredentialsInvalidException()
    
    project = await project_repo.collection.aggregate(
        [
            {
                "$match":{
                    "profile_id":current_user.profile_id
                }
            },
            {
                "$project":{
                    "created_at":0,
                    "updated_at":0
                }
            }
        ]
    ).to_list(None)
    
    return {
        "success":True,
        "message":"Data Fetched Successfully",
        "data":project
    }

@user.get("/user/achievement",response_class=ORJSONResponse)
async def userAchievement(
    current_user : TokenData = Depends(get_current_user)
):
    if current_user.user_type != "Student" and current_user.user_type != "University":
        raise http_expection.CredentialsInvalidException()
    
    achievement = await achievement_repo.collection.aggregate(
        [
            {
                "$match":{
                    "profile_id":current_user.profile_id
                }
            },
            {
                "$project":{
                    "created_at":0,
                    "updated_at":0
                }
            }
        ]
    ).to_list(None)
    
    return {
        "success":True,
        "message":"Data Fetched Successfully",
        "data":achievement
    }
    
@user.get("/user/certificate",response_class=ORJSONResponse)
async def userProject(
    current_user : TokenData = Depends(get_current_user)
):
    if current_user.user_type != "Student" and current_user.user_type != "University":
        raise http_expection.CredentialsInvalidException()
    
    certification_repo = await certification_repo.collection.aggregate(
        [
            {
                "$match":{
                    "profile_id":current_user.profile_id
                }
            },
            {
                "$project":{
                    "created_at":0,
                    "updated_at":0
                }
            }
        ]
    ).to_list(None)
    
    return {
        "success":True,
        "message":"Data Fetched Successfully",
        "data":certification_repo
    }
    
@user.get("/user/education",response_class=ORJSONResponse)
async def userProject(
    current_user : TokenData = Depends(get_current_user)
):
    if current_user.user_type != "Student" and current_user.user_type != "University":
        raise http_expection.CredentialsInvalidException()
    
    education = await education_repo.collection.aggregate(
        [
            {
                "$match":{
                    "profile_id":current_user.profile_id
                }
            },
            {
                "$project":{
                    "created_at":0,
                    "updated_at":0
                }
            }
        ]
    ).to_list(None)
    
    return {
        "success":True,
        "message":"Data Fetched Successfully",
        "data":education
    }
    
    
@user.get('/get/user/details',response_class=ORJSONResponse)
async def getUserDetails(
    current_user : TokenData = Depends(get_current_user)
):
    if current_user.user_type != "Student" and current_user.user_type != "University":
        raise http_expection.CredentialsInvalidException()
    
    current_user.user_id = "LEAVE-0009"
    pipeline = [
        {
            "$match":{
                "_id":current_user.user_id
            }
        },
        {
            "$lookup":{
                "from":"profile",
                "localField":"profileID",
                "foreignField":"_id",
                "as":"profileData"
            }
        },
        {
            "$set":{
                "profile":{"$arrayElemAt":["$profileData",0]}
            }
        },
        {
            "$lookup":{
                "from":"college",
                "localField":"profile.college",
                "foreignField":"_id",
                "as":"collegeData"
            }
        },
        {
            "$set":{
                "college":{"$arrayElemAt":["$collegeData",0]}
            }
        },
        {
            "$project":{
                "collegeData":0
            }
        },
        {
            "$lookup":{
                "from":"university",
                "localField":"profile.university",
                "foreignField":"_id",
                "as":"universityData"
            }
        },
        {
            "$set":{
                "university":{"$arrayElemAt":["$universityData",0]}
            }
        },
        {
            "$project":{
                "universityData":0
            }
        },
        {
            "$lookup":{
                "from":"branch",
                "localField":"profile.branch",
                "foreignField":"_id",
                "as":"branchData"
            }
        },
        {
            "$set":{
                "branch":{"$arrayElemAt":["$branchData",0]}
            }
        },
        {
            "$project":{
                "branchData":0
            }
        },
        {
            "$set":{
                "branchName":"$branch.branchName",
                "universityName":"$university.universityName",
                "collegeName":"$college.collegeName",
            }
        },
        {
            "$project":{
                "created_at":0,
                "updated_at":0,
                "profileData":0,
                "profile":0,
                "college":0,
                "university":0,
                "branch":0
            }
        }
    ]
    
    return await user_repo.collection.aggregate(pipeline=pipeline).to_list(None)
from fastapi import FastAPI ,HTTPException,Depends
from pydantic import BaseModel
from typing import List,Annotated,Optional
from database import get_database_url,engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from models import EmploiyesModel,DemandeModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import models
from print.Demande_de_prêt import generate_demande_de_prêt
from print.demande_de_subvention import generate_demande_pdf_type_d
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
DATABASE_URL = get_database_url()
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

class EmploiyesBase(BaseModel):
    NumCompte: str
    Nom: str
    Grade: str
    Poste: str
    lieu_de_travail: str
    residence_admin:str

class DemandeBase(BaseModel):
    NumCompte: str
    type_prestation: str
    gestion: str
    Période_Déduction: str  # Adjust type as necessary
    Début_Déduction: str  # Adjust type as necessary
    Fin_Déduction: str  # Adjust type as necessary
    montant: Optional[float] = None  # Allow None values
    demande_statut: Optional[str] = None
    class Config:
        from_attributes = True 
class DemandeResponse(DemandeBase):
    demande_id: int
    employee_name: str
# Create a new SQLAlchemy engine instance
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        


db_depandance = Annotated[Session,Depends(get_db())]

# Emploiyes https :
@app.post("/Emploiyes/", response_model=EmploiyesBase)  # Corrected endpoint and response model name
async def add_employee(employee: EmploiyesBase, db: Session = Depends(get_db)):
    # Create an Employee instance
    new_employee = EmploiyesModel(
        NumCompte=employee.NumCompte,  # Assuming NumCompte needs to be passed
        Nom=employee.Nom,
        Grade=employee.Grade,
        Poste=employee.Poste,
        lieu_de_travail=employee.lieu_de_travail,
        residence_admin = employee.residence_admin
    )
    
    # Add the new employee to the session and commit
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)  # Refresh to get the new ID

    return new_employee  # Return the created employee
@app.get("/Emploiyes/", response_model=List[EmploiyesBase])
async def get_all_Emploiyess(db: Session = Depends(get_db)):
    Emploiyes = db.query(EmploiyesModel).all()
    return Emploiyes

@app.get("/Emploiyes/search/", response_model=List[EmploiyesBase])
async def search_Emploiyes(
    NumCompte: Optional[str] = None,
    NOM: Optional[str] = None,
    Gade: Optional[str] = None,
    Post: Optional[str] = None,
    lieu_de_travail: Optional[str] = None,
    residence_admin : Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(EmploiyesModel)
    
    # Apply filters only for provided parameters
    if NumCompte:
        query = query.filter(EmploiyesModel.NumCompte.contains(NumCompte))
    if NOM:
        query = query.filter(EmploiyesModel.NOM.contains(NOM))
    if Gade:
        query = query.filter(EmploiyesModel.Gade.contains(Gade))
    if Post:
        query = query.filter(EmploiyesModel.Post.contains(Post))
    if lieu_de_travail:
        query = query.filter(EmploiyesModel.lieu_de_travail.contains(lieu_de_travail))
    if residence_admin:
        query = query.filter(EmploiyesModel.residence_admin.contains(residence_admin))
    
    Emploiyes = query.all()
    
    if not Emploiyes:
        raise HTTPException(status_code=404, detail="No Emploiyes found")
    
    return Emploiyes


@app.get("/Emploiyes/{num_compte}", response_model=EmploiyesBase)
async def get_employee(num_compte: str, db: Session = Depends(get_db)):
    employee = db.query(EmploiyesModel).filter(EmploiyesModel.NumCompte == num_compte).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/Emploiyes/{num_compte}", response_model=EmploiyesBase)
async def update_employee(num_compte: str, employee: EmploiyesBase, db: Session = Depends(get_db)):
    existing_employee = db.query(EmploiyesModel).filter(EmploiyesModel.NumCompte == num_compte).first()
    if existing_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    existing_employee.Nom = employee.Nom
    existing_employee.Grade = employee.Grade
    existing_employee.Poste = employee.Poste
    existing_employee.lieu_de_travail = employee.lieu_de_travail
    existing_employee.residence_admin = employee.residence_admin
    
    db.commit()
    db.refresh(existing_employee)

    return existing_employee

@app.delete("/Emploiyes/{num_compte}", response_model=dict)
async def delete_employee(num_compte: str, db: Session = Depends(get_db)):
    employee = db.query(EmploiyesModel).filter(EmploiyesModel.NumCompte == num_compte).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(employee)
    db.commit()

    return {"detail": "Employee deleted successfully"}

# Demande https :

@app.post("/Demande/", response_model=DemandeBase)
async def add_demande(demande: DemandeBase, db: Session = Depends(get_db)):
    # Check if the employee exists first
    employee = db.query(EmploiyesModel).filter(EmploiyesModel.NumCompte == demande.NumCompte).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    try:
        new_demande = DemandeModel(
            
            NumCompte=demande.NumCompte,
            type_prestation=demande.type_prestation,
            gestion=demande.gestion,
            Période_Déduction=demande.Période_Déduction,
            Début_Déduction=demande.Début_Déduction,
            Fin_Déduction=demande.Fin_Déduction,
            montant = demande.montant,
            demande_statut = demande.demande_statut

        )
        
        db.add(new_demande)
        db.commit()
        db.refresh(new_demande)
        
        return new_demande

    except Exception as e:
        db.rollback()  # Rollback the session if there's an error
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/Demande/", response_model=List[DemandeResponse])
async def get_all_demandes(db: Session = Depends(get_db)):
    demandes = (
        db.query(
            DemandeModel,
            EmploiyesModel.Nom  # Select the employee name
        )
        .join(EmploiyesModel, DemandeModel.NumCompte == EmploiyesModel.NumCompte)
        .all()
    )
    
    response_data = []
    for demande, employee_name in demandes:  # Unpack the results
        response_data.append({
            "demande_id": demande.demande_id,  # Access the DemandeModel attributes
            "NumCompte": demande.NumCompte,
            "type_prestation": demande.type_prestation,
            "gestion": demande.gestion,
            "Début_Déduction": demande.Début_Déduction, 
            "Fin_Déduction": demande.Fin_Déduction,
            "Période_Déduction": demande.Période_Déduction,
            "demande_statut": demande.demande_statut,
            "montant": demande.montant,
            "employee_name": employee_name  # Directly use the unpacked employee name
        })

    return response_data
@app.get("/Demande/search/", response_model=List[DemandeResponse])
async def search_demandes(
    demande_id: Optional[int] = None,
    NumCompte: Optional[str] = None,
    type_prestation: Optional[str] = None,
    gestion: Optional[str] = None,
    Période_Déduction: Optional[str] = None,
    demande_statut:Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(DemandeModel).join(EmploiyesModel, DemandeModel.NumCompte == EmploiyesModel.NumCompte)

    # Apply filters only for provided parameters
    if demande_id is not None:
        query = query.filter(DemandeModel.demande_id == demande_id)
    if NumCompte:
        query = query.filter(DemandeModel.NumCompte.contains(NumCompte))
    if type_prestation:
        query = query.filter(DemandeModel.type_prestation.contains(type_prestation))
    if gestion:
        query = query.filter(DemandeModel.gestion.contains(gestion))
    if Période_Déduction:
        query = query.filter(DemandeModel.Période_Déduction.contains(Période_Déduction))
    if demande_statut:
        query = query.filter(DemandeModel.demande_statut.contains(demande_statut))
    demandes = query.all()

    if not demandes:
        raise HTTPException(status_code=404, detail="No demandes found")
    
    # Prepare the response to include employee names
    response_data = []
    for demande in demandes:
        response_data.append({
            "demande_id": demande.demande_id,
            "NumCompte": demande.NumCompte,
            "type_prestation": demande.type_prestation,
            "gestion": demande.gestion,
            "Début_Déduction":  demande.Début_Déduction, 
            "Fin_Déduction":demande.Fin_Déduction,
            "montant": demande.montant,
            "Période_Déduction": demande.Période_Déduction,
            "demande_statut": demande.demande_statut,
            "employee_name": demande.employee.Nom  # Adjust according to your Employee model
        })

    return response_data

@app.put("/Demande/{demande_id}", response_model=DemandeBase)
async def update_demande(demande_id: int, demande: DemandeBase, db: Session = Depends(get_db)):
    existing_demande = db.query(DemandeModel).filter(DemandeModel.demande_id == demande_id).first()
    if existing_demande is None:
        raise HTTPException(status_code=404, detail="Demande not found")

    existing_demande.NumCompte = demande.NumCompte
    existing_demande.type_prestation = demande.type_prestation
    existing_demande.gestion = demande.gestion
    existing_demande.Période_Déduction = demande.Période_Déduction
    existing_demande.Début_Déduction = demande.Début_Déduction
    existing_demande.Fin_Déduction = demande.Fin_Déduction
    existing_demande.demande_statut = demande.demande_statut
    existing_demande.montant = demande.montant

    db.commit()
    db.refresh(existing_demande)

    return existing_demande

class DemandeResponseD(BaseModel):
    message: str
    demande_id: int

@app.delete("/Demande/{demande_id}", response_model=DemandeResponseD)
async def delete_demande(demande_id: int, db: Session = Depends(get_db)):
    """Delete a demande by ID"""
    demande = db.query(DemandeModel).filter(DemandeModel.demande_id == demande_id).first()
    
    if not demande:
        raise HTTPException(status_code=404, detail="Demande not found")
    
    db.delete(demande)
    db.commit()

    return DemandeResponseD(
        message="Demande deleted successfully",
        demande_id=demande_id
    )  

class CombinedResponse(BaseModel):
    demande: DemandeResponse
    employee: EmploiyesBase

@app.get("/Demande/{demande_id}", response_model=CombinedResponse)
async def get_demande_and_employee(demande_id: int, db: Session = Depends(get_db)):
    # Fetch Demande
    demande = db.query(DemandeModel).filter(DemandeModel.demande_id == demande_id).first()
    if demande is None:
        raise HTTPException(status_code=404, detail="Demande not found")

    # Fetch Employee using num_compte from Demande
    employee = db.query(EmploiyesModel).filter(EmploiyesModel.NumCompte == demande.NumCompte).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Return both Demande and Employee details
    return {"demande": demande, "employee": employee}


@app.post('/print/{demande_id}')
async def print_demande(
    demande_id: int,
    db: Session = Depends(get_db)
):
    demande_and_employee = await get_demande_and_employee(demande_id, db)
    demande_type = {
    "قرض مالي": generate_demande_de_prêt,
    "منحة مرضية":'',
    "العمرة": '',
    "ختان": generate_demande_pdf_type_d
}

    demande = demande_and_employee["demande"]
    employee = demande_and_employee["employee"]

    doc_type = demande.type_prestation  

    generator = demande_type.get(doc_type)
    if generator is None:
        raise ValueError(f"Unknown type_prestation: {doc_type}")

    pdf_path = generator(
        demande,
        employee,
        output_dir="print",
        subdirs=["demandes", f"emp_{employee.NumCompte}"]
    )

    return {
        "message": "Printing process initiated!",
        "demande_id": demande_id,
        "document_type": doc_type,
        "pdf_path": pdf_path
    }

# Mount static files - this should come AFTER API routes
app.mount("/static", StaticFiles(directory="UI"), name="static")

# HTML page routes - these should come AFTER mount
@app.get("/employees-page")
async def read_employees_page():
    return FileResponse('UI/Employees_Page.html')

@app.get("/")
async def read_index():
    return FileResponse('UI/Demande_Page.html')
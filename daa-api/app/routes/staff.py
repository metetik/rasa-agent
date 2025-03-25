from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated
from sqlmodel import Session, select
from app.database import get_session
from app.models import Staff
from app import schemas


router = APIRouter(tags=["staff"])

@router.post("/staff", response_model=schemas.StaffGetResponse, status_code=status.HTTP_201_CREATED)
async def create_staff(staff_data: schemas.StaffCreate, db_session: Session = Depends(get_session)):
    """
    Creates a new Staff member record.

    **Parameters:**
        - staff_data (schemas.StaffCreate): The Staff data to create. Must include first_name, last_name, role.
        - db_session (Session): The database session dependency.

    **Returns:**
        - schemas.StaffGetResponse: The created Staff object on success.

    **Raises:**
        - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        new_staff = Staff(**staff_data.model_dump())
        db_session.add(new_staff)
        db_session.commit()
        db_session.refresh(new_staff)
        return new_staff
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating staff member: {str(e)}"
        )

@router.get("/staff", response_model=List[schemas.StaffGetResponse])
async def list_staff(db_session: Session = Depends(get_session)):
    """
    Retrieves all staff members.

    **Parameters:**
        - db_session (Session): The database session dependency.

    **Returns:**
        - List[schemas.StaffGetResponse]: List of all staff members.

    **Raises:**
        - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        staff_list = db_session.execute(select(Staff)).scalars().all()
        return staff_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving staff list: {str(e)}"
        )

@router.get("/staff/{staff_id}", response_model=schemas.StaffGetResponse)
async def get_staff(staff_id: int, db_session: Session = Depends(get_session)):
    """
    Retrieves a specific staff member by ID.

    **Parameters:**
        - staff_id (int): The ID of the staff member to retrieve.
        - db_session (Session): The database session dependency.

    **Returns:**
        - schemas.StaffGetResponse: The requested staff member.

    **Raises:**
        - HTTPException: 404 Not Found if staff member doesn't exist.
    """
    staff = db_session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff member with ID {staff_id} not found"
        )
    return staff

@router.put("/staff/{staff_id}", response_model=schemas.StaffGetResponse)
async def update_staff(
    staff_id: int,
    staff_data: schemas.StaffUpdate,
    db_session: Session = Depends(get_session)
):
    """
    Updates all fields of an existing staff member.

    **Parameters:**
        - staff_id (int): The ID of the staff member to update.
        - staff_data (schemas.StaffUpdate): The updated staff data. All fields required.
        - db_session (Session): The database session dependency.

    **Returns:**
        - schemas.StaffGetResponse: The updated staff member.

    **Raises:**
        - HTTPException: 404 Not Found if staff member doesn't exist.
        - HTTPException: 500 Internal Server Error if there's a database error.
    """
    staff = db_session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff member with ID {staff_id} not found"
        )
    
    try:
        staff_data_dict = staff_data.model_dump()
        for key, value in staff_data_dict.items():
            setattr(staff, key, value)
        
        db_session.add(staff)
        db_session.commit()
        db_session.refresh(staff)
        return staff
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating staff member: {str(e)}"
        )

@router.patch("/staff/{staff_id}", response_model=schemas.StaffGetResponse)
async def patch_staff(
    staff_id: int,
    staff_data: schemas.StaffPatch,
    db_session: Session = Depends(get_session)
):
    """
    Partially updates an existing staff member.

    **Parameters:**
        - staff_id (int): The ID of the staff member to update.
        - staff_data (schemas.StaffPatch): The partial staff data. All fields optional.
        - db_session (Session): The database session dependency.

    **Returns:**
        - schemas.StaffGetResponse: The updated staff member.

    **Raises:**
        - HTTPException: 404 Not Found if staff member doesn't exist.
        - HTTPException: 500 Internal Server Error if there's a database error.
    """
    staff = db_session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff member with ID {staff_id} not found"
        )
    
    try:
        staff_data_dict = staff_data.model_dump()
        for key, value in staff_data_dict.items():
            setattr(staff, key, value)
        
        db_session.add(staff)
        db_session.commit()
        db_session.refresh(staff)
        return staff
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating staff member: {str(e)}"
        )

@router.delete("/staff/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(staff_id: int, db_session: Session = Depends(get_session)):
    """
    Deletes a staff member.

    **Parameters:**
        - staff_id (int): The ID of the staff member to delete.
        - db_session (Session): The database session dependency.

    **Returns:**
        - None

    **Raises:**
        - HTTPException: 404 Not Found if staff member doesn't exist.
        - HTTPException: 500 Internal Server Error if there's a database error.
    """
    staff = db_session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff member with ID {staff_id} not found"
        )
    
    try:
        db_session.delete(staff)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting staff member: {str(e)}"
        )

@router.get("/staff/dentist/name/", response_model=schemas.StaffGetResponse)
async def get_dentist_by_name(first_name: Annotated[str, "Dentist's first name"],
                               last_name: Annotated[str, "Dentist's last name"],
                               db_session=Depends(get_session)):
    """
    Retrieves a Dentist record by first and last name.
    
    **Parameters:**
    - first_name (str): The first name of the Dentist to retrieve.
    - last_name (str): The last name of the Dentist to retrieve.
    
    **Returns:**
    - schemas.StaffGetResponse: The requested staff member.
    
    **Raises:**
    - HTTPException: 404 Not Found if no Dentist with the given names exists.
    - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        dentist = db_session.query(Staff).filter(
            Staff.first_name == first_name,
            Staff.last_name == last_name,
            Staff.role == "Dentist"
        ).first()

        if dentist is None:
            raise HTTPException(status_code=404, detail="Dentist not found")
        
        return dentist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import company as crud_company
from app.schemas.company import CompanyCreate, CompanyResponse
from app.models.company import Company

router = APIRouter(prefix="/api/v1", tags=["company"])

@router.post("/companies", response_model=CompanyResponse, status_code=201)
async def create_company(
    request: CompanyCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    새로운 Company를 생성합니다.
    """
    # Company 객체 생성
    company = Company(
        name=request.name
    )
    
    # DB에 저장
    created_company = await crud_company.create_company(db, company)
    
    return created_company

@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    특정 Company의 정보를 조회합니다.
    """
    company = await crud_company.get_company(db, company_id=company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.database import get_database

router = APIRouter()

@router.get("/products")
async def get_products(
    category: Optional[str] = None,
    species: Optional[str] = None,
    db=Depends(get_database)
):
    """Get products with optional filters"""
    query = {}
    
    if category:
        query["category"] = category
    if species:
        query["suitable_for"] = species
    
    products = []
    for product in db.find("products", query if query else None):
        product["id"] = product.pop("_id", product.get("id"))
        products.append(product)
    
    return products

@router.get("/products/{product_id}")
async def get_product(product_id: str, db=Depends(get_database)):
    """Get single product details"""
    product = db.find_one("products", {"_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product["id"] = product.pop("_id", product.get("id"))
    return product

@router.get("/categories")
async def get_categories(db=Depends(get_database)):
    """Get all product categories"""
    categories = db.distinct("products", "category")
    return {"categories": categories}

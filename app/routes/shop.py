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
    
    products_data = await db.products.find(query)
    products = []
    for product in products_data:
        product["id"] = str(product.pop("_id"))
        products.append(product)
    
    return products

@router.get("/products/{product_id}")
async def get_product(product_id: str, db=Depends(get_database)):
    """Get single product details"""
    product = await db.products.find_one({"_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product["id"] = str(product.pop("_id"))
    return product

@router.get("/categories")
async def get_categories(db=Depends(get_database)):
    """Get all product categories"""
    categories = await db.products.distinct("category")
    return {"categories": categories}

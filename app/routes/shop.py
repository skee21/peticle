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
    try:
        query = {}
        
        if category:
            query["category"] = category
        if species:
            query["suitable_for"] = species
        
        products_data = await db.products.find(query if query else None)
        products = []
        for product in products_data:
            product_id_value = product.pop("_id", None)
            product["id"] = str(product_id_value) if product_id_value else None
            products.append(product)
        
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {str(e)}")

@router.get("/products/{product_id}")
async def get_product(product_id: str, db=Depends(get_database)):
    """Get single product details"""
    try:
        product = await db.products.find_one({"_id": product_id})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product_id_value = product.pop("_id", None)
        product["id"] = str(product_id_value) if product_id_value else product_id
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch product: {str(e)}")

@router.get("/categories")
async def get_categories(db=Depends(get_database)):
    """Get all product categories"""
    try:
        categories = await db.products.distinct("category")
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch categories: {str(e)}")

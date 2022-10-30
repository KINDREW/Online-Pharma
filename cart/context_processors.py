"""Context processor"""
from .cart import Cart

def cart(request):
    """Context manager"""
    return {"cart":Cart(request)}

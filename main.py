"""
This module implements a basic CRUD (Create, Read, Update, Delete) for
managing product inventory.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Any
from decimal import Decimal
import sys
from abc import ABC, abstractmethod

# Type aliases for better code readability
ProductID = int
ProductDict = Dict[str, Dict[ProductID, Any]]

# Constants
MENU_OPTIONS = {
    1: "Agregar",
    2: "Eliminar",
    3: "Actualizar",
    4: "Salir"
}

SEPARATOR_LENGTH = 25
MIN_PRICE = Decimal('0.0')
MIN_STOCK = 0

@dataclass(frozen=True)
class ProductData:
    """
    Data structure for product validation.
    
    Attributes:
        name_min_length (int): Minimum length for product name
        name_max_length (int): Maximum length for product name
        max_price (Decimal): Maximum allowed price
        max_stock (int): Maximum allowed stock
    """
    name_min_length: int = 1
    name_max_length: int = 50
    max_price: Decimal = Decimal('999999.99')
    max_stock: int = 99999

@dataclass
class Product:
    """
    Represents a product in the inventory.
    
    Attributes:
        name (str): Name of the product
        price (Decimal): Price of the product
        stock (int): Available quantity in stock
    """
    name: str
    price: Decimal
    stock: int

    def __post_init__(self) -> None:
        """Validate product attributes after initialization."""
        self.validate()

    def validate(self) -> None:
        """
        Validate product attributes against defined constraints.
        
        Raises:
            ValueError: If any attribute doesn't meet the validation criteria
        """
        if not ProductData.name_min_length <= len(self.name.strip()) <= ProductData.name_max_length:
            raise ValueError(f"El nombre debe tener entre {ProductData.name_min_length} y {ProductData.name_max_length} caracteres")
        
        if not MIN_PRICE <= self.price <= ProductData.max_price:
            raise ValueError(f"El precio debe estar entre {MIN_PRICE} y {ProductData.max_price}")
        
        if not MIN_STOCK <= self.stock <= ProductData.max_stock:
            raise ValueError(f"El stock debe estar entre {MIN_STOCK} y {ProductData.max_stock}")

class InventoryInterface(ABC):
    """Abstract base class defining the interface for inventory operations."""
    
    @abstractmethod
    def get(self) -> None:
        """Display all products in inventory."""
        pass

    @abstractmethod
    def add(self) -> None:
        """Add a new product to inventory."""
        pass

    @abstractmethod
    def delete(self) -> None:
        """Delete a product from inventory."""
        pass

    @abstractmethod
    def update(self) -> None:
        """Update an existing product in inventory."""
        pass

    @abstractmethod
    def save(self) -> ProductDict:
        """Save current inventory state."""
        pass

class CRUD(InventoryInterface):
    """
    Implementation of CRUD operations for inventory management.
    
    This class provides the core functionality for managing products in the
    inventory system, including adding, updating, deleting, and displaying products.
    """

    def __init__(self, initial_products: Optional[ProductDict] = None) -> None:
        """
        Initialize the CRUD system with optional initial products.
        
        Args:
            initial_products: Dictionary containing initial product data
        """
        self.products: Dict[ProductID, Product] = {}
        if initial_products:
            self._load_initial_products(initial_products)

    def _load_initial_products(self, initial_data: ProductDict) -> None:
        """
        Load initial products into the system.
        
        Args:
            initial_data: Dictionary containing initial product data
        """
        for id, name in initial_data["Productos"].items():
            self.products[id] = Product(
                name=name,
                price=Decimal(str(initial_data["Precios"][id])),
                stock=initial_data["Stock"][id]
            )

    def get(self) -> None:
        """Display all products in a formatted table."""
        print("=" * SEPARATOR_LENGTH)
        print("Lista de Productos:")
        print("ID  |  Nombre  |  Precio  |  Cantidad")
        print("=" * SEPARATOR_LENGTH)
        for id, product in self.products.items():
            print(f"{id:<4}|  {product.name:<8}|  {product.price:<8.2f}|  {product.stock}")
        print("=" * SEPARATOR_LENGTH)

    def _validate_price(self, price: str) -> Decimal:
        """
        Validate and convert price input.
        
        Args:
            price: String representation of the price
            
        Returns:
            Decimal: Validated price value
            
        Raises:
            ValueError: If price is invalid
        """
        try:
            price_decimal = Decimal(price)
            if price_decimal < MIN_PRICE:
                raise ValueError("El precio debe ser mayor a 0")
            return price_decimal
        except (ValueError, TypeError):
            raise ValueError("Por favor ingrese un precio válido")

    def _validate_stock(self, stock: str) -> int:
        """
        Validate and convert stock input.
        
        Args:
            stock: String representation of the stock quantity
            
        Returns:
            int: Validated stock value
            
        Raises:
            ValueError: If stock is invalid
        """
        try:
            stock_int = int(stock)
            if stock_int < MIN_STOCK:
                raise ValueError("La cantidad en stock debe ser mayor o igual a 0")
            return stock_int
        except (ValueError, TypeError):
            raise ValueError("Por favor ingrese una cantidad válida")

    def add(self) -> None:
        """
        Add a new product to the inventory.
        
        Raises:
            ValueError: If input validation fails
        """
        try:
            name = input("Ingrese nombre del producto: ").strip()
            price = self._validate_price(input("Ingrese precio del producto: "))
            stock = self._validate_stock(input("Ingrese cantidad en stock: "))

            new_id = max(self.products.keys(), default=0) + 1
            self.products[new_id] = Product(name, price, stock)
            print("Producto agregado exitosamente")
        except ValueError as e:
            raise ValueError(f"Error al agregar producto: {str(e)}")

    def delete(self) -> None:
        """
        Delete a product from the inventory.
        
        Raises:
            ValueError: If product ID is invalid
        """
        try:
            id = int(input("Ingrese ID del producto a eliminar: "))
            if id not in self.products:
                raise ValueError("ID de producto no encontrado")
            del self.products[id]
            print("Producto eliminado exitosamente")
        except ValueError as e:
            raise ValueError(f"Error al eliminar producto: {str(e)}")

    def update(self) -> None:
        """
        Update an existing product in the inventory.
        
        Raises:
            ValueError: If input validation fails
        """
        try:
            id = int(input("Ingrese ID del producto a actualizar: "))
            if id not in self.products:
                raise ValueError("ID de producto no encontrado")

            product = self.products[id]
            print(f"Producto actual: {product.name} - {product.price:.2f} - Stock: {product.stock}")

            # Get and validate new values
            self._update_product_fields(product)
            print("Producto actualizado exitosamente")
        except ValueError as e:
            raise ValueError(f"Error al actualizar producto: {str(e)}")
    
    def _update_product_fields(self, product: Product) -> None:
        """
        Update individual fields of a product.
        
        Args:
            product: Product instance to update
            
        Raises:
            ValueError: If input validation fails
        """
        name = input("Nuevo nombre (Enter para mantener actual): ").strip()
        price_str = input("Nuevo precio (Enter para mantener actual): ").strip()
        stock_str = input("Nueva cantidad (Enter para mantener actual): ").strip()

        if name:
            product.name = name
        if price_str:
            product.price = self._validate_price(price_str)
        if stock_str:
            product.stock = self._validate_stock(stock_str)

    def save(self) -> ProductDict:
        """
        Save current inventory state to dictionary format.
        
        Returns:
            Dictionary containing all product data
        """
        return {
            "Productos": {id: product.name for id, product in self.products.items()},
            "Precios": {id: float(product.price) for id, product in self.products.items()},
            "Stock": {id: product.stock for id, product in self.products.items()}
        }

    def run(self) -> None:
        """
        Main program loop handling user interaction.
        
        This method runs continuously until the user chooses to exit or
        interrupts the program.
        """
        while True:
            try:
                self.get()
                print("\n".join(f"[{key}] {value}" for key, value in MENU_OPTIONS.items()))
                option_input = input("Seleccione una opción: ").strip()
            
                if not option_input.isdigit():
                    raise ValueError("Debe ingresar un número válido")

                option = int(option_input)
                
                if option == 4:
                    print("Saliendo del programa...")
                    sys.exit(0)
                    
                if option not in MENU_OPTIONS:
                    raise ValueError("Opción invalida")

                {1: self.add, 2: self.delete, 3: self.update}[option]()
                
            except ValueError as e:
                print(f"Error: {str(e)}")
            except KeyboardInterrupt:
                print("\nPrograma terminado")
                sys.exit(0)


def main() -> None:
    """
    Main entry point of the program.
    
    Initializes the inventory system with sample data and starts the main loop.
    """
    initial_data = {
        "Productos": {1: "Pantalones", 2: "Camisas", 3: "Corbatas", 4: "Casacas"},
        "Precios": {1: 200.00, 2: 120.00, 3: 50.00, 4: 350.00},
        "Stock": {1: 50, 2: 45, 3: 30, 4: 15},
    }

    system = CRUD(initial_data)
    system.run()


if __name__ == "__main__":
    main()
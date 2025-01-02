# Inventory Management System

This program implements a simple CLI-based inventory management system using Python. It provides CRUD (Create, Read, Update, Delete) operations to manage a list of products. Each product has a name, price, and stock quantity.

## Features

- Display a list of products with their details (ID, name, price, and stock).
- Add new products to the inventory.
- Delete existing products by their ID.
- Update the details of existing products.
- Save the current state of the inventory.

## Data Structure

The inventory system uses the following dictionaries to manage products:

```python
Productos = {1: 'Pantalones', 2: 'Camisas', 3: 'Corbatas', 4: 'Casacas'}
Precios = {1: 200.00, 2: 120.00, 3: 50.00, 4: 350.00}
Stock = {1: 50, 2: 45, 3: 30, 4: 15}
```

Each dictionary is keyed by a unique product ID.

## Menu Options

When the program runs, the user is presented with the following menu:

```
[1] Agregar
[2] Eliminar
[3] Actualizar
[4] Salir
```

### Actions
1. **Agregar**: Adds a new product by providing its name, price, and stock.
2. **Eliminar**: Removes an existing product by its ID.
3. **Actualizar**: Updates the name, price, or stock of an existing product.
4. **Salir**: Exits the program.

## Code Structure

### Classes

1. **`Product`**
   - Represents a single product.
   - Validates attributes such as name, price, and stock during initialization.

2. **`CRUD`**
   - Implements the main logic for managing the inventory.
   - Methods:
     - `get`: Displays all products in a table format.
     - `add`: Adds a new product to the inventory.
     - `delete`: Deletes a product from the inventory.
     - `update`: Updates the attributes of an existing product.
     - `save`: Saves the current inventory state to a dictionary.
     - `run`: Main loop for user interaction.

### Input Validation

- **Price**: Ensures it is a positive decimal.
- **Stock**: Ensures it is a non-negative integer.
- **Name**: Ensures it meets length constraints.

### Constants

- `MENU_OPTIONS`: Defines the available menu actions.
- `SEPARATOR_LENGTH`: Length of separators in the display.
- `MIN_PRICE` and `MIN_STOCK`: Minimum allowed values for price and stock.

## Example Usage

### Initial State

```
========================================
Lista de Productos:
========================================
ID  |  Nombre      |  Precio   |  Cantidad
========================================
1   |  Pantalones  |  200.00   |  50
2   |  Camisas     |  120.00   |  45
3   |  Corbatas    |  50.00    |  30
4   |  Casacas     |  350.00   |  15
========================================
[1] Agregar, [2] Eliminar, [3] Actualizar, [4] Salir
```

### Adding a Product

User chooses option `[1]` and provides the following details:
- Name: `Zapatos`
- Price: `250`
- Stock: `20`

Result:

```
Producto agregado exitosamente.
```

### Deleting a Product

User chooses option `[2]` and provides ID: `3`.

Result:

```
Producto eliminado exitosamente.
```

### Updating a Product

User chooses option `[3]` and provides ID: `2`.
- New Name: `Polos`
- New Price: `130`
- New Stock: `50`

Result:

```
Producto actualizado exitosamente.
```

### Exiting the Program

User chooses option `[4]`:

```
Saliendo del programa...
```

## Running the Program

To execute the program:

1. Save the script in a `.py` file.
2. Run the file using Python:

```bash
python inventory.py
```

## Future Improvements

- Persist data to a file or database for use across sessions.
- Add sorting and filtering options for the product list.
- Implement a GUI for better user experience.
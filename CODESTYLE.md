

# CODESTYLE.md

## Estilo de Nombres

### Nombres de Variables
- **Formato:** Se permite el uso de `camelCase` o guion bajo (`snake_case`) para los nombres de las variables.
- **Ejemplos:**
  - `miVariable`
  - `nombre_usuario`
  - `totalVehiculos`
  - `total_vehiculos`

### Nombres de Funciones y Métodos
- **Formato:** Se permite el uso de `camelCase` o guion bajo (`snake_case`) para los nombres de funciones y métodos.
- **Ejemplos:**
  - `calcularTotalVehiculos()`
  - `calcular_total_vehiculos()`
  - `validarDocumento()`
  - `validar_documento()`

### Nombres de Clases
- Usar `PascalCase` para el nombre de las clases.
  - **Ejemplo:** `ClaseVehiculo`, `HistorialMantenimiento`

---

## Reglas de Indentación
- Utilizar **4 espacios** por cada nivel de indentación. No se deben usar tabuladores.
- **Ejemplo:**
  ```python
  def calcular_precio_total(precio_base, impuestos):
      precio_final = precio_base + impuestos
      return precio_final
  ```



## Comentarios y Documentación

### Comentarios en Línea
- Utilizar `#` para comentarios en línea que expliquen partes específicas del código.
- **Ejemplo:**
  ```python
  precio_base = 100  # Precio base del vehículo
  ```

### Comentarios de Bloque
- Para comentarios más extensos que describen funciones, clases o bloques de código, utilizar el siguiente formato de documentación:
  - **Funciones/Métodos:**
    ```python
    def calcular_precio_total(precio_base, impuestos):
        """
        Calcula el precio total del vehículo sumando el precio base e impuestos.

        Args:
            precio_base (float): El precio base del vehículo.
            impuestos (float): Impuestos a aplicar sobre el precio base.

        Returns:
            float: El precio total después de aplicar los impuestos.
        """
        precio_final = precio_base + impuestos
        return precio_final
    ```

  - **Clases:**
    ```python
    class Vehiculo:
        """
        Representa un vehículo en el sistema.

        Attributes:
            marca (str): La marca del vehículo.
            modelo (str): El modelo del vehículo.
            año (int): El año de fabricación.
        """
        def __init__(self, marca, modelo, año):
            self.marca = marca
            self.modelo = modelo
            self.año = año
    ```

---

## Convenciones de Commits

Para los mensajes de commits, seguiremos las reglas de [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Los mensajes de commit deben estar estructurados de la siguiente manera:

```
<tipo>: <descripción>
```

### Tipos de Commits Permitidos

- `feat`: Para la adición de nuevas características o funcionalidades.
- `fix`: Para la corrección de errores o bugs.
- `docs`: Para cambios en la documentación, sin afectar el código fuente.
- `style`: Para ajustes relacionados con el formato y estilo del código (por ejemplo, espacios, puntos y comas faltantes), sin modificar la lógica del código.
- `refactor`: Para refactorizaciones del código que no introducen nuevas funcionalidades ni corrigen errores.

### Ejemplos de Commits
- **Nuevas funcionalidades:** 
  - `feat: añadir funcionalidad de búsqueda de vehículos por año`
- **Corrección de errores:** 
  - `fix: corregir error en la validación de tipo de combustible`
- **Documentación:** 
  - `docs: agregar estilo de codificación a CODESTYLE.md`
- **Estilo:** 
  - `style: ajustar formato de indentación en archivo vehiculo.py`
- **Refactorización:** 
  - `refactor: simplificar la función calcularPrecioTotal`

---

## Convención de Nombres de Ramas

Las ramas deben seguir una convención clara basada en la funcionalidad que se está desarrollando o corrigiendo. Se acepta el uso de guion bajo (`_`) en los nombres de las ramas para mayor legibilidad. Utiliza las siguientes convenciones para nombrar las ramas:

- **Para nuevas características:**
  ```bash
  feat/<nombre_funcionalidad>
  ```
  **Ejemplo:** `feat/agregar_vehiculo`
  
- **Para corrección de errores:**
  ```bash
  fix/<descripcion_error>
  ```
  **Ejemplo:** `fix/corregir_validacion_combustible`

- **Para cambios en la documentación:**
  ```bash
  docs/<actualizacion_documentacion>
  ```
  **Ejemplo:** `docs/actualizar_readme`




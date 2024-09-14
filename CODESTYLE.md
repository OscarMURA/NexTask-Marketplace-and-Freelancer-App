

# CODESTYLE.md

## Estilo de Nombres

### Nombres de Variables
- **Formato:** Utilizar `camelCase` para los nombres de las variables.
- **Ejemplos:**
  - `miVariable`
  - `nombreUsuario`
  - `totalVehiculos`

### Nombres de Funciones y Clases
- **Funciones y Métodos:**
  - Utilizar `PascalCase` para los nombres de funciones y métodos.
  - **Ejemplo:** `CalcularTotalVehiculos()`, `ValidarDocumento()`
- **Clases:**
  - Usar `PascalCase` para el nombre de las clases.
  - **Ejemplo:** `ClaseVehiculo`, `HistorialMantenimiento`

---

## Reglas de Indentación
- Utilizar **4 espacios** por cada nivel de indentación. No se deben usar tabuladores.
- **Ejemplo:**
  ```python
  def calcularPrecioTotal(precioBase, impuestos):
      precioFinal = precioBase + impuestos
      return precioFinal
  ```

---

## Longitud Máxima de las Líneas de Código
- Mantener una longitud máxima de **80 caracteres** por línea de código para asegurar la legibilidad.
- Si una línea es muy larga, dividirla en múltiples líneas usando sangría adecuada.

---

## Comentarios y Documentación

### Comentarios en Línea
- Utilizar `#` para comentarios en línea que expliquen partes específicas del código.
- **Ejemplo:**
  ```python
  precioBase = 100  # Precio base del vehículo
  ```

### Comentarios de Bloque
- Para comentarios más extensos que describen funciones, clases o bloques de código, utilizar el siguiente formato de documentación:
  - **Funciones/Métodos:**
    ```python
    def calcularPrecioTotal(precioBase, impuestos):
        """
        Calcula el precio total del vehículo sumando el precio base e impuestos.

        Args:
            precioBase (float): El precio base del vehículo.
            impuestos (float): Impuestos a aplicar sobre el precio base.

        Returns:
            float: El precio total después de aplicar los impuestos.
        """
        precioFinal = precioBase + impuestos
        return precioFinal
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

Las ramas deben seguir una convención clara basada en la funcionalidad que se está desarrollando o corrigiendo. Utiliza las siguientes convenciones para nombrar las ramas:

- **Para nuevas características:**
  ```
  feat/<nombre-funcionalidad>
  ```
  **Ejemplo:** `feat/agregar-vehiculo`
  
- **Para corrección de errores:**
  ```
  fix/<descripción-error>
  ```
  **Ejemplo:** `fix/corregir-validacion-combustible`

- **Para cambios en la documentación:**
  ```
  docs/<actualización-documentación>
  ```
  **Ejemplo:** `docs/actualizar-readme`

---

## Prácticas Generales

1. **Testing:** Asegúrate de escribir pruebas unitarias para toda nueva funcionalidad que se agregue.
2. **Revisiones de Código:** Todo código debe ser revisado por al menos un compañero antes de ser integrado a la rama principal.
3. **Limpieza de Código:** Antes de realizar un commit, asegúrate de eliminar cualquier código comentado que no sea relevante o necesario.


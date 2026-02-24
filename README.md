# Portafolio Académico FEN-UNAB

Aplicación web para consulta y actualización de portafolios académicos.

## Archivos

- `index.html` — La aplicación completa
- `academicos.json` — Datos de los académicos (generado con `generar_json.py`)
- `generar_json.py` — Script para regenerar el JSON desde CSVs de SharePoint

## Actualizar datos

1. Exportar CSVs desde SharePoint (Evidencias, ExpLaboralDescripcion)
2. Colocar junto a `generar_json.py` con `maestro_academicos.csv`
3. Ejecutar `python generar_json.py`
4. Subir el nuevo `academicos.json` al repositorio

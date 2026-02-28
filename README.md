# Portafolio Académico FEN-UNAB

Portal web para que los académicos de la FEN-UNAB revisen su portafolio de evidencias, reporten errores y agreguen nuevas actividades o experiencia laboral. Funciona como sitio estático en **GitHub Pages** — no requiere servidor.

## Archivos del repositorio

```
├── index.html              ← El portal (renombrar portafolio.html → index.html)
├── portafolio_data.json    ← Datos exportados desde la app de gestión local
└── README.md               ← Este archivo
```

## Cómo funciona

1. El profesor abre la URL del sitio GitHub Pages.
2. El portal carga `portafolio_data.json` automáticamente y pide al profesor su correo institucional para identificarse.
3. El profesor ve sus evidencias y experiencia laboral, puede reportar errores, y agregar nuevas actividades.
4. Al finalizar, el portal genera dos archivos descargables:
   - `cambios_XXXX_fecha.json` → para importar en la app de gestión local
   - `portafolio_XXXX_fecha.csv` → respaldo legible
5. Se abre un borrador de correo dirigido a `c.troncosovalverde@uandresbello.edu` con instrucciones para adjuntar ambos archivos.

## Despliegue paso a paso

### Primera vez

1. Crear un repositorio en GitHub (puede ser privado con GitHub Pages habilitado, o público).
2. En **Settings → Pages**, activar GitHub Pages desde la rama `main` (o `master`).
3. Renombrar `portafolio.html` a `index.html` y subirlo al repositorio.
4. Desde la app de gestión local, hacer click en **Exportar Portal** (menú lateral). Esto genera `portafolio_data.json`.
5. Subir `portafolio_data.json` al mismo repositorio.
6. Esperar 1-2 minutos a que GitHub Pages publique. La URL será: `https://<usuario>.github.io/<repo>/`

### Actualizar datos (cada vez que cambien)

1. En la app de gestión local, click en **Exportar Portal**.
2. Reemplazar `portafolio_data.json` en el repositorio con el nuevo archivo (commit + push, o subir directamente desde la interfaz web de GitHub).
3. GitHub Pages actualiza automáticamente en ~1 minuto.

### Actualizar el portal (si hay nueva versión del HTML)

1. Renombrar el nuevo `portafolio.html` a `index.html`.
2. Reemplazar `index.html` en el repositorio.

## Flujo de trabajo completo

```
┌──────────────────┐     Exportar Portal      ┌────────────────────┐
│   App de gestión  │ ──────────────────────► │   GitHub Pages      │
│   (index.html     │   portafolio_data.json   │   (portal público)  │
│    local)         │                          │                     │
│                   │ ◄────────────────────── │                     │
│                   │   Importar cambios prof. │   Profesor envía    │
│                   │   cambios_*.json         │   cambios_*.json    │
└──────────────────┘                          └────────────────────┘
```

1. **Admin** exporta datos → sube `portafolio_data.json` a GitHub.
2. **Admin** envía correo masivo a profesores con la URL del portal.
3. **Profesor** entra, revisa, agrega actividades, envía archivos por correo.
4. **Admin** recibe correos, descarga los `cambios_*.json`.
5. **Admin** en la app local: **Importar cambios prof.** → selecciona los JSON recibidos.
6. Las nuevas evidencias quedan como `pendiente` para revisión del admin.

## Tipos de actividades

El portal agrupa las actividades en 5 categorías más experiencia laboral:

- **Investigación — Lista I**: publicaciones WOS/Scopus, libros, casos editoriales
- **Investigación — Lista II**: conferencias, proyectos competitivos, supervisión de tesis, etc.
- **Gestión y Docencia**: cargos académicos, comités, rediseño de cursos, etc.
- **Experiencia Profesional — Lista III**: consultoría, directorios, certificaciones
- **Vinculación y Debate Público — Lista III**: medios, extensión, seminarios, etc.
- **Experiencia Laboral**: cargos profesionales con período de vigencia
- **"Mi actividad no aparece en la lista"**: opción guiada que pide descripción + actividad más cercana

Las actividades con naturaleza de cargo continuo (puesto en directorio, editor de revista, cargo académico, comité, etc.) piden **año inicio / año fin / vigente** en vez de un solo año.

## Datos que contiene portafolio_data.json

El archivo es generado por la app de gestión y contiene:

- Lista de académicos (RUT, nombre, email, planta, unidad, grado)
- Todas las evidencias del académico (con estado de revisión)
- Toda la experiencia laboral (sin filtrar por calificante)
- Horas de contacto (SCH)
- Año de evaluación

**No contiene** revistas predatorias ni datos sensibles de clasificación AACSB.

## Notas técnicas

- El portal es un archivo HTML único con React (cargado desde CDN). No requiere build ni instalación.
- Los datos se cargan via `fetch("portafolio_data.json")` relativo a la URL del sitio.
- No se almacena nada en el servidor — todo funciona en el navegador del profesor.
- Los archivos generados (`cambios_*.json`, `portafolio_*.csv`) se descargan al equipo del profesor y se envían manualmente por correo.
- Compatible con cualquier navegador moderno (Chrome, Firefox, Edge, Safari).

## Solución de problemas

| Problema | Causa probable | Solución |
|---|---|---|
| "Error cargando datos" | `portafolio_data.json` no existe o tiene error | Verificar que el archivo esté en el repositorio y sea JSON válido |
| Profesor no aparece | Su email no coincide con el registrado | Verificar email en la app de gestión; el profesor puede solicitar corrección |
| Datos desactualizados | `portafolio_data.json` no fue actualizado | Re-exportar desde la app de gestión y subir al repo |
| Página en blanco | Error de JavaScript | Abrir consola del navegador (F12) y verificar errores |

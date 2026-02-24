#!/usr/bin/env python3
"""
generar_json.py
===============
Genera academicos.json a partir de los CSV exportados de SharePoint.

USO:
    python generar_json.py

ARCHIVOS REQUERIDOS (en la misma carpeta):
    - Evidencias.csv          → Exportar desde lista SharePoint "Evidencias"
    - ExpLaboralDescripcion.csv → Exportar desde lista SharePoint "ExpLaboralDescripcion"
    - maestro_academicos.csv  → Datos base de cada académico (ver plantilla abajo)

FORMATO DE maestro_academicos.csv:
    RUT,NombreCompleto,Email,Grado,GradoDetalle,Unidad,TipoContrato,Suficiencia,ClasificacionAACSB
    15331942-1,MARCO GUILLERMO OPAZO BASÁEZ,m.opazobasez@uandresbello.edu,Doctorado,"PhD in Business Administration — U. de Granada (2019)",Administración & Innovación,Regular (FT),Participating,SA

SALIDA:
    academicos.json → Colocar en la misma carpeta que index.html
"""

import csv
import json
import os
import sys
from collections import defaultdict


def parse_evidencia(e):
    """Convierte un registro de Evidencias en formato display."""
    code = e.get('ActividadCodigo', '')
    cat = e.get('DescripcionActividad', '')
    yr = (e.get('Anio') or e.get('AnioPublicacion') or '').replace(',', '').strip()

    desc = ''
    if code == 'pub_paper':
        desc = (e.get('TituloArticulo') or '')[:80]
        journal = e.get('NombreRevista', '')
        idx = e.get('IndexArticle', '')
        q = e.get('QuartilArticle', '')
        if journal: desc += f' — {journal}'
        if idx: desc += f' [{idx}'
        if q: desc += f' {q}'
        if idx: desc += ']'
    elif code == 'pub_libro':
        desc = (e.get('TituloCapitulo') or e.get('TituloLibro') or '')[:70]
        if e.get('Editorial'): desc += f' — {e["Editorial"]}'
    elif code == 'conf_ext':
        desc = (e.get('TituloPonencia') or '')[:60]
        if e.get('NombreEvento'): desc += f' @ {e["NombreEvento"]}'
    elif code == 'cargo_academico':
        desc = e.get('CargoGestion', '') or ''
    elif code == 'media_regular':
        desc = (e.get('TituloNota') or '')[:70]
        if e.get('NombreMedio'): desc += f' — {e["NombreMedio"]}'
    elif code == 'editor_revista':
        desc = e.get('NombreRevista', '') or ''
        if e.get('RolEditorial'): desc = f'{e["RolEditorial"]} — {desc}'
    elif code == 'sup_tesis':
        desc = (e.get('TituloTesis') or '')[:60]
        if e.get('NombreProgramaTesis'): desc += f' ({e["NombreProgramaTesis"]})'
    elif code == 'consultoria_alta':
        desc = (e.get('NombreProyecto') or '')[:60]
        if e.get('NombreCliente'): desc += f' — {e["NombreCliente"]}'
    elif code == 'puesto_directorio':
        desc = (e.get('CargoDirectorio') or '')[:40]
    elif code == 'peer_review':
        desc = e.get('NombreRevista', '') or ''
    elif code in ('panelista_foro', 'extension_com', 'org_seminario'):
        desc = (e.get('NombreEvento') or '')[:80]
    elif code == 'working_paper':
        desc = (e.get('TituloWP') or '')[:80]
    elif code == 'proy_comp':
        desc = (e.get('TituloProyecto') or '')[:60]
        if e.get('Agencia'): desc += f' — {e["Agencia"]}'
    elif code == 'material_ensenanza':
        desc = (e.get('NombreMaterial') or '')[:80]
    elif code == 'perfeccion_acad':
        desc = (e.get('NombrePrograma') or '')[:80]
    elif code == 'part_comite':
        desc = (e.get('NombreComite') or '')[:80]
    else:
        desc = (e.get('TextoLibre') or '')[:80]

    return {'code': code, 'cat': cat, 'year': yr, 'desc': desc.strip()}


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Check required files
    files = {
        'evidencias': os.path.join(script_dir, 'Evidencias.csv'),
        'explaboral': os.path.join(script_dir, 'ExpLaboralDescripcion.csv'),
        'maestro': os.path.join(script_dir, 'maestro_academicos.csv'),
    }

    missing = [name for name, path in files.items() if not os.path.exists(path)]
    if missing:
        print(f"ERROR: Archivos no encontrados: {', '.join(missing)}")
        print(f"       Deben estar en: {script_dir}")
        if 'maestro' in missing:
            print("\n  NOTA: Si es la primera vez, cree maestro_academicos.csv con columnas:")
            print("  RUT,NombreCompleto,Email,Grado,GradoDetalle,Unidad,TipoContrato,Suficiencia,ClasificacionAACSB")
        sys.exit(1)

    # Load CSVs
    def load_csv(path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            return list(csv.DictReader(f))

    evidencias = load_csv(files['evidencias'])
    exp_desc = load_csv(files['explaboral'])
    maestro = load_csv(files['maestro'])

    print(f"Cargados: {len(evidencias)} evidencias, {len(exp_desc)} exp. laboral, {len(maestro)} registros maestros")

    # Build master lookup
    master_map = {}
    for m in maestro:
        master_map[m['RUT'].strip()] = m

    # Get all RUTs
    all_ruts = set()
    for e in evidencias: all_ruts.add(e['RUT'].strip())
    for e in exp_desc: all_ruts.add(e['RUT'].strip())
    for m in maestro: all_ruts.add(m['RUT'].strip())

    # Build result
    result = {}
    missing_master = []

    for rut in sorted(all_ruts):
        # Parse evidencias
        evs_raw = [e for e in evidencias if e['RUT'].strip() == rut]
        parsed_evs = [parse_evidencia(e) for e in evs_raw]

        # Parse exp laboral
        exps_raw = [e for e in exp_desc if e['RUT'].strip() == rut]
        parsed_exps = [{
            'cargo': ex.get('nombre', ''),
            'empresa': ex.get('EMPRESA', ''),
            'inicio': ex.get('AÑO_INICIO', '').replace(',', '').strip(),
            'fin': ex.get('AÑO_FINAL', '').replace(',', '').strip()
        } for ex in exps_raw]

        # Master data
        m = master_map.get(rut, {})
        if not m:
            missing_master.append(rut)
            # Try to get name/email from evidencias
            name = evs_raw[0].get('NombreCompleto', '') if evs_raw else ''
            email = evs_raw[0].get('Email', '') if evs_raw else ''
            if not name and exps_raw:
                n = exps_raw[0]
                name = f"{n.get('NOMBRES','')} {n.get('APELLIDO_PATERNO','')} {n.get('APELLIDO_MATERNO','')}".strip()
        else:
            name = m.get('NombreCompleto', '')
            email = m.get('Email', '')

        result[rut] = {
            'name': name,
            'email': email,
            'grado': m.get('Grado', ''),
            'gradoDetalle': m.get('GradoDetalle', ''),
            'unidad': m.get('Unidad', ''),
            'contrato': m.get('TipoContrato', ''),
            'suficiencia': m.get('Suficiencia', ''),
            'clasificacion': m.get('ClasificacionAACSB', ''),
            'evidencias': parsed_evs,
            'expLaboral': parsed_exps,
        }

    # Save
    output_path = os.path.join(script_dir, 'academicos.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Generado: {output_path}")
    print(f"  {len(result)} académicos")
    print(f"  {sum(len(v['evidencias']) for v in result.values())} evidencias")
    print(f"  {sum(len(v['expLaboral']) for v in result.values())} registros exp. laboral")
    print(f"  {os.path.getsize(output_path)/1024:.0f} KB")

    if missing_master:
        print(f"\n⚠ {len(missing_master)} RUTs sin datos en maestro_academicos.csv:")
        for rut in missing_master[:10]:
            name = result[rut]['name'] or '(sin nombre)'
            print(f"    {rut} — {name}")
        if len(missing_master) > 10:
            print(f"    ... y {len(missing_master) - 10} más")
        print("  → Agregar estos RUTs a maestro_academicos.csv y volver a ejecutar")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
convertir_a_gltf.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Convierte los 6 STL del monumento Osvaldo Bayer a GLB
(GLTF binario) con materiales PBR correctos.

Instalación:
    pip install trimesh numpy

Uso:
    python3 convertir_a_gltf.py
    python3 convertir_a_gltf.py --entrada files/ --salida files_glb/

Compresión Draco (opcional, reduce ~70% más):
    npm install -g gltf-pipeline
    gltf-pipeline -i files_glb/piso.glb -o files_glb/piso.glb -d
    (o corré: python3 convertir_a_gltf.py --draco)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os
import sys
import argparse
import subprocess

try:
    import numpy as np
    import trimesh
    import trimesh.visual.material as mat
except ImportError:
    print("❌  Faltan dependencias. Instalá con:")
    print("       pip install trimesh numpy")
    sys.exit(1)


# ─────────────────────────────────────────────────────
# Definición de cada pieza: color + parámetros PBR
# Los colores coinciden con los asignados en index.html
# ─────────────────────────────────────────────────────
def hex_to_rgba(h):
    return [
        ((h >> 16) & 0xFF) / 255.0,
        ((h >> 8)  & 0xFF) / 255.0,
        ( h        & 0xFF) / 255.0,
        1.0,
    ]

PARTES = [
    {
        "stl":       "piso.stl",
        "glb":       "piso.glb",
        "nombre":    "Piso del monumento",
        "color":     0xF2EDE0,
        "roughness": 0.85,
        "metalness": 0.00,
    },
    {
        "stl":       "base.stl",
        "glb":       "base.glb",
        "nombre":    "Bloque con inscripción",
        "color":     0xEEE9DC,
        "roughness": 0.80,
        "metalness": 0.00,
    },
    {
        "stl":       "frase.stl",
        "glb":       "frase.glb",
        "nombre":    "Texto La Patagonia Rebelde",
        "color":     0x141210,
        "roughness": 0.60,
        "metalness": 0.05,
    },
    {
        "stl":       "bayer_fixed.stl",
        "glb":       "bayer_fixed.glb",
        "nombre":    "Figura de Osvaldo Bayer",
        "color":     0x111111,
        "roughness": 0.40,
        "metalness": 0.05,
    },
    {
        "stl":       "cara_fixed.stl",
        "glb":       "cara_fixed.glb",
        "nombre":    "Detalle del rostro",
        "color":     0x1A1614,
        "roughness": 0.50,
        "metalness": 0.05,
    },
    {
        "stl":       "placa_fixed.stl",
        "glb":       "placa_fixed.glb",
        "nombre":    "Placa Osvaldo Bayer 1927-2018",
        "color":     0xF5F0E5,
        "roughness": 0.75,
        "metalness": 0.00,
    },
]


# ─────────────────────────────────────────────────────
def convertir(entrada_dir, salida_dir, aplicar_draco=False):

    os.makedirs(salida_dir, exist_ok=True)

    total_stl = 0
    total_glb = 0
    errores   = []

    print(f"\n{'─'*55}")
    print(f"  Monumento Osvaldo Bayer — STL → GLB")
    print(f"  Entrada : {os.path.abspath(entrada_dir)}/")
    print(f"  Salida  : {os.path.abspath(salida_dir)}/")
    print(f"{'─'*55}\n")

    for p in PARTES:
        src = os.path.join(entrada_dir, p["stl"])
        dst = os.path.join(salida_dir,  p["glb"])

        if not os.path.exists(src):
            msg = f"No encontrado: {src}"
            print(f"  ⚠️   {msg}")
            errores.append(msg)
            continue

        print(f"  → {p['nombre']}")
        print(f"    {p['stl']}", end=" ... ")
        sys.stdout.flush()

        try:
            # Cargar STL
            mesh = trimesh.load(src, force="mesh")

            # Aplicar material PBR
            material = mat.PBRMaterial(
                baseColorFactor = hex_to_rgba(p["color"]),
                roughnessFactor  = p["roughness"],
                metallicFactor   = p["metalness"],
                doubleSided      = False,
            )
            mesh.visual = trimesh.visual.TextureVisuals(material=material)

            # Exportar GLB
            glb_bytes = trimesh.exchange.gltf.export_glb(mesh)
            with open(dst, "wb") as f:
                f.write(glb_bytes)

            # Reporte de tamaño
            sz_stl = os.path.getsize(src)
            sz_glb = os.path.getsize(dst)
            pct    = (1 - sz_glb / sz_stl) * 100 if sz_stl > 0 else 0
            total_stl += sz_stl
            total_glb += sz_glb

            print(f"✓")
            print(f"    {_kb(sz_stl):>7} → {_kb(sz_glb):>7}  ({pct:+.0f}%)\n")

        except Exception as e:
            print(f"✗  ERROR")
            print(f"    {e}\n")
            errores.append(f"{p['stl']}: {e}")

    # ── Resumen ──────────────────────────────────────
    print(f"{'─'*55}")
    if total_stl > 0:
        total_pct = (1 - total_glb / total_stl) * 100
        print(f"  TOTAL  {_kb(total_stl):>8} → {_kb(total_glb):>8}  ({total_pct:+.0f}%)")
    if errores:
        print(f"\n  ⚠️  {len(errores)} error(es):")
        for e in errores:
            print(f"     • {e}")
    else:
        print(f"\n  ✅  Conversión completa sin errores.")

    # ── Draco ────────────────────────────────────────
    if aplicar_draco:
        _aplicar_draco(salida_dir)

    print(f"\n{'─'*55}")
    print(f"  Próximo paso: actualizá index.html para usar")
    print(f"  GLTFLoader en vez de STLLoader.")
    print(f"  Ver comentarios en el script para más info.")
    print(f"{'─'*55}\n")


def _kb(n):
    if n >= 1_048_576:
        return f"{n/1_048_576:.1f} MB"
    return f"{n/1024:.0f} KB"


def _aplicar_draco(salida_dir):
    """
    Aplica compresión Draco a todos los GLB usando gltf-pipeline.
    Requiere: npm install -g gltf-pipeline
    """
    print(f"\n  Aplicando compresión Draco...")

    # Verificar que gltf-pipeline esté instalado
    try:
        subprocess.run(
            ["gltf-pipeline", "--version"],
            check=True, capture_output=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ⚠️  gltf-pipeline no encontrado.")
        print("      Instalá con: npm install -g gltf-pipeline")
        print("      Luego corré manualmente:")
        for p in PARTES:
            f = os.path.join(salida_dir, p["glb"])
            print(f"        gltf-pipeline -i {f} -o {f} -d")
        return

    antes = 0
    despues = 0

    for p in PARTES:
        f = os.path.join(salida_dir, p["glb"])
        if not os.path.exists(f):
            continue

        sz_antes = os.path.getsize(f)
        antes += sz_antes

        try:
            subprocess.run(
                ["gltf-pipeline", "-i", f, "-o", f, "--draco.compressionLevel=7"],
                check=True, capture_output=True
            )
            sz_despues = os.path.getsize(f)
            despues += sz_despues
            pct = (1 - sz_despues / sz_antes) * 100
            print(f"    ✓  {p['glb']:30}  {_kb(sz_antes):>7} → {_kb(sz_despues):>7}  ({pct:.0f}%)")
        except subprocess.CalledProcessError as e:
            print(f"    ✗  {p['glb']}: {e}")

    if antes > 0:
        pct_total = (1 - despues / antes) * 100
        print(f"\n  Draco total: {_kb(antes)} → {_kb(despues)}  ({pct_total:.0f}%)")


# ─────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convierte los STL del monumento Bayer a GLB con materiales PBR."
    )
    parser.add_argument(
        "--entrada", "-i",
        default="files",
        help="Carpeta con los archivos STL (default: files/)"
    )
    parser.add_argument(
        "--salida", "-o",
        default="files_glb",
        help="Carpeta de salida para los GLB (default: files_glb/)"
    )
    parser.add_argument(
        "--draco", "-d",
        action="store_true",
        help="Aplicar compresión Draco después de convertir (requiere gltf-pipeline)"
    )

    args = parser.parse_args()
    convertir(args.entrada, args.salida, aplicar_draco=args.draco)

"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRÓXIMOS PASOS: actualizar index.html para usar GLB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Cambiar el importmap para agregar GLTFLoader:
   (ya incluido en three/addons/ — no requiere cambio)

2. Reemplazar STLLoader por GLTFLoader:

   // ANTES
   import { STLLoader } from 'three/addons/loaders/STLLoader.js';
   const loader = new STLLoader();
   loader.load(part.file, (geometry) => {
       geometry.computeBoundingBox();
       geometry.center();
       geometry.scale(S, S, S);
       const mesh = new THREE.Mesh(geometry, material);
   });

   // DESPUÉS
   import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
   import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

   const draco = new DRACOLoader();
   draco.setDecoderPath('https://unpkg.com/three@0.158.0/examples/jsm/libs/draco/');

   const loader = new GLTFLoader();
   loader.setDRACOLoader(draco);

   loader.load(part.file, (gltf) => {
       const mesh = gltf.scene.children[0];
       mesh.geometry.computeBoundingBox();
       mesh.geometry.center();
       mesh.geometry.scale(S, S, S);
       // El material ya viene del GLB — no hace falta asignarlo
   });

3. Actualizar los paths en PARTS:
   file: 'files_glb/piso.glb'   (en vez de 'files/piso.stl')

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

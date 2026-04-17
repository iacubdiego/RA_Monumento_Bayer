# Monumento a Osvaldo Bayer — Experiencia AR

Réplica digital del monumento destruido el 25 de marzo de 2025.  
Armado animado en Realidad Aumentada, directo desde el navegador del celular.

---

## ¿Cómo funciona?

Al abrir el proyecto en el celular:
1. La cámara se activa
2. Apuntás al piso de la plaza
3. Tocás la pantalla para colocar el monumento
4. Las 6 piezas caen desde arriba en orden:
   - Piso (bandeja base)
   - Bloque central con inscripción
   - Texto "La Patagonia Rebelde"
   - Figura de Osvaldo Bayer
   - Detalle del rostro
   - Placa "Osvaldo Bayer 1927–2018"

---

## ⚠️ Requisito importante: HTTPS

WebXR (la tecnología de AR) **solo funciona en sitios HTTPS**.  
No podés abrir `index.html` directo desde el explorador de archivos.

---

## Opciones para publicar / compartir

### Opción A — GitHub Pages (gratis, sin instalar nada)

1. Creá una cuenta en [github.com](https://github.com)
2. Creá un repositorio nuevo (público)
3. Subí toda la carpeta `monument-ar/`  
   (arrastrá los archivos al explorador web del repo)
4. Andá a **Settings → Pages → Source: main branch / root**
5. En unos minutos tenés una URL tipo:  
   `https://tunombre.github.io/monument-ar/`
6. Abrí esa URL desde el celular → listo

### Opción B — Netlify Drop (más rápido aún)

1. Andá a [app.netlify.com/drop](https://app.netlify.com/drop)
2. Arrastrá la carpeta `monument-ar/` completa
3. Obtenés una URL pública en segundos

### Opción C — Servidor local con Python (para testear en casa)

Necesitás Python 3 y el celular en la misma red Wi-Fi.

```bash
# 1. Instalar el módulo de servidor HTTPS simple
pip install trustme

# 2. Ir a la carpeta del proyecto
cd monument-ar

# 3. Servidor HTTPS rápido
python3 -m http.server 8443
```

Luego abrí `http://[IP-de-tu-compu]:8443` en el celular.  
(Si no funciona WebXR con http, usá la Opción A o B.)

### Opción D — ngrok (túnel HTTPS instantáneo)

```bash
# 1. Instalar ngrok desde https://ngrok.com
# 2. Correr servidor local
cd monument-ar && python3 -m http.server 8080
# 3. En otra terminal
ngrok http 8080
# 4. Usar la URL https://xxx.ngrok.io que aparece
```

---

## Compatibilidad

| Dispositivo | Estado |
|---|---|
| Android — Chrome | ✅ AR completo (ARCore) |
| iPhone iOS 16+ — Safari | ✅ AR completo (ARKit) |
| Desktop Chrome/Firefox | ✅ Modo 3D (sin AR) |
| Android — Firefox | ⚠️ Solo modo 3D |

---

## Estructura de archivos

```
monument-ar/
├── index.html          ← Toda la experiencia (una sola página)
├── README.md           ← Este archivo
└── files/
    ├── piso.stl        ← Bandeja base
    ├── base.stl        ← Bloque con inscripción
    ├── frase.stl       ← Panel "La Patagonia Rebelde"
    ├── bayer_fixed.stl ← Silueta de Bayer
    ├── cara_fixed.stl  ← Detalle del rostro
    └── placa_fixed.stl ← Placa "Osvaldo Bayer 1927–2018"
```

---

## Créditos

Modelos 3D originales: [mpv_ en Thingiverse](https://www.thingiverse.com/thing:6999576)  
Licencia: CC Attribution-ShareAlike

**La memoria no se destruye.**

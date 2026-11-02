"""Create a synthetic, non-personal review fixture under outputs/."""
from pathlib import Path
import pymupdf
from manuscrito.cli import extraer, guardar, revisar

carpeta = Path('outputs/synthetic-review')
carpeta.mkdir(parents=True, exist_ok=True)
ruta = carpeta/'source.pdf'
pdf = pymupdf.open()
pagina = pdf.new_page()
regiones = []
for indice, caracter in enumerate('abcabc'):
    x = 20 + indice*25
    pagina.insert_text((x, 40), caracter)
    regiones.append(dict(character=caracter, page=1, rect=[x-1, 28, x+10, 43]))
pdf.save(ruta)
pdf.close()
biblioteca = extraer(ruta, dict(source_cell=24, regions=regiones))
guardar(carpeta/'candidates.json', biblioteca)
(carpeta/'review.html').write_text(revisar(biblioteca), encoding='utf-8')
print(carpeta/'review.html')

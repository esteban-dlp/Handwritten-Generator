"""Local CLI for rendering, extraction and explicit sample approval."""
import argparse
import base64
import hashlib
import html
import json
import random
from pathlib import Path

CONFIGURACION = dict(width=595.28, height=841.89, cell=18, margin_cells=1,
    paper='grid', font_size=12, seed=42, deformation=[0.985, 1.015],
    gap=[0.05, 0.08], word_space=0.38, ink='#202124')


def leer(ruta):
    return json.loads(Path(ruta).read_text(encoding='utf-8'))


def guardar(ruta, datos):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding='utf-8')


class Bolsa:
    def __init__(self, semilla):
        self.azar = random.Random(semilla)
        self.estados = {}

    def elegir(self, caracter, muestras):
        if not muestras:
            raise ValueError('Empty sample list: ' + caracter)
        estado = self.estados.setdefault(caracter, dict(resto=[], ultimo=None, orden=None))
        if not estado['resto']:
            orden = list(range(len(muestras)))
            while True:
                self.azar.shuffle(orden)
                if len(orden) == 1 or (orden[0] != estado['ultimo'] and
                        (len(orden) < 3 or tuple(orden) != estado['orden'])):
                    break
            estado['orden'] = tuple(orden)
            estado['resto'] = orden[:]
        indice = estado['resto'].pop(0)
        estado['ultimo'] = indice
        return muestras[indice]


def versionar(carpeta):
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    numero = 1
    while (carpeta / f'v{numero:04d}').exists():
        numero += 1
    destino = carpeta / f'v{numero:04d}'
    destino.mkdir()
    return destino


def documento(cuerpo, config):
    ancho, alto, paso = config['width'], config['height'], config['cell']
    fondo = ''
    if config['paper'] in ('grid', 'ruled'):
        fondo += ''.join(f'<line x1="0" y1="{y}" x2="{ancho}" y2="{y}"/>'
            for y in range(int(paso), int(alto), int(paso)))
    if config['paper'] == 'grid':
        fondo += ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{alto}"/>'
            for x in range(int(paso), int(ancho), int(paso)))
    return (f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Handwriting document</title>'
        f'<style>@page{{size:{ancho}pt {alto}pt;margin:0}}body{{margin:0}}'
        f'.page{{width:{ancho}pt;height:{alto}pt;display:block;break-after:page}}'
        '.page:last-child{break-after:auto}svg{display:block}</style>' +
        ''.join(f'<svg class="page" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}">'
        f'<g stroke="#dce4ec" stroke-width="0.3">{fondo}</g>{pagina}</svg>' for pagina in cuerpo))


def exportar(texto, destino, config):
    import pymupdf
    from weasyprint import HTML
    (destino / 'document.html').write_text(texto, encoding='utf-8')
    pdf = destino / 'document.pdf'
    HTML(string=texto).write_pdf(pdf)
    with pymupdf.open(pdf) as documento_pdf:
        for pagina in documento_pdf:
            if abs(pagina.rect.width-config['width']) > 0.1 or abs(pagina.rect.height-config['height']) > 0.1:
                raise ValueError('Unexpected PDF page dimensions')
    archivos = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in destino.iterdir() if p.is_file()}
    guardar(destino / 'manifest.json', dict(config=config, sha256=archivos))


def renderizar(texto, biblioteca, config):
    import pymupdf
    paso = config['cell']
    if paso < 2 or config['width'] <= 4*paso or config['height'] <= 4*paso:
        raise ValueError('Invalid page/cell dimensions')
    minimo, maximo = config['deformation']
    if not 0 < minimo <= 1 <= maximo:
        raise ValueError('Deformation must contain 1.0')
    muestras = biblioteca.get('characters', {})
    faltantes = sorted(set(texto) - set(muestras) - set(' \n\r\t'))
    if biblioteca.get('mode') != 'font' and faltantes:
        raise ValueError('Missing characters: ' + repr(''.join(faltantes)))
    azar = random.Random(config['seed'])
    bolsa = Bolsa(config['seed'])
    margen = config['margin_cells']*paso
    cursor, fila = margen, margen
    paginas, partes = [], []
    for caracter in texto.replace('\r', ''):
        if caracter == '\n':
            cursor, fila = margen, fila+paso
            continue
        if caracter in ' \t':
            cursor += paso*config['word_space']*(4 if caracter == '\t' else 1)
            continue
        sx, sy = (azar.uniform(minimo, maximo), 1) if azar.getrandbits(1) else (1, azar.uniform(minimo, maximo))
        if biblioteca.get('mode') == 'font':
            altura = config['font_size']
            ancho = pymupdf.get_text_length(caracter, fontsize=altura)
            trazo = None
        else:
            muestra = bolsa.elegir(caracter, muestras[caracter])
            escala = paso/biblioteca.get('source_cell', 16)
            ancho, altura = muestra['width']*escala, muestra['height']*escala
            trazo = muestra['png']
        ancho, altura = ancho*sx, altura*sy
        if altura > paso*0.95 or ancho > config['width']-2*margen:
            raise ValueError('Sample exceeds layout: ' + caracter)
        if cursor+ancho > config['width']-margen:
            cursor, fila = margen, fila+paso
        if fila+paso > config['height']-margen:
            paginas.append(''.join(partes))
            partes, cursor, fila = [], margen, margen
        centro = azar.uniform(0.45, 0.55)
        if caracter in ',.':
            centro = 0.77
        elif caracter in "'’":
            centro = 0.24
        y = fila+max(0, min(paso-altura, paso*centro-altura/2))
        if trazo:
            partes.append(f'<image x="{cursor}" y="{y}" width="{ancho}" height="{altura}" '
                f'preserveAspectRatio="none" href="data:image/png;base64,{trazo}"/>')
        else:
            partes.append(f'<text x="0" y="0" font-family="serif" font-style="italic" '
                f'font-size="{config["font_size"]}" fill="{config["ink"]}" '
                f'transform="translate({cursor} {y+altura*0.8}) scale({sx} {sy})">{html.escape(caracter)}</text>')
        cursor += ancho+paso*azar.uniform(*config['gap'])
    paginas.append(''.join(partes))
    return documento(paginas, config)


def extraer(ruta, mapa):
    import pymupdf
    resultado = dict(source_cell=mapa.get('source_cell', 16), characters={})
    huellas = set()
    with pymupdf.open(ruta) as pdf:
        for region in mapa['regions']:
            caracter = region['character']
            if len(caracter) != 1:
                raise ValueError('Each region must label one Unicode character')
            pagina = pdf[region['page']-1]
            caja = pymupdf.Rect(region['rect'])
            if caja.is_empty or not pagina.rect.contains(caja):
                raise ValueError('Region outside page')
            imagen = pagina.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=caja, alpha=True)
            datos = imagen.tobytes('png')
            huella = hashlib.sha256(datos).hexdigest()
            if (caracter, huella) in huellas:
                continue
            huellas.add((caracter, huella))
            muestra = dict(id=huella[:16], width=caja.width, height=caja.height,
                png=base64.b64encode(datos).decode(), source=Path(ruta).name,
                page=region['page'], rect=list(caja), status='candidate')
            resultado['characters'].setdefault(caracter, []).append(muestra)
    return resultado


def revisar(biblioteca):
    # las etiquetas se serializan como json y se insertan con textcontent
    datos = json.dumps(biblioteca, ensure_ascii=True).replace('<', '\\u003c')
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sample review</title>
<style>body{font:16px system-ui;max-width:1100px;margin:24px auto;padding:16px;background:#f5f7fb}button{padding:10px;cursor:pointer}section{background:white;padding:16px;margin:16px 0;border-radius:12px}.samples{display:flex;flex-wrap:wrap;gap:12px}label{border:1px solid #ccd;padding:12px;display:grid;gap:8px}img{width:52px;height:52px;object-fit:contain} @media print{button,input{display:none}body{background:white}}</style>
<h1>Review handwriting samples</h1><p>Uncheck unwanted samples, then download the approved library. This page does not modify the source file.</p><button id="save">Download approved library</button><main id="library"></main><script>
const library=DATA;const main=document.getElementById('library');
for(const [character,samples] of Object.entries(library.characters)){const section=document.createElement('section');const h=document.createElement('h2');h.textContent=character+' — '+samples.length+' samples';section.append(h);const row=document.createElement('div');row.className='samples';for(const sample of samples){const label=document.createElement('label');const input=document.createElement('input');input.type='checkbox';input.checked=true;input.dataset.id=sample.id;const image=document.createElement('img');image.src='data:image/png;base64,'+sample.png;const caption=document.createElement('span');caption.textContent=sample.id;label.append(input,image,caption);row.append(label)}section.append(row);main.append(section)}
document.getElementById('save').onclick=()=>{const rejected=new Set([...document.querySelectorAll('input:not(:checked)')].map(x=>x.dataset.id));const result=structuredClone(library);for(const c in result.characters){result.characters[c]=result.characters[c].filter(s=>!rejected.has(s.id)).map(s=>({...s,status:'approved'}));if(!result.characters[c].length)delete result.characters[c]}const a=document.createElement('a');const url=URL.createObjectURL(new Blob([JSON.stringify(result,null,2)],{type:'application/json'}));a.href=url;a.download='approved-library.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
</script></html>'''.replace('DATA', datos)


def principal():
    parser = argparse.ArgumentParser(description='Local handwriting renderer and sample review tools')
    sub = parser.add_subparsers(dest='command', required=True)
    setup = sub.add_parser('setup'); setup.add_argument('--config', required=True)
    render = sub.add_parser('render'); render.add_argument('text'); render.add_argument('--library', required=True); render.add_argument('--config', required=True); render.add_argument('--output', default='outputs')
    extract = sub.add_parser('extract'); extract.add_argument('pdf'); extract.add_argument('--regions', required=True); extract.add_argument('--output', required=True)
    review = sub.add_parser('review'); review.add_argument('library'); review.add_argument('--output', required=True)
    count = sub.add_parser('counts'); count.add_argument('library')
    argumentos = parser.parse_args()
    if argumentos.command == 'setup':
        ruta = Path(argumentos.config)
        if ruta.exists():
            parser.error('Config already exists; edit it explicitly instead of overwriting')
        guardar(ruta, CONFIGURACION)
    elif argumentos.command == 'extract':
        guardar(argumentos.output, extraer(argumentos.pdf, leer(argumentos.regions)))
    elif argumentos.command == 'review':
        ruta = Path(argumentos.output); ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(revisar(leer(argumentos.library)), encoding='utf-8')
    elif argumentos.command == 'counts':
        print(json.dumps({c:len(v) for c,v in leer(argumentos.library)['characters'].items()}, ensure_ascii=False, indent=2))
    else:
        config = CONFIGURACION | leer(argumentos.config)
        texto = Path(argumentos.text).read_text(encoding='utf-8')
        salida = versionar(argumentos.output)
        exportar(renderizar(texto, leer(argumentos.library), config), salida, config)
        print(salida)


if __name__ == '__main__':
    principal()

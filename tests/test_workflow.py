import json
import tempfile
import unittest
from pathlib import Path
import pymupdf
from manuscrito.cli import Bolsa, CONFIGURACION, documento, exportar, extraer, renderizar, revisar, versionar


class Pruebas(unittest.TestCase):
    def test_bolsa_ciclos(self):
        bolsa = Bolsa(42)
        valores = [bolsa.elegir('a', list(range(8))) for _ in range(80)]
        for i in range(0, 80, 8):
            self.assertEqual(set(valores[i:i+8]), set(range(8)))
        self.assertTrue(all(a != b for a, b in zip(valores, valores[1:])))
        self.assertNotEqual(valores[:8], valores[8:16])

    def test_semilla(self):
        a, b = Bolsa(12), Bolsa(12)
        self.assertEqual([a.elegir('a', [1,2,3]) for _ in range(30)],
            [b.elegir('a', [1,2,3]) for _ in range(30)])

    def test_faltantes(self):
        with self.assertRaises(ValueError):
            renderizar('x', {'characters': {}}, CONFIGURACION)

    def test_versiones(self):
        with tempfile.TemporaryDirectory() as carpeta:
            self.assertEqual(versionar(carpeta).name, 'v0001')
            self.assertEqual(versionar(carpeta).name, 'v0002')

    def test_pdf_y_paginacion(self):
        with tempfile.TemporaryDirectory() as carpeta:
            texto = renderizar(('A short line\n'*100), {'mode':'font'}, CONFIGURACION)
            self.assertGreater(texto.count('class="page"'), 1)
            destino = versionar(carpeta)
            exportar(texto, destino, CONFIGURACION)
            with pymupdf.open(destino/'document.pdf') as pdf:
                self.assertGreater(len(pdf), 1)
                self.assertAlmostEqual(pdf[0].rect.width, CONFIGURACION['width'], places=1)
            self.assertTrue((destino/'manifest.json').exists())

    def test_extraccion_y_revision(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta)/'synthetic.pdf'
            pdf = pymupdf.open()
            pagina = pdf.new_page()
            pagina.insert_text((20, 40), 'a')
            pdf.save(ruta)
            pdf.close()
            region = dict(character='a', page=1, rect=[18, 25, 30, 44])
            biblioteca = extraer(ruta, dict(source_cell=24, regions=[region, region]))
            self.assertEqual(len(biblioteca['characters']['a']), 1)
            self.assertIn('Download approved library', revisar(biblioteca))
            self.assertIn('data:image/png;base64,', renderizar('a', biblioteca, CONFIGURACION | {'cell':32}))

    def test_eje_unico(self):
        import re
        texto = renderizar('a'*80, {'mode':'font'}, CONFIGURACION)
        escalas = re.findall(r'scale\(([^ ]+) ([^)]+)\)', texto)
        self.assertEqual(len(escalas), 80)
        for x,y in escalas:
            x,y = float(x),float(y)
            self.assertTrue(0.985 <= x <= 1.015 and 0.985 <= y <= 1.015)
            self.assertTrue(x == 1 or y == 1)

    def test_revision_segura(self):
        resultado = revisar({'characters': {'<': []}})
        self.assertIn('\\u003c', resultado)


if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-
"""Genera capturas de WhatsApp para los testimonios: HTML -> Playwright -> WebP.

Tipos de mensaje: txt | audio | img
Cada mensaje es un dict: {q:'in'|'out', tipo, t, h, seg, src, reply:(quien,texto), tick:'gris'|'azul'}
"""
import io, sys, os, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright
from PIL import Image

BASE = pathlib.Path(__file__).parent.parent
OUT = BASE / 'img' / 'wa'
OUT.mkdir(parents=True, exist_ok=True)
AV = 'https://czocbnyoenjbpxmcqobn.supabase.co/storage/v1/object/public/algoritmia-img/adiestramiento-canino/testi'
YO = 'https://czocbnyoenjbpxmcqobn.supabase.co/storage/v1/object/public/algoritmia-img/adiestramiento-canino/andres/retrato.webp'
FOTO = (BASE / 'img' / 'wa' / 'foto-perro.webp').as_uri()

def T(q, t, h, **k): return dict(q=q, tipo='txt', t=t, h=h, **k)
def A(q, seg, h, **k): return dict(q=q, tipo='audio', seg=seg, h=h, **k)
def I(q, src, h, t=None, **k): return dict(q=q, tipo='img', src=src, t=t, h=h, **k)

CHATS = [
 ('wa-1', 'Mónica', f'{AV}/real-1.webp', 'en línea', 'HOY', [
   T('in', 'andres perdón que te escriba un domingo', '11:04'),
   T('in', 'pero tenia que contarte', '11:04'),
   T('in', 'hoy fuimos a la plaza, lo solté y volvió a la primera 😭😭', '11:05'),
   I('in', FOTO, '11:05', 'quedó así después jaja'),
   T('in', 'dos años que no lo podia soltar en ningun lado', '11:06'),
   A('out', '0:23', '11:19'),
   T('in', 'siii lo voy a hacer. gracias en serio 🙏', '11:24'),
 ]),
 ('wa-2', 'Esteban', f'{AV}/real-2.webp', 'últ. vez hoy a las 9:41', 'AYER', [
   T('in', 'che la clase 3 me voló la cabeza', '21:38'),
   T('in', 'le estaba dando el premio TARDE. todo este tiempo 🤦‍♂️', '21:38'),
   T('in', 'cambié eso solo y en 3 dias se sienta a la primera', '21:39'),
   T('out', 'es el error mas comun de todos y no lo ve nadie', '21:45'),
   T('in', 'tengo 4 libros de perros y ninguno me lo habia dicho asi', '21:47',
     reply=('Andrés', 'es el error mas comun de todos y no lo ve nadie')),
   T('out', 'jaja bienvenido al club', '21:52', tick='gris'),
 ]),
 ('wa-3', 'Rosana', f'{AV}/real-3.webp', 'en línea', 'HOY', [
   T('in', 'Hola Andrés!! te queria agradecer', '19:22'),
   T('in', 'compre el completo medio dudando de los cuidados, pensé que no los iba a usar nunca', '19:22'),
   T('in', 'ayer se corto una pata y se la cure sola', '19:23'),
   T('in', 'quieto, sin bozal, sin morderme. un domingo a la noche con todo cerrado', '19:23'),
   T('in', 'no lo puedo creer todavia', '19:24'),
   A('out', '0:41', '19:31'),
 ]),
 ('wa-4', 'Martín', f'{AV}/real-5.webp', 'últ. vez hoy a las 20:10', 'HOY', [
   T('in', '3 años peleandome con la correa', '20:05'),
   T('in', 'una semana con la fase 2 y hoy hicimos la cuadra entera con la correa floja', '20:05'),
   T('in', 'no me faltaba mano dura. me faltaba orden', '20:06'),
   T('out', 'esa es exactamente la frase 👌', '20:09',
     reply=('Martín', 'no me faltaba mano dura. me faltaba orden')),
   T('in', 'la voy a poner en el cuadro jajaja', '20:11'),
 ]),
('wa-5', 'Vanina', f'{AV}/real-4.webp', 'en línea', 'HOY', [
   T('in', 'tres semanas exactas', '13:12'),
   T('in', 'se sienta a la primera, sin que le muestre la comida', '13:12'),
   T('in', 'mi marido no lo podia creer jajaja', '13:13'),
   T('out', 'jaja pasa siempre eso', '13:20'),
   T('out', 'ahora empeza a soltar el premio de a poco, como en la clase 6', '13:20', tick='gris'),
 ]),
 ('wa-6', 'Diego', f'{AV}/real-6.webp', 'últ. vez ayer a las 22:03', 'AYER', [
   T('in', 'vinieron mis suegros el domingo', '18:44'),
   T('in', 'no salto NI UNA VEZ', '18:44'),
   T('in', 'antes tenia que agarrarlo del collar apenas tocaban el timbre', '18:45'),
   T('out', 'y cuanto tardaste?', '18:51'),
   T('in', 'como diez dias. lo hice todos los dias 5 min antes de cenar', '18:53'),
 ]),
 ('wa-7', 'Carolina', f'{AV}/real-1.webp', 'en línea', 'HOY', [
   T('in', 'Andrés te tengo que contar algo', '09:31'),
   T('in', 'me fui a trabajar y volvi 6 horas despues', '09:31'),
   T('in', 'la vecina no me dijo nada. NADA. antes me escribia todos los dias', '09:32'),
   T('in', 'lloraba desde que cerraba la puerta hasta que volvia 😭', '09:32'),
   A('out', '0:35', '09:48'),
 ]),
 ('wa-8', 'Lucas', f'{AV}/real-3.webp', 'últ. vez hoy a las 11:20', 'HOY', [
   T('in', 'compre el avanzado hace 2 meses', '11:02'),
   T('in', 'hoy fuimos al parque y jugamos al frisbee media hora', '11:02'),
   T('in', 'lo suelto y se queda conmigo. sin correa, sin premios en la mano', '11:03'),
   T('out', 'eso es exactamente el punto del ultimo tramo 👏', '11:14'),
   T('in', 'la gente me pregunta a que escuela lo mande jajaja', '11:16'),
 ]),
]

DOODLE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='260' height='260' "
          "viewBox='0 0 260 260'%3E%3Cg fill='none' stroke='%23d9d0c4' stroke-width='1.4' opacity='.55'%3E"
          "%3Ccircle cx='40' cy='36' r='9'/%3E%3Cpath d='M96 30h22M96 38h14'/%3E"
          "%3Cpath d='M172 24c6-6 16-6 22 0s6 16 0 22'/%3E%3Ccircle cx='226' cy='62' r='6'/%3E"
          "%3Cpath d='M26 104c8-9 22-9 30 0'/%3E%3Cpath d='M112 96l12 12-12 12-12-12z'/%3E"
          "%3Cpath d='M186 104h26M186 112h16'/%3E%3Ccircle cx='60' cy='168' r='11'/%3E"
          "%3Cpath d='M128 160c7-7 19-7 26 0s7 19 0 26'/%3E%3Cpath d='M212 166l10 10-10 10-10-10z'/%3E"
          "%3Cpath d='M34 226h24M34 234h15'/%3E%3Ccircle cx='120' cy='230' r='8'/%3E"
          "%3Cpath d='M190 222c8-8 20-8 28 0'/%3E%3C/g%3E%3C/svg%3E\")")

TICK = ('<svg class="tk {cls}" viewBox="0 0 16 11"><path d="M11.07.65 5.5 6.22 4.2 4.93l-.7.7 2 2 6.27-6.28z"/>'
        '<path d="M15.07.65 9.5 6.22 8.2 4.93l-.7.7 2 2L15.77 1.35z"/></svg>')

# barras de la onda de audio, alturas fijas para que parezca real
ONDA = [6,11,17,9,14,20,13,8,16,22,12,7,15,19,10,6,13,18,11,8,14,9,17,12,7,15,10,6,12,8]

def meta(m):
    t = TICK.format(cls=m.get('tick', 'azul')) if m['q'] == 'out' else ''
    return f'<span class="mt">{m["h"]}{t}</span>'

def quote(m):
    if 'reply' not in m: return ''
    who, txt = m['reply']
    return f'<div class="rp"><b>{who}</b><span>{txt}</span></div>'

def burbuja(m, avatar):
    q = m['q']
    if m['tipo'] == 'audio':
        barras = ''.join(f'<i style="height:{h}px"></i>' for h in ONDA)
        return (f'<div class="ln {q}"><div class="bb au">'
                f'<img class="aav" src="{YO if q == chr(111)+chr(117)+chr(116) else avatar}">'
                f'<svg class="pl" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>'
                f'<div class="wv">{barras}</div>'
                f'<div class="ad">{m["seg"]}<svg class="mic" viewBox="0 0 24 24">'
                f'<path d="M12 14a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v5a3 3 0 0 0 3 3z"/>'
                f'<path d="M18 11a6 6 0 0 1-12 0H4a8 8 0 0 0 7 7.9V22h2v-3.1A8 8 0 0 0 20 11z"/></svg>'
                f'{meta(m)}</div></div></div>')
    if m['tipo'] == 'img':
        pie = f'<div class="ic-t">{m["t"]}{meta(m)}</div>' if m.get('t') else f'<div class="ic-s">{meta(m)}</div>'
        return f'<div class="ln {q}"><div class="bb im">{quote(m)}<img src="{m["src"]}">{pie}</div></div>'
    return f'<div class="ln {q}"><div class="bb">{quote(m)}{m["t"]}{meta(m)}</div></div>'

def chat_html(nombre, avatar, estado, dia, msgs):
    return f'''<div class="wa">
  <div class="hd">
    <svg class="bk" viewBox="0 0 24 24"><path d="M15.5 4 8 12l7.5 8" fill="none" stroke="#fff" stroke-width="2.2"
      stroke-linecap="round" stroke-linejoin="round"/></svg>
    <img class="av" src="{avatar}">
    <div class="nm"><b>{nombre}</b><span>{estado}</span></div>
    <svg class="ic" viewBox="0 0 24 24"><path d="M15 8.5V7a1.5 1.5 0 0 0-1.5-1.5h-9A1.5 1.5 0 0 0 3 7v10a1.5 1.5 0
      0 0 1.5 1.5h9A1.5 1.5 0 0 0 15 17v-1.5l6 3.5v-14z" fill="#fff"/></svg>
    <svg class="ic" viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6
      3.7.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.7.1.3 0
      .7-.2 1z" fill="#fff"/></svg>
    <svg class="ic dots" viewBox="0 0 24 24"><circle cx="12" cy="5" r="1.8" fill="#fff"/><circle cx="12" cy="12"
      r="1.8" fill="#fff"/><circle cx="12" cy="19" r="1.8" fill="#fff"/></svg>
  </div>
  <div class="bd">
    <div class="dia"><span>{dia}</span></div>
    {''.join(burbuja(m, avatar) for m in msgs)}
  </div>
</div>'''

CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#fff;font-family:'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif;
  display:flex;flex-wrap:wrap;gap:26px;padding:26px}}
.wa{{width:400px;background:#efeae2;border-radius:10px;overflow:hidden;
  box-shadow:0 1px 3px rgba(0,0,0,.14)}}
.hd{{background:#008069;display:flex;align-items:center;gap:9px;padding:9px 12px}}
.bk{{width:19px;height:19px;flex:0 0 auto}}
.av{{width:37px;height:37px;border-radius:50%;object-fit:cover;flex:0 0 auto}}
.nm{{flex:1;min-width:0;line-height:1.2}}
.nm b{{display:block;color:#fff;font-size:15.5px;font-weight:600}}
.nm span{{display:block;color:#cfe9e2;font-size:12px}}
.ic{{width:19px;height:19px;flex:0 0 auto;opacity:.95}}
.ic.dots{{width:15px}}
.bd{{background:#efeae2;background-image:{DOODLE};padding:12px 10px 16px;min-height:120px}}
.dia{{text-align:center;margin:2px 0 12px}}
.dia span{{background:#e2f2ea;color:#5b6b66;font-size:11px;font-weight:600;letter-spacing:.4px;
  padding:5px 11px;border-radius:7px;box-shadow:0 1px 1px rgba(0,0,0,.07)}}
.ln{{display:flex;margin-bottom:5px}}
.ln.out{{justify-content:flex-end}}
.bb{{position:relative;max-width:82%;background:#fff;border-radius:8px;padding:6px 9px 5px 10px;
  font-size:14.6px;line-height:1.36;color:#111b21;box-shadow:0 1px .5px rgba(11,20,26,.13);
  word-wrap:break-word}}
.ln.out .bb{{background:#d9fdd3}}
.bb .mt{{float:right;margin:6px 0 -2px 9px;font-size:11px;color:#667781;
  display:inline-flex;align-items:center;gap:3px;white-space:nowrap}}
.tk{{width:15px;height:11px}}
.tk.azul{{fill:#53bdeb}}
.tk.gris{{fill:#8696a0}}

/* respuesta citada */
.rp{{background:rgba(0,0,0,.05);border-left:3.5px solid #06cf9c;border-radius:5px;
  padding:5px 8px;margin-bottom:4px;font-size:12.8px;line-height:1.3;overflow:hidden}}
.ln.out .rp{{border-left-color:#53bdeb}}
.rp b{{display:block;color:#06cf9c;font-size:12.6px;font-weight:600}}
.ln.out .rp b{{color:#53bdeb}}
.rp span{{display:block;color:#5b6b66;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}

/* audio */
.bb.au{{display:flex;align-items:center;gap:8px;padding:8px 10px 8px 8px;min-width:270px}}
.aav{{width:34px;height:34px;border-radius:50%;object-fit:cover;flex:0 0 auto}}
.pl{{width:19px;height:19px;fill:#54656f;flex:0 0 auto}}
.wv{{flex:1;display:flex;align-items:center;gap:2px;height:24px}}
.wv i{{display:block;width:2px;border-radius:1px;background:#c3ccd1}}
.wv i:nth-child(-n+7){{background:#8696a0}}
.ad{{font-size:11px;color:#667781;display:flex;align-items:center;gap:4px;white-space:nowrap}}
.ad .mt{{float:none;margin:0}}
.mic{{width:13px;height:13px;fill:#8696a0}}

/* imagen */
.bb.im{{padding:3px 3px 3px 3px;max-width:74%}}
.bb.im img{{width:100%;display:block;border-radius:6px}}
.ic-t{{padding:5px 6px 2px;font-size:14.6px;line-height:1.36}}
.ic-s{{position:absolute;right:9px;bottom:8px;background:rgba(0,0,0,.35);border-radius:9px;padding:1px 6px}}
.ic-s .mt{{float:none;margin:0;color:#fff}}
.ic-s .tk{{fill:#fff}}
'''

def main():
    html = ('<!doctype html><meta charset="utf-8"><style>' + CSS + '</style>' +
            ''.join(chat_html(n, a, e, d, m) for _, n, a, e, d, m in CHATS))
    tmp = BASE / '_qa' / '_wa.html'
    tmp.parent.mkdir(exist_ok=True)
    tmp.write_text(html, encoding='utf-8')

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1400, 'height': 1400}, device_scale_factor=2)
        pg.goto(tmp.as_uri())
        pg.wait_for_load_state('networkidle')
        pg.wait_for_timeout(1000)
        for i, (slug, *_r) in enumerate(CHATS):
            png = OUT / (slug + '.png')
            pg.locator('.wa').nth(i).screenshot(path=str(png))
            im = Image.open(png).convert('RGB')
            im.save(OUT / (slug + '.webp'), 'WEBP', quality=88, method=6)
            os.remove(png)
            print('%-7s %s  %d KB' % (slug, im.size, os.path.getsize(OUT / (slug + '.webp')) // 1024))
        b.close()
    tmp.unlink()
    print('\nLISTO ->', OUT)

if __name__ == '__main__':
    main()

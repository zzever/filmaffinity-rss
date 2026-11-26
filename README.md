# RSS de estrenos en plataformas desde FilmAffinity

Este paquete genera RSS con los estrenos/incorporaciones fechadas que FilmAffinity publica para estas plataformas:

- Movistar Plus+
- Filmin
- Prime Video España
- HBO Max / Max España
- Netflix España
- Disney+ España
- Apple TV+
- SkyShowtime
- Cartelera de cines

## Uso

```bash
pip install curl_cffi beautifulsoup4
python fa_rss.py
```

## URLs finales en GitHub Pages

```text
https://zzever.github.io/filmaffinity-rss/feeds/movistar.xml
https://zzever.github.io/filmaffinity-rss/feeds/filmin.xml
https://zzever.github.io/filmaffinity-rss/feeds/prime-video.xml
https://zzever.github.io/filmaffinity-rss/feeds/hbo-max.xml
https://zzever.github.io/filmaffinity-rss/feeds/netflix.xml
https://zzever.github.io/filmaffinity-rss/feeds/disney-plus.xml
https://zzever.github.io/filmaffinity-rss/feeds/apple-tv-plus.xml
https://zzever.github.io/filmaffinity-rss/feeds/skyshowtime.xml
https://zzever.github.io/filmaffinity-rss/feeds/cartelera.xml
```

## Actualización automática
<ul>
  <li><a href="feeds/movistar.xml">Movistar Plus+</a></li>
  <li><a href="feeds/filmin.xml">Filmin</a></li>
  <li><a href="feeds/prime-video.xml">Prime Video</a></li>
  <li><a href="feeds/hbo-max.xml">HBO Max</a></li>
  <li><a href="feeds/netflix.xml">Netflix</a></li>
  <li><a href="feeds/disney-plus.xml">Disney+</a></li>
  <li><a href="feeds/apple-tv-plus.xml">Apple TV+</a></li>
  <li><a href="feeds/skyshowtime.xml">SkyShowtime</a></li>
  <li><a href="feeds/cartelera.xml">Cartelera</a></li>
</ul>

El workflow incluido actualiza los RSS cada 6 horas.

Requiere que en el repositorio esté activado **Settings → Pages → Source: Deploy from a branch → `main` / `root`**, y que el workflow tenga permiso de escritura (**Settings → Actions → General → Workflow permissions → Read and write permissions**).

## Notas

FilmAffinity está detrás de Cloudflare y responde `403` a peticiones con `requests`/`curl`. Por eso el script usa `curl_cffi` con impersonación de Chrome, que sí obtiene el HTML. Si en el futuro vuelve a fallar con `403`, actualiza `curl_cffi` o cambia el valor de `impersonate` en `fa_rss.py`.


## Aviso legal

- Proyecto personal, sin ánimo de lucro y **sin ninguna afiliación** con FilmAffinity ni con las
  plataformas de streaming mencionadas. Sus marcas y logotipos pertenecen a sus titulares y aquí
  solo se citan de forma descriptiva.
- Los títulos, sinopsis, fechas y demás datos pertenecen a sus respectivos titulares. Los feeds los
  reproducen con fines informativos y de uso personal. El repositorio no aloja carteles, tráilers ni
  contenido audiovisual, ni da acceso a catálogos de pago.
- Los feeds están pensados para uso personal en un lector RSS. No se autoriza su uso comercial ni su
  redistribución masiva.
- El proyecto se limita a leer páginas públicas y no recoge ni almacena datos personales de terceros.
- Si algún titular de derechos considera que este repositorio excede el uso informativo, puede abrir
  un *issue* y el contenido en cuestión se retira.
- Los feeds pueden dejar de funcionar si el sitio de origen cambia su estructura o sus condiciones.
  Quien los consuma es responsable del uso que haga de ellos.

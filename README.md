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

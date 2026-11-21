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

Crea:

```text
feeds/movistar.xml
feeds/filmin.xml
feeds/prime-video.xml
feeds/hbo-max.xml
feeds/netflix.xml
feeds/disney-plus.xml
feeds/apple-tv-plus.xml
feeds/skyshowtime.xml
feeds/cartelera.xml
```

## URLs finales en GitHub Pages

```text
/filmaffinity-rss/feeds/movistar.xml
/filmaffinity-rss/feeds/filmin.xml
/filmaffinity-rss/feeds/prime-video.xml
/filmaffinity-rss/feeds/hbo-max.xml
/filmaffinity-rss/feeds/netflix.xml
/filmaffinity-rss/feeds/disney-plus.xml
/filmaffinity-rss/feeds/apple-tv-plus.xml
/filmaffinity-rss/feeds/skyshowtime.xml
/filmaffinity-rss/feeds/cartelera.xml
```

## Actualización automática

El workflow incluido actualiza los RSS cada 6 horas.

Requiere que en el repositorio esté activado **Settings → Pages → Source: Deploy from a branch → `main` / `root`**, y que el workflow tenga permiso de escritura (**Settings → Actions → General → Workflow permissions → Read and write permissions**).

## Notas

FilmAffinity está detrás de Cloudflare y responde `403` a peticiones con `requests`/`curl`. Por eso el script usa `curl_cffi` con impersonación de Chrome, que sí obtiene el HTML. Si en el futuro vuelve a fallar con `403`, actualiza `curl_cffi` o cambia el valor de `impersonate` en `fa_rss.py`.

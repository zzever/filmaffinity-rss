# RSS de estrenos en plataformas desde FilmAffinity

Este paquete genera RSS con los estrenos/incorporaciones fechadas que FilmAffinity publica para estas plataformas:

- Movistar Plus+
- Filmin
- Prime Video España
- HBO Max / Max España



## Uso

```bash
pip install requests beautifulsoup4
python fa_rss.py
```

Crea:

```text
feeds/movistar.xml
feeds/filmin.xml
feeds/prime-video.xml
feeds/max-hbo.xml
```

## URLs finales en GitHub Pages

```text
/filmaffinity-rss/feeds/movistar.xml
/filmaffinity-rss/feeds/filmin.xml
/filmaffinity-rss/feeds/prime-video.xml
/filmaffinity-rss/feeds/max-hbo.xml
```

## Actualización automática

El workflow incluido actualiza los RSS cada 6 horas.

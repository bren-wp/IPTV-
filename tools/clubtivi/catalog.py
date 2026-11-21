"""IPTV+ opt-in catalog of independent IPTV public directories.

Listings are references to externally maintained M3U indexes; their inclusion
is not proof of retransmission rights. Never bundle actual stream URLs.
"""
from urllib.parse import urlparse

GROUPS = [
  "🇭🇷 Hrvatska",
  "🇸🇮 Slovenija",
  "🇧🇦 Bosna i Hercegovina",
  "🇷🇸 Srbija",
  "🌍 Ostale države",
  "⚽ Sport i vijesti",
  "🎬 Filmovi i zabava",
  "🧸 Djeca i obitelj",
  "📚 Dokumentarni i edukativni",
  "🎵 Glazba i kultura",
  "🏠 Ostali žanrovi",
  "🌐 Ostali javni izvori"
]
SOURCES = [
  {
    "id": "iptvplus-country-hr",
    "name": "Hrvatska · iptv-org",
    "group": "🇭🇷 Hrvatska",
    "url": "https://iptv-org.github.io/iptv/countries/hr.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-si",
    "name": "Slovenija · iptv-org",
    "group": "🇸🇮 Slovenija",
    "url": "https://iptv-org.github.io/iptv/countries/si.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-ba",
    "name": "Bosna i Hercegovina · iptv-org",
    "group": "🇧🇦 Bosna i Hercegovina",
    "url": "https://iptv-org.github.io/iptv/countries/ba.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-rs",
    "name": "Srbija · iptv-org",
    "group": "🇷🇸 Srbija",
    "url": "https://iptv-org.github.io/iptv/countries/rs.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-me",
    "name": "Crna Gora · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/me.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-mk",
    "name": "Sjeverna Makedonija · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/mk.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-at",
    "name": "Austrija · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/at.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-de",
    "name": "Njemačka · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/de.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-it",
    "name": "Italija · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/it.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-hu",
    "name": "Mađarska · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/hu.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-ch",
    "name": "Švicarska · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/ch.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-gb",
    "name": "Ujedinjeno Kraljevstvo · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/gb.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-fr",
    "name": "Francuska · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/fr.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-es",
    "name": "Španjolska · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/es.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-nl",
    "name": "Nizozemska · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/nl.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-us",
    "name": "SAD · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-ca",
    "name": "Kanada · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/ca.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-country-au",
    "name": "Australija · iptv-org",
    "group": "🌍 Ostale države",
    "url": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "icon": "Icons.flag_outlined"
  },
  {
    "id": "iptvplus-category-sports",
    "name": "Sport · iptv-org",
    "group": "⚽ Sport i vijesti",
    "url": "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-news",
    "name": "Vijesti · iptv-org",
    "group": "⚽ Sport i vijesti",
    "url": "https://iptv-org.github.io/iptv/categories/news.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-business",
    "name": "Poslovne vijesti · iptv-org",
    "group": "⚽ Sport i vijesti",
    "url": "https://iptv-org.github.io/iptv/categories/business.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-legislative",
    "name": "Parlamenti · iptv-org",
    "group": "⚽ Sport i vijesti",
    "url": "https://iptv-org.github.io/iptv/categories/legislative.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-movies",
    "name": "Filmovi · iptv-org",
    "group": "🎬 Filmovi i zabava",
    "url": "https://iptv-org.github.io/iptv/categories/movies.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-series",
    "name": "Serije · iptv-org",
    "group": "🎬 Filmovi i zabava",
    "url": "https://iptv-org.github.io/iptv/categories/series.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-entertainment",
    "name": "Zabava · iptv-org",
    "group": "🎬 Filmovi i zabava",
    "url": "https://iptv-org.github.io/iptv/categories/entertainment.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-comedy",
    "name": "Komedija · iptv-org",
    "group": "🎬 Filmovi i zabava",
    "url": "https://iptv-org.github.io/iptv/categories/comedy.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-classic",
    "name": "Klasici · iptv-org",
    "group": "🎬 Filmovi i zabava",
    "url": "https://iptv-org.github.io/iptv/categories/classic.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-general",
    "name": "Opći programi · iptv-org",
    "group": "🎬 Filmovi i zabava",
    "url": "https://iptv-org.github.io/iptv/categories/general.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-kids",
    "name": "Dječji programi · iptv-org",
    "group": "🧸 Djeca i obitelj",
    "url": "https://iptv-org.github.io/iptv/categories/kids.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-animation",
    "name": "Crtani filmovi · iptv-org",
    "group": "🧸 Djeca i obitelj",
    "url": "https://iptv-org.github.io/iptv/categories/animation.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-family",
    "name": "Obiteljski programi · iptv-org",
    "group": "🧸 Djeca i obitelj",
    "url": "https://iptv-org.github.io/iptv/categories/family.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-documentary",
    "name": "Dokumentarci · iptv-org",
    "group": "📚 Dokumentarni i edukativni",
    "url": "https://iptv-org.github.io/iptv/categories/documentary.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-education",
    "name": "Obrazovanje · iptv-org",
    "group": "📚 Dokumentarni i edukativni",
    "url": "https://iptv-org.github.io/iptv/categories/education.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-science",
    "name": "Znanost · iptv-org",
    "group": "📚 Dokumentarni i edukativni",
    "url": "https://iptv-org.github.io/iptv/categories/science.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-music",
    "name": "Glazba · iptv-org",
    "group": "🎵 Glazba i kultura",
    "url": "https://iptv-org.github.io/iptv/categories/music.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-culture",
    "name": "Kultura · iptv-org",
    "group": "🎵 Glazba i kultura",
    "url": "https://iptv-org.github.io/iptv/categories/culture.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-lifestyle",
    "name": "Životni stil · iptv-org",
    "group": "🏠 Ostali žanrovi",
    "url": "https://iptv-org.github.io/iptv/categories/lifestyle.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-cooking",
    "name": "Kuhanje · iptv-org",
    "group": "🏠 Ostali žanrovi",
    "url": "https://iptv-org.github.io/iptv/categories/cooking.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-travel",
    "name": "Putovanja · iptv-org",
    "group": "🏠 Ostali žanrovi",
    "url": "https://iptv-org.github.io/iptv/categories/travel.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-weather",
    "name": "Vrijeme · iptv-org",
    "group": "🏠 Ostali žanrovi",
    "url": "https://iptv-org.github.io/iptv/categories/weather.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-auto",
    "name": "Automobili · iptv-org",
    "group": "🏠 Ostali žanrovi",
    "url": "https://iptv-org.github.io/iptv/categories/auto.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-outdoor",
    "name": "Priroda i aktivnosti · iptv-org",
    "group": "🏠 Ostali žanrovi",
    "url": "https://iptv-org.github.io/iptv/categories/outdoor.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-public",
    "name": "Javni programi · iptv-org",
    "group": "🏠 Ostali žanrovi",
    "url": "https://iptv-org.github.io/iptv/categories/public.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-religious",
    "name": "Vjerski programi · iptv-org",
    "group": "🏠 Ostali žanrovi",
    "url": "https://iptv-org.github.io/iptv/categories/religious.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-shop",
    "name": "Kupovina · iptv-org",
    "group": "🏠 Ostali žanrovi",
    "url": "https://iptv-org.github.io/iptv/categories/shop.m3u",
    "icon": "Icons.category_outlined"
  },
  {
    "id": "iptvplus-category-relax",
    "name": "Opuštanje · iptv-org",
    "group": "🏠 Ostali žanrovi",
    "url": "https://iptv-org.github.io/iptv/categories/relax.m3u",
    "icon": "Icons.category_outlined"
  }
]

def validate():
    ids = [item["id"] for item in SOURCES]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate IPTV+ directory IDs")
    if len(SOURCES) < 40:
        raise ValueError("Missing catalog categories")
    for item in SOURCES:
        uri = urlparse(item["url"])
        if (uri.scheme != "https" or uri.hostname != "iptv-org.github.io"
                or uri.username or uri.password or item["group"] not in GROUPS):
            raise ValueError("Invalid public directory: " + item["id"])

def escape_dart(value):
    return value.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")

def as_flutter_entries():
    validate()
    return "\n".join(
        "    FreeTvProvider(\n"
        "      id: '" + escape_dart(source["id"]) + "',\n"
        "      name: '" + escape_dart(source["name"]) + "',\n"
        "      group: '" + escape_dart(source["group"]) + "',\n"
        "      url: '" + escape_dart(source["url"]) + "',\n"
        "      description: 'Vanjski izvor; prava i dostupnost nisu zajamčeni.',\n"
        "      icon: " + source["icon"] + ",\n"
        "    ),"
        for source in SOURCES
    )

def as_flutter_groups():
    return "\n".join("    '" + escape_dart(group) + "'," for group in GROUPS)

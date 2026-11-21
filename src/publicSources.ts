import { type Channel, type Country, parseM3U } from './catalog';

/** Public playlist directories; this is not a license to retransmit their streams. */
export type PublicSource = {
  id: string;
  name: string;
  country: Country | 'GLOBAL';
  repo: string;
  url: string;
  tier: 'curated' | 'community';
  credit: string;
  notes: string;
};

export const PUBLIC_SOURCES: readonly PublicSource[] = [
  ...([
    ['hr', 'Hrvatska', 'HR'],
    ['ba', 'Bosna i Hercegovina', 'BA'],
    ['rs', 'Srbija', 'RS']
  ] as const).map(([code, label, country]): PublicSource => ({
    id: 'doubo-' + code,
    name: 'Doubo — ' + label,
    country,
    repo: 'https://github.com/streamline-iptv/iptv-playlists',
    url: 'https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/' + code + '.m3u',
    tier: 'curated',
    credit: 'Doubo Public Channel Directory (CC BY 4.0)',
    notes: 'Autor zbirke provodi strožu provjeru službenih streamova, ali prava svakog emitera ostaju zasebna.'
  })),
  ...([
    ['hr', 'Hrvatska', 'HR'],
    ['si', 'Slovenija', 'SI'],
    ['ba', 'Bosna i Hercegovina', 'BA'],
    ['rs', 'Srbija', 'RS']
  ] as const).map(([code, label, country]): PublicSource => ({
    id: 'iptvorg-' + code,
    name: 'iptv-org — ' + label,
    country,
    repo: 'https://github.com/iptv-org/iptv',
    url: 'https://iptv-org.github.io/iptv/countries/' + code + '.m3u',
    tier: 'community',
    credit: 'iptv-org community directory',
    notes: 'Javni indeks poveznica; nije neovisna potvrda dopuštenja za retransmisiju ili gledanje.'
  })),
  {
    id: 'biskyt-live',
    name: 'Legal Free IPTV — javni TV',
    country: 'GLOBAL',
    repo: 'https://github.com/biskyt/legalFreeIPTVplaylist',
    url: 'https://biskyt.github.io/legalFreeIPTVplaylist/live.m3u',
    tier: 'curated',
    credit: 'biskyt/legalFreeIPTVplaylist',
    notes: 'Popis s pravnim obrazloženjima i izvorima; uvjeti pojedinog streama i dalje vrijede.'
  },
  {
    id: 'biskyt-movies',
    name: 'Legal Free IPTV — filmovi',
    country: 'GLOBAL',
    repo: 'https://github.com/biskyt/legalFreeIPTVplaylist',
    url: 'https://biskyt.github.io/legalFreeIPTVplaylist/movies.m3u',
    tier: 'curated',
    credit: 'biskyt/legalFreeIPTVplaylist',
    notes: 'Autor navodi filmove iz javne domene ili otvorenih licenci; trajanje autorskih prava ovisi o državi.'
  },
  {
    id: 'biskyt-series',
    name: 'Legal Free IPTV — serije',
    country: 'GLOBAL',
    repo: 'https://github.com/biskyt/legalFreeIPTVplaylist',
    url: 'https://biskyt.github.io/legalFreeIPTVplaylist/series.m3u',
    tier: 'curated',
    credit: 'biskyt/legalFreeIPTVplaylist',
    notes: 'Pojedina prava mogu se razlikovati po teritoriju; korisnik treba poštovati lokalne uvjete.'
  }
] as const;

const PREMIUM_MARKER = /\b(arena\s*sport|hbo|sky\s*sport|sport\s*klub|premiere\s*sport|cinemax|netflix|disney\s*plus)\b/i;

export function sanitizePublicPlaylist(channels: Channel[], source: PublicSource): Channel[] {
  return channels
    .filter(ch => !PREMIUM_MARKER.test(ch.name + ' ' + ch.group))
    .map(ch => ({ ...ch, country: ch.country === 'OTHER' && source.country !== 'GLOBAL' ? source.country : ch.country, sourceId: source.id }));
}

export function getSelectedSources(): string[] {
  try {
    const saved: unknown = JSON.parse(localStorage.getItem('iptv-plus-public-sources') ?? '[]');
    if (!Array.isArray(saved)) return [];
    const validIds = new Set(PUBLIC_SOURCES.map(s => s.id));
    return saved.filter((id): id is string => typeof id === 'string' && validIds.has(id)).slice(0, 12);
  } catch { return []; }
}

export function saveSelectedSources(ids: string[]): void {
  try { localStorage.setItem('iptv-plus-public-sources', JSON.stringify(ids)); }
  catch { /* Private browsing or restricted WebView storage */ }
}

export async function fetchPublicPlaylist(source: PublicSource, signal?: AbortSignal): Promise<Channel[]> {
  if (!PUBLIC_SOURCES.some(known => known.id === source.id && known.url === source.url))
    throw new Error('Nepoznat ili neodobren izvor liste.');
  const remote = new URL(source.url);
  if (remote.protocol !== 'https:' || remote.username || remote.password)
    throw new Error('Liste se dohvaćaju isključivo HTTPS-om.');
  const response = await fetch(remote.toString(), { method: 'GET', cache: 'no-store', redirect: 'follow', signal });
  if (!response.ok) throw new Error('Izvor trenutno nije dostupan (' + response.status + ').');
  const maxBytes = 5_000_000;
  const declared = Number(response.headers.get('content-length') || 0);
  if (declared > maxBytes) throw new Error('Lista je veća od dopuštenih 5 MB.');
  if (!response.body) throw new Error('Izvor nije poslao sadržaj.');
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let size = 0;
  try {
    while (true) {
      const chunk = await reader.read();
      if (chunk.done) break;
      size += chunk.value.length;
      if (size > maxBytes) throw new Error('Izvor premašuje ograničenje od 5 MB.');
      chunks.push(chunk.value);
    }
  } finally { reader.releaseLock(); }
  const bytes = new Uint8Array(size);
  let cursor = 0;
  for (const chunk of chunks) { bytes.set(chunk, cursor); cursor += chunk.length; }
  const parsed = parseM3U(new TextDecoder('utf-8').decode(bytes));
  return sanitizePublicPlaylist(parsed, source);
}

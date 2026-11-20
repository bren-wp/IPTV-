/**
 * IPTV+ imports only user-supplied M3U content. Demonstration entries never include
 * playable URLs. Importing a playlist does not grant streaming/distribution rights.
 */
export type Country = 'HR' | 'SI' | 'BA' | 'RS' | 'OTHER';
export type Category = 'TV' | 'SPORT' | 'MOVIES' | 'SERIES' | 'KIDS' | 'MUSIC' | 'OTHER';
export type Channel = {
  id: string;
  name: string;
  group: string;
  country: Country;
  category: Category;
  logo?: string;
  url?: string;
  demo?: boolean;
};

export const regions: { code: Country; label: string; flag: string }[] = [
  { code: 'HR', label: 'Hrvatska', flag: '🇭🇷' },
  { code: 'SI', label: 'Slovenija', flag: '🇸🇮' },
  { code: 'BA', label: 'BiH', flag: '🇧🇦' },
  { code: 'RS', label: 'Srbija', flag: '🇷🇸' }
];

function identifyCountry(value: string): Country {
  const v = value.toLowerCase();
  if (/(^|[\s|/()\[\]-])(hr|hrvatska|croatia|croatian)(?=$|[\s|/()\[\]-])/.test(v)) return 'HR';
  if (/(^|[\s|/()\[\]-])(si|slovenija|slovenia|slovenian)(?=$|[\s|/()\[\]-])/.test(v)) return 'SI';
  if (/(^|[\s|/()\[\]-])(ba|bih|bosna|bosnia)(?=$|[\s|/()\[\]-])/.test(v)) return 'BA';
  if (/(^|[\s|/()\[\]-])(rs|srbija|serbia|serbian)(?=$|[\s|/()\[\]-])/.test(v)) return 'RS';
  return 'OTHER';
}
function identifyCategory(value: string): Category {
  const v = value.toLowerCase();
  if (/(sport|arena|nogomet|football|sports)/.test(v)) return 'SPORT';
  if (/(kids|djeca|deca|crtani|cartoon|children)/.test(v)) return 'KIDS';
  if (/(film|movie|cinema|vod)/.test(v)) return 'MOVIES';
  if (/(serij|series|show)/.test(v)) return 'SERIES';
  if (/(music|glazba|muzika)/.test(v)) return 'MUSIC';
  return 'TV';
}

export function safeMediaUrl(input: string): string | undefined {
  try {
    const url = new URL(input.trim());
    if (!['https:', 'http:'].includes(url.protocol) || !url.hostname || url.username || url.password) return undefined;
    return url.toString();
  } catch {
    return undefined;
  }
}
function attribute(meta: string, key: string): string {
  return meta.match(new RegExp('(?:^|\\s)' + key + '="([^"]*)"','i'))?.[1]?.trim() ?? '';
}
function stableId(value: string): string {
  let hash = 2166136261;
  for (let i = 0; i < value.length; i++) hash = Math.imul(hash ^ value.charCodeAt(i), 16777619);
  return 'ch-' + (hash >>> 0).toString(36);
}

export function parseM3U(input: string): Channel[] {
  if (input.length > 5_000_000) throw new Error('Lista je prevelika (najviše 5 MB).');
  const lines = input.replace(/^\uFEFF/, '').split(/\r?\n/);
  if (!lines.some(line => /^#EXTM3U\b/i.test(line.trim()))) throw new Error('Datoteka nije valjana M3U lista (#EXTM3U).');
  const result: Channel[] = [];
  const used = new Set<string>();
  let pending: { name: string; group: string; logo?: string } | undefined;
  for (const raw of lines) {
    const line = raw.trim();
    if (line.startsWith('#EXTINF:')) {
      const separator = line.indexOf(',');
      const header = separator >= 0 ? line.slice(0, separator) : line;
      const name = (separator >= 0 ? line.slice(separator + 1) : '').trim();
      pending = {
        name: (name || attribute(header, 'tvg-name') || 'Nepoznati kanal').slice(0, 120),
        group: (attribute(header, 'group-title') || 'Ostalo').slice(0, 80),
        logo: safeMediaUrl(attribute(header, 'tvg-logo'))
      };
    } else if (line && !line.startsWith('#') && pending) {
      const url = safeMediaUrl(line);
      if (url && !used.has(url) && result.length < 2000) {
        used.add(url);
        const searchable = pending.group + ' ' + pending.name;
        result.push({
          id: stableId(url), name: pending.name, group: pending.group,
          logo: pending.logo, country: identifyCountry(searchable),
          category: identifyCategory(searchable), url
        });
      }
      pending = undefined;
    }
  }
  return result;
}

const samples: Array<[string, Country, Category, string]> = [
  ['Informativni program', 'HR', 'TV', 'Vijesti'],
  ['Regionalna televizija', 'HR', 'TV', 'Regionalni'],
  ['Sportska emisija', 'HR', 'SPORT', 'Sport'],
  ['Slovenski program', 'SI', 'TV', 'Općenito'],
  ['Slovenski sport', 'SI', 'SPORT', 'Sport'],
  ['BiH program', 'BA', 'TV', 'Općenito'],
  ['BiH dokumentarni', 'BA', 'TV', 'Dokumentarni'],
  ['Srpski program', 'RS', 'TV', 'Općenito'],
  ['Filmska kategorija', 'RS', 'MOVIES', 'Filmovi'],
  ['Dječji program', 'HR', 'KIDS', 'Djeca'],
  ['Katalog serija', 'HR', 'SERIES', 'Serije'],
  ['Glazbeni program', 'SI', 'MUSIC', 'Glazba']
];
export const demoChannels: Channel[] = samples.map(([name, country, category, group], index) => ({
  id: 'demo-' + index, name, country, category, group, demo: true
}));

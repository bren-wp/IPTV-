import { describe, expect, it } from 'vitest';
import { PUBLIC_SOURCES, sanitizePublicPlaylist } from './publicSources';
import type { Channel } from './catalog';

describe('curated public playlist directory', () => {
  it('contains only HTTPS known endpoints without embedded credentials', () => {
    expect(PUBLIC_SOURCES.length).toBeGreaterThan(7);
    for (const item of PUBLIC_SOURCES) {
      const url = new URL(item.url);
      expect(url.protocol).toBe('https:');
      expect(url.username).toBe('');
      expect(url.password).toBe('');
    }
  });

  it('does not promote clearly premium streams from community directories', () => {
    const source = PUBLIC_SOURCES.find(s => s.id === 'iptvorg-hr')!;
    const items: Channel[] = [
      { id: '1', name: 'Arena Sport 1', group: 'Sport', country: 'OTHER', category: 'SPORT', url: 'https://example.org/a.m3u8' },
      { id: '2', name: 'Javni program', group: 'Općenito', country: 'OTHER', category: 'TV', url: 'https://example.org/b.m3u8' }
    ];
    const output = sanitizePublicPlaylist(items, source);
    expect(output).toHaveLength(1);
    expect(output[0].country).toBe('HR');
    expect(output[0].sourceId).toBe(source.id);
  });
});

import { describe, expect, it } from 'vitest';
import { parseM3U, safeMediaUrl } from './catalog';

describe('M3U import', () => {
  it('parses regional metadata and rejects duplicates', () => {
    const data = '#EXTM3U\n#EXTINF:-1 group-title="Hrvatska Sport",Sportski kanal\nhttps://example.org/live.m3u8\n#EXTINF:-1,Duplikat\nhttps://example.org/live.m3u8';
    const items = parseM3U(data);
    expect(items).toHaveLength(1);
    expect(items[0].country).toBe('HR');
    expect(items[0].category).toBe('SPORT');
    expect(items[0].name).toBe('Sportski kanal');
  });
  it('disallows embedded credentials and local protocols', () => {
    expect(safeMediaUrl('file:///etc/passwd')).toBeUndefined();
    expect(safeMediaUrl('http://user:secret@example.com/live')).toBeUndefined();
    expect(safeMediaUrl('javascript:alert(1)')).toBeUndefined();
  });
  it('rejects malformed playlists', () => {
    expect(() => parseM3U('hello')).toThrow('M3U');
  });
  it('never promotes unsafe stream schemes to playable channels', () => {
    expect(parseM3U('#EXTM3U\n#EXTINF:-1,Unsafe\nfile:///test')).toHaveLength(0);
  });
});

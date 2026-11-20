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

import { parseApprovedCatalog } from './catalog';
describe('approved source catalog', () => {
  it('rejects unverified or malformed bundled streams', () => {
    expect(parseApprovedCatalog({schemaVersion:1,channels:[{name:'Unverified',url:'https://example.org/live.m3u8',country:'HR',category:'TV'}]})).toEqual([]);
  });
  it('accepts only documented approved source records', () => {
    const channels = parseApprovedCatalog({schemaVersion:1,channels:[
      {name:'Approved test',url:'https://example.org/live.m3u8',country:'HR',category:'TV',rights:{status:'approved',evidenceUrl:'https://example.org/license',reviewedAt:'2026-11-21'}}
    ]});
    expect(channels).toHaveLength(1);
  });
});

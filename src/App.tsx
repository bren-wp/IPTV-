import { useEffect, useMemo, useRef, useState } from 'react';
import Hls from 'hls.js';
import {
  Baby, CalendarDays, Check, ChevronDown, ChevronRight, Clapperboard, FileUp,
  Film, Globe2, Heart, Home, Info, ListVideo, Menu, MonitorPlay,
  Play, Search, Settings2, ShieldCheck, SlidersHorizontal, Sparkles, Star,
  Tv2, Upload, X
} from 'lucide-react';
import { type Channel, type Country, demoChannels, parseM3U, regions, loadApprovedCatalog } from './catalog';

type Screen = 'home' | 'live' | 'guide' | 'movies' | 'series' | 'kids' | 'favorites' | 'search' | 'sources' | 'settings';
type MenuItem = { id: Screen; label: string; icon: typeof Home };
const navigation: MenuItem[] = [
  { id: 'home', label: 'Početna', icon: Home },
  { id: 'live', label: 'TV uživo', icon: Tv2 },
  { id: 'guide', label: 'TV vodič (EPG)', icon: CalendarDays },
  { id: 'movies', label: 'Filmovi', icon: Film },
  { id: 'series', label: 'Serije', icon: Clapperboard },
  { id: 'kids', label: 'Djeca', icon: Baby },
  { id: 'favorites', label: 'Favoriti', icon: Heart },
  { id: 'search', label: 'Pretraživanje', icon: Search },
  { id: 'sources', label: 'Izvori i liste', icon: ListVideo },
  { id: 'settings', label: 'Postavke', icon: Settings2 }
];
const views: Record<Screen, string> = {
  home: 'Dobro došli u IPTV+', live: 'TV uživo', guide: 'TV vodič (EPG)',
  movies: 'Filmovi', series: 'Serije', kids: 'Dječji sadržaj',
  favorites: 'Moji favoriti', search: 'Pretraživanje', sources: 'Izvori i liste', settings: 'Postavke'
};
const gradients = ['purple', 'blue', 'teal', 'pink', 'gold', 'indigo'];
const allCountry = 'ALL' as const;
type CountryFilter = Country | typeof allCountry;

function readFlag(key: string, initial: boolean): boolean {
  try { return localStorage.getItem(key) === null ? initial : localStorage.getItem(key) === 'true'; }
  catch { return initial; }
}
function persistFlag(key: string, value: boolean): void {
  try { localStorage.setItem(key, String(value)); } catch { /* restricted storage */ }
}
function readFavorites(): string[] {
  try {
    const value: unknown = JSON.parse(localStorage.getItem('iptv-plus-favorites') ?? '[]');
    return Array.isArray(value) ? value.filter((x): x is string => typeof x === 'string').slice(0, 10000) : [];
  } catch { return []; }
}
function ChannelTile({ channel, index, isFavorite, onOpen, onFavorite }: {
  channel: Channel; index: number; isFavorite: boolean; onOpen: (c: Channel) => void; onFavorite: (c: Channel) => void
}) {
  return (
    <article className="channel-card">
      <button className={`channel-visual tone-${gradients[index % gradients.length]}`} onClick={() => onOpen(channel)}
        aria-label={`Otvori ${channel.name}`}>
        {channel.logo ? <img alt="" loading="lazy" referrerPolicy="no-referrer" src={channel.logo} onError={event => { event.currentTarget.style.display = 'none'; }} /> : <Tv2 size={36} strokeWidth={1.6} />}
        <span className="card-play"><Play size={18} fill="currentColor" /></span>
        {channel.demo && <span className="demo-tag">PRIMJER</span>}
      </button>
      <div className="channel-info">
        <div className="channel-names"><strong title={channel.name}>{channel.name}</strong><span>{channel.group} · {channel.country}</span></div>
        <button className={`icon-btn favorite ${isFavorite ? 'selected' : ''}`} onClick={() => onFavorite(channel)}
          aria-label={isFavorite ? `Ukloni ${channel.name} iz favorita` : `Spremi ${channel.name} u favorite`}>
          <Heart size={17} fill={isFavorite ? 'currentColor' : 'none'} />
        </button>
      </div>
    </article>
  );
}
function VideoPlayer({ channel, onClose }: { channel: Channel; onClose: () => void }) {
  const video = useRef<HTMLVideoElement>(null);
  const [error, setError] = useState('');
  useEffect(() => {
    setError('');
    const node = video.current;
    if (!node || !channel.url) return;
    let hls: Hls | undefined;
    if (channel.url.toLowerCase().includes('.m3u8') && Hls.isSupported()) {
      hls = new Hls({ enableWorker: true, lowLatencyMode: true });
      hls.loadSource(channel.url);
      hls.attachMedia(node);
      hls.on(Hls.Events.ERROR, (_event, data) => { if (data.fatal) setError('Reprodukcija nije uspjela. Provjeri dostupnost izvora, CORS i podršku kodeka.'); });
    } else {
      node.src = channel.url;
    }
    const onError = () => setError('Video format nije podržan ili izvor nije dostupan.');
    node.addEventListener('error', onError);
    void node.play().catch(() => { /* autoplay may require direct user action */ });
    return () => { node.removeEventListener('error', onError); node.pause(); hls?.destroy(); node.removeAttribute('src'); node.load(); };
  }, [channel]);
  useEffect(() => {
    const handler = (event: KeyboardEvent) => { if (event.key === 'Escape') onClose(); };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [onClose]);
  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={event => { if (event.target === event.currentTarget) onClose(); }}>
      <section className="player-dialog" role="dialog" aria-modal="true" aria-label={`Reproduktor: ${channel.name}`}>
        <div className="dialog-head"><span><MonitorPlay size={20} /> <strong>{channel.name}</strong></span><button className="icon-btn" onClick={onClose} aria-label="Zatvori"><X /></button></div>
        <div className="player-stage">
          {channel.demo ? <div className="player-placeholder"><Tv2 size={48}/><h3>Prikaz dizajna — bez streama</h3><p>Dodaj vlastitu legalnu M3U listu da pokreneš stvarni sadržaj.</p></div>
            : <video ref={video} controls playsInline autoPlay className="video-element" />}
        </div>
        {error && <p className="alert" role="alert">{error}</p>}
        <div className="player-bottom"><span>IPTV+ Player · HLS / HTML5</span><span>{channel.demo ? 'Demo kanal' : 'Korisnički izvor'}</span></div>
      </section>
    </div>
  );
}

export default function App() {
  const [screen, setScreen] = useState<Screen>('home');
  const [channels, setChannels] = useState<Channel[]>(demoChannels);
  const [favorites, setFavorites] = useState<string[]>(readFavorites);
  const pro = import.meta.env.VITE_IPTV_EDITION === 'pro';
  const [reducedMotion, setReducedMotion] = useState<boolean>(() => readFlag('iptv-plus-reduced-motion', false));
  const [compact, setCompact] = useState<boolean>(() => readFlag('iptv-plus-compact', false));
  const [country, setCountry] = useState<CountryFilter>(allCountry);
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState<Channel | null>(null);
  const [playlistText, setPlaylistText] = useState('');
  const [playlistCount, setPlaylistCount] = useState(0);
  const [notice, setNotice] = useState('');
  const [importError, setImportError] = useState('');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  useEffect(() => {
    let cancelled = false;
    void loadApprovedCatalog().then(approved => {
      if (!cancelled && approved.length > 0) setChannels(approved);
    }).catch(() => { /* katalog može biti privremeno nedostupan */ });
    return () => { cancelled = true; };
  }, []);
  const realCount = channels.filter(c => !c.demo).length;
  const visibleChannels = useMemo(() => {
    let values = channels;
    if (screen === 'favorites') values = values.filter(c => favorites.includes(c.id));
    if (screen === 'movies') values = values.filter(c => c.category === 'MOVIES');
    if (screen === 'series') values = values.filter(c => c.category === 'SERIES');
    if (screen === 'kids') values = values.filter(c => c.category === 'KIDS');
    if (country !== allCountry) values = values.filter(c => c.country === country);
    if (query.trim()) {
      const needle = query.trim().toLowerCase();
      values = values.filter(c => `${c.name} ${c.group} ${c.country}`.toLowerCase().includes(needle));
    }
    return values;
  }, [channels, screen, favorites, country, query]);
  const setView = (value: Screen) => { setScreen(value); setQuery(''); setMobileMenuOpen(false); setCountry(allCountry); };
  const toggleFavorite = (channel: Channel) => {
    setFavorites(current => {
      const exists = current.includes(channel.id);
      if (!exists && !pro && current.length >= 10) { setNotice('Free način podržava do 10 favorita. Za više favorita instaliraj IPTV+ Pro.'); return current; }
      const next = exists ? current.filter(x => x !== channel.id) : [...current, channel.id];
      try { localStorage.setItem('iptv-plus-favorites', JSON.stringify(next)); } catch { /* storage blocked */ }
      return next;
    });
  };
  const ingest = (source: string) => {
    try {
      if (!pro && playlistCount >= 1) throw new Error('Free način podržava jednu listu. Koristi zasebno IPTV+ Pro izdanje za više lista.');
      const imported = parseM3U(source);
      if (imported.length === 0) throw new Error('Lista ne sadrži podržane HTTP(S) izvore.');
      setChannels(current => [...current.filter(x => x.demo), ...current.filter(x => !x.demo && !imported.some(y => y.id === x.id)), ...imported]);
      setPlaylistCount(n => n + 1);
      setPlaylistText('');
      setImportError('');
      setNotice(`Uvezeno: ${imported.length} kanala. Popis se obrađuje samo na uređaju i nije trajno pohranjen.`);
      setView('live');
    } catch (error) { setImportError(error instanceof Error ? error.message : 'Uvoz nije uspio.'); }
  };
  const onFile = async (file?: File) => {
    if (!file) return;
    if (file.size > 5_000_000) { setImportError('Datoteka je veća od 5 MB.'); return; }
    try { ingest(await file.text()); } catch { setImportError('Datoteka se ne može pročitati.'); }
  };
  const categories: { id: Screen; label: string; symbol: typeof Tv2; tone: string }[] = [
    { id: 'live', label: 'TV uživo', symbol: Tv2, tone: 'purple' },
    { id: 'guide', label: 'TV vodič', symbol: CalendarDays, tone: 'blue' },
    { id: 'movies', label: 'Filmovi', symbol: Film, tone: 'pink' },
    { id: 'series', label: 'Serije', symbol: Clapperboard, tone: 'indigo' },
    { id: 'kids', label: 'Djeca', symbol: Baby, tone: 'gold' },
    { id: 'favorites', label: 'Favoriti', symbol: Heart, tone: 'teal' }
  ];
  const showCards = ['home','live','movies','series','kids','favorites','search'].includes(screen);
  return (
    <div className={`app-shell ${compact ? 'compact' : ''} ${reducedMotion ? 'reduced-motion' : ''}`}>
      <aside className={`sidebar ${mobileMenuOpen ? 'open' : ''}`}>
        <button className="brand" onClick={() => setView('home')} aria-label="IPTV+ početna">
          <span className="brand-mark"><Tv2 size={25}/><Play size={12} fill="currentColor" className="brand-play" /></span>
          <span>IPTV<span className="brand-plus">+</span></span>
        </button>
        <div className="side-caption">OTKRIJ SADRŽAJ</div>
        <nav className="side-nav" aria-label="Glavna navigacija">
          {navigation.map(item => {
            const Icon = item.icon;
            return <button key={item.id} className={`nav-item ${screen === item.id ? 'active' : ''}`}
              onClick={() => setView(item.id)} aria-current={screen === item.id ? 'page' : undefined}>
              <Icon size={19}/><span>{item.label}</span>{screen === item.id && <span className="nav-dot"/>}
            </button>;
          })}
        </nav>
        <div className="sidebar-footer"><div className="sidebar-edition"><Sparkles size={16}/><div><b>IPTV+ {pro ? 'Pro' : 'Free'}</b><small>Bez računa i oglasa</small></div></div><div className="copyright">© 2026 IPTV+ · Brendigo</div></div>
      </aside>
      <div className="mobile-overlay" hidden={!mobileMenuOpen} onClick={() => setMobileMenuOpen(false)}/>
      <div className="main-shell">
        <header className="topbar">
          <div className="topbar-left">
            <button className="icon-btn burger" onClick={() => setMobileMenuOpen(v => !v)} aria-label="Otvori izbornik"><Menu size={24}/></button>
            <div className="location"><span className="eyebrow">IPTV+ / {pro ? 'PRO' : 'FREE'}</span><strong>{views[screen]}</strong></div>
          </div>
          <div className="topbar-actions">
            <button className="search-pill" onClick={() => setView('search')}><Search size={17}/><span>Pretraži kanale...</span><kbd>⌕</kbd></button>
            <button className="icon-btn" onClick={() => setView('sources')} title="Dodaj izvor" aria-label="Dodaj izvor"><Upload size={19}/></button>
            <button className="profile-pill" onClick={() => setView('settings')} title="Postavke">IP<span>+</span></button>
          </div>
        </header>
        <main className="content">
          {notice && <div className="notice" role="status"><Info size={17}/><span>{notice}</span><button onClick={() => setNotice('')} aria-label="Zatvori obavijest"><X size={17}/></button></div>}
          {screen === 'home' && <>
            <section className="hero">
              <div className="hero-glow"/>
              <div className="hero-copy">
                <div className="overline"><span className="live-dot"/> TELEVIZIJA PO TVOME</div>
                <h1>Svi tvoji kanali.<br/><em>Jedno mjesto.</em></h1>
                <p>Hrvatska, Slovenija, BiH i Srbija na prvome mjestu. Dodaj vlastite legalne izvore i uživaj u brzom, preglednom iskustvu bez registracije i reklama.</p>
                <div className="hero-actions"><button className="btn primary" onClick={() => setView('live')}><Play size={18} fill="currentColor"/> Istraži kanale</button><button className="btn secondary" onClick={() => setView('sources')}><FileUp size={17}/> Dodaj M3U listu</button></div>
              </div>
              <div className="hero-art" aria-hidden="true"><div className="orbit orbit-a"/><div className="orbit orbit-b"/><div className="hero-tv"><span className="hero-tv-text">IPTV<span>+</span></span><div className="hero-tv-play"><Play fill="currentColor" size={46}/></div></div></div>
              <div className="hero-index">01 / 04</div>
            </section>
            <section className="content-section"><div className="section-head"><div><span className="eyebrow">ZA SVAKOGA PONEŠTO</span><h2>Kategorije sadržaja</h2></div><button className="link-btn" onClick={() => setView('live')}>Svi kanali <ChevronRight size={16}/></button></div>
              <div className="category-grid">{categories.map(cat => { const Icon=cat.symbol; return <button key={cat.id} className={`category-tile tone-${cat.tone}`} onClick={() => setView(cat.id)}><Icon size={26}/><strong>{cat.label}</strong><ChevronRight size={17} className="category-arrow"/></button>; })}</div>
            </section>
            <section className="content-section"><div className="section-head"><div><span className="eyebrow">PRVO REGIJA</span><h2>Kanali po državama</h2></div></div>
              <div className="region-grid">{regions.map(region => <button className="region-tile" key={region.code} onClick={() => { setView('live'); setCountry(region.code); }}><span className="flag">{region.flag}</span><span><strong>{region.label}</strong><small>Istraži katalog</small></span><ChevronRight size={17}/></button>)}</div>
            </section>
          </>}
          {showCards && <section className="content-section channels-section">
            <div className="section-head"><div><span className="eyebrow">{realCount === 0 ? 'DEMONSTRACIJSKI KATALOG' : `${realCount} UVEZENIH IZVORA`}</span><h2>{screen === 'home' ? 'Pregled sučelja' : views[screen]}</h2></div>
              {screen !== 'home' && <div className="filters"><SlidersHorizontal size={16}/><select aria-label="Filtriraj po državi" value={country} onChange={e => setCountry(e.target.value as CountryFilter)}><option value="ALL">Sve države</option>{regions.map(c => <option value={c.code} key={c.code}>{c.flag} {c.label}</option>)}<option value="OTHER">Ostalo</option></select><ChevronDown size={14}/></div>}
            </div>
            {screen === 'search' && <label className="search-field"><Search size={20}/><input value={query} onChange={e => setQuery(e.target.value)} autoFocus placeholder="Pretraži naziv, skupinu ili državu..." /></label>}
            {realCount === 0 && <p className="hint"><Info size={16}/> Trenutačno vidiš demonstracijske kartice bez TV signala. Za gledanje dodaj vlastitu legalnu M3U listu.</p>}
            {visibleChannels.length ? <div className="channels-grid">{visibleChannels.slice(0, screen === 'home' ? 6 : 2000).map((channel, index) => <ChannelTile key={channel.id} channel={channel} index={index} isFavorite={favorites.includes(channel.id)} onOpen={setSelected} onFavorite={toggleFavorite}/>)}</div>
              : <div className="empty-state"><Search size={30}/><h3>Nema rezultata</h3><p>Provjeri filtre ili dodaj listu sa sadržajem ove kategorije.</p><button className="btn secondary" onClick={() => setView('sources')}>Dodaj izvor</button></div>}
          </section>}
          {screen === 'guide' && <section className="content-section"><div className="section-head"><div><span className="eyebrow">TV VODIČ</span><h2>Programski raspored</h2></div></div>
            <div className="guide-frame"><div className="guide-hours"><span>Kanal</span><span>18:00</span><span>19:00</span><span>20:00</span><span>21:00</span></div>
              {demoChannels.slice(0, 5).map((c,index)=><div key={c.id} className="guide-row"><strong>{c.name}</strong><div className={`guide-program tone-${gradients[index % gradients.length]}`}>Demonstracijski prikaz EPG-a</div><div className="guide-program muted">Poveži XMLTV</div></div>)}</div>
            <p className="hint"><Info size={16}/> Ovo je dizajnerski prikaz. Stvarni XMLTV EPG, vremenske zone i arhiva programa tek trebaju biti povezani.</p>
          </section>}
          {screen === 'sources' && <section className="content-section"><div className="section-head"><div><span className="eyebrow">UPRAVLJANJE SADRŽAJEM</span><h2>Dodaj svoju M3U listu</h2></div></div>
            <div className="sources-layout"><div className="panel"><div className="panel-icon"><Upload size={24}/></div><h3>Uvezi datoteku</h3><p>Odaberi .m3u, .m3u8 ili tekstualnu datoteku do 5 MB. Unos i analiza odvijaju se na uređaju.</p><label className="btn primary upload-label"><FileUp size={18}/> Odaberi datoteku<input type="file" accept=".m3u,.m3u8,.txt" onChange={e => { void onFile(e.target.files?.[0]); e.target.value=''; }} /></label></div>
              <div className="panel"><div className="panel-icon violet"><ListVideo size={24}/></div><h3>Zalijepi sadržaj liste</h3><p>M3U format mora početi oznakom #EXTM3U. Iz sigurnosnih razloga URL-ovi s ugrađenim korisničkim podacima nisu dopušteni.</p><textarea value={playlistText} onChange={e => setPlaylistText(e.target.value)} placeholder={'#EXTM3U\n#EXTINF:-1 group-title="Hrvatska",Moj kanal\nhttps://example.org/live.m3u8'} aria-label="Sadržaj M3U liste" rows={5}/><button className="btn secondary" onClick={() => ingest(playlistText)} disabled={!playlistText.trim()}>Uvezi sadržaj</button></div></div>
              {importError && <p className="alert" role="alert">{importError}</p>}
              <div className="source-summary"><ShieldCheck size={22}/><div><strong>Privatnost prije svega</strong><p>Nema IPTV+ računa ni prijenosa lista na naš poslužitelj. Izvori se trenutačno čuvaju samo tijekom rada aplikacije; sigurna lokalna trajna pohrana i automatska ažuriranja su planirani.</p></div></div>
          </section>}
          {screen === 'settings' && <section className="content-section"><div className="section-head"><div><span className="eyebrow">PRILAGODI ISKUSTVO</span><h2>Postavke</h2></div></div>
            <div className="settings-grid">
              <div className="panel settings-panel"><div className="settings-heading"><Sparkles/><div><h3>Izdanje aplikacije</h3><p>Ovo je zaseban Free ili Pro paket, bez registracije i oglasa.</p></div></div><div className="setting-line"><span><b>IPTV+ Pro</b><small>Više lista i neograničeni favoriti</small></span><span className="settings-value">{pro ? 'IPTV+ Pro' : 'IPTV+ Free'}</span></div><div className="setting-line"><span><b>Trenutačna verzija</b><small>Razvojni pregled v0.1.0</small></span><span className="settings-value">{pro ? 'Pro' : 'Free'}</span></div></div>
              <div className="panel settings-panel"><div className="settings-heading"><SlidersHorizontal/><div><h3>Prikaz</h3><p>Jedinstven IPTV+ izgled na svim platformama.</p></div></div><div className="setting-line"><span><b>Kompaktan prikaz</b><small>Više kartica na ekranu</small></span><button className={`toggle ${compact ? 'on' : ''}`} role="switch" aria-checked={compact} aria-label="Kompaktan prikaz" onClick={() => { setCompact(!compact); persistFlag('iptv-plus-compact', !compact); }}><span/></button></div><div className="setting-line"><span><b>Smanji animacije</b><small>Pristupačnost i slabiji uređaji</small></span><button className={`toggle ${reducedMotion ? 'on' : ''}`} role="switch" aria-checked={reducedMotion} aria-label="Smanji animacije" onClick={() => { setReducedMotion(!reducedMotion); persistFlag('iptv-plus-reduced-motion', !reducedMotion); }}><span/></button></div></div>
              <div className="panel settings-panel"><div className="settings-heading"><Globe2/><div><h3>Jezik i regija</h3><p>Regionalni kanali na prvome mjestu.</p></div></div><div className="setting-line"><span><b>Jezik sučelja</b><small>Ostali jezici dolaze u kasnijoj fazi</small></span><span className="settings-value">Hrvatski <Check size={15}/></span></div><div className="setting-line"><span><b>Preferirane regije</b><small>Hrvatska, Slovenija, BiH, Srbija</small></span><span className="settings-value">HR · SI · BA · RS</span></div></div>
              <div className="panel settings-panel"><div className="settings-heading"><ShieldCheck/><div><h3>Privatnost i sigurnost</h3><p>Bez obveznog računa, bez reklamnih SDK-ova.</p></div></div><div className="setting-line"><span><b>Trajno spremanje izvora</b><small>Planirano uz sigurno spremište</small></span><span className="settings-value">U pripremi</span></div><div className="setting-line"><span><b>EPG i automatska sinkronizacija</b><small>Planirano uz provjerene izvore</small></span><span className="settings-value">U pripremi</span></div></div>
            </div>
          </section>}
          <footer className="app-footer"><span>IPTV+ · Tvoj sadržaj, tvoj izbor.</span><span><ShieldCheck size={14}/> Samo sadržaj za koji imaš pravo pristupa · <Star size={14}/> 2026 Brendigo</span></footer>
        </main>
      </div>
      <nav className="bottom-nav" aria-label="Mobilna navigacija">
        {[navigation[0],navigation[1],navigation[2],navigation[6],navigation[9]].map(item => { const Icon=item.icon; return <button key={item.id} className={screen===item.id?'active':''} onClick={()=>setView(item.id)}><Icon size={20}/><small>{item.id==='guide'?'Vodič':item.id==='favorites'?'Favoriti':item.id==='settings'?'Postavke':item.label}</small></button>; })}
      </nav>
      {selected && <VideoPlayer channel={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}

# IPTV+ — sigurnosni model (v0.1, razvojno izdanje)

- Aplikacija ne preuzima niti uključuje kanale bez dozvole nositelja prava.
- Iz korisničkih M3U lista prihvaća samo HTTP(S) URL-ove. Odbacuju se `file:`, `javascript:`, ugrađeni URL username/password i nevaljan M3U format.
- M3U datoteka ograničena je na 5 MB, katalog na 2000 stavki po uvozu.
- Demo kanali ne sadrže reproduktivne linkove.
- Ne koristiti liste koje zaobilaze DRM, zaštitu pristupa ili teritorijalna ograničenja.
- Popis uvezenih kanala čuva se samo u memoriji trenutačne sesije. Favoriti i UI postavke spremaju se lokalno, **bez pristupnih podataka**.
- CORS, DRM i kodeci ovise o izvornom streamu i WebViewu. Nema skrivenog proksija niti pokušaja zaobilaženja ograničenja.
- Prije produkcijskog izdanja: audit ovisnosti, CSP, testovi Android WebView/Windows WebView2, provjera ispravnog rukovanja prijavom/ulogama, sigurnija trajna pohrana korisničkih izvora, pristupačnost i kompletna release-signing revizija.
- UI uvoz i lokalna obrada sami po sebi ne potvrđuju prava korisnika na gledanje ili distribuciju.
- IPTV+ ne sadrži reklamne SDK-ove i ne traži registraciju.

Prijave propusta: otvorite privatnu sigurnosnu prijavu preko GitHub Security Advisories repozitorija, ne javni issue s osjetljivim podacima.

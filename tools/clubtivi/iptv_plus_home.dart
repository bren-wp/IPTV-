// IPTV+ downstream UI by Brendigo, original design adaptation.
// Uses clubTivi as engine for M3U, Xtream, EPG and playback.
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class IptvPlusHomeScreen extends StatelessWidget {
  const IptvPlusHomeScreen({super.key});

  static const bg = Color(0xFF080D1C);
  static const surface = Color(0xFF111A2C);
  static const accent = Color(0xFF7C5CFF);
  static const aqua = Color(0xFF27D3C3);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: bg,
      body: SafeArea(
        child: LayoutBuilder(builder: (context, constraints) {
          final wide = constraints.maxWidth >= 850;
          final pad = wide ? 32.0 : 16.0;
          return CustomScrollView(
            slivers: [
              SliverPadding(
                padding: EdgeInsets.fromLTRB(pad, 20, pad, 30),
                sliver: SliverList(
                  delegate: SliverChildListDelegate([
                    Row(children: [
                      Image.asset('assets/icon/iptv-plus-icon.png',
                        width: 44, height: 44, semanticLabel: 'IPTV+ ikona'),
                      const SizedBox(width: 12),
                      const Text('IPTV+', style: TextStyle(fontSize: 28,
                        fontWeight: FontWeight.w800, color: Colors.white)),
                      const Spacer(),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 13, vertical: 8),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: accent.withValues(alpha: .6)),
                          color: accent.withValues(alpha: .14),
                        ),
                        child: const Text('Sve uključeno', style: TextStyle(
                            color: Colors.white, fontWeight: FontWeight.w700)),
                      ),
                    ]),
                    const SizedBox(height: 23),
                    Container(
                      constraints: BoxConstraints(minHeight: wide ? 265 : 240),
                      padding: EdgeInsets.all(wide ? 30 : 23),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(24),
                        gradient: const LinearGradient(
                          colors: [Color(0xFF17264B), Color(0xFF38236D),
                            Color(0xFF0A3851)]),
                        border: Border.all(color: accent.withValues(alpha: .45)),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Row(mainAxisSize: MainAxisSize.min, children: [
                            Icon(Icons.circle, size: 9, color: aqua),
                            SizedBox(width: 9),
                            Text('TELEVIZIJA PO TVOME',
                                style: TextStyle(color: aqua, letterSpacing: 1.4,
                                    fontWeight: FontWeight.w800, fontSize: 11)),
                          ]),
                          const SizedBox(height: 17),
                          Text('Svi tvoji kanali.\nJedno mjesto.',
                            style: TextStyle(color: Colors.white,
                              fontSize: wide ? 43 : 32,
                              height: 1.12, fontWeight: FontWeight.w800)),
                          const SizedBox(height: 14),
                          const Text('Hrvatska · Slovenija · BiH · Srbija',
                            style: TextStyle(color: Color(0xFFD9DBF9),
                                fontSize: 13)),
                          const SizedBox(height: 21),
                          Wrap(spacing: 12, runSpacing: 10, children: [
                            FilledButton.icon(
                              onPressed: () => context.go('/'),
                              icon: const Icon(Icons.play_arrow_rounded),
                              label: const Text('TV uživo'),
                              style: FilledButton.styleFrom(
                                backgroundColor: accent, foregroundColor: Colors.white,
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 19, vertical: 14)),
                            ),
                            OutlinedButton.icon(
                              onPressed: () => context.go('/providers'),
                              icon: const Icon(Icons.playlist_add_rounded),
                              label: const Text('Izaberi listu'),
                              style: OutlinedButton.styleFrom(
                                foregroundColor: Colors.white,
                                side: BorderSide(color: Colors.white.withValues(alpha: .45)),
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 19, vertical: 14)),
                            ),
                          ]),
                        ],
                      ),
                    ),
                    const SizedBox(height: 30),
                    const _SectionHeading(title: 'Istraži sadržaj',
                        description: 'Odaberi kategoriju koja te zanima'),
                    const SizedBox(height: 13),
                    LayoutBuilder(builder: (context, inner) {
                      final columns = inner.maxWidth >= 1050 ? 6 :
                        inner.maxWidth >= 560 ? 3 : 2;
                      final cards = <_TileData>[
                        const _TileData('TV uživo', Icons.live_tv_rounded, '/',
                            Color(0xFF6644C6)),
                        const _TileData('TV vodič', Icons.calendar_month_rounded,
                            '/guide', Color(0xFF215DAD)),
                        const _TileData('Filmovi i serije',
                            Icons.movie_creation_outlined, '/shows', Color(0xFF993C8D)),
                        const _TileData('Moji izvori', Icons.playlist_play_rounded,
                            '/providers', Color(0xFF1F7475)),
                        const _TileData('EPG postavke',
                            Icons.view_timeline_rounded, '/epg-mapping',
                            Color(0xFF6A4FA9)),
                        const _TileData('Postavke', Icons.settings_rounded,
                            '/settings', Color(0xFF8A6921)),
                      ];
                      return GridView.builder(
                        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: columns, crossAxisSpacing: 11,
                          mainAxisSpacing: 11, childAspectRatio: wide ? 1.4 : 1.65),
                        itemCount: cards.length, shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemBuilder: (context, index) => _CategoryTile(cards[index]),
                      );
                    }),
                    const SizedBox(height: 27),
                    const _SectionHeading(title: 'Regije',
                      description: 'Prioritetni kanali iz naše regije'),
                    const SizedBox(height: 14),
                    Wrap(spacing: 10, runSpacing: 11, children: [
                      for (final name in const [
                        '🇭🇷  Hrvatska', '🇸🇮  Slovenija',
                        '🇧🇦  BiH', '🇷🇸  Srbija'
                      ])
                        ActionChip(
                          avatar: const Icon(Icons.public, size: 16, color: aqua),
                          label: Text(name),
                          onPressed: () => context.go('/providers'),
                          side: BorderSide(color: accent.withValues(alpha: .35)),
                          backgroundColor: surface, labelStyle:
                            const TextStyle(color: Colors.white)),
                    ]),
                    const SizedBox(height: 24),
                    const Text(
                      'Izvori su javne zbirke ili vlastite IPTV liste. '
                      'Dostupnost streamova i dopuštenja nositelja prava '
                      'nisu zajamčeni. Bez IPTV+ registracije i reklamnih SDK-ova.',
                      style: TextStyle(color: Color(0xFF97A7C4),
                          fontSize: 12, height: 1.5)),
                  ]),
                ),
              ),
            ],
          );
        }),
      ),
    );
  }
}

class _SectionHeading extends StatelessWidget {
  final String title;
  final String description;
  const _SectionHeading({required this.title, required this.description});

  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text(title, style: const TextStyle(
        fontSize: 23, color: Colors.white, fontWeight: FontWeight.w800)),
      const SizedBox(height: 4),
      Text(description, style: const TextStyle(
        fontSize: 12, color: Color(0xFFA1B0D0))),
    ],
  );
}

class _TileData {
  final String label;
  final IconData icon;
  final String route;
  final Color color;
  const _TileData(this.label, this.icon, this.route, this.color);
}

class _CategoryTile extends StatelessWidget {
  final _TileData data;
  const _CategoryTile(this.data);

  @override
  Widget build(BuildContext context) => Material(
    color: data.color, borderRadius: BorderRadius.circular(16),
    child: InkWell(
      borderRadius: BorderRadius.circular(16),
      onTap: () => context.go(data.route),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(data.icon, size: 28, color: Colors.white),
            Text(data.label, maxLines: 2, overflow: TextOverflow.ellipsis,
                style: const TextStyle(color: Colors.white,
                  fontSize: 14, fontWeight: FontWeight.w700)),
          ],
        ),
      ),
    ),
  );
}

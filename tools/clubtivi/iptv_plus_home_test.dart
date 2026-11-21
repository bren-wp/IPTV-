// IPTV+ downstream widget test — verifies home branding and routes.
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:clubtivi/features/home/iptv_plus_home.dart';

void main() {
  testWidgets('IPTV+ home shows brand, editions and functional entry points',
      (tester) async {
    final router = GoRouter(initialLocation: '/home', routes: [
      GoRoute(path: '/home', builder: (_, _) => const IptvPlusHomeScreen()),
      for (final route in ['/','/guide','/shows','/providers','/epg-mapping','/settings'])
        GoRoute(path: route, builder: (_, _) => const Scaffold(
          body: Center(child: Text('Ruta učitana')))),
    ]);
    await tester.pumpWidget(MaterialApp.router(routerConfig: router));
    await tester.pumpAndSettle();
    expect(find.text('IPTV+'), findsOneWidget);
    expect(find.text('Svi tvoji kanali.\nJedno mjesto.'), findsOneWidget);
    expect(find.text('TV uživo'), findsWidgets);
    await tester.tap(find.widgetWithText(FilledButton, 'TV uživo'));
    await tester.pumpAndSettle();
    expect(find.text('Ruta učitana'), findsOneWidget);
    router.dispose();
  });
}

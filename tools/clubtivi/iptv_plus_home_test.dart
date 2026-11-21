// IPTV+ responsive layout and navigation widget smoke tests.
// These tests are not a substitute for real pixel-diff/device QA.
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:clubtivi/features/home/iptv_plus_home.dart';

void main() {
  for (final size in const [
    Size(360, 800),
    Size(412, 915),
    Size(1280, 800),
    Size(1920, 1080),
  ]) {
    testWidgets('IPTV+ home fits and navigates at ${size.width}x${size.height}',
        (tester) async {
      tester.view.physicalSize = size;
      tester.view.devicePixelRatio = 1;
      addTearDown(() {
        tester.view.resetPhysicalSize();
        tester.view.resetDevicePixelRatio();
      });

      final router = GoRouter(initialLocation: '/home', routes: [
        GoRoute(path: '/home', builder: (_, _) => const IptvPlusHomeScreen()),
        for (final route in [
          '/', '/guide', '/shows', '/providers', '/epg-mapping', '/settings'
        ])
          GoRoute(path: route, builder: (_, _) => const Scaffold(
              body: Center(child: Text('Ruta učitana')))),
      ]);
      await tester.pumpWidget(MaterialApp.router(routerConfig: router));
      await tester.pumpAndSettle();

      expect(find.text('IPTV+'), findsOneWidget);
      expect(find.text('Svi tvoji kanali.\nJedno mjesto.'), findsOneWidget);
      expect(find.text('TV uživo'), findsWidgets);
      expect(tester.takeException(), isNull,
          reason: 'Responsive IPTV+ homepage must not overflow');

      await tester.tap(find.widgetWithText(FilledButton, 'TV uživo'));
      await tester.pumpAndSettle();
      expect(find.text('Ruta učitana'), findsOneWidget);
      expect(tester.takeException(), isNull);
      router.dispose();
    });
  }
}

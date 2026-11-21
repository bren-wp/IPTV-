# IPTV+ — ažuriranje ovisnosti (21. 11. 2026.)

**Flutter 3.50.1**, Dart 3.14, Gradle 9.5.0, AGP 9.3.1 i Kotlin 2.4.20 primarna su stabilna osnova. ClubTivi je zaključani Apache 2.0 Git submodule.

U `tools/clubtivi/prepare.py` povećane su minimalne verzije izravnih paketa:

| Paket | Staro | Novo |
|---|---|---|
| dio | ^5.7.0 | ^5.11.1 |
| drift | ^2.22.1 | 2.22.1 (pinned for codegen compatibility) |
| drift_dev | ^2.22.1 | 2.22.1 (pinned with Freezed 2) |
| shared_preferences | ^2.5.4 | ^2.5.6 |
| media_kit | ^1.1.11 | ^1.2.6 |
| go_router | ^14.8.1 | ^18.1.4 |

Flutter CI pokreće `flutter pub upgrade`: tako se i ostale direktne/tranzitivne ovisnosti podižu na najnovije verzije **unutar dopuštenih kompatibilnih raspona**. Nakon toga obvezni su analiza i testiranje Android/Windows builda. Promjene koje lome API (npr. Riverpod 2 → 3 i pripadajući generatori) nisu automatski proglašene dovršenima; traže posebnu migraciju i regresijske testove.

Za dugoročnu reproducibilnost treba pohraniti ažurirani downstream `pubspec.lock` nakon potvrđenog CI-a. Trenutačno je rješavanje ovisnosti dinamičko u provjerama.

Verzije: https://pub.dev/packages/dio · https://pub.dev/packages/drift · https://pub.dev/packages/shared_preferences · https://pub.dev/packages/media_kit · https://pub.dev/packages/go_router .

**Kompatibilnost:** Noviji `drift_dev 2.35.3` zahtijeva `build >=3`, a `freezed 2.x` koristi `build ^2.3.1`; zbog toga su `drift` i `drift_dev` privremeno zaključani na 2.22.1 dok se ne izvrši koordinirana nadogradnja generatora. Ne prikazivati sve ovisnosti kao najnovije.

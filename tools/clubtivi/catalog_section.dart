// IPTV+ regional and genre catalog, connected to the upstream importer.
class _IptvPlusCatalogGroup extends StatelessWidget {
  final String group;
  final List<FreeTvProvider> sources;
  final Set<String> addedIds;
  const _IptvPlusCatalogGroup({
    required this.group,
    required this.sources,
    required this.addedIds,
  });

  @override
  Widget build(BuildContext context) {
    if (sources.isEmpty) return const SizedBox.shrink();
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      clipBehavior: Clip.antiAlias,
      child: ExpansionTile(
        key: PageStorageKey<String>('iptvplus-' + group),
        initiallyExpanded: group.contains('Hrvatska'),
        collapsedIconColor: const Color(0xFF27D3C3),
        iconColor: const Color(0xFF7C5CFF),
        tilePadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
        title: Text(group, maxLines: 2, overflow: TextOverflow.ellipsis,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
        subtitle: Text(sources.length.toString() + ' izvora · odaberi za pregled',
            style: const TextStyle(fontSize: 12, color: Colors.white60)),
        childrenPadding: const EdgeInsets.fromLTRB(10, 0, 10, 12),
        children: sources.map((source) => _FreeTvProviderTile(
          freeProvider: source,
          isAdded: addedIds.contains(source.id),
        )).toList(),
      ),
    );
  }
}

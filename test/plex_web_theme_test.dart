import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:plezy/theme/mono_theme.dart';
import 'package:plezy/theme/mono_tokens.dart';

void main() {
  group('LoungeMedia Windows Plex Web visual theme', () {
    setUp(() {
      debugDefaultTargetPlatformOverride = TargetPlatform.windows;
    });

    tearDown(() {
      debugDefaultTargetPlatformOverride = null;
    });

    test('dark palette uses reference charcoal and gold', () {
      expect(MonoPalette.dark.bg, const Color(0xFF1E1E1E));
      expect(MonoPalette.dark.surface, const Color(0xFF1A1A1A));
      expect(MonoPalette.dark.accent, const Color(0xFFE5A00D));
    });

    test('Windows theme uses compact square card geometry', () {
      final theme = monoThemeUncached(MonoPalette.dark);
      final design = theme.extension<MonoTokens>();

      expect(theme.colorScheme.primary, const Color(0xFFE5A00D));
      expect(theme.colorScheme.onSurface, const Color(0xFFF3F3F3));
      expect(design?.radiusSm, 4);
      expect(design?.radiusLg, 6);
    });
  });
}

import 'package:flutter/material.dart';

import 'screens/dashboard_screen.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const TradingRobotApp());
}

class TradingRobotApp extends StatelessWidget {
  const TradingRobotApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MT5 Robot',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.blue),
      routes: {
        '/': (_) => const LoginScreen(),
        '/dashboard': (_) => const DashboardScreen(),
      },
      initialRoute: '/',
    );
  }
}

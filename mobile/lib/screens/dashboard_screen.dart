import 'package:flutter/material.dart';

import '../models/dashboard_model.dart';
import '../services/api_service.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final _api = ApiService();
  DashboardModel? _dashboard;
  String _mode = 'ultra_scalping';
  bool _busy = false;
  String _lastRobotAction = 'Idle';

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final loginId = ModalRoute.of(context)!.settings.arguments as int? ?? 0;
    _load(loginId);
  }

  Future<void> _load(int loginId) async {
    if (loginId == 0) return;
    final data = await _api.dashboard(loginId);
    setState(() => _dashboard = data);
  }

  Future<void> _startRobot() async {
    setState(() => _busy = true);
    final result = await _api.startRobot(
      mode: _mode,
      lotSize: 0.2,
      maxTrades: 3,
      dailyLossLimit: 50,
      maxDrawdownPct: 10,
    );
    setState(() {
      _busy = false;
      _lastRobotAction = '${result['action']} (${result['reason']})';
    });
  }

  @override
  Widget build(BuildContext context) {
    final d = _dashboard;
    return Scaffold(
      appBar: AppBar(title: const Text('Trading Dashboard')),
      body: d == null
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Text('Balance: \$${d.balance.toStringAsFixed(2)}'),
                Text('Equity: \$${d.equity.toStringAsFixed(2)}'),
                Text('Open Trades: ${d.openTrades}'),
                Text('Daily Profit: ${d.dailyProfit >= 0 ? '+' : ''}\$${d.dailyProfit.toStringAsFixed(2)}'),
                Text('Robot Status: ${d.robotStatus}'),
                const SizedBox(height: 16),
                const Text('Markets detected:'),
                ...d.symbols.map((s) => Text('• $s')),
                const SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  initialValue: _mode,
                  decoration: const InputDecoration(labelText: 'Trading Mode'),
                  items: const [
                    DropdownMenuItem(value: 'ultra_scalping', child: Text('Ultra Scalping (M1)')),
                    DropdownMenuItem(value: 'scalping', child: Text('Scalping (M5)')),
                    DropdownMenuItem(value: 'long_trade', child: Text('Long Trade (M30-H1)')),
                  ],
                  onChanged: (value) => setState(() => _mode = value ?? _mode),
                ),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    FilledButton(
                      onPressed: _busy ? null : _startRobot,
                      child: const Text('Start Robot'),
                    ),
                    OutlinedButton(
                      onPressed: _busy
                          ? null
                          : () async {
                              await _api.pauseRobot();
                              setState(() => _lastRobotAction = 'Paused');
                            },
                      child: const Text('Pause Trading'),
                    ),
                    OutlinedButton(
                      onPressed: _busy
                          ? null
                          : () async {
                              await _api.stopRobot();
                              setState(() => _lastRobotAction = 'Stopped');
                            },
                      child: const Text('Stop Robot'),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Text('Last Robot Action: $_lastRobotAction'),
              ],
            ),
    );
  }
}

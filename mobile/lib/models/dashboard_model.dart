class DashboardModel {
  final double balance;
  final double equity;
  final int openTrades;
  final double dailyProfit;
  final String robotStatus;
  final List<String> symbols;

  DashboardModel({
    required this.balance,
    required this.equity,
    required this.openTrades,
    required this.dailyProfit,
    required this.robotStatus,
    required this.symbols,
  });

  factory DashboardModel.fromJson(Map<String, dynamic> json) {
    return DashboardModel(
      balance: (json['balance'] as num).toDouble(),
      equity: (json['equity'] as num).toDouble(),
      openTrades: json['open_trades'] as int,
      dailyProfit: (json['daily_profit'] as num).toDouble(),
      robotStatus: json['robot_status'] as String,
      symbols: (json['symbols'] as List<dynamic>).cast<String>(),
    );
  }
}

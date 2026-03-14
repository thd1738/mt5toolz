import 'package:dio/dio.dart';

import '../models/dashboard_model.dart';

class ApiService {
  ApiService({String baseUrl = 'http://localhost:8000'})
      : _dio = Dio(BaseOptions(baseUrl: baseUrl));

  final Dio _dio;

  Future<void> connect({
    required int loginId,
    required String password,
    required String brokerServer,
  }) async {
    await _dio.post('/api/v1/connect', data: {
      'login_id': loginId,
      'password': password,
      'broker_server': brokerServer,
    });
  }

  Future<DashboardModel> dashboard(int loginId) async {
    final response = await _dio.get('/api/v1/dashboard/$loginId');
    return DashboardModel.fromJson(response.data as Map<String, dynamic>);
  }

  Future<Map<String, dynamic>> startRobot({
    required String mode,
    required double lotSize,
    required int maxTrades,
    required double dailyLossLimit,
    required double maxDrawdownPct,
  }) async {
    final response = await _dio.post('/api/v1/robot/start', data: {
      'mode': mode,
      'risk': {
        'lot_size': lotSize,
        'max_trades': maxTrades,
        'daily_loss_limit': dailyLossLimit,
        'max_drawdown_pct': maxDrawdownPct,
      }
    });
    return response.data as Map<String, dynamic>;
  }

  Future<void> stopRobot() async {
    await _dio.post('/api/v1/robot/stop');
  }

  Future<void> pauseRobot() async {
    await _dio.post('/api/v1/robot/pause');
  }
}

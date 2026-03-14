import 'package:flutter/material.dart';

import '../services/api_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _loginController = TextEditingController();
  final _passwordController = TextEditingController();
  final _serverController = TextEditingController(text: 'Deriv-Server');
  final _api = ApiService();
  bool _loading = false;

  Future<void> _connect() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      await _api.connect(
        loginId: int.parse(_loginController.text),
        password: _passwordController.text,
        brokerServer: _serverController.text,
      );
      if (!mounted) return;
      Navigator.pushNamed(context, '/dashboard', arguments: int.parse(_loginController.text));
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Connection failed. Check MT5 credentials.')),
      );
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Connect MT5 Account')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _loginController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(labelText: 'MT5 Login ID'),
                validator: (value) => (value == null || value.isEmpty) ? 'Required' : null,
              ),
              TextFormField(
                controller: _passwordController,
                obscureText: true,
                decoration: const InputDecoration(labelText: 'Password'),
                validator: (value) => (value == null || value.isEmpty) ? 'Required' : null,
              ),
              TextFormField(
                controller: _serverController,
                decoration: const InputDecoration(labelText: 'Broker Server'),
                validator: (value) => (value == null || value.isEmpty) ? 'Required' : null,
              ),
              const SizedBox(height: 24),
              Row(
                children: [
                  Expanded(
                    child: FilledButton(
                      onPressed: _loading ? null : _connect,
                      child: _loading
                          ? const SizedBox(height: 18, width: 18, child: CircularProgressIndicator())
                          : const Text('Connect Account'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () {
                        _loginController.clear();
                        _passwordController.clear();
                      },
                      child: const Text('Disconnect'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

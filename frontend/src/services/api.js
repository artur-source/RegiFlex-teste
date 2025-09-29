const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Erro na requisição');
      }

      return data;
    } catch (error) {
      console.error('Erro na API:', error);
      throw error;
    }
  }

  // Autenticação
  async login(username, password) {
    return this.request('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
  }

  async logout() {
    return this.request('/logout', { method: 'POST' });
  }

  async getCurrentUser() {
    return this.request('/me');
  }

  // Pacientes
  async getPacientes(page = 1, perPage = 10) {
    return this.request(`/pacientes?page=${page}&per_page=${perPage}`);
  }

  async getPaciente(id) {
    return this.request(`/pacientes/${id}`);
  }

  async createPaciente(pacienteData) {
    return this.request('/pacientes', {
      method: 'POST',
      body: JSON.stringify(pacienteData)
    });
  }

  async updatePaciente(id, pacienteData) {
    return this.request(`/pacientes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(pacienteData)
    });
  }

  async deletePaciente(id) {
    return this.request(`/pacientes/${id}`, { method: 'DELETE' });
  }

  async searchPacientes(query) {
    return this.request(`/pacientes/search?q=${encodeURIComponent(query)}`);
  }

  // Sessões
  async getSessoes(filters = {}) {
    const params = new URLSearchParams(filters).toString();
    return this.request(`/sessoes?${params}`);
  }

  async getSessao(id) {
    return this.request(`/sessoes/${id}`);
  }

  async createSessao(sessaoData) {
    return this.request('/sessoes', {
      method: 'POST',
      body: JSON.stringify(sessaoData)
    });
  }

  async updateSessao(id, sessaoData) {
    return this.request(`/sessoes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(sessaoData)
    });
  }

  async createEvolucao(sessaoId, conteudo) {
    return this.request(`/sessoes/${sessaoId}/evolucao`, {
      method: 'POST',
      body: JSON.stringify({ conteudo })
    });
  }

  async updateEvolucao(sessaoId, conteudo) {
    return this.request(`/sessoes/${sessaoId}/evolucao`, {
      method: 'PUT',
      body: JSON.stringify({ conteudo })
    });
  }

  // QR Code
  async generateQRCode(pacienteId) {
    return this.request(`/qr/generate/${pacienteId}`);
  }

  async readQRCode(qrData) {
    return this.request('/qr/read', {
      method: 'POST',
      body: JSON.stringify({ qr_data: qrData })
    });
  }

  async validateQRCode(qrData) {
    return this.request(`/qr/validate/${encodeURIComponent(qrData)}`);
  }

  // Relatórios
  async getDashboardData() {
    return this.request('/relatorios/dashboard');
  }

  async getRelatorioSessoes(filters = {}) {
    const params = new URLSearchParams(filters).toString();
    return this.request(`/relatorios/sessoes?${params}`);
  }

  async getRelatorioPacientes(filters = {}) {
    const params = new URLSearchParams(filters).toString();
    return this.request(`/relatorios/pacientes?${params}`);
  }

  // IA
  async getAlertasIA() {
    return this.request('/ia/alertas');
  }

  async getAnalisePaciente(pacienteId, dias = 30) {
    return this.request(`/ia/analise-paciente/${pacienteId}?dias=${dias}`);
  }

  async getPadroesCancelamento(dias = 60) {
    return this.request(`/ia/padroes-cancelamento?dias=${dias}`);
  }

  // Usuários (apenas admin)
  async getUsuarios() {
    return this.request('/usuarios');
  }

  async createUsuario(usuarioData) {
    return this.request('/usuarios', {
      method: 'POST',
      body: JSON.stringify(usuarioData)
    });
  }

  async updateUsuario(id, usuarioData) {
    return this.request(`/usuarios/${id}`, {
      method: 'PUT',
      body: JSON.stringify(usuarioData)
    });
  }

  async deleteUsuario(id) {
    return this.request(`/usuarios/${id}`, { method: 'DELETE' });
  }
}

export default new ApiService();

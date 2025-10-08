import { supabase } from '../lib/supabaseClient';

class SupabaseApiService {
  // Autenticação
  async login(username, password) {
    try {
      // Primeiro, buscar o usuário pelo username
      const { data: usuarios, error: searchError } = await supabase
        .from('usuarios')
        .select('*')
        .eq('username', username)
        .single();

      if (searchError || !usuarios) {
        throw new Error('Usuário não encontrado');
      }

      // Por enquanto, vamos usar o Supabase Auth com email
      // Nota: Isso requer configuração adicional no Supabase
      const { data, error } = await supabase.auth.signInWithPassword({
        email: usuarios.email,
        password: password
      });

      if (error) throw error;

      return {
        token: data.session.access_token,
        user: {
          id: usuarios.id,
          username: usuarios.username,
          email: usuarios.email,
          role: usuarios.role
        }
      };
    } catch (error) {
      console.error('Erro no login:', error);
      throw error;
    }
  }

  async logout() {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    return { message: 'Logout realizado com sucesso' };
  }

  async getCurrentUser() {
    try {
      const { data: { user }, error } = await supabase.auth.getUser();
      if (error) throw error;

      // Buscar dados adicionais do usuário na tabela usuarios
      const { data: userData, error: userError } = await supabase
        .from('usuarios')
        .select('*')
        .eq('email', user.email)
        .single();

      if (userError) throw userError;

      return {
        user: {
          id: userData.id,
          username: userData.username,
          email: userData.email,
          role: userData.role
        }
      };
    } catch (error) {
      console.error('Erro ao buscar usuário atual:', error);
      throw error;
    }
  }

  // Pacientes
  async getPacientes(page = 1, perPage = 10) {
    try {
      const from = (page - 1) * perPage;
      const to = from + perPage - 1;

      const { data, error, count } = await supabase
        .from('pacientes')
        .select('*', { count: 'exact' })
        .order('created_at', { ascending: false })
        .range(from, to);

      if (error) throw error;

      return {
        pacientes: data,
        total: count,
        page: page,
        per_page: perPage,
        total_pages: Math.ceil(count / perPage)
      };
    } catch (error) {
      console.error('Erro ao buscar pacientes:', error);
      throw error;
    }
  }

  async getPaciente(id) {
    try {
      const { data, error } = await supabase
        .from('pacientes')
        .select('*')
        .eq('id', id)
        .single();

      if (error) throw error;
      return { paciente: data };
    } catch (error) {
      console.error('Erro ao buscar paciente:', error);
      throw error;
    }
  }

  async createPaciente(pacienteData) {
    try {
      // Gerar QR code data único
      const qrCodeData = `PAC-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      
      const { data, error } = await supabase
        .from('pacientes')
        .insert([{ ...pacienteData, qr_code_data: qrCodeData }])
        .select()
        .single();

      if (error) throw error;
      return { paciente: data, message: 'Paciente criado com sucesso' };
    } catch (error) {
      console.error('Erro ao criar paciente:', error);
      throw error;
    }
  }

  async updatePaciente(id, pacienteData) {
    try {
      const { data, error } = await supabase
        .from('pacientes')
        .update({ ...pacienteData, updated_at: new Date().toISOString() })
        .eq('id', id)
        .select()
        .single();

      if (error) throw error;
      return { paciente: data, message: 'Paciente atualizado com sucesso' };
    } catch (error) {
      console.error('Erro ao atualizar paciente:', error);
      throw error;
    }
  }

  async deletePaciente(id) {
    try {
      const { error } = await supabase
        .from('pacientes')
        .delete()
        .eq('id', id);

      if (error) throw error;
      return { message: 'Paciente excluído com sucesso' };
    } catch (error) {
      console.error('Erro ao excluir paciente:', error);
      throw error;
    }
  }

  async searchPacientes(query) {
    try {
      const { data, error } = await supabase
        .from('pacientes')
        .select('*')
        .or(`nome_completo.ilike.%${query}%,cpf.ilike.%${query}%,telefone.ilike.%${query}%`)
        .order('nome_completo');

      if (error) throw error;
      return { pacientes: data };
    } catch (error) {
      console.error('Erro ao buscar pacientes:', error);
      throw error;
    }
  }

  // Sessões
  async getSessoes(filters = {}) {
    try {
      let query = supabase
        .from('sessoes')
        .select(`
          *,
          paciente:pacientes(*),
          psicologo:usuarios(*)
        `)
        .order('data_hora', { ascending: false });

      // Aplicar filtros
      if (filters.paciente_id) {
        query = query.eq('paciente_id', filters.paciente_id);
      }
      if (filters.psicologo_id) {
        query = query.eq('psicologo_id', filters.psicologo_id);
      }
      if (filters.status) {
        query = query.eq('status', filters.status);
      }
      if (filters.data_inicio) {
        query = query.gte('data_hora', filters.data_inicio);
      }
      if (filters.data_fim) {
        query = query.lte('data_hora', filters.data_fim);
      }

      const { data, error } = await query;

      if (error) throw error;
      return { sessoes: data };
    } catch (error) {
      console.error('Erro ao buscar sessões:', error);
      throw error;
    }
  }

  async getSessao(id) {
    try {
      const { data, error } = await supabase
        .from('sessoes')
        .select(`
          *,
          paciente:pacientes(*),
          psicologo:usuarios(*),
          evolucao(*)
        `)
        .eq('id', id)
        .single();

      if (error) throw error;
      return { sessao: data };
    } catch (error) {
      console.error('Erro ao buscar sessão:', error);
      throw error;
    }
  }

  async createSessao(sessaoData) {
    try {
      const { data, error } = await supabase
        .from('sessoes')
        .insert([sessaoData])
        .select()
        .single();

      if (error) throw error;
      return { sessao: data, message: 'Sessão criada com sucesso' };
    } catch (error) {
      console.error('Erro ao criar sessão:', error);
      throw error;
    }
  }

  async updateSessao(id, sessaoData) {
    try {
      const { data, error } = await supabase
        .from('sessoes')
        .update({ ...sessaoData, updated_at: new Date().toISOString() })
        .eq('id', id)
        .select()
        .single();

      if (error) throw error;
      return { sessao: data, message: 'Sessão atualizada com sucesso' };
    } catch (error) {
      console.error('Erro ao atualizar sessão:', error);
      throw error;
    }
  }

  async createEvolucao(sessaoId, conteudo) {
    try {
      const { data, error } = await supabase
        .from('evolucao')
        .insert([{ sessao_id: sessaoId, conteudo }])
        .select()
        .single();

      if (error) throw error;
      return { evolucao: data, message: 'Evolução criada com sucesso' };
    } catch (error) {
      console.error('Erro ao criar evolução:', error);
      throw error;
    }
  }

  async updateEvolucao(sessaoId, conteudo) {
    try {
      const { data, error } = await supabase
        .from('evolucao')
        .update({ conteudo, updated_at: new Date().toISOString() })
        .eq('sessao_id', sessaoId)
        .select()
        .single();

      if (error) throw error;
      return { evolucao: data, message: 'Evolução atualizada com sucesso' };
    } catch (error) {
      console.error('Erro ao atualizar evolução:', error);
      throw error;
    }
  }

  // QR Code
  async generateQRCode(pacienteId) {
    try {
      const { data, error } = await supabase
        .from('pacientes')
        .select('qr_code_data')
        .eq('id', pacienteId)
        .single();

      if (error) throw error;
      return { qr_code: data.qr_code_data };
    } catch (error) {
      console.error('Erro ao gerar QR code:', error);
      throw error;
    }
  }

  async readQRCode(qrData) {
    try {
      const { data, error } = await supabase
        .from('pacientes')
        .select('*')
        .eq('qr_code_data', qrData)
        .single();

      if (error) throw error;
      return { paciente: data };
    } catch (error) {
      console.error('Erro ao ler QR code:', error);
      throw error;
    }
  }

  async validateQRCode(qrData) {
    try {
      const { data, error } = await supabase
        .from('pacientes')
        .select('id, nome_completo')
        .eq('qr_code_data', qrData)
        .single();

      if (error) throw error;
      return { valid: true, paciente: data };
    } catch (error) {
      return { valid: false };
    }
  }

  // Relatórios
  async getDashboardData() {
    try {
      // Total de pacientes
      const { count: totalPacientes } = await supabase
        .from('pacientes')
        .select('*', { count: 'exact', head: true });

      // Total de sessões
      const { count: totalSessoes } = await supabase
        .from('sessoes')
        .select('*', { count: 'exact', head: true });

      // Sessões por status
      const { data: sessoesPorStatus } = await supabase
        .from('sessoes')
        .select('status');

      const statusCount = sessoesPorStatus.reduce((acc, sessao) => {
        acc[sessao.status] = (acc[sessao.status] || 0) + 1;
        return acc;
      }, {});

      return {
        total_pacientes: totalPacientes,
        total_sessoes: totalSessoes,
        sessoes_agendadas: statusCount.agendada || 0,
        sessoes_realizadas: statusCount.realizada || 0,
        sessoes_canceladas: statusCount.cancelada || 0
      };
    } catch (error) {
      console.error('Erro ao buscar dados do dashboard:', error);
      throw error;
    }
  }

  async getRelatorioSessoes(filters = {}) {
    return this.getSessoes(filters);
  }

  async getRelatorioPacientes(filters = {}) {
    try {
      let query = supabase
        .from('pacientes')
        .select(`
          *,
          sessoes(count)
        `)
        .order('created_at', { ascending: false });

      const { data, error } = await query;

      if (error) throw error;
      return { pacientes: data };
    } catch (error) {
      console.error('Erro ao buscar relatório de pacientes:', error);
      throw error;
    }
  }

  // IA - Placeholder (implementação futura)
  async getAlertasIA() {
    return { alertas: [] };
  }

  async getAnalisePaciente(pacienteId, dias = 30) {
    return { analise: null };
  }

  async getPadroesCancelamento(dias = 60) {
    return { padroes: [] };
  }

  // Usuários (apenas admin)
  async getUsuarios() {
    try {
      const { data, error } = await supabase
        .from('usuarios')
        .select('id, username, email, role, created_at')
        .order('created_at', { ascending: false });

      if (error) throw error;
      return { usuarios: data };
    } catch (error) {
      console.error('Erro ao buscar usuários:', error);
      throw error;
    }
  }

  async createUsuario(usuarioData) {
    try {
      // Criar usuário no Supabase Auth
      const { data: authData, error: authError } = await supabase.auth.signUp({
        email: usuarioData.email,
        password: usuarioData.password
      });

      if (authError) throw authError;

      // Criar registro na tabela usuarios
      const { data, error } = await supabase
        .from('usuarios')
        .insert([{
          username: usuarioData.username,
          email: usuarioData.email,
          password_hash: 'managed_by_supabase_auth',
          role: usuarioData.role || 'psicologo'
        }])
        .select()
        .single();

      if (error) throw error;
      return { usuario: data, message: 'Usuário criado com sucesso' };
    } catch (error) {
      console.error('Erro ao criar usuário:', error);
      throw error;
    }
  }

  async updateUsuario(id, usuarioData) {
    try {
      const { data, error } = await supabase
        .from('usuarios')
        .update(usuarioData)
        .eq('id', id)
        .select()
        .single();

      if (error) throw error;
      return { usuario: data, message: 'Usuário atualizado com sucesso' };
    } catch (error) {
      console.error('Erro ao atualizar usuário:', error);
      throw error;
    }
  }

  async deleteUsuario(id) {
    try {
      const { error } = await supabase
        .from('usuarios')
        .delete()
        .eq('id', id);

      if (error) throw error;
      return { message: 'Usuário excluído com sucesso' };
    } catch (error) {
      console.error('Erro ao excluir usuário:', error);
      throw error;
    }
  }
}

export default new SupabaseApiService();

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Users, 
  Calendar, 
  CalendarCheck, 
  TrendingUp,
  AlertTriangle,
  Clock,
  CheckCircle,
  XCircle
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import apiService from '../services/api';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [alertas, setAlertas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
    fetchAlertas();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const data = await apiService.getDashboardData();
      setDashboardData(data);
    } catch (error) {
      setError('Erro ao carregar dados do dashboard');
      console.error('Erro:', error);
    }
  };

  const fetchAlertas = async () => {
    try {
      const data = await apiService.getAlertasIA();
      setAlertas(data.alertas || []);
    } catch (error) {
      console.error('Erro ao carregar alertas:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severidade) => {
    const colors = {
      baixa: 'bg-blue-100 text-blue-800',
      media: 'bg-yellow-100 text-yellow-800',
      alta: 'bg-red-100 text-red-800'
    };
    return colors[severidade] || colors.baixa;
  };

  const getStatusIcon = (status) => {
    const icons = {
      agendada: <Clock className="h-4 w-4 text-blue-600" />,
      realizada: <CheckCircle className="h-4 w-4 text-green-600" />,
      cancelada: <XCircle className="h-4 w-4 text-red-600" />
    };
    return icons[status] || icons.agendada;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total de Pacientes</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dashboardData?.estatisticas?.total_pacientes || 0}
                </p>
              </div>
              <Users className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Sessões Hoje</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dashboardData?.estatisticas?.sessoes_hoje || 0}
                </p>
              </div>
              <Calendar className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Sessões esta Semana</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dashboardData?.estatisticas?.sessoes_semana || 0}
                </p>
              </div>
              <CalendarCheck className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Sessões este Mês</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dashboardData?.estatisticas?.sessoes_mes || 0}
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Alertas de IA */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertTriangle className="mr-2 h-5 w-5" />
              Alertas Inteligentes
            </CardTitle>
            <CardDescription>
              Insights gerados pela análise de dados
            </CardDescription>
          </CardHeader>
          <CardContent>
            {alertas.length > 0 ? (
              <div className="space-y-3">
                {alertas.map((alerta, index) => (
                  <div key={index} className="p-3 border rounded-lg">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <h4 className="font-medium text-sm">{alerta.titulo}</h4>
                          <Badge className={getSeverityColor(alerta.severidade)}>
                            {alerta.severidade}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{alerta.mensagem}</p>
                        {alerta.acao && (
                          <p className="text-xs text-blue-600 font-medium">
                            💡 {alerta.acao}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-500 text-center py-4">
                Nenhum alerta no momento
              </p>
            )}
          </CardContent>
        </Card>

        {/* Próximas Sessões */}
        <Card>
          <CardHeader>
            <CardTitle>Próximas Sessões</CardTitle>
            <CardDescription>
              Sessões agendadas para os próximos 7 dias
            </CardDescription>
          </CardHeader>
          <CardContent>
            {dashboardData?.proximas_sessoes?.length > 0 ? (
              <div className="space-y-3">
                {dashboardData.proximas_sessoes.map((sessao) => (
                  <div key={sessao.id} className="flex items-center space-x-3 p-3 border rounded-lg">
                    {getStatusIcon(sessao.status)}
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-sm truncate">
                        {sessao.paciente?.nome_completo}
                      </p>
                      <p className="text-xs text-gray-500">
                        {formatDate(sessao.data_hora)} • {sessao.duracao_minutos}min
                      </p>
                    </div>
                    <Badge variant="outline">
                      {sessao.status}
                    </Badge>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-500 text-center py-4">
                Nenhuma sessão agendada
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sessões por Status */}
        <Card>
          <CardHeader>
            <CardTitle>Sessões por Status (Este Mês)</CardTitle>
          </CardHeader>
          <CardContent>
            {dashboardData?.sessoes_por_status?.length > 0 ? (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={dashboardData.sessoes_por_status}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="status" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3B82F6" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-sm text-gray-500 text-center py-8">
                Dados insuficientes para o gráfico
              </p>
            )}
          </CardContent>
        </Card>

        {/* Sessões por Dia da Semana */}
        <Card>
          <CardHeader>
            <CardTitle>Sessões por Dia da Semana</CardTitle>
          </CardHeader>
          <CardContent>
            {dashboardData?.sessoes_por_dia?.length > 0 ? (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={dashboardData.sessoes_por_dia}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="dia" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#10B981" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-sm text-gray-500 text-center py-8">
                Dados insuficientes para o gráfico
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;

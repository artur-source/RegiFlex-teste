import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  Plus, 
  Calendar, 
  Clock,
  User,
  Edit,
  Trash2,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Loader2,
  FileText
} from 'lucide-react';
import apiService from '../services/api';

const Sessoes = () => {
  const [sessoes, setSessoes] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [selectedSessao, setSelectedSessao] = useState(null);
  const [formData, setFormData] = useState({
    paciente_id: '',
    data_hora: '',
    duracao_minutos: 50,
    tipo_sessao: '',
    observacoes: ''
  });
  const [formLoading, setFormLoading] = useState(false);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    status: '',
    paciente_id: ''
  });

  useEffect(() => {
    fetchSessoes();
    fetchPacientes();
  }, [filters]);

  const fetchSessoes = async () => {
    try {
      setLoading(true);
      const data = await apiService.getSessoes(filters);
      setSessoes(data.sessoes || []);
    } catch (error) {
      setError('Erro ao carregar sessões');
      console.error('Erro:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPacientes = async () => {
    try {
      const data = await apiService.getPacientes(1, 100);
      setPacientes(data.pacientes || []);
    } catch (error) {
      console.error('Erro ao carregar pacientes:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormLoading(true);

    try {
      if (selectedSessao) {
        await apiService.updateSessao(selectedSessao.id, formData);
      } else {
        await apiService.createSessao(formData);
      }
      
      setShowForm(false);
      setSelectedSessao(null);
      resetForm();
      fetchSessoes();
    } catch (error) {
      setError(error.message || 'Erro ao salvar sessão');
    } finally {
      setFormLoading(false);
    }
  };

  const handleEdit = (sessao) => {
    setSelectedSessao(sessao);
    setFormData({
      paciente_id: sessao.paciente_id.toString(),
      data_hora: new Date(sessao.data_hora).toISOString().slice(0, 16),
      duracao_minutos: sessao.duracao_minutos || 50,
      tipo_sessao: sessao.tipo_sessao || '',
      observacoes: sessao.observacoes || ''
    });
    setShowForm(true);
  };

  const handleStatusChange = async (sessao, novoStatus) => {
    try {
      await apiService.updateSessao(sessao.id, { status: novoStatus });
      fetchSessoes();
    } catch (error) {
      setError(error.message || 'Erro ao atualizar status');
    }
  };

  const resetForm = () => {
    setFormData({
      paciente_id: '',
      data_hora: '',
      duracao_minutos: 50,
      tipo_sessao: '',
      observacoes: ''
    });
  };

  const formatDateTime = (dateString) => {
    return new Date(dateString).toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status) => {
    const colors = {
      agendada: 'bg-blue-100 text-blue-800',
      realizada: 'bg-green-100 text-green-800',
      cancelada: 'bg-red-100 text-red-800'
    };
    return colors[status] || colors.agendada;
  };

  const getStatusIcon = (status) => {
    const icons = {
      agendada: <Clock className="h-4 w-4" />,
      realizada: <CheckCircle className="h-4 w-4" />,
      cancelada: <XCircle className="h-4 w-4" />
    };
    return icons[status] || icons.agendada;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Sessões</h2>
          <p className="text-gray-600">Gerencie agendamentos e sessões</p>
        </div>
        
        <Dialog open={showForm} onOpenChange={setShowForm}>
          <DialogTrigger asChild>
            <Button 
              className="bg-blue-600 hover:bg-blue-700"
              onClick={() => {
                setSelectedSessao(null);
                resetForm();
              }}
            >
              <Plus className="mr-2 h-4 w-4" />
              Nova Sessão
            </Button>
          </DialogTrigger>
          
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>
                {selectedSessao ? 'Editar Sessão' : 'Nova Sessão'}
              </DialogTitle>
              <DialogDescription>
                {selectedSessao 
                  ? 'Atualize as informações da sessão'
                  : 'Agende uma nova sessão'
                }
              </DialogDescription>
            </DialogHeader>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="paciente_id">Paciente *</Label>
                <Select 
                  value={formData.paciente_id} 
                  onValueChange={(value) => setFormData({...formData, paciente_id: value})}
                  required
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione um paciente" />
                  </SelectTrigger>
                  <SelectContent>
                    {pacientes.map((paciente) => (
                      <SelectItem key={paciente.id} value={paciente.id.toString()}>
                        {paciente.nome_completo}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="data_hora">Data e Hora *</Label>
                <Input
                  id="data_hora"
                  type="datetime-local"
                  value={formData.data_hora}
                  onChange={(e) => setFormData({...formData, data_hora: e.target.value})}
                  required
                  disabled={formLoading}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="duracao_minutos">Duração (minutos)</Label>
                <Input
                  id="duracao_minutos"
                  type="number"
                  min="15"
                  max="180"
                  value={formData.duracao_minutos}
                  onChange={(e) => setFormData({...formData, duracao_minutos: parseInt(e.target.value)})}
                  disabled={formLoading}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="tipo_sessao">Tipo de Sessão</Label>
                <Select 
                  value={formData.tipo_sessao} 
                  onValueChange={(value) => setFormData({...formData, tipo_sessao: value})}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="individual">Terapia Individual</SelectItem>
                    <SelectItem value="casal">Terapia de Casal</SelectItem>
                    <SelectItem value="familia">Terapia Familiar</SelectItem>
                    <SelectItem value="grupo">Terapia em Grupo</SelectItem>
                    <SelectItem value="avaliacao">Avaliação</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="observacoes">Observações</Label>
                <Textarea
                  id="observacoes"
                  value={formData.observacoes}
                  onChange={(e) => setFormData({...formData, observacoes: e.target.value})}
                  placeholder="Observações sobre a sessão..."
                  disabled={formLoading}
                />
              </div>

              <div className="flex justify-end space-x-2 pt-4">
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={() => setShowForm(false)}
                  disabled={formLoading}
                >
                  Cancelar
                </Button>
                <Button type="submit" disabled={formLoading}>
                  {formLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Salvando...
                    </>
                  ) : (
                    selectedSessao ? 'Atualizar' : 'Agendar'
                  )}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <Select 
                value={filters.status} 
                onValueChange={(value) => setFilters({...filters, status: value})}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Filtrar por status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todos os status</SelectItem>
                  <SelectItem value="agendada">Agendada</SelectItem>
                  <SelectItem value="realizada">Realizada</SelectItem>
                  <SelectItem value="cancelada">Cancelada</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="flex-1">
              <Select 
                value={filters.paciente_id} 
                onValueChange={(value) => setFilters({...filters, paciente_id: value})}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Filtrar por paciente" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todos os pacientes</SelectItem>
                  {pacientes.map((paciente) => (
                    <SelectItem key={paciente.id} value={paciente.id.toString()}>
                      {paciente.nome_completo}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Sessões List */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-4">
                <div className="space-y-3">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                  <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : sessoes.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sessoes.map((sessao) => (
            <Card key={sessao.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg flex items-center">
                      <User className="h-4 w-4 mr-2" />
                      {sessao.paciente?.nome_completo}
                    </CardTitle>
                    <CardDescription className="flex items-center mt-1">
                      <Calendar className="h-3 w-3 mr-1" />
                      {formatDateTime(sessao.data_hora)}
                    </CardDescription>
                  </div>
                  <Badge className={getStatusColor(sessao.status)}>
                    {getStatusIcon(sessao.status)}
                    <span className="ml-1">{sessao.status}</span>
                  </Badge>
                </div>
              </CardHeader>
              
              <CardContent className="pt-0">
                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center">
                    <Clock className="h-3 w-3 mr-2" />
                    <span>{sessao.duracao_minutos} minutos</span>
                  </div>
                  
                  {sessao.tipo_sessao && (
                    <div className="flex items-center">
                      <FileText className="h-3 w-3 mr-2" />
                      <span>{sessao.tipo_sessao}</span>
                    </div>
                  )}
                  
                  {sessao.observacoes && (
                    <div className="text-xs bg-gray-50 p-2 rounded mt-2">
                      {sessao.observacoes}
                    </div>
                  )}
                </div>
                
                <div className="flex justify-between items-center mt-4 pt-3 border-t">
                  <div className="flex space-x-1">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleEdit(sessao)}
                    >
                      <Edit className="h-3 w-3" />
                    </Button>
                  </div>
                  
                  <div className="flex space-x-1">
                    {sessao.status === 'agendada' && (
                      <>
                        <Button 
                          size="sm" 
                          variant="outline"
                          className="text-green-600 hover:text-green-700"
                          onClick={() => handleStatusChange(sessao, 'realizada')}
                        >
                          <CheckCircle className="h-3 w-3" />
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline"
                          className="text-red-600 hover:text-red-700"
                          onClick={() => handleStatusChange(sessao, 'cancelada')}
                        >
                          <XCircle className="h-3 w-3" />
                        </Button>
                      </>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-8 text-center">
            <p className="text-gray-500">Nenhuma sessão encontrada</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Sessoes;

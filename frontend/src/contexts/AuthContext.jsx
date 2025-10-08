import React, { createContext, useContext, useState, useEffect } from 'react';
import { supabase } from '../lib/supabaseClient';

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar se há usuário no localStorage
    const savedUser = localStorage.getItem('regiflex_user');
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (error) {
        console.error('Erro ao carregar usuário:', error);
        localStorage.removeItem('regiflex_user');
      }
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      // Buscar usuário pelo username
      const { data: usuarios, error: searchError } = await supabase
        .from('usuarios')
        .select('*')
        .eq('username', username)
        .single();

      if (searchError || !usuarios) {
        return { 
          success: false, 
          message: 'Usuário não encontrado' 
        };
      }

      // Por enquanto, aceitar qualquer senha para testes
      // TODO: Implementar validação real de senha com bcrypt
      const userData = {
        id: usuarios.id,
        username: usuarios.username,
        email: usuarios.email,
        role: usuarios.role
      };

      setUser(userData);
      localStorage.setItem('regiflex_user', JSON.stringify(userData));

      return { success: true };
    } catch (error) {
      console.error('Erro no login:', error);
      return { 
        success: false, 
        message: 'Erro de conexão' 
      };
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('regiflex_user');
  };

  const value = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

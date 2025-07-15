import React, { createContext, useContext, useReducer, useEffect } from 'react';

const AuthContext = createContext();

const initialState = {
  user: null,
  isAuthenticated: false,
  hasCompletedOnboarding: false,
  isLoading: false,
  error: null,
  userType: null, // 'individual' or 'corporate'
  companyInfo: null,
  onboardingStep: 0,
  selectedGoals: [],
  assessmentData: {},
  deviceIntegrations: []
};

function authReducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        error: null
      };
    
    case 'LOGOUT':
      return {
        ...initialState
      };
    
    case 'SET_USER_TYPE':
      return { ...state, userType: action.payload };
    
    case 'SET_COMPANY_INFO':
      return { ...state, companyInfo: action.payload };
    
    case 'SET_ONBOARDING_STEP':
      return { ...state, onboardingStep: action.payload };
    
    case 'SET_SELECTED_GOALS':
      return { ...state, selectedGoals: action.payload };
    
    case 'SET_ASSESSMENT_DATA':
      return { ...state, assessmentData: action.payload };
    
    case 'ADD_DEVICE_INTEGRATION':
      return {
        ...state,
        deviceIntegrations: [...state.deviceIntegrations, action.payload]
      };
    
    case 'COMPLETE_ONBOARDING':
      return {
        ...state,
        hasCompletedOnboarding: true,
        onboardingStep: 0
      };
    
    case 'RESTORE_SESSION':
      return {
        ...state,
        ...action.payload
      };
    
    default:
      return state;
  }
}

export function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  useEffect(() => {
    // Restore session from localStorage
    const savedAuth = localStorage.getItem('teamWellyAuth');
    if (savedAuth) {
      const parsedAuth = JSON.parse(savedAuth);
      dispatch({ type: 'RESTORE_SESSION', payload: parsedAuth });
    }
  }, []);

  useEffect(() => {
    // Save auth state to localStorage
    localStorage.setItem('teamWellyAuth', JSON.stringify({
      user: state.user,
      isAuthenticated: state.isAuthenticated,
      hasCompletedOnboarding: state.hasCompletedOnboarding,
      userType: state.userType,
      companyInfo: state.companyInfo,
      selectedGoals: state.selectedGoals,
      assessmentData: state.assessmentData,
      deviceIntegrations: state.deviceIntegrations
    }));
  }, [state]);

  const login = async (credentials) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const user = {
        id: 1,
        email: credentials.email,
        name: credentials.name || 'User',
        avatar: '/api/placeholder/40/40',
        joinDate: new Date().toISOString(),
        plan: 'premium'
      };

      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
      return user;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const signUp = async (userData) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const user = {
        id: Math.floor(Math.random() * 1000),
        email: userData.email,
        name: userData.name,
        avatar: '/api/placeholder/40/40',
        joinDate: new Date().toISOString(),
        plan: userData.plan || 'basic'
      };

      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
      return user;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const socialLogin = async (provider) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null });

    try {
      // Simulate social login
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const user = {
        id: Math.floor(Math.random() * 1000),
        email: `user@${provider}.com`,
        name: `${provider} User`,
        avatar: '/api/placeholder/40/40',
        joinDate: new Date().toISOString(),
        plan: 'basic',
        provider
      };

      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
      return user;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const logout = () => {
    dispatch({ type: 'LOGOUT' });
    localStorage.removeItem('teamWellyAuth');
    localStorage.removeItem('teamWellyAppState');
  };

  const value = {
    ...state,
    actions: {
      login,
      signUp,
      socialLogin,
      logout,
      setUserType: (type) => dispatch({ type: 'SET_USER_TYPE', payload: type }),
      setCompanyInfo: (info) => dispatch({ type: 'SET_COMPANY_INFO', payload: info }),
      setOnboardingStep: (step) => dispatch({ type: 'SET_ONBOARDING_STEP', payload: step }),
      setSelectedGoals: (goals) => dispatch({ type: 'SET_SELECTED_GOALS', payload: goals }),
      setAssessmentData: (data) => dispatch({ type: 'SET_ASSESSMENT_DATA', payload: data }),
      addDeviceIntegration: (device) => dispatch({ type: 'ADD_DEVICE_INTEGRATION', payload: device }),
      completeOnboarding: () => dispatch({ type: 'COMPLETE_ONBOARDING' })
    }
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
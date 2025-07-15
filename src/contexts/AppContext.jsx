import React, { createContext, useContext, useReducer, useEffect } from 'react';

const AppContext = createContext();

const initialState = {
  user: null,
  userProgress: {
    dailyCompletion: 0,
    weeklyTrends: [],
    wellyPoints: 0,
    currentStreak: 0,
    completedChallenges: [],
    bookmarkedPrograms: [],
    completedPrograms: []
  },
  todaysSuggestions: [],
  upcomingBookings: [],
  challenges: [],
  programs: [],
  notifications: [],
  theme: 'light',
  settings: {
    notifications: {
      push: true,
      email: true,
      frequency: 'daily'
    },
    privacy: {
      dataSharing: false,
      analytics: true
    }
  }
};

function appReducer(state, action) {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    
    case 'UPDATE_PROGRESS':
      return {
        ...state,
        userProgress: { ...state.userProgress, ...action.payload }
      };
    
    case 'ADD_WELLY_POINTS':
      return {
        ...state,
        userProgress: {
          ...state.userProgress,
          wellyPoints: state.userProgress.wellyPoints + action.payload
        }
      };
    
    case 'COMPLETE_CHALLENGE':
      return {
        ...state,
        userProgress: {
          ...state.userProgress,
          completedChallenges: [...state.userProgress.completedChallenges, action.payload]
        }
      };
    
    case 'BOOKMARK_PROGRAM':
      return {
        ...state,
        userProgress: {
          ...state.userProgress,
          bookmarkedPrograms: [...state.userProgress.bookmarkedPrograms, action.payload]
        }
      };
    
    case 'REMOVE_BOOKMARK':
      return {
        ...state,
        userProgress: {
          ...state.userProgress,
          bookmarkedPrograms: state.userProgress.bookmarkedPrograms.filter(id => id !== action.payload)
        }
      };
    
    case 'SET_PROGRAMS':
      return { ...state, programs: action.payload };
    
    case 'SET_CHALLENGES':
      return { ...state, challenges: action.payload };
    
    case 'SET_TODAYS_SUGGESTIONS':
      return { ...state, todaysSuggestions: action.payload };
    
    case 'SET_UPCOMING_BOOKINGS':
      return { ...state, upcomingBookings: action.payload };
    
    case 'ADD_NOTIFICATION':
      return {
        ...state,
        notifications: [action.payload, ...state.notifications]
      };
    
    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload)
      };
    
    case 'UPDATE_SETTINGS':
      return {
        ...state,
        settings: { ...state.settings, ...action.payload }
      };
    
    case 'SET_THEME':
      return { ...state, theme: action.payload };
    
    default:
      return state;
  }
}

export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  useEffect(() => {
    // Load initial data from localStorage
    const savedState = localStorage.getItem('teamWellyAppState');
    if (savedState) {
      const parsedState = JSON.parse(savedState);
      dispatch({ type: 'SET_USER', payload: parsedState.user });
      dispatch({ type: 'UPDATE_PROGRESS', payload: parsedState.userProgress });
      dispatch({ type: 'UPDATE_SETTINGS', payload: parsedState.settings });
    }

    // Initialize mock data
    initializeMockData();
  }, []);

  useEffect(() => {
    // Save state to localStorage whenever it changes
    localStorage.setItem('teamWellyAppState', JSON.stringify({
      user: state.user,
      userProgress: state.userProgress,
      settings: state.settings
    }));
  }, [state.user, state.userProgress, state.settings]);

  const initializeMockData = () => {
    // Mock today's suggestions
    const suggestions = [
      {
        id: 1,
        type: 'stretch',
        title: 'Morning Neck & Shoulder Stretch',
        duration: '5 min',
        thumbnail: '/api/placeholder/200/150',
        completed: false
      },
      {
        id: 2,
        type: 'breathwork',
        title: 'Box Breathing for Focus',
        duration: '3 min',
        thumbnail: '/api/placeholder/200/150',
        completed: false
      },
      {
        id: 3,
        type: 'meditation',
        title: 'Mindful Moment',
        duration: '7 min',
        thumbnail: '/api/placeholder/200/150',
        completed: false
      }
    ];

    // Mock upcoming bookings
    const bookings = [
      {
        id: 1,
        type: '1-on-1',
        title: 'Recovery Session with Chris',
        date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
        duration: '30 min',
        coach: 'Chris Thompson'
      },
      {
        id: 2,
        type: 'group',
        title: 'Workplace Wellness Workshop',
        date: new Date(Date.now() + 72 * 60 * 60 * 1000).toISOString(),
        duration: '45 min',
        coach: 'Fran Martinez'
      }
    ];

    // Mock challenges
    const challenges = [
      {
        id: 1,
        title: 'Stretch 5 minutes today',
        description: 'Complete any stretch routine',
        points: 50,
        completed: false,
        type: 'daily'
      },
      {
        id: 2,
        title: 'Log a deep breath session',
        description: 'Practice breathing exercises',
        points: 30,
        completed: false,
        type: 'daily'
      },
      {
        id: 3,
        title: 'Week-long wellness streak',
        description: 'Complete activities 7 days in a row',
        points: 200,
        completed: false,
        type: 'weekly'
      }
    ];

    dispatch({ type: 'SET_TODAYS_SUGGESTIONS', payload: suggestions });
    dispatch({ type: 'SET_UPCOMING_BOOKINGS', payload: bookings });
    dispatch({ type: 'SET_CHALLENGES', payload: challenges });
  };

  const value = {
    state,
    dispatch,
    actions: {
      setUser: (user) => dispatch({ type: 'SET_USER', payload: user }),
      updateProgress: (progress) => dispatch({ type: 'UPDATE_PROGRESS', payload: progress }),
      addWellyPoints: (points) => dispatch({ type: 'ADD_WELLY_POINTS', payload: points }),
      completeChallenge: (challenge) => dispatch({ type: 'COMPLETE_CHALLENGE', payload: challenge }),
      bookmarkProgram: (programId) => dispatch({ type: 'BOOKMARK_PROGRAM', payload: programId }),
      removeBookmark: (programId) => dispatch({ type: 'REMOVE_BOOKMARK', payload: programId }),
      addNotification: (notification) => dispatch({ type: 'ADD_NOTIFICATION', payload: notification }),
      removeNotification: (id) => dispatch({ type: 'REMOVE_NOTIFICATION', payload: id }),
      updateSettings: (settings) => dispatch({ type: 'UPDATE_SETTINGS', payload: settings }),
      setTheme: (theme) => dispatch({ type: 'SET_THEME', payload: theme })
    }
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
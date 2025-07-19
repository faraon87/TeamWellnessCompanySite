import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { 
  Home, 
  BookOpen, 
  Users, 
  Trophy, 
  Settings, 
  Shield,
  Heart,
  BarChart3
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

const Navigation = () => {
  const location = useLocation();
  const { user } = useAuth();

  const navigationItems = [
    { path: '/', icon: Home, label: 'Dashboard', color: 'text-blue-600' },
    { path: '/programs', icon: BookOpen, label: 'Programs', color: 'text-green-600' },
    { path: '/coaching', icon: Users, label: 'Coaching', color: 'text-purple-600' },
    { path: '/challenges', icon: Trophy, label: 'Challenges', color: 'text-orange-600' },
    { path: '/settings', icon: Settings, label: 'Settings', color: 'text-gray-600' }
  ];

  // Add admin navigation for corporate users
  if (user?.plan === 'corporate' || user?.role === 'admin') {
    navigationItems.push({
      path: '/admin',
      icon: Shield,
      label: 'Admin',
      color: 'text-red-600'
    });
  }

  return (
    <>
      {/* Desktop Sidebar */}
      <nav className="hidden md:fixed md:inset-y-0 md:flex md:w-60 md:flex-col">
        <div className="flex flex-col flex-grow bg-white border-r border-gray-200 pt-5 pb-4 overflow-y-auto">
          {/* Logo */}
          <div className="flex items-center flex-shrink-0 px-4 mb-8">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center">
                <Heart className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Team Welly</h1>
                <p className="text-xs text-gray-500">Health & Wellness</p>
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="flex-grow flex flex-col">
            <nav className="flex-1 px-2 space-y-1">
              {navigationItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                
                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors ${
                      isActive
                        ? 'bg-green-50 text-green-700 border-r-2 border-green-500'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <Icon
                      className={`mr-3 h-5 w-5 transition-colors ${
                        isActive ? item.color : 'text-gray-400 group-hover:text-gray-500'
                      }`}
                    />
                    {item.label}
                  </NavLink>
                );
              })}
            </nav>
          </div>

          {/* User Profile */}
          <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
            <div className="flex items-center space-x-3">
              <img
                className="h-8 w-8 rounded-full"
                src={user?.avatar || '/api/placeholder/32/32'}
                alt={user?.name || 'User'}
              />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user?.name || 'User'}
                </p>
                <p className="text-xs text-gray-500 truncate">
                  {user?.plan || 'Basic'} Plan
                </p>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Bottom Navigation */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-2 py-1 z-50">
        <div className="flex justify-around">
          {navigationItems.slice(0, 5).map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={`flex flex-col items-center py-2 px-3 min-w-0 flex-1 text-center transition-colors ${
                  isActive ? 'text-green-600' : 'text-gray-500'
                }`}
              >
                <Icon className={`h-5 w-5 ${isActive ? item.color : 'text-gray-400'}`} />
                <span className="text-xs mt-1 truncate">{item.label}</span>
              </NavLink>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default Navigation;
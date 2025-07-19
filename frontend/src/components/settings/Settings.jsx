import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Button from '../common/Button';
import { 
  User, 
  Bell, 
  Smartphone, 
  Shield, 
  HelpCircle, 
  LogOut,
  Mail,
  Phone,
  MapPin,
  Camera,
  Check,
  X
} from 'lucide-react';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [notificationSettings, setNotificationSettings] = useState({
    push: true,
    email: true,
    sms: false,
    frequency: 'daily'
  });

  const [connectedDevices, setConnectedDevices] = useState([
    { id: 1, name: 'Apple Health', connected: true, icon: '🏥' },
    { id: 2, name: 'Fitbit', connected: false, icon: '⌚' },
    { id: 3, name: 'Garmin', connected: false, icon: '🏃' }
  ]);

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'devices', label: 'Connected Devices', icon: Smartphone },
    { id: 'privacy', label: 'Privacy', icon: Shield },
    { id: 'support', label: 'Support', icon: HelpCircle }
  ];

  const toggleDevice = (deviceId) => {
    setConnectedDevices(devices =>
      devices.map(device =>
        device.id === deviceId
          ? { ...device, connected: !device.connected }
          : device
      )
    );
  };

  const handleNotificationChange = (key, value) => {
    setNotificationSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
              <p className="text-sm text-gray-600">Manage your account and preferences</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <div className="lg:w-64 flex-shrink-0">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <nav className="space-y-2">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                        activeTab === tab.id
                          ? 'bg-green-50 text-green-700 border-r-2 border-green-500'
                          : 'text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span className="text-sm font-medium">{tab.label}</span>
                    </button>
                  );
                })}
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            {/* Profile Settings */}
            {activeTab === 'profile' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-2xl shadow-sm p-6"
              >
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Profile Information</h2>
                
                <div className="space-y-6">
                  {/* Avatar */}
                  <div className="flex items-center space-x-4">
                    <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center">
                      <User className="w-10 h-10 text-gray-400" />
                    </div>
                    <div>
                      <Button variant="outline" size="small" icon={Camera}>
                        Change Photo
                      </Button>
                      <p className="text-xs text-gray-500 mt-1">
                        JPG, PNG up to 5MB
                      </p>
                    </div>
                  </div>

                  {/* Form Fields */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Full Name
                      </label>
                      <input
                        type="text"
                        defaultValue="John Doe"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Email Address
                      </label>
                      <input
                        type="email"
                        defaultValue="john.doe@example.com"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Phone Number
                      </label>
                      <input
                        type="tel"
                        defaultValue="+1 (555) 123-4567"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Location
                      </label>
                      <input
                        type="text"
                        defaultValue="San Francisco, CA"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end space-x-3">
                    <Button variant="outline">Cancel</Button>
                    <Button>Save Changes</Button>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Notification Settings */}
            {activeTab === 'notifications' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-2xl shadow-sm p-6"
              >
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Notification Preferences</h2>
                
                <div className="space-y-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-gray-900">Push Notifications</h3>
                        <p className="text-sm text-gray-500">
                          Receive notifications on your device
                        </p>
                      </div>
                      <button
                        onClick={() => handleNotificationChange('push', !notificationSettings.push)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          notificationSettings.push ? 'bg-green-600' : 'bg-gray-200'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            notificationSettings.push ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-gray-900">Email Notifications</h3>
                        <p className="text-sm text-gray-500">
                          Get updates via email
                        </p>
                      </div>
                      <button
                        onClick={() => handleNotificationChange('email', !notificationSettings.email)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          notificationSettings.email ? 'bg-green-600' : 'bg-gray-200'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            notificationSettings.email ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-gray-900">SMS Notifications</h3>
                        <p className="text-sm text-gray-500">
                          Receive text messages
                        </p>
                      </div>
                      <button
                        onClick={() => handleNotificationChange('sms', !notificationSettings.sms)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          notificationSettings.sms ? 'bg-green-600' : 'bg-gray-200'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            notificationSettings.sms ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>
                  </div>

                  <div>
                    <h3 className="font-medium text-gray-900 mb-3">Frequency</h3>
                    <div className="space-y-2">
                      {['immediate', 'daily', 'weekly'].map((freq) => (
                        <label key={freq} className="flex items-center space-x-2">
                          <input
                            type="radio"
                            name="frequency"
                            value={freq}
                            checked={notificationSettings.frequency === freq}
                            onChange={(e) => handleNotificationChange('frequency', e.target.value)}
                            className="text-green-600 focus:ring-green-500"
                          />
                          <span className="text-sm text-gray-700 capitalize">{freq}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Connected Devices */}
            {activeTab === 'devices' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-2xl shadow-sm p-6"
              >
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Connected Devices</h2>
                
                <div className="space-y-4">
                  {connectedDevices.map((device) => (
                    <div key={device.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-xl">
                      <div className="flex items-center space-x-3">
                        <div className="text-2xl">{device.icon}</div>
                        <div>
                          <h3 className="font-medium text-gray-900">{device.name}</h3>
                          <p className="text-sm text-gray-500">
                            {device.connected ? 'Connected' : 'Not connected'}
                          </p>
                        </div>
                      </div>
                      <Button
                        variant={device.connected ? 'outline' : 'primary'}
                        size="small"
                        onClick={() => toggleDevice(device.id)}
                        icon={device.connected ? X : Check}
                      >
                        {device.connected ? 'Disconnect' : 'Connect'}
                      </Button>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Privacy Settings */}
            {activeTab === 'privacy' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-2xl shadow-sm p-6"
              >
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Privacy Settings</h2>
                
                <div className="space-y-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-gray-900">Data Sharing</h3>
                        <p className="text-sm text-gray-500">
                          Share anonymized data to improve our services
                        </p>
                      </div>
                      <button className="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-200">
                        <span className="inline-block h-4 w-4 transform rounded-full bg-white translate-x-1" />
                      </button>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-medium text-gray-900">Analytics</h3>
                        <p className="text-sm text-gray-500">
                          Help us improve by sharing usage analytics
                        </p>
                      </div>
                      <button className="relative inline-flex h-6 w-11 items-center rounded-full bg-green-600">
                        <span className="inline-block h-4 w-4 transform rounded-full bg-white translate-x-6" />
                      </button>
                    </div>
                  </div>

                  <div className="border-t pt-6">
                    <h3 className="font-medium text-gray-900 mb-3">Data Management</h3>
                    <div className="space-y-3">
                      <Button variant="outline" fullWidth>
                        Download My Data
                      </Button>
                      <Button variant="outline" fullWidth>
                        Delete My Account
                      </Button>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Support */}
            {activeTab === 'support' && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white rounded-2xl shadow-sm p-6"
              >
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Support & Help</h2>
                
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 border border-gray-200 rounded-xl">
                      <Mail className="w-8 h-8 text-blue-600 mb-3" />
                      <h3 className="font-medium text-gray-900 mb-2">Email Support</h3>
                      <p className="text-sm text-gray-600 mb-3">
                        Get help via email within 24 hours
                      </p>
                      <Button variant="outline" size="small">
                        Contact Support
                      </Button>
                    </div>

                    <div className="p-4 border border-gray-200 rounded-xl">
                      <Phone className="w-8 h-8 text-green-600 mb-3" />
                      <h3 className="font-medium text-gray-900 mb-2">Phone Support</h3>
                      <p className="text-sm text-gray-600 mb-3">
                        Call us Monday-Friday 9AM-5PM
                      </p>
                      <Button variant="outline" size="small">
                        Call Now
                      </Button>
                    </div>
                  </div>

                  <div>
                    <h3 className="font-medium text-gray-900 mb-3">Frequently Asked Questions</h3>
                    <div className="space-y-2">
                      <details className="border border-gray-200 rounded-lg">
                        <summary className="p-4 cursor-pointer font-medium text-gray-900">
                          How do I sync my fitness devices?
                        </summary>
                        <div className="p-4 pt-0 text-sm text-gray-600">
                          Go to Settings &gt; Connected Devices and follow the setup instructions for your device.
                        </div>
                      </details>
                      <details className="border border-gray-200 rounded-lg">
                        <summary className="p-4 cursor-pointer font-medium text-gray-900">
                          How do WellyPoints work?
                        </summary>
                        <div className="p-4 pt-0 text-sm text-gray-600">
                          Earn points by completing daily challenges, programs, and wellness activities.
                        </div>
                      </details>
                      <details className="border border-gray-200 rounded-lg">
                        <summary className="p-4 cursor-pointer font-medium text-gray-900">
                          Can I use Team Welly offline?
                        </summary>
                        <div className="p-4 pt-0 text-sm text-gray-600">
                          Some features are available offline once you've downloaded content.
                        </div>
                      </details>
                    </div>
                  </div>

                  <div className="border-t pt-6">
                    <Button variant="outline" fullWidth icon={LogOut}>
                      Sign Out
                    </Button>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Button from '../common/Button';
import { 
  BarChart3, 
  Users, 
  MessageSquare, 
  Settings, 
  FileText,
  TrendingUp,
  Activity,
  Calendar,
  Award,
  Clock,
  Target,
  Send,
  Plus,
  Download
} from 'lucide-react';

const AdminPortal = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [message, setMessage] = useState('');

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'employees', label: 'Employees', icon: Users },
    { id: 'messaging', label: 'Messaging', icon: MessageSquare },
    { id: 'settings', label: 'Package Settings', icon: Settings },
    { id: 'reports', label: 'ROI Reports', icon: FileText }
  ];

  const dashboardStats = [
    { label: 'Total Employees', value: '156', change: '+12%', color: 'text-blue-600' },
    { label: 'Active Users', value: '142', change: '+8%', color: 'text-green-600' },
    { label: 'Programs Completed', value: '1,234', change: '+24%', color: 'text-purple-600' },
    { label: 'Coaching Sessions', value: '89', change: '+15%', color: 'text-orange-600' }
  ];

  const topPrograms = [
    { name: 'Desk Warrior Routine', completions: 89, percentage: 92 },
    { name: 'Stress Management', completions: 76, percentage: 78 },
    { name: 'Morning Stretch', completions: 71, percentage: 73 },
    { name: 'Breathing Exercises', completions: 65, percentage: 67 }
  ];

  const employees = [
    { id: 1, name: 'Sarah Johnson', department: 'Marketing', lastActive: '2 hours ago', progress: 85 },
    { id: 2, name: 'Mike Chen', department: 'Engineering', lastActive: '1 day ago', progress: 72 },
    { id: 3, name: 'Emma Wilson', department: 'Sales', lastActive: '3 hours ago', progress: 91 },
    { id: 4, name: 'Alex Rodriguez', department: 'HR', lastActive: '5 hours ago', progress: 68 }
  ];

  const sendMessage = () => {
    if (message.trim()) {
      console.log('Sending message:', message);
      setMessage('');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Admin Portal</h1>
              <p className="text-sm text-gray-600">Manage your corporate wellness program</p>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="small" icon={Download}>
                Export Data
              </Button>
              <Button size="small" icon={Plus}>
                Add Event
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tabs */}
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg mb-8 w-fit">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-white text-green-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Dashboard */}
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {dashboardStats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-2xl shadow-sm p-6"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">{stat.label}</p>
                      <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                    </div>
                    <div className={`text-sm font-medium ${stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                      {stat.change}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Charts and Analytics */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-2xl shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Programs</h3>
                <div className="space-y-4">
                  {topPrograms.map((program) => (
                    <div key={program.name} className="flex items-center justify-between">
                      <div className="flex-1">
                        <p className="text-sm font-medium text-gray-900">{program.name}</p>
                        <p className="text-xs text-gray-500">{program.completions} completions</p>
                      </div>
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-green-500 h-2 rounded-full"
                          style={{ width: `${program.percentage}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white rounded-2xl shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Engagement Trends</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Daily Active Users</span>
                    <span className="text-sm font-medium text-green-600">+15%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Program Completion Rate</span>
                    <span className="text-sm font-medium text-green-600">+8%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Coaching Bookings</span>
                    <span className="text-sm font-medium text-green-600">+22%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Challenge Participation</span>
                    <span className="text-sm font-medium text-green-600">+31%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Employees */}
        {activeTab === 'employees' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Employee Overview</h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="text-left text-sm text-gray-600">
                      <th className="pb-3">Employee</th>
                      <th className="pb-3">Department</th>
                      <th className="pb-3">Last Active</th>
                      <th className="pb-3">Progress</th>
                    </tr>
                  </thead>
                  <tbody className="space-y-2">
                    {employees.map((employee) => (
                      <tr key={employee.id} className="border-t">
                        <td className="py-3">
                          <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                              <Users className="w-4 h-4 text-gray-400" />
                            </div>
                            <span className="font-medium text-gray-900">{employee.name}</span>
                          </div>
                        </td>
                        <td className="py-3 text-sm text-gray-600">{employee.department}</td>
                        <td className="py-3 text-sm text-gray-600">{employee.lastActive}</td>
                        <td className="py-3">
                          <div className="flex items-center space-x-2">
                            <div className="w-16 bg-gray-200 rounded-full h-2">
                              <div
                                className="bg-green-500 h-2 rounded-full"
                                style={{ width: `${employee.progress}%` }}
                              />
                            </div>
                            <span className="text-sm text-gray-600">{employee.progress}%</span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Messaging */}
        {activeTab === 'messaging' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Send Message to Employees</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Message Type
                  </label>
                  <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                    <option>Wellness Tip</option>
                    <option>Challenge Announcement</option>
                    <option>Program Recommendation</option>
                    <option>General Update</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Message Content
                  </label>
                  <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Type your message here..."
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>
                
                <div className="flex items-center space-x-4">
                  <Button onClick={sendMessage} icon={Send} iconPosition="left">
                    Send Message
                  </Button>
                  <Button variant="outline">Schedule for Later</Button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Package Settings */}
        {activeTab === 'settings' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Package Customization</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Available Modules</h4>
                  <div className="space-y-2">
                    {[
                      { name: 'Programs Library', enabled: true },
                      { name: 'Live Coaching', enabled: true },
                      { name: 'Team Challenges', enabled: true },
                      { name: 'Progress Analytics', enabled: false },
                      { name: 'Custom Branding', enabled: false }
                    ].map((module) => (
                      <div key={module.name} className="flex items-center justify-between">
                        <span className="text-sm text-gray-700">{module.name}</span>
                        <button
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            module.enabled ? 'bg-green-600' : 'bg-gray-200'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              module.enabled ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ROI Reports */}
        {activeTab === 'reports' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">ROI Reports</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="p-4 bg-gray-50 rounded-xl">
                  <h4 className="font-medium text-gray-900 mb-2">Stress Score Improvement</h4>
                  <p className="text-2xl font-bold text-green-600">-23%</p>
                  <p className="text-sm text-gray-600">Average reduction</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-xl">
                  <h4 className="font-medium text-gray-900 mb-2">Sick Days Reduction</h4>
                  <p className="text-2xl font-bold text-green-600">-15%</p>
                  <p className="text-sm text-gray-600">Year over year</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-xl">
                  <h4 className="font-medium text-gray-900 mb-2">Productivity Increase</h4>
                  <p className="text-2xl font-bold text-green-600">+18%</p>
                  <p className="text-sm text-gray-600">Based on surveys</p>
                </div>
              </div>
              <div className="mt-6">
                <Button icon={Download} iconPosition="left">
                  Download Full Report
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminPortal;
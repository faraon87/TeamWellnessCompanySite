import React, { useState } from 'react';

// Inline styles to avoid any CSS issues
const styles = {
  app: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    backgroundColor: '#f8f9fa',
    minHeight: '100vh',
    color: '#333333'
  },
  welcomeContainer: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '16px'
  },
  welcomeCard: {
    maxWidth: '400px',
    width: '100%',
    backgroundColor: '#ffffff',
    borderRadius: '16px',
    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.1)',
    padding: '32px',
    textAlign: 'center'
  },
  logo: {
    width: '64px',
    height: '64px',
    background: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '0 auto 24px',
    color: '#ffffff',
    fontSize: '32px'
  },
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: '8px'
  },
  subtitle: {
    color: '#6b7280',
    marginBottom: '32px',
    lineHeight: '1.6'
  },
  button: {
    width: '100%',
    backgroundColor: '#16a34a',
    color: '#ffffff',
    border: 'none',
    borderRadius: '12px',
    padding: '16px 24px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px'
  },
  buttonHover: {
    backgroundColor: '#15803d',
    transform: 'translateY(-1px)'
  },
  buttonLoading: {
    backgroundColor: '#9ca3af',
    cursor: 'not-allowed'
  },
  dashboard: {
    minHeight: '100vh',
    backgroundColor: '#f8f9fa'
  },
  header: {
    backgroundColor: '#ffffff',
    borderBottom: '1px solid #e5e7eb',
    padding: '16px 24px'
  },
  headerTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: '4px'
  },
  headerSubtitle: {
    color: '#6b7280',
    fontSize: '14px'
  },
  headerStats: {
    display: 'flex',
    gap: '16px',
    marginTop: '16px'
  },
  stat: {
    backgroundColor: '#f0fdf4',
    padding: '8px 16px',
    borderRadius: '20px',
    fontSize: '14px',
    fontWeight: '500',
    color: '#16a34a'
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '32px 24px'
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '32px'
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '16px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.07)',
    padding: '24px'
  },
  cardTitle: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#111827',
    marginBottom: '16px'
  },
  suggestionGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '16px'
  },
  suggestion: {
    backgroundColor: '#f8f9fa',
    borderRadius: '12px',
    padding: '16px',
    textAlign: 'center'
  },
  suggestionTitle: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#111827',
    marginBottom: '8px'
  },
  suggestionMeta: {
    fontSize: '14px',
    color: '#6b7280',
    marginBottom: '16px'
  },
  smallButton: {
    width: '100%',
    backgroundColor: '#16a34a',
    color: '#ffffff',
    border: 'none',
    borderRadius: '8px',
    padding: '8px 16px',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer'
  },
  booking: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '16px',
    backgroundColor: '#f8f9fa',
    borderRadius: '12px',
    marginBottom: '12px'
  },
  bookingInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px'
  },
  bookingIcon: {
    width: '48px',
    height: '48px',
    backgroundColor: '#dbeafe',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: '#2563eb',
    fontSize: '20px'
  },
  bookingTitle: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#111827'
  },
  bookingTime: {
    fontSize: '14px',
    color: '#6b7280'
  },
  navigation: {
    position: 'fixed',
    bottom: '0',
    left: '0',
    right: '0',
    backgroundColor: '#ffffff',
    borderTop: '1px solid #e5e7eb',
    padding: '8px 16px',
    display: 'flex',
    justifyContent: 'space-around'
  },
  navItem: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '8px 12px',
    cursor: 'pointer',
    color: '#6b7280',
    fontSize: '12px',
    fontWeight: '500'
  },
  navItemActive: {
    color: '#16a34a'
  },
  navIcon: {
    fontSize: '20px',
    marginBottom: '4px'
  },
  programsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '24px'
  },
  programCard: {
    backgroundColor: '#ffffff',
    borderRadius: '16px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.07)',
    padding: '24px',
    textAlign: 'center'
  },
  programIcon: {
    width: '48px',
    height: '48px',
    backgroundColor: '#f0fdf4',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '0 auto 16px',
    color: '#16a34a',
    fontSize: '20px'
  },
  programTitle: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#111827',
    marginBottom: '8px'
  },
  programDesc: {
    fontSize: '14px',
    color: '#6b7280',
    marginBottom: '16px'
  },
  sectionHeader: {
    textAlign: 'center',
    marginBottom: '32px'
  },
  sectionTitle: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: '8px'
  },
  sectionSubtitle: {
    fontSize: '16px',
    color: '#6b7280'
  }
};

// Main App Component
const TeamWellyApp = () => {
  const [currentView, setCurrentView] = useState('welcome');
  const [isLoading, setIsLoading] = useState(false);

  const handleWelcome = () => {
    setIsLoading(true);
    setTimeout(() => {
      setCurrentView('dashboard');
      setIsLoading(false);
    }, 1000);
  };

  const renderWelcome = () => (
    <div style={styles.welcomeContainer}>
      <div style={styles.welcomeCard}>
        <div style={styles.logo}>❤️</div>
        <h1 style={styles.title}>Welcome to Team Welly</h1>
        <p style={styles.subtitle}>
          Your comprehensive health and wellness companion. Let's get you started on your journey to better health.
        </p>
        <button
          style={{
            ...styles.button,
            ...(isLoading ? styles.buttonLoading : {})
          }}
          onClick={handleWelcome}
          disabled={isLoading}
          onMouseOver={(e) => !isLoading && Object.assign(e.target.style, styles.buttonHover)}
          onMouseOut={(e) => !isLoading && Object.assign(e.target.style, styles.button)}
        >
          🎯 {isLoading ? 'Setting up...' : 'Start Your Wellness Journey'}
        </button>
        <div style={{ marginTop: '32px', fontSize: '12px', color: '#9ca3af' }}>
          By continuing, you agree to our Terms of Service and Privacy Policy
        </div>
      </div>
    </div>
  );

  const renderDashboard = () => (
    <div style={styles.dashboard}>
      <div style={styles.header}>
        <h1 style={styles.headerTitle}>Good morning! 👋</h1>
        <p style={styles.headerSubtitle}>Ready to make today amazing?</p>
        <div style={styles.headerStats}>
          <div style={styles.stat}>🏆 2,250 WellyPoints</div>
          <div style={styles.stat}>🔥 3 day streak</div>
        </div>
      </div>
      
      <div style={styles.container}>
        <div style={styles.grid}>
          {/* Today's Suggestions */}
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Today's Suggestions</h2>
            <div style={styles.suggestionGrid}>
              {[
                { title: 'Morning Neck Stretch', type: 'Stretch', duration: '5 min' },
                { title: 'Box Breathing', type: 'Breathwork', duration: '3 min' },
                { title: 'Mindful Moment', type: 'Meditation', duration: '7 min' }
              ].map((item, index) => (
                <div key={index} style={styles.suggestion}>
                  <div style={{ ...styles.logo, width: '40px', height: '40px', fontSize: '16px', margin: '0 auto 12px' }}>
                    ▶️
                  </div>
                  <h3 style={styles.suggestionTitle}>{item.title}</h3>
                  <p style={styles.suggestionMeta}>{item.type} • {item.duration}</p>
                  <button style={styles.smallButton}>Start Now</button>
                </div>
              ))}
            </div>
          </div>

          {/* Upcoming Sessions */}
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Upcoming Sessions</h2>
            {[
              { title: 'Recovery Session with Chris', time: 'Today, 2:00 PM' },
              { title: 'Workplace Wellness Workshop', time: 'Tomorrow, 10:00 AM' }
            ].map((booking, index) => (
              <div key={index} style={styles.booking}>
                <div style={styles.bookingInfo}>
                  <div style={styles.bookingIcon}>📅</div>
                  <div>
                    <div style={styles.bookingTitle}>{booking.title}</div>
                    <div style={styles.bookingTime}>{booking.time}</div>
                  </div>
                </div>
                <button style={styles.smallButton}>Join</button>
              </div>
            ))}
          </div>

          {/* Quick Stats */}
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Quick Stats</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {[
                { icon: '❤️', label: 'Programs Completed', value: '12' },
                { icon: '⚡', label: 'Total Sessions', value: '45' },
                { icon: '⭐', label: 'Badges Earned', value: '8' }
              ].map((stat, index) => (
                <div key={index} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={styles.programIcon}>{stat.icon}</div>
                    <span style={{ fontSize: '14px', fontWeight: '500' }}>{stat.label}</span>
                  </div>
                  <span style={{ fontSize: '14px', fontWeight: 'bold' }}>{stat.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderPrograms = () => (
    <div style={styles.dashboard}>
      <div style={styles.header}>
        <div style={styles.sectionHeader}>
          <h1 style={styles.sectionTitle}>Programs Library</h1>
          <p style={styles.sectionSubtitle}>Discover wellness programs tailored for you</p>
        </div>
      </div>
      
      <div style={styles.container}>
        <div style={styles.programsGrid}>
          {[
            { title: 'Stretch & Mobility', desc: 'Improve flexibility and movement', icon: '🤸' },
            { title: 'Pain to Performance', desc: 'Transform pain into strength', icon: '💪' },
            { title: 'Strength Foundations', desc: 'Build core stability', icon: '🏋️' },
            { title: 'Breath & Stress', desc: 'Master breathing techniques', icon: '🧘' },
            { title: 'Workplace Wellness', desc: 'Perfect for office workers', icon: '💼' },
            { title: 'Mindset & Growth', desc: 'Develop mental resilience', icon: '🧠' }
          ].map((program, index) => (
            <div key={index} style={styles.programCard}>
              <div style={styles.programIcon}>{program.icon}</div>
              <h3 style={styles.programTitle}>{program.title}</h3>
              <p style={styles.programDesc}>{program.desc}</p>
              <button style={styles.smallButton}>Explore</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderComingSoon = (title) => (
    <div style={styles.dashboard}>
      <div style={{ ...styles.container, textAlign: 'center', paddingTop: '100px' }}>
        <h1 style={styles.sectionTitle}>{title}</h1>
        <p style={styles.sectionSubtitle}>This section is coming soon!</p>
      </div>
    </div>
  );

  const renderNavigation = () => (
    <div style={styles.navigation}>
      {[
        { id: 'dashboard', icon: '🏠', label: 'Dashboard' },
        { id: 'programs', icon: '📚', label: 'Programs' },
        { id: 'coaching', icon: '👥', label: 'Coaching' },
        { id: 'challenges', icon: '🏆', label: 'Challenges' },
        { id: 'settings', icon: '⚙️', label: 'Settings' }
      ].map((item) => (
        <div
          key={item.id}
          style={{
            ...styles.navItem,
            ...(currentView === item.id ? styles.navItemActive : {})
          }}
          onClick={() => setCurrentView(item.id)}
        >
          <div style={styles.navIcon}>{item.icon}</div>
          <span>{item.label}</span>
        </div>
      ))}
    </div>
  );

  return (
    <div style={styles.app}>
      {currentView === 'welcome' && renderWelcome()}
      {currentView === 'dashboard' && renderDashboard()}
      {currentView === 'programs' && renderPrograms()}
      {currentView === 'coaching' && renderComingSoon('Coaching')}
      {currentView === 'challenges' && renderComingSoon('Challenges')}
      {currentView === 'settings' && renderComingSoon('Settings')}
      {currentView !== 'welcome' && renderNavigation()}
    </div>
  );
};

export default TeamWellyApp;
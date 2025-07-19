import React, { useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (typeof window !== 'undefined' && window.location.hostname.includes('railway.app') ? 
    'https://teamwellnesscompanysite-production.up.railway.app' : 
    'http://localhost:8001');

const TeamWellnessLanding = () => {
  const [showSignInModal, setShowSignInModal] = useState(false);
  const [showLearnMoreModal, setShowLearnMoreModal] = useState(false);
  const [showLegalModal, setShowLegalModal] = useState(false);
  const [showSignUpModal, setShowSignUpModal] = useState(false);
  const [showFoundersModal, setShowFoundersModal] = useState(false);
  const [showIndividualPricingModal, setShowIndividualPricingModal] = useState(false);
  const [showEnterprisePricingModal, setShowEnterprisePricingModal] = useState(false);
  const [showFAQModal, setShowFAQModal] = useState(false);

  // OAuth Functions
  const initiateGoogleOAuth = () => {
    console.log('Initiating Google OAuth...');
    window.location.href = `${API_BASE_URL}/api/auth/google`;
  };

  const initiateAppleOAuth = () => {
    console.log('Initiating Apple OAuth...');
    window.location.href = `${API_BASE_URL}/api/auth/apple`;
  };

  const initiateTwitterOAuth = () => {
    console.log('Initiating Twitter/X OAuth...');
    window.location.href = `${API_BASE_URL}/api/auth/twitter`;
  };

  return (
    <div className="container">
      {/* Logo in top right */}
      <div className="logo">
        <img src="/twclogo_new.png" alt="Team Welly Logo" className="team-welly-logo-img" />
      </div>

      {/* Main Content */}
      <div className="main-content">
        <div className="header">
          <h1 className="main-title">TEAM WELLNESS COMPANY</h1>
          <p className="subtitle">Transforming workplace wellness through innovative programs and personalized solutions</p>
        </div>
        
        {/* Buttons Grid */}
        <div className="buttons-grid">
          <button className="action-button" onClick={() => setShowSignInModal(true)}>
            SIGN IN
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="9,18 15,12 9,6"></polyline>
            </svg>
          </button>
          <button className="action-button" onClick={() => setShowLearnMoreModal(true)}>
            LEARN MORE
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="9,18 15,12 9,6"></polyline>
            </svg>
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="footer">
        <div className="social-link">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
          </svg>
          <a href="https://instagram.com/teamwellnesscompany" target="_blank" rel="noopener noreferrer">
            @teamwellnesscompany
          </a>
        </div>
        
        <div className="linkedin-link">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
          </svg>
          <a href="https://linkedin.com/company/team-wellness-company" target="_blank" rel="noopener noreferrer">
            Team Wellness Company
          </a>
        </div>
        
        <div className="email-link">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-.904.732-1.636 1.636-1.636h1.064l9.3 6.962 9.3-6.962h1.064A1.636 1.636 0 0 1 24 5.457z"/>
          </svg>
          <a href="mailto:Drchriszeiter@gmail.com">
            Drchriszeiter@gmail.com
          </a>
        </div>
        
        <div className="legal-link">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
          </svg>
          <a href="#" onClick={() => setShowLegalModal(true)}>
            Legal Notice
          </a>
        </div>
      </div>

      {/* Sign In Modal */}
      {showSignInModal && (
        <div className="modal" style={{display: 'block'}}>
          <div className="modal-content">
            <div className="modal-header">
              <h2>Welcome Back!</h2>
              <span className="close" onClick={() => setShowSignInModal(false)}>&times;</span>
            </div>
            <div className="modal-body">
              <div className="signin-options">
                <div className="sso-section">
                  <h3>Sign in with Social Media</h3>
                  <div className="sso-buttons">
                    <button className="sso-button" onClick={initiateGoogleOAuth}>
                      <svg width="20" height="20" viewBox="0 0 24 24">
                        <path fill="#4285f4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="#34a853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="#fbbc05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                        <path fill="#ea4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                      </svg>
                      Continue with Google
                    </button>
                    
                    <button className="sso-button" onClick={initiateAppleOAuth}>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/>
                      </svg>
                      Continue with Apple
                    </button>
                    
                    <button className="sso-button" onClick={initiateTwitterOAuth}>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                      </svg>
                      Continue with X
                    </button>
                  </div>
                </div>
                
                <div className="divider">
                  <span>OR CHOOSE ACCOUNT TYPE</span>
                </div>
                
                <div className="traditional-section">
                  <h3>Login Type Selection</h3>
                  <div className="traditional-buttons">
                    <button className="traditional-button">
                      Corporate Account
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="9,18 15,12 9,6"></polyline>
                      </svg>
                    </button>
                    <button className="traditional-button">
                      Individual Account
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="9,18 15,12 9,6"></polyline>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Learn More Modal */}
      {showLearnMoreModal && (
        <div className="modal" style={{display: 'block'}}>
          <div className="modal-content learn-more-modal">
            <div className="modal-header">
              <h2>About Team Wellness Company</h2>
              <span className="close" onClick={() => setShowLearnMoreModal(false)}>&times;</span>
            </div>
            <div className="modal-body">
              <div className="learn-more-content">
                <section>
                  <h3>🎯 Our Mission</h3>
                  <p>We believe that when people feel better, they lead better — at home, at work, and everywhere in between.</p>
                  <p>Team Welly was created to make wellness actionable, measurable, and meaningful for both individuals and companies. Whether you're recovering from stress, aiming to move better, or leading a high-performing team, our platform helps you build sustainable routines that actually stick.</p>
                  <p>We're not just another wellness app. We're a movement towards daily ownership of mind, body, and culture.</p>
                </section>
                
                <section>
                  <h3>💼 Corporate Solutions</h3>
                  <ul>
                    <li><strong>Comprehensive Wellness Programs</strong> - Fitness, nutrition, mental health</li>
                    <li><strong>Employee Engagement Platform</strong> - Gamification and challenges</li>
                    <li><strong>Health Risk Assessments</strong> - Data-driven wellness insights</li>
                    <li><strong>ROI Analytics</strong> - Measure program effectiveness</li>
                  </ul>
                </section>
                
                <section>
                  <h3>👤 Individual Programs</h3>
                  <ul>
                    <li><strong>Personalized Coaching</strong> - 1-on-1 sessions with certified professionals</li>
                    <li><strong>Wellness Challenges</strong> - Community-driven fitness and health goals</li>
                    <li><strong>Progress Tracking</strong> - Comprehensive health and fitness monitoring</li>
                    <li><strong>Resource Library</strong> - Expert-curated wellness content</li>
                  </ul>
                </section>
                
                <section>
                  <div className="founders-section">
                    <h3 
                      style={{cursor: 'pointer', textDecoration: 'underline'}} 
                      onClick={() => setShowFoundersModal(true)}
                    >
                      👥 Meet The Founders
                    </h3>
                    <p>Click to learn about the team behind Team Wellness Company</p>
                  </div>
                </section>
                
                <section>
                  <h3>📊 Pricing Options</h3>
                  <div className="pricing-nav-buttons">
                    <button className="cta-button secondary" onClick={() => setShowIndividualPricingModal(true)}>
                      Individual Pricing
                    </button>
                    <button className="cta-button secondary" onClick={() => setShowEnterprisePricingModal(true)}>
                      Enterprise Pricing
                    </button>
                  </div>
                </section>

                <section>
                  <h3 
                    style={{cursor: 'pointer', textDecoration: 'underline'}} 
                    onClick={() => setShowFAQModal(true)}
                  >
                    ❓ FAQ & What's Coming
                  </h3>
                  <p>Learn about our roadmap and frequently asked questions</p>
                </section>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Legal Notice Modal */}
      {showLegalModal && (
        <div className="modal" style={{display: 'block'}}>
          <div className="modal-content">
            <div className="modal-header">
              <h2>Legal Notice</h2>
              <span className="close" onClick={() => setShowLegalModal(false)}>&times;</span>
            </div>
            <div className="modal-body">
              <div className="legal-notice-content">
                <div className="legal-placeholder">
                  <h3>Privacy Policy</h3>
                  <p>Your privacy is important to us. We collect and use your information in accordance with our privacy policy to provide and improve our wellness services.</p>
                  
                  <h3>Terms of Service</h3>
                  <p>By using our platform, you agree to our terms of service. Our wellness programs are designed to support your health journey and are not a substitute for professional medical advice.</p>
                  
                  <h3>Data Security</h3>
                  <p>We employ industry-standard security measures to protect your personal and health information. All data is encrypted and stored securely.</p>
                  
                  <h3>Contact Information</h3>
                  <p>For legal inquiries, please contact us at <a href="mailto:Drchriszeiter@gmail.com" className="contact-link">Drchriszeiter@gmail.com</a></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Sign Up Modal */}
      {showSignUpModal && (
        <div className="modal" style={{display: 'block'}}>
          <div className="modal-content">
            <div className="modal-header">
              <h2>Create Your Account</h2>
              <span className="close" onClick={() => setShowSignUpModal(false)}>&times;</span>
            </div>
            <div className="modal-body">
              <form className="signup-form">
                <div className="form-group">
                  <label>Full Name</label>
                  <input type="text" placeholder="Enter your full name" required />
                </div>
                <div className="form-group">
                  <label>Email Address</label>
                  <input type="email" placeholder="Enter your email" required />
                </div>
                <div className="form-group">
                  <label>Password</label>
                  <input type="password" placeholder="Create a password" required />
                </div>
                <div className="form-group">
                  <label>Account Type</label>
                  <select required>
                    <option value="">Select account type</option>
                    <option value="individual">Individual</option>
                    <option value="corporate">Corporate</option>
                  </select>
                </div>
                <button type="submit" className="cta-button primary">Create Account</button>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Meet the Founders Modal */}
      {showFoundersModal && (
        <div className="modal" style={{display: 'block'}}>
          <div className="modal-content learn-more-modal">
            <div className="modal-header">
              <h2>Meet The Founders</h2>
              <span className="close" onClick={() => setShowFoundersModal(false)}>&times;</span>
            </div>
            <div className="modal-body">
              <div className="founders-content">
                <div className="founder-profile">
                  <div className="founder-image-placeholder">
                    <img src="/api/placeholder/150/150" alt="Dr. Chris Zeiter" className="founder-image" />
                  </div>
                  <h3>Dr. Chris Zeiter, DC, CPT, CCWS</h3>
                  <h4>Chiropractor · Trainer · Recovery Director · Corporate Wellness Specialist</h4>
                  <p>Dr. Chris Zeiter's journey began with pain — years of unresolved back issues that affected not just his body, but his confidence, mindset, and daily life. One breakthrough moment changed everything: a single visit where someone finally listened to his story, addressed the root cause, and helped him move forward.</p>
                  <p>That experience became his purpose.</p>
                  <p>Today, Dr. Zeiter empowers others to take control of their health before pain becomes permanent. With a deep understanding of the human body, behavior change, and movement mechanics, he bridges the gap between passive treatment and proactive performance. His approach blends mobility, nervous system regulation, and real-world recovery tools to guide people from discomfort and confusion toward consistency, clarity, and long-term wellness.</p>
                  <p>Driven by personal experience and professional expertise, Dr. Zeiter has helped countless individuals move better, feel stronger, and reclaim their potential — not just in the gym, but in work, life, and everything in between.</p>
                </div>

                <div className="founder-profile">
                  <div className="founder-image-placeholder">
                    <img src="/api/placeholder/150/150" alt="Franchesca Yates" className="founder-image" />
                  </div>
                  <h3>Franchesca Yates, SHRM-CP</h3>
                  <h4>People & Culture Manager · HR Consultant · Wellness Culture Strategist · Certified Sculpt Instructor</h4>
                  <p>With 7+ years of experience in fast-paced, high-growth companies, Fran has built HR programs that prioritize real employee wellbeing — not just check-the-box perks. She's supported teams through sensitive employee relations cases, led culture-building initiatives across both remote and hybrid teams, and helped implement wellness strategies that fuel both people and performance. Her approach is grounded in empathy, transparency, and a deep commitment to helping employees succeed while companies scale sustainably.</p>
                  <p>Fran's passion for wellness doesn't stop at the workplace. As a sculpt instructor, she has seen firsthand how movement can build resilience, boost confidence, and reconnect people to their purpose. After years of navigating demanding roles, she understands what it takes to show up for yourself — mentally, physically, and emotionally — and she's bringing that lived experience into everything she helps design.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Individual Pricing Modal */}
      {showIndividualPricingModal && (
        <div className="modal" style={{display: 'block'}}>
          <div className="modal-content learn-more-modal">
            <div className="modal-header">
              <h2>Individual Pricing</h2>
              <span className="close" onClick={() => setShowIndividualPricingModal(false)}>&times;</span>
            </div>
            <div className="modal-body">
              <div className="pricing-banner">
                <h3>Individual Plans</h3>
                <p>Choose your level of commitment and support.</p>
                <ul>
                  <li><strong>Personalized Coaching</strong> - 1-on-1 sessions with certified professionals</li>
                  <li><strong>Wellness Challenges</strong> - Community-driven fitness and health goals</li>
                  <li><strong>Progress Tracking</strong> - Comprehensive health and fitness monitoring</li>
                  <li><strong>Resource Library</strong> - Expert-curated wellness content</li>
                </ul>
              </div>
              
              <div className="individual-pricing-table">
                <div className="pricing-tier">
                  <h4>Core Recovery</h4>
                  <div className="price">$99/mo</div>
                  <p>Guided mobility + breathwork routines, daily wellness dashboard</p>
                </div>
                <div className="pricing-tier">
                  <h4>Flex & Focus</h4>
                  <div className="price">$199/mo</div>
                  <p>All of Core + custom progressions + email support</p>
                </div>
                <div className="pricing-tier featured">
                  <h4>1-on-1 Coaching</h4>
                  <div className="price">$299/mo</div>
                  <p>All of above + 1 monthly virtual session with a coach</p>
                </div>
                <div className="pricing-tier">
                  <h4>Elite Plan</h4>
                  <div className="price">$499/mo</div>
                  <p>Full access, advanced tracking, 2x coaching sessions, performance programming</p>
                </div>
              </div>
              
              <div className="integration-note">
                <p><strong>All plans include:</strong> Apple Health/Fitbit/Oura integration + WellyPoints system</p>
              </div>
              
              <div className="action-buttons">
                <button className="cta-button primary">Start my Plan</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Enterprise Pricing Modal */}
      {showEnterprisePricingModal && (
        <div className="modal" style={{display: 'block'}}>
          <div className="modal-content learn-more-modal">
            <div className="modal-header">
              <h2>Enterprise Pricing</h2>
              <span className="close" onClick={() => setShowEnterprisePricingModal(false)}>&times;</span>
            </div>
            <div className="modal-body">
              <div className="pricing-banner">
                <h3>Corporate Wellness</h3>
                <p>Bring better health to your culture.</p>
                <ul>
                  <li><strong>Comprehensive Wellness Programs</strong> - Fitness, nutrition, mental health</li>
                  <li><strong>Employee Engagement Platform</strong> - Gamification and challenges</li>
                  <li><strong>Health Risk Assessments</strong> - Data-driven wellness insights</li>
                  <li><strong>ROI Analytics</strong> - Measure program effectiveness</li>
                </ul>
              </div>
              
              <div className="enterprise-pricing-table">
                <div className="corporate-tier">
                  <div className="team-size">0–15 employees</div>
                  <div className="price">$350 Monthly</div>
                </div>
                <div className="corporate-tier">
                  <div className="team-size">16–50 employees</div>
                  <div className="price">$750 Monthly</div>
                </div>
                <div className="corporate-tier">
                  <div className="team-size">51–100 employees</div>
                  <div className="price">$1,200 Monthly</div>
                </div>
                <div className="corporate-tier">
                  <div className="team-size">100+ employees</div>
                  <div className="price">Custom quote</div>
                </div>
              </div>
              
              <div className="enterprise-features">
                <h4>What's Included:</h4>
                <ul>
                  <li>Monthly virtual wellness talks</li>
                  <li>Employee onboarding and wellness assessments</li>
                  <li>1-on-1 coaching access (optional)</li>
                  <li>Admin dashboard with usage + engagement data</li>
                  <li>Customized reporting for ROI tracking</li>
                </ul>
              </div>
              
              <div className="action-buttons">
                <button className="cta-button primary" onClick={() => window.open('https://calendly.com/drchriszeiter', '_blank')}>
                  Talk to Sales
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* FAQ Modal */}
      {showFAQModal && (
        <div className="modal" style={{display: 'block'}}>
          <div className="modal-content learn-more-modal">
            <div className="modal-header">
              <h2>FAQ & What's Coming</h2>
              <span className="close" onClick={() => setShowFAQModal(false)}>&times;</span>
            </div>
            <div className="modal-body">
              <div className="faq-content">
                <section>
                  <h3>What's Coming</h3>
                  <p>We're building for now and the future.</p>
                  
                  <h4>Phase 1 (Months 1–3):</h4>
                  <ul>
                    <li>Daily dashboard, program library, and wellness goals</li>
                    <li>WellyPoints + HR reporting system</li>
                    <li>Apple Health / Fitbit / Oura Ring syncing</li>
                  </ul>
                  
                  <h4>Phase 2 (Months 4–6):</h4>
                  <ul>
                    <li>AI-powered program recommendations</li>
                    <li>Video coaching + scheduling tools</li>
                    <li>Community leaderboards + challenge automation</li>
                    <li>Deep analytics & ROI tracking</li>
                  </ul>
                </section>

                <section>
                  <h3>Why Team Welly?</h3>
                  <div className="why-welly-grid">
                    <div className="why-item">
                      <h4>We're proactive, not reactive.</h4>
                      <p>Burnout, stress, and disconnection don't come with easy fixes — and many companies simply don't have the tools to address them. We meet you where you are and help build simple, sustainable systems that support wellbeing from the inside out.</p>
                    </div>
                    <div className="why-item">
                      <h4>We solve real pain points.</h4>
                      <p>Lack of consistency. Low engagement. Mental fatigue. We've seen it, supported it, and now we're creating wellness solutions that truly work in fast-moving, high-pressure environments.</p>
                    </div>
                    <div className="why-item">
                      <h4>Wellness grounded in real-world experience.</h4>
                      <p>With backgrounds in HR and holistic health, we understand what it takes to support people — emotionally, mentally, and physically — while helping your business thrive.</p>
                    </div>
                    <div className="why-item">
                      <h4>Personalized, secure, and built for scale.</h4>
                      <p>Whether your teams are remote, in-office, or hybrid across the U.S., our platform adapts to your needs — with data security, flexibility, and measurable outcomes at its core.</p>
                    </div>
                    <div className="why-item">
                      <h4>Human-centered, never one-size-fits-all.</h4>
                      <p>We blend everyday simplicity with intentional care — so wellness feels accessible, personal, and part of the culture.</p>
                    </div>
                    <div className="why-item">
                      <h4>Because when your people feel better, they perform better.</h4>
                      <p>We turn daily habits into long-term resilience, engagement, and impact.</p>
                    </div>
                  </div>
                </section>

                <section>
                  <h3>FAQ</h3>
                  <div className="faq-item">
                    <h4>Q: Can my company customize the program?</h4>
                    <p>A: Yes. We work with People teams to tailor onboarding, programming, and engagement strategy.</p>
                  </div>
                  <div className="faq-item">
                    <h4>Q: Are coaching sessions included?</h4>
                    <p>A: Individuals can choose coaching tiers. Companies can add sessions à la carte or in bundles.</p>
                  </div>
                  <div className="faq-item">
                    <h4>Q: How long does onboarding take?</h4>
                    <p>A: Less than 5 minutes for individuals. For companies, 10-14 days depending on company size.</p>
                  </div>
                  <div className="faq-item">
                    <h4>Q: What tech is supported?</h4>
                    <p>A: Apple HealthKit, Fitbit, Oura, Calendly/Zoom, Outlook, Eventbrite, SurveyMonkey, Google Forms, and more.</p>
                  </div>
                </section>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeamWellnessLanding;
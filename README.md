# Team Wellness Company - Landing Page Website

A professional landing page website for Team Wellness Company, featuring a modern design with sign-in and learn more functionality. The site showcases our wellness services, pricing plans, and company information with an elegant dark theme and responsive design.

## 🌟 Features

### Landing Page
- **Professional Design** with dark blue gradient theme and SensaWild-Fill font
- **Sign In Modal** with Apple, Google, and X SSO options plus traditional login
- **Learn More Modal** with comprehensive business information, pricing, and contact forms
- **Responsive Layout** optimized for all screen sizes
- **Interactive Elements** with smooth animations and hover effects

### Business Information
- **Company Mission** and founder profiles
- **Service Offerings** with detailed descriptions
- **Pricing Plans** for individual and corporate clients
- **Contact Information** with Calendly integration and email links
- **Social Media Links** and newsletter signup

### Technical Features
- **Static HTML/CSS/JavaScript** for optimal performance
- **Custom SVG Logo** with Team Welly branding
- **Modal System** for enhanced user experience
- **Responsive Design** for mobile and desktop
- **Professional Typography** with custom font integration

## 🚀 Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with gradients and animations
- **Typography**: SensaWild-Fill custom font
- **Icons**: Custom SVG icons and social media icons
- **Responsive Design**: Mobile-first approach
- **Backend**: FastAPI Python (for future integration)
- **Database**: MongoDB (for future user data)

## 📱 Installation & Setup

### Prerequisites
- Modern web browser
- Local web server (optional for development)

### Development Setup
```bash
# Clone the repository
git clone https://github.com/faraon87/TeamWellnessCompanySite.git

# Navigate to project directory
cd TeamWellnessCompanySite

# Open index.html in your browser
# Or use a local web server:
python -m http.server 8000
# Then visit http://localhost:8000
```

### File Structure
```
/
├── index.html           # Main landing page
├── styles.css          # Custom CSS styling
├── fonts/              # Custom font files
│   ├── SensaWild-Fill.otf
│   └── SensaWild-Fill.ttf
├── public/             # Static assets
│   ├── background.png  # Background image
│   └── twclogo.svg     # Team Welly logo
└── README.md           # This file
```

## 🌐 Deployment

### Static Hosting
This website can be deployed on any static hosting service:

1. **Vercel** - Simple deployment from GitHub
2. **Netlify** - Drag and drop deployment
3. **GitHub Pages** - Free hosting for public repositories
4. **AWS S3** - Scalable static website hosting

### Deployment Steps
1. Upload all files to your hosting service
2. Ensure `index.html` is in the root directory
3. Configure custom domain (optional)
4. Test all functionality including modals and links

### Environment Configuration
- No build process required - pure HTML/CSS/JS
- All assets should be properly linked in `index.html`
- Verify custom fonts are loading correctly
- Test responsive design on various devices

## 🏗️ Architecture

### File Structure
```
/
├── index.html           # Main landing page with modal structure
├── styles.css          # All CSS styling and responsive design
├── fonts/              # Custom typography
│   ├── SensaWild-Fill.otf
│   └── SensaWild-Fill.ttf
├── public/             # Static assets
│   ├── background.png  # Custom background image
│   ├── twclogo.svg     # Team Welly logo
│   └── favicon.ico     # Site icon
└── README.md           # Documentation
```

### Key Components
- **Landing Page**: Main content with title, buttons, and footer
- **Sign In Modal**: SSO options and traditional login choices
- **Learn More Modal**: Complete business information and pricing
- **Responsive Design**: Mobile-first CSS with breakpoints
- **Typography**: Custom font integration with fallbacks

## 🎯 Key Features

### Landing Page Experience
1. **Professional Welcome**: Company title and tagline with elegant typography
2. **Call-to-Action Buttons**: "Sign In" and "Learn More" with smooth interactions
3. **Responsive Design**: Optimized for desktop, tablet, and mobile devices
4. **Social Media Integration**: Instagram and email contact links
5. **Modern Aesthetics**: Dark theme with blue-green gradients

### Sign In Modal
1. **SSO Options**: Apple, Google, and X (Twitter) authentication
2. **Traditional Login**: Corporate and individual user options
3. **User-Friendly Interface**: Clean design with hover effects
4. **Accessibility**: Keyboard navigation and screen reader support

### Learn More Modal
1. **Company Information**: Mission, founders, and business details
2. **Pricing Tables**: Individual and corporate pricing plans
3. **Contact Forms**: Newsletter signup and contact information
4. **Service Details**: Comprehensive feature descriptions
5. **Call-to-Action**: Multiple conversion points throughout

## 🔧 Customization

### Styling
- **Colors**: Modify CSS variables in `styles.css` for theme changes
- **Typography**: Replace SensaWild-Fill font files for different branding
- **Layout**: Adjust responsive breakpoints and grid layouts
- **Animations**: Customize hover effects and transitions

### Content
- **Business Information**: Update company details in the Learn More modal
- **Pricing**: Modify pricing plans and features in `index.html`
- **Contact Info**: Update email addresses and social media links
- **Logo**: Replace SVG logo with custom branding

### Assets
- **Background**: Replace `background.png` with custom background image
- **Logo**: Update `twclogo.svg` with your company logo
- **Icons**: Modify SVG icons for social media and buttons
- **Fonts**: Add custom font files to the `/fonts/` directory

## 🔧 Development Guidelines

### Code Structure
- **HTML**: Semantic markup with proper accessibility attributes
- **CSS**: Organized with responsive design and custom properties
- **JavaScript**: Vanilla ES6+ for modal functionality and interactions
- **Assets**: Optimized images and scalable vector graphics

### Best Practices
- **Performance**: Optimized images and minimal JavaScript
- **Accessibility**: ARIA labels and keyboard navigation
- **SEO**: Proper meta tags and semantic HTML structure
- **Cross-browser**: Compatible with modern browsers
- **Mobile-first**: Responsive design approach

-- ============================================
-- TEAM WELLY DATABASE SCHEMA
-- Comprehensive schema for corporate wellness platform
-- ============================================

-- ============================================
-- CORE USER MANAGEMENT
-- ============================================

-- Users table - handles both individual and corporate users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role ENUM('individual', 'employee', 'hr_admin', 'platform_admin') NOT NULL DEFAULT 'individual',
    
    -- Subscription information
    subscription_plan ENUM('core_recovery', 'flex_focus', 'coaching', 'elite', 'corporate') DEFAULT 'core_recovery',
    subscription_status ENUM('active', 'inactive', 'trial', 'cancelled') DEFAULT 'trial',
    subscription_start_date TIMESTAMP,
    subscription_end_date TIMESTAMP,
    
    -- Profile information
    phone VARCHAR(20),
    date_of_birth DATE,
    profile_image_url VARCHAR(500),
    timezone VARCHAR(50) DEFAULT 'UTC',
    
    -- Wellness goals and preferences
    primary_goals JSON, -- ["reduce_pain", "improve_flexibility", "boost_mental_health", "increase_productivity"]
    pain_areas JSON, -- ["neck", "shoulders", "lower_back", "knees"]
    fitness_level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    available_time_minutes INTEGER DEFAULT 15, -- Daily wellness time commitment
    
    -- Corporate association
    company_id UUID REFERENCES companies(id),
    company_code VARCHAR(20), -- Used during registration
    employee_id VARCHAR(50), -- Company's internal employee ID
    department VARCHAR(100),
    job_title VARCHAR(100),
    
    -- Account status
    email_verified BOOLEAN DEFAULT false,
    onboarding_completed BOOLEAN DEFAULT false,
    terms_accepted BOOLEAN DEFAULT false,
    privacy_accepted BOOLEAN DEFAULT false,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    deleted_at TIMESTAMP -- Soft delete
);

-- Companies table - corporate clients
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255), -- Company email domain (e.g., "acme.com")
    
    -- Subscription details
    plan_type ENUM('starter', 'professional', 'enterprise', 'custom') NOT NULL,
    employee_count INTEGER NOT NULL,
    monthly_price DECIMAL(10,2) NOT NULL, -- $350, $750, $1200, or custom
    billing_cycle ENUM('monthly', 'annual') DEFAULT 'monthly',
    
    -- Company details
    industry VARCHAR(100),
    company_size ENUM('0-15', '16-50', '51-100', '100+') NOT NULL,
    address TEXT,
    website VARCHAR(255),
    
    -- Contact information
    primary_contact_id UUID REFERENCES users(id),
    billing_contact_email VARCHAR(255),
    support_contact_email VARCHAR(255),
    
    -- Settings and customization
    company_logo_url VARCHAR(500),
    brand_colors JSON, -- {"primary": "#4a9eff", "secondary": "#1a1a1a"}
    welcome_message TEXT,
    custom_domain VARCHAR(255), -- For white-label clients
    
    -- Features enabled
    features_enabled JSON, -- ["coaching", "analytics", "integrations", "custom_challenges"]
    integrations_enabled JSON, -- ["slack", "teams", "calendly"]
    
    -- Status
    status ENUM('active', 'trial', 'suspended', 'cancelled') DEFAULT 'trial',
    trial_end_date TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- WELLNESS CONTENT & PROGRAMS
-- ============================================

-- Program categories (Stretch & Mobility, Pain to Performance, etc.)
CREATE TABLE program_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL, -- "Stretch & Mobility", "Pain to Performance"
    slug VARCHAR(100) UNIQUE NOT NULL, -- "stretch-mobility", "pain-to-performance"
    description TEXT,
    icon_url VARCHAR(500),
    color_hex VARCHAR(7), -- "#4a9eff"
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Individual wellness programs
CREATE TABLE programs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id UUID REFERENCES program_categories(id),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    
    -- Content details
    duration_minutes INTEGER, -- 5, 10, 15, 30
    difficulty_level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    equipment_needed JSON, -- ["none", "chair", "resistance_band"]
    target_areas JSON, -- ["neck", "shoulders", "core", "legs"]
    
    -- Media content
    thumbnail_url VARCHAR(500),
    video_url VARCHAR(500),
    audio_url VARCHAR(500),
    
    -- Program structure
    steps JSON, -- [{"step": 1, "title": "Neck rolls", "duration": 30, "description": "..."}]
    instructions TEXT,
    
    -- Gamification
    wellypoints_reward INTEGER DEFAULT 10,
    
    -- Metadata
    is_premium BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    view_count INTEGER DEFAULT 0,
    average_rating DECIMAL(3,2) DEFAULT 0.0,
    
    -- Creator information
    created_by UUID REFERENCES users(id), -- Chris or Fran
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- USER PROGRESS & GAMIFICATION
-- ============================================

-- User progress tracking for programs
CREATE TABLE user_program_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) NOT NULL,
    program_id UUID REFERENCES programs(id) NOT NULL,
    
    -- Progress tracking
    status ENUM('not_started', 'in_progress', 'completed') DEFAULT 'not_started',
    completion_percentage INTEGER DEFAULT 0, -- 0-100
    current_step INTEGER DEFAULT 1,
    
    -- Session data
    sessions_completed INTEGER DEFAULT 0,
    total_time_spent INTEGER DEFAULT 0, -- in minutes
    last_session_date TIMESTAMP,
    
    -- User feedback
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    user_feedback TEXT,
    
    -- Timestamps
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, program_id)
);

-- WellyPoints system
CREATE TABLE user_points (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) NOT NULL,
    
    -- Point tracking
    total_points INTEGER DEFAULT 0,
    points_this_week INTEGER DEFAULT 0,
    points_this_month INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0, -- consecutive days
    longest_streak INTEGER DEFAULT 0,
    
    -- Level system
    current_level INTEGER DEFAULT 1,
    points_to_next_level INTEGER DEFAULT 100,
    
    -- Weekly reset tracking
    last_weekly_reset DATE,
    last_monthly_reset DATE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id)
);

-- Individual point transactions
CREATE TABLE point_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) NOT NULL,
    
    -- Transaction details
    points_awarded INTEGER NOT NULL,
    activity_type ENUM('program_completion', 'daily_login', 'streak_bonus', 'coaching_session', 'challenge_completion', 'assessment_completion') NOT NULL,
    activity_id UUID, -- Reference to specific program, challenge, etc.
    activity_description VARCHAR(255),
    
    -- Metadata
    multiplier DECIMAL(3,2) DEFAULT 1.0, -- For streak bonuses, company challenges
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- HEALTH DATA INTEGRATION
-- ============================================

-- User health data from Apple Health, Fitbit, etc.
CREATE TABLE user_health_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) NOT NULL,
    
    -- Data source
    source ENUM('apple_health', 'google_fit', 'fitbit', 'garmin', 'oura', 'whoop', 'manual') NOT NULL,
    source_device_id VARCHAR(255),
    
    -- Health metrics
    date DATE NOT NULL,
    steps INTEGER,
    calories_burned INTEGER,
    active_minutes INTEGER,
    sleep_duration_minutes INTEGER,
    sleep_quality_score INTEGER, -- 1-100
    heart_rate_avg INTEGER,
    heart_rate_resting INTEGER,
    hrv_score DECIMAL(5,2), -- Heart Rate Variability
    stress_level INTEGER, -- 1-10
    energy_level INTEGER, -- 1-10
    mood_score INTEGER, -- 1-10
    
    -- Additional metrics
    weight_kg DECIMAL(5,2),
    body_fat_percentage DECIMAL(4,1),
    muscle_mass_kg DECIMAL(5,2),
    
    -- Sync information
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, date, source)
);

-- ============================================
-- ASSESSMENTS & SURVEYS
-- ============================================

-- Baseline assessments and periodic surveys
CREATE TABLE assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    type ENUM('baseline', 'wellness_check', 'program_feedback', 'corporate_survey') NOT NULL,
    description TEXT,
    
    -- Assessment structure
    questions JSON, -- Array of question objects
    estimated_duration_minutes INTEGER DEFAULT 5,
    
    -- Targeting
    target_audience ENUM('all_users', 'individual_users', 'corporate_users', 'specific_company') DEFAULT 'all_users',
    target_company_id UUID REFERENCES companies(id),
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    is_required BOOLEAN DEFAULT false,
    
    -- Creator
    created_by UUID REFERENCES users(id),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User assessment responses
CREATE TABLE user_assessment_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) NOT NULL,
    assessment_id UUID REFERENCES assessments(id) NOT NULL,
    
    -- Response data
    responses JSON NOT NULL, -- {"question_1": "answer", "question_2": 7, ...}
    completion_status ENUM('started', 'completed') DEFAULT 'started',
    completion_percentage INTEGER DEFAULT 0,
    
    -- Calculated scores
    overall_score DECIMAL(5,2),
    category_scores JSON, -- {"stress": 7.5, "energy": 6.2, "pain": 3.1}
    
    -- Timing
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    time_spent_minutes INTEGER,
    
    UNIQUE(user_id, assessment_id)
);

-- ============================================
-- COACHING SYSTEM
-- ============================================

-- Coaching sessions (1-on-1 and group)
CREATE TABLE coaching_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Session details
    title VARCHAR(255) NOT NULL,
    type ENUM('one_on_one', 'group', 'corporate_workshop') NOT NULL,
    description TEXT,
    
    -- Scheduling
    scheduled_start TIMESTAMP NOT NULL,
    scheduled_end TIMESTAMP NOT NULL,
    duration_minutes INTEGER NOT NULL,
    timezone VARCHAR(50) DEFAULT 'UTC',
    
    -- Capacity (for group sessions)
    max_participants INTEGER DEFAULT 1, -- 1 for 1-on-1, higher for group
    current_participants INTEGER DEFAULT 0,
    
    -- Coach information
    coach_id UUID REFERENCES users(id) NOT NULL, -- Chris or Fran
    coach_notes TEXT,
    
    -- Session content
    topic VARCHAR(255),
    focus_areas JSON, -- ["pain_management", "stress_reduction", "ergonomics"]
    materials_needed JSON, -- ["yoga_mat", "resistance_band"]
    
    -- Integration
    calendly_event_id VARCHAR(255), -- Link to Calendly booking
    zoom_meeting_id VARCHAR(255),
    zoom_meeting_url VARCHAR(500),
    
    -- Status
    status ENUM('scheduled', 'in_progress', 'completed', 'cancelled', 'no_show') DEFAULT 'scheduled',
    
    -- Recording and follow-up
    recording_url VARCHAR(500),
    follow_up_notes TEXT,
    homework_assigned TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Session participants
CREATE TABLE session_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES coaching_sessions(id) NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,
    
    -- Participation details
    registration_status ENUM('registered', 'waitlisted', 'confirmed', 'cancelled') DEFAULT 'registered',
    attendance_status ENUM('pending', 'attended', 'no_show', 'cancelled') DEFAULT 'pending',
    
    -- Session-specific data
    goals_for_session TEXT,
    session_feedback TEXT,
    session_rating INTEGER CHECK (session_rating >= 1 AND session_rating <= 5),
    
    -- Timestamps
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attended_at TIMESTAMP
);

-- ============================================
-- CHALLENGES & GAMIFICATION
-- ============================================

-- Team and company challenges
CREATE TABLE challenges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Challenge details
    type ENUM('individual', 'team', 'company_wide') NOT NULL,
    category ENUM('daily_activity', 'program_completion', 'streak_building', 'wellness_assessment', 'custom') NOT NULL,
    
    -- Targeting
    target_company_id UUID REFERENCES companies(id), -- NULL for platform-wide challenges
    target_department VARCHAR(100),
    
    -- Challenge parameters
    goal_value INTEGER NOT NULL, -- Target number (steps, points, completions)
    goal_unit VARCHAR(50) NOT NULL, -- "steps", "points", "programs", "minutes"
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    
    -- Timing
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    duration_days INTEGER,
    
    -- Rewards
    wellypoints_reward INTEGER DEFAULT 50,
    badge_reward VARCHAR(255),
    custom_reward TEXT,
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    participants_count INTEGER DEFAULT 0,
    completion_count INTEGER DEFAULT 0,
    
    -- Creator
    created_by UUID REFERENCES users(id),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Challenge participation
CREATE TABLE challenge_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    challenge_id UUID REFERENCES challenges(id) NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,
    
    -- Progress tracking
    current_progress INTEGER DEFAULT 0,
    completion_percentage DECIMAL(5,2) DEFAULT 0.0,
    is_completed BOOLEAN DEFAULT false,
    
    -- Timestamps
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- ============================================
-- ANALYTICS & REPORTING
-- ============================================

-- Daily user activity summary
CREATE TABLE daily_user_activity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) NOT NULL,
    date DATE NOT NULL,
    
    -- Activity metrics
    programs_completed INTEGER DEFAULT 0,
    total_exercise_minutes INTEGER DEFAULT 0,
    wellypoints_earned INTEGER DEFAULT 0,
    
    -- Engagement metrics
    app_opens INTEGER DEFAULT 0,
    session_duration_minutes INTEGER DEFAULT 0,
    features_used JSON, -- ["dashboard", "programs", "coaching"]
    
    -- Wellness metrics
    mood_rating INTEGER, -- 1-10 if user logs it
    energy_rating INTEGER, -- 1-10 if user logs it
    stress_rating INTEGER, -- 1-10 if user logs it
    pain_rating INTEGER, -- 1-10 if user logs it
    
    -- Calculated at end of day
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, date)
);

-- Company analytics aggregation
CREATE TABLE company_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id) NOT NULL,
    date DATE NOT NULL,
    
    -- Participation metrics
    total_employees INTEGER NOT NULL,
    active_users INTEGER DEFAULT 0, -- Logged in within last 7 days
    engaged_users INTEGER DEFAULT 0, -- Completed activity within last 7 days
    new_users INTEGER DEFAULT 0,
    
    -- Activity metrics
    total_programs_completed INTEGER DEFAULT 0,
    total_coaching_sessions INTEGER DEFAULT 0,
    total_wellypoints_earned INTEGER DEFAULT 0,
    average_session_duration DECIMAL(5,2) DEFAULT 0,
    
    -- Wellness trends
    average_mood_score DECIMAL(3,2),
    average_energy_score DECIMAL(3,2),
    average_stress_score DECIMAL(3,2),
    stress_reduction_percentage DECIMAL(5,2), -- Month-over-month
    
    -- ROI metrics
    productivity_score DECIMAL(5,2), -- Calculated metric
    engagement_score DECIMAL(5,2), -- Calculated metric
    estimated_roi DECIMAL(10,2), -- Based on engagement and health improvements
    
    -- Generated automatically each day
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(company_id, date)
);

-- ============================================
-- INTEGRATIONS & EXTERNAL SERVICES
-- ============================================

-- Integration configurations
CREATE TABLE integration_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID REFERENCES companies(id), -- NULL for platform-wide integrations
    user_id UUID REFERENCES users(id), -- For user-specific integrations
    
    -- Integration details
    service_name ENUM('stripe', 'apple_health', 'google_fit', 'fitbit', 'garmin', 'oura', 'whoop', 'calendly', 'slack', 'teams', 'hubspot', 'mailchimp', 'qualtrics') NOT NULL,
    
    -- Configuration data
    config JSON NOT NULL, -- Service-specific configuration
    credentials JSON, -- Encrypted API keys, tokens
    webhook_url VARCHAR(500),
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    last_sync_at TIMESTAMP,
    sync_frequency_hours INTEGER DEFAULT 24,
    
    -- Error tracking
    last_error TEXT,
    error_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Webhook events log
CREATE TABLE webhook_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    integration_config_id UUID REFERENCES integration_configs(id),
    
    -- Event details
    service_name VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSON,
    
    -- Processing
    processing_status ENUM('pending', 'processed', 'failed', 'ignored') DEFAULT 'pending',
    processed_at TIMESTAMP,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Timestamps
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- NOTIFICATIONS & COMMUNICATIONS
-- ============================================

-- Notification system
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    company_id UUID REFERENCES companies(id), -- For company-wide notifications
    
    -- Notification details
    type ENUM('wellness_reminder', 'coaching_session', 'challenge_update', 'achievement', 'system_update', 'billing') NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    -- Delivery channels
    send_push BOOLEAN DEFAULT true,
    send_email BOOLEAN DEFAULT false,
    send_slack BOOLEAN DEFAULT false,
    
    -- Status tracking
    is_read BOOLEAN DEFAULT false,
    delivered_at TIMESTAMP,
    read_at TIMESTAMP,
    
    -- Action button (optional)
    action_url VARCHAR(500),
    action_text VARCHAR(100),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scheduled_for TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- User-related indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_company_id ON users(company_id);
CREATE INDEX idx_users_subscription_status ON users(subscription_status);
CREATE INDEX idx_users_role ON users(role);

-- Progress tracking indexes
CREATE INDEX idx_user_program_progress_user_id ON user_program_progress(user_id);
CREATE INDEX idx_user_program_progress_status ON user_program_progress(status);
CREATE INDEX idx_point_transactions_user_id ON point_transactions(user_id);
CREATE INDEX idx_point_transactions_created_at ON point_transactions(created_at);

-- Health data indexes
CREATE INDEX idx_user_health_data_user_date ON user_health_data(user_id, date);
CREATE INDEX idx_user_health_data_source ON user_health_data(source);

-- Analytics indexes
CREATE INDEX idx_daily_user_activity_user_date ON daily_user_activity(user_id, date);
CREATE INDEX idx_company_analytics_company_date ON company_analytics(company_id, date);

-- Session indexes
CREATE INDEX idx_coaching_sessions_coach_id ON coaching_sessions(coach_id);
CREATE INDEX idx_coaching_sessions_scheduled_start ON coaching_sessions(scheduled_start);
CREATE INDEX idx_session_participants_session_id ON session_participants(session_id);
CREATE INDEX idx_session_participants_user_id ON session_participants(user_id);

-- ============================================
-- EXAMPLE DATA INSERTS
-- ============================================

-- Example program categories
INSERT INTO program_categories (name, slug, description, icon_url, color_hex, sort_order) VALUES
('Stretch & Mobility', 'stretch-mobility', 'Full body stretching and mobility routines', '/icons/stretch.svg', '#4a9eff', 1),
('Pain to Performance', 'pain-to-performance', 'Targeted pain relief and recovery programs', '/icons/recovery.svg', '#ff6b6b', 2),
('Strength Foundations', 'strength-foundations', 'Core stability and functional strength', '/icons/strength.svg', '#51cf66', 3),
('Breath & Stress', 'breath-stress', 'Breathing exercises and stress management', '/icons/meditation.svg', '#845ef7', 4),
('Workplace Wellness', 'workplace-wellness', 'Desk-friendly exercises and ergonomics', '/icons/office.svg', '#fd7e14', 5),
('Mindset & Growth', 'mindset-growth', 'Mental wellness and personal development', '/icons/brain.svg', '#20c997', 6);

-- Example company
INSERT INTO companies (name, domain, plan_type, employee_count, monthly_price, company_size) VALUES
('Acme Corporation', 'acme.com', 'professional', 45, 750.00, '16-50');

-- Example assessment
INSERT INTO assessments (title, type, description, questions, estimated_duration_minutes) VALUES
(
    'Baseline Wellness Assessment',
    'baseline',
    'Initial assessment to understand your current wellness state and goals',
    '[
        {"id": 1, "type": "scale", "question": "How would you rate your current stress level?", "min": 1, "max": 10},
        {"id": 2, "type": "multiple_choice", "question": "What areas of your body experience the most pain?", "options": ["neck", "shoulders", "lower_back", "knees", "none"]},
        {"id": 3, "type": "scale", "question": "How many hours of sleep do you typically get?", "min": 4, "max": 12},
        {"id": 4, "type": "multiple_choice", "question": "What are your primary wellness goals?", "options": ["reduce_pain", "improve_flexibility", "boost_mental_health", "increase_productivity"], "multiple": true}
    ]',
    5
);

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository: `https://github.com/faraon87/TeamWellnessCompanySite`
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Contribution Guidelines
- Follow existing code style and structure
- Test on multiple devices and browsers
- Optimize images and assets before committing
- Update documentation for any new features
- Ensure accessibility standards are maintained

## 📞 Support

For support and inquiries:
- **Email**: [Drchriszeiter@gmail.com](mailto:Drchriszeiter@gmail.com)
- **Calendly**: [Schedule a meeting](https://calendly.com/drchriszeiter)
- **Instagram**: [@teamwellnesscompany](https://www.instagram.com/teamwellnesscompany)
- **Repository Issues**: [GitHub Issues](https://github.com/faraon87/TeamWellnessCompanySite/issues)

---

**Team Wellness Company - Restoring Your Aura One Breath at a Time! 🌱**

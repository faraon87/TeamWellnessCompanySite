import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'
import TeamWellnessLanding from './TeamWellnessLanding.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <TeamWellnessLanding />
  </StrictMode>,
)

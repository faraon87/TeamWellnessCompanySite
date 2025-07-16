import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import StandaloneApp from './StandaloneApp.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <StandaloneApp />
  </StrictMode>,
)

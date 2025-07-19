import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '../styles.css'
import BackendIntegratedApp from './BackendIntegratedApp.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BackendIntegratedApp />
  </StrictMode>,
)

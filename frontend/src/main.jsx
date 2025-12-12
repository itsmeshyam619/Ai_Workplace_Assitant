import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Upload from './pages/Upload'
import Ask from './pages/Ask'
import './styles.css'

function App(){
  return (
    <BrowserRouter>
      <div className="p-6 max-w-3xl mx-auto">
        <nav className="flex gap-4 mb-6">
          <Link to="/" className="text-blue-600">Upload</Link>
          <Link to="/ask" className="text-blue-600">Ask</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Upload/>} />
          <Route path="/ask" element={<Ask/>} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')).render(<App />)

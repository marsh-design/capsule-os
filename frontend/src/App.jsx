import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import QuarterSetup from './pages/QuarterSetup'
import CapsuleOutput from './pages/CapsuleOutput'
import ItemScanner from './pages/ItemScanner'
import Layout from './components/Layout'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<QuarterSetup />} />
          <Route path="/capsule" element={<CapsuleOutput />} />
          <Route path="/scanner" element={<ItemScanner />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

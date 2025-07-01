import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './style.css';
import Sidebar from './Sidebar';
import WelcomeSection from './WelcomeSection';
import ChartsSection from './ChartsSection';
import PortfolioValuesSection from './PortfolioValuesSection';
import OpenPositionsSection from './OpenPositionsSection';
import ClosedPositionsSection from './ClosedPositionsSection';
import AddTransactionSection from './AddTransactionSection';

function App() {
  return (
    <Router basename="/app">
      <div className="container">
        <Sidebar />
        <div className="content-area">
          <h1>My Portfolio Dashboard</h1>
          <Routes>
            <Route path="/" element={<WelcomeSection />} />
            <Route path="/charts" element={<ChartsSection />} />
            <Route path="/portfolio-values" element={<PortfolioValuesSection />} />
            <Route path="/open-positions" element={<OpenPositionsSection />} />
            <Route path="/closed-positions" element={<ClosedPositionsSection />} />
            <Route path="/add-transaction" element={<AddTransactionSection />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
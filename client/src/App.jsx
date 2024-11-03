import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './assets/components/Navbar';
import FilterSearch from './assets/components/FilterSearch';
import LodgesGrid from './assets/components/LodgesGrid';
import LodgeDetail from './assets/components/LodgeDetail';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<><FilterSearch /><LodgesGrid /></>} />
          <Route path="/lodge/:id" element={<LodgeDetail />} />
        </Routes>
      </div>
    </Router>
  );
}


export default App;

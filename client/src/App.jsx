import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Navbar from './assets/components/Navbar';
import FilterSearch from './assets/components/FilterSearch';
import LodgesGrid from './assets/components/LodgesGrid';
import LodgeDetail from './assets/components/LodgeDetail';
import Footer from './assets/components/Footer';
import About from './assets/components/About';
import Contact from './assets/components/Contact';

function App() {
  const [filteredLodges, setFilteredLodges] = useState([]);

  const handleApplyFilters = (lodges) => {
    setFilteredLodges(lodges); 
  };

  return (
    <Router>
      <Navbar />
      <div className="main-content">
        <Routes>
          <Route
            path="/"
            element={
              <>
                <FilterSearch applyFilters={handleApplyFilters} />
                <LodgesGrid filteredLodges={filteredLodges} />
              </>
            }
          />
          <Route path="/lodge/:id" element={<LodgeDetail />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </div>
      {!window.location.pathname.includes("/about") && <Footer />}
    </Router>
  );
}

export default App;

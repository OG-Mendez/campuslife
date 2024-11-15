// App.jsx
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './assets/components/Navbar';
import FilterSearch from './assets/components/FilterSearch';
import LodgesGrid from './assets/components/LodgesGrid';
import LodgeDetail from './assets/components/LodgeDetail';
import Footer from './assets/components/Footer';

function App() {
  const [filteredLodges, setFilteredLodges] = useState([]);

  const handleApplyFilters = (lodges) => {
    setFilteredLodges(lodges); // Set filtered lodges to pass into LodgesGrid
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
        </Routes>
      </div>
      <Footer />
    </Router>
  );
}

export default App;

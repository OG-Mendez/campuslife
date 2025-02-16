import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import Navbar from './assets/components/Navbar/Navbar';
import FilterSearch from './assets/components/FilterSearch/FilterSearch';
import LodgesGrid from './assets/components/Lodge Grid/LodgesGrid';
import LodgeDetail from './assets/components/LodgeDetail/LodgeDetail';
import Footer from './assets/components/Footer/Footer';
import About from './assets/components/About Us/About';
import Contact from './assets/components/Contact/Contact';
import Login from './assets/components/Login/Login';
import Signup from './assets/components/Login/Signup';
import Logout from './assets/components/Login/Logout';
import { UserProvider } from './assets/components/Context/UserContext';
import ForgotPassword from './assets/components/Login/ForgottenPassword';
import MapComponent from './assets/components/Map/Map';
import { trackPageView } from './assets/components/G-Analytics';

function App() {
  const [filteredLodges, setFilteredLodges] = useState([]);
  const location = useLocation();

  const handleApplyFilters = (lodges) => {
    setFilteredLodges(lodges);
  };

  useEffect(() => {
    trackPageView(location.pathname);
  }, [location]);

  // Check if the current path is login, signup, or forgot-password
  const hideFooterPaths = ['/login', '/signup', '/forgot-password', '/map'];

  return (
    <UserProvider>
      <div>
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
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/map" element={<MapComponent />} />
          </Routes>
        </div>
        {/* Conditionally render Footer based on the current path */}
        {!hideFooterPaths.includes(location.pathname) && <Footer />}
      </div>
    </UserProvider>
  );
}

function AppWithRouter() {
  return (
    <Router>
      <App />
    </Router>
  );
}

export default AppWithRouter;

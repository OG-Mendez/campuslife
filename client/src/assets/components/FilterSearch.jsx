import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FilterModal from './FilterModal';
import './FilterSearch.css';

const FilterSearch = ({ applyFilters }) => {
  const [showModal, setShowModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [filteredLodges, setFilteredLodges] = useState([]);
  const [loading, setLoading] = useState(false);
  const [vacancy, setVacancy] = useState("Any");
  const [location, setLocation] = useState("Any");
  const [price, setPrice] = useState([60000, 600000]);
  const [debounceTimeout, setDebounceTimeout] = useState(null);
  const [showNoResultsPopup, setShowNoResultsPopup] = useState(false);
  const navigate = useNavigate();

  const handleShow = () => setShowModal(true);
  const handleClose = () => setShowModal(false);

  const handleSearch = async (searchTerm) => {
    setLoading(true);
    try {
      const response = await fetch('https://campuslife-c9je.onrender.com/api/pictures/');
      if (!response.ok) throw new Error('Failed to fetch suggestions');

      const lodges = await response.json();
      const filteredBySearch = lodges.filter((lodge) =>
        lodge.lodge_name.toLowerCase().includes(searchTerm.toLowerCase())
      );

      setSuggestions(filteredBySearch);
      setFilteredLodges(filteredBySearch);
    } catch (error) {
      console.error('Error fetching lodges:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterApply = async (vacancy, location, price) => {
    setLoading(true);
    try {
      const response = await fetch('https://campuslife-c9je.onrender.com/api/pictures/');
      if (!response.ok) throw new Error('Failed to fetch lodges');

      const lodges = await response.json();
      console.log("Fetched lodges from API:", lodges);

      const filteredByAll = lodges.filter((lodge) => {
        const lodgePrice = parseInt(lodge.lodge_price.replace(/,/g, ''), 10); // Parse price
        const isVacant = lodge.available_vacancy > 0 ? "Vacancy" : "No vacancy";

        const isVacancyMatch = vacancy === "Any" || isVacant === vacancy;
        const isLocationMatch = location === "Any" || lodge.lodge_location === location;
        const isPriceMatch = lodgePrice >= price[0] && lodgePrice <= price[1];

        
        console.log({
          lodgeName: lodge.lodge_name,
          lodgePrice,
          lodgeVacancy: isVacant,
          lodgeLocation: lodge.lodge_location,
          isVacancyMatch,
          isLocationMatch,
          isPriceMatch,
          included: isVacancyMatch && isLocationMatch && isPriceMatch,
        });

        return isVacancyMatch && isLocationMatch && isPriceMatch;
      });

      console.log("Filtered lodges:", filteredByAll);
      setFilteredLodges(filteredByAll);
      applyFilters(filteredByAll);

      if (filteredByAll.length === 0) {
        setShowNoResultsPopup(true);
      }
    } catch (error) {
      console.error('Error applying filters:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setSearchTerm(value);

    if (debounceTimeout) {
      clearTimeout(debounceTimeout);
    }

    const newTimeout = setTimeout(() => {
      if (value) {
        handleSearch(value);
      } else {
        setSuggestions([]);
      }
    }, 500);

    setDebounceTimeout(newTimeout);
  };

  const handleClosePopup = () => setShowNoResultsPopup(false);

  const handleApplyFilters = ({ vacancy, location, price }) => {
    console.log("Filters received from modal:", { vacancy, location, price });
    setVacancy(vacancy);
    setLocation(location);
    setPrice(price);
    handleFilterApply(vacancy, location, price);
  };

  return (
    <div className="filter-search-container">
      <button className="filter-button" onClick={handleShow}>
        <span className="filter-icon">
          <img
            src="/filterlogo.svg"
            alt=""
            width="15"
            height="18"
            className="d-inline-block align-text-top"
          />
        </span>
        Filter display
      </button>

      <form className="search-container" onSubmit={(e) => e.preventDefault()}>
        <input
          type="text"
          placeholder="Search for lodge"
          className="search-input"
          value={searchTerm}
          onChange={handleInputChange}
        />
        <button
          type="button"
          className="search-button"
          onClick={() => handleSearch(searchTerm)}
        >
          Search
        </button>

        {searchTerm && suggestions.length > 0 && (
          <ul className="search-dropdown">
            {suggestions.slice(0, 10).map((lodge) => (
              <li
                key={lodge.id}
                className="search-item"
                onClick={() => navigate(`/lodge/${lodge.id}`)}
              >
                <p>{lodge.lodge_name}</p>
              </li>
            ))}
          </ul>
        )}

        {!loading && searchTerm && suggestions.length === 0 && (
          <ul className="search-dropdown">
            <li className="no-results">No results found</li>
          </ul>
        )}
      </form>

      <FilterModal show={showModal} handleClose={handleClose} applyFilters={handleApplyFilters} />
      
      {showNoResultsPopup && (
        <div className="popup-container">
          <div className="popup">
            <p>No lodges found matching the criteria.</p>
            <button onClick={handleClosePopup} className="popup-close-button">
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterSearch;

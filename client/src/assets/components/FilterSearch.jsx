import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import FilterModal from './FilterModal';
import './FilterSearch.css';

const FilterSearch = () => {
  const [showModal, setShowModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [filteredLodges, setFilteredLodges] = useState([]); // State for filtered lodges
  const [loading, setLoading] = useState(false);
  const [vacancy, setVacancy] = useState("Any");
  const [location, setLocation] = useState("Any");
  const [price, setPrice] = useState([60000, 260000]); // Initial price range
  const [debounceTimeout, setDebounceTimeout] = useState(null);
  const navigate = useNavigate();

  const handleShow = () => setShowModal(true);
  const handleClose = () => setShowModal(false);

  // Function to fetch and filter the lodges based on the search term and filters
  const handleSearch = async (term) => {
    setLoading(true);
    try {
      const response = await fetch(`https://campuslife-c9je.onrender.com/api/pictures/`);
      if (!response.ok) throw new Error('Failed to fetch suggestions');
      
      const lodges = await response.json();
      console.log('Fetched Lodges:', lodges);

      // First filter by search term
      const filteredBySearch = lodges.filter((lodge) =>
        lodge.lodge_name.toLowerCase().includes(term.toLowerCase())
      );

      // Apply additional filters for vacancy, location, and price range
      const filteredByAll = filteredBySearch.filter((lodge) => {
        const isVacancyMatch = vacancy === "Any" || lodge.available_vacancy === vacancy;
        const isLocationMatch = location === "Any" || lodge.lodge_location === location;
        const isPriceMatch = lodge.lodge_price >= price[0] && lodge.lodge_price <= price[1];
        return isVacancyMatch && isLocationMatch && isPriceMatch;
      });

      setSuggestions(filteredByAll);
      setFilteredLodges(filteredByAll); // Update the filtered lodges list
    } catch (error) {
      console.error('Error fetching lodges:', error);
    } finally {
      setLoading(false);
    }
  };

  // Handle input change with debounce to prevent too many API calls
  const handleInputChange = (e) => {
    const value = e.target.value;
    setSearchTerm(value);

    // Clear previous debounce timeout
    if (debounceTimeout) {
      clearTimeout(debounceTimeout);
    }

    // Set a new debounce timeout
    const newTimeout = setTimeout(() => {
      if (value) {
        handleSearch(value); // Call search function after debounce delay
      } else {
        setSuggestions([]); // Clear suggestions if input is empty
      }
    }, 500); // 500ms delay before calling the search function

    setDebounceTimeout(newTimeout); // Store the timeout ID
  };

  // Function to apply filters from the FilterModal
  const applyFilters = ({ vacancy, location, price }) => {
    setVacancy(vacancy);
    setLocation(location);
    setPrice(price);
    handleSearch(searchTerm); // Reapply the search with the selected filters
  };

  return (
    <div className="filter-search-container">
      <button className="filter-button" onClick={handleShow}>
        <span className="filter-icon">
          <img
            src="./filterlogo.svg"
            alt=""
            width="20"
            height="25"
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
          onClick={() => handleSearch(searchTerm)} // Trigger search on button click
        >
          Search
        </button>

        {/* Conditionally render the dropdown only when there's a search term and suggestions */}
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

      <FilterModal show={showModal} handleClose={handleClose} applyFilters={applyFilters} />
    </div>
  );
};

export default FilterSearch;

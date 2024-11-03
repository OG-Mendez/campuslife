import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import FilterModal from './FilterModal';
import './FilterSearch.css';

const FilterSearch = () => {
  const [showModal, setShowModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleShow = () => setShowModal(true);
  const handleClose = () => setShowModal(false);

  const applyFilters = (filters) => {
    console.log('Filters applied:', filters);
  };

  const handleSearch = async () => {
    if (searchTerm.trim() === '') {
      setSuggestions([]);
      return;
    }
    setLoading(true);
    try {
      const response = await fetch(`https://campuslife-c9je.onrender.com/api/pictures/`);
      if (!response.ok) throw new Error('Failed to fetch suggestions');
      const lodges = await response.json();

      // Filter lodges based on the search term and limit to 3 suggestions
      const filteredLodges = lodges
        .filter((lodge) => lodge.lodge_name.toLowerCase().includes(searchTerm.toLowerCase()))
        .slice(0, 3); // Limit to 3 suggestions

      setSuggestions(filteredLodges);
    } catch (error) {
      console.error('Error fetching lodges:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (id) => {
    navigate(`/lodge/${id}`); // Navigate to the lodge detail page by ID
  };

  useEffect(() => {
    if (searchTerm) {
      handleSearch();
    } else {
      setSuggestions([]); // Clear suggestions when search term is empty
    }
  }, [searchTerm]);

  return (
    <div className="filter-search-container">
      <button className="filter-button" onClick={handleShow}>
        <span className="filter-icon"></span>
        Filter display
      </button>

      <div className="search-container">
        <input
          type="text"
          placeholder="Search for lodge"
          className="search-input"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button className="search-button" onClick={handleSearch}>Search</button>

        {suggestions.length > 0 && (
          <ul className="dropdown-menu">
            {suggestions.map((lodge) => (
              <li
                key={lodge.id}
                className="dropdown-item"
                onClick={() => handleSuggestionClick(lodge.id)}
              >
                {lodge.lodge_name}
              </li>
            ))}
          </ul>
        )}
      </div>

      <FilterModal
        show={showModal}
        handleClose={handleClose}
        applyFilters={applyFilters}
      />
    </div>
  );
};

export default FilterSearch;

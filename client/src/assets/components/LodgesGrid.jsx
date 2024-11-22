import React, { useEffect, useState } from 'react';
import LodgeCard from './LodgeCard';
import './LodgesGrid.css';

const LodgesGrid = ({ filteredLodges }) => {
  const [lodges, setLodges] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const lodgesPerPage = 12;

  useEffect(() => {
    if (filteredLodges && filteredLodges.length > 0) {
      setLodges(filteredLodges); 
      setIsLoading(false);
    } else {
      const fetchLodges = async () => {
        setIsLoading(true);
        try {
          const response = await fetch('https://campuslife-c9je.onrender.com/api/pictures/');
          if (!response.ok) throw new Error('Network response was not ok');
          
          const data = await response.json();
          setLodges(data);
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          setIsLoading(false);
        }
      };
      fetchLodges();
    }
  }, [filteredLodges]);

  const indexOfLastLodge = currentPage * lodgesPerPage;
  const indexOfFirstLodge = indexOfLastLodge - lodgesPerPage;
  const currentLodges = lodges.slice(indexOfFirstLodge, indexOfLastLodge);

  const handleNextPage = () => {
    if (indexOfLastLodge < lodges.length) {
      setCurrentPage((prevPage) => prevPage + 1);
      window.scrollTo(0, 0);  // Scroll to the top of the page
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage((prevPage) => prevPage - 1);
      window.scrollTo(0, 0);  // Scroll to the top of the page
    }
  };

  return (
    <div className="lodges-grid">
      {isLoading ? (
        Array.from({ length: lodgesPerPage }).map((_, index) => (
          <div key={index} className="lodge-card-skeleton">
            <div className="skeleton-image skeleton"></div>
            <div className="skeleton-text skeleton"></div>
            <div className="skeleton-text skeleton" style={{ width: '60%' }}></div>
          </div>
        ))
      ) : (
        currentLodges.map((lodge) => (
          <LodgeCard key={lodge.id} lodge={lodge} />
        ))
      )}

      <div className="pagination-buttons">
        {!isLoading && currentPage > 1 && (
          <button onClick={handlePreviousPage} className="prev-button">
            Previous
          </button>
        )}
        {!isLoading && indexOfLastLodge < lodges.length && (
          <button onClick={handleNextPage} className="next-button">
            Next
          </button>
        )}
      </div>
    </div>
  );
};

export default LodgesGrid;

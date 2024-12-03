import React, { useEffect, useState } from 'react';
import LodgeCard from './LodgeCard';
import { useLocation, useNavigate } from 'react-router-dom';
import './LodgesGrid.css';

const LodgesGrid = ({ filteredLodges }) => {
  const [lodges, setLodges] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const lodgesPerPage = 12;

  const location = useLocation();
  const navigate = useNavigate();

  // Extract page number from the query string
  const queryParams = new URLSearchParams(location.search);
  const initialPage = parseInt(queryParams.get('page'), 10) || 1;

  const [currentPage, setCurrentPage] = useState(initialPage);

  // Sync `currentPage` with the query string
  useEffect(() => {
    const page = parseInt(queryParams.get('page'), 10);
    if (page && page !== currentPage) {
      setCurrentPage(page);
    }
  }, [queryParams, currentPage]);

  // Fetch lodges
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
          console.error('Error fetching lodges:', error);
        } finally {
          setIsLoading(false);
        }
      };
      fetchLodges();
    }
  }, [filteredLodges]);

  // Paginate lodges
  const indexOfLastLodge = currentPage * lodgesPerPage;
  const indexOfFirstLodge = indexOfLastLodge - lodgesPerPage;
  const currentLodges = lodges.slice(indexOfFirstLodge, indexOfLastLodge);

  // Handle page changes
  const handlePageChange = (page) => {
    setCurrentPage(page);
    navigate(`?page=${page}`);
    window.scrollTo(0, 0);
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
        currentLodges.map((lodge) => <LodgeCard key={lodge.id} lodge={lodge} />)
      )}

      <div className="pagination-buttons">
        {!isLoading && currentPage > 1 && (
          <button onClick={() => handlePageChange(currentPage - 1)} className="prev-button">
            Previous
          </button>
        )}
        {!isLoading && indexOfLastLodge < lodges.length && (
          <button onClick={() => handlePageChange(currentPage + 1)} className="next-button">
            Next
          </button>
        )}
      </div>
    </div>
  );
};

export default LodgesGrid;

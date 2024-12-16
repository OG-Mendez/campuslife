import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import 'react-lazy-load-image-component/src/effects/blur.css';
import './LodgeDetail.css';

const LodgeDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [lodge, setLodge] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchLodge = async () => {
      console.log('Fetching lodge data...');
      try {
        const response = await fetch('https://campuslife-c9je.onrender.com/api/pictures/');
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        const selectedLodge = data.find((lodge) => lodge.id === parseInt(id)); 
        if (!selectedLodge) throw new Error('Lodge not found');
        //I added this code to clean the url because it has refused to clean from the backend
        if (selectedLodge?.image) {
  const prefix = 'image/upload/';
  if (selectedLodge.image.startsWith(prefix)) {
    selectedLodge.image = `https://res.cloudinary.com/dem4ececb/${selectedLodge.image}`;
  }
    }
        setLodge(selectedLodge);
      } catch (error) {
        console.error('Error fetching lodge details:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchLodge();
  }, [id]);

  const handleBack = () => {
    navigate(`/${location.search}`);
  };

  return (
    <div className="lodge-detail">
      {isLoading ? (
        <div className="skeleton-content">
          <div className="skeleton-image1 skeleton1"></div>
          <div className="skeleton-text1 skeleton1" style={{ width: '50%' }}></div>
          <div className="skeleton-text1 skeleton1" style={{ width: '80%' }}></div>
          <div className="skeleton-text1 skeleton1" style={{ width: '60%' }}></div>
          <div className="skeleton-text1 skeleton1" style={{ width: '40%' }}></div>
        </div>
      ) : (
        <>
          <div className="lodge-image-carousel">
            <img
              src={lodge.image || 'https://via.placeholder.com/150'}
              alt={lodge.lodge_name || 'Lodge'}
            />
            <div className="lodge-detail-h4">
              <h4>{lodge.lodge_name || 'Unknown Lodge'}</h4>
            </div>
          </div>
          <div className="lodge-info">
            <div className="lodge-info-item">
              <p>Vacancy</p>
              <strong>
                {lodge.available_vacancy === 1? '1 room' : lodge.available_vacancy > 1 ? `${lodge.available_vacancy} rooms` : 'No Vacancy'}
              </strong>
            </div>
            <div className="lodge-info-item">
              <p>Location</p>
              <strong>{lodge.lodge_location || 'Unknown'}</strong>
            </div>
            <div className="lodge-info-item">
              <p>Price</p>
              <strong>{lodge.lodge_price ? `₦${lodge.lodge_price}` : 'Price Unavailable'}</strong>
            </div>
            <div className="lodge-info-item-cn">
              <p>Caretaker's number</p>
              <strong>{lodge.caretaker_number || 'Not available'}</strong>
            </div>
            <p className="disclaimer">
              Disclaimer : Campuslife Technologies does not collect any payments and is not
              responsible for any loss. Please, go to the lodge, and ensure to meet the Caretaker in
              person before proceeding with any payment. Thank you!
            </p>
          </div>
        </>
      )}
    </div>
  );
};

export default LodgeDetail;

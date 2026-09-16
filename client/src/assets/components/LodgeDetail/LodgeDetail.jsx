import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import 'react-lazy-load-image-component/src/effects/blur.css';
import './LodgeDetail.css';
import ReviewSection from '../Review/ReviewSection';
import AverageRating from '../Review/AverageRating';
import { API_BASE_URL } from '../../../config/api';

const LodgeDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [lodge, setLodge] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchLodge = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/pictures/`);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        const selectedLodge = data.find((lodge) => lodge.id === parseInt(id));
        if (!selectedLodge) throw new Error('Lodge not found');

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
        <div className="details-container">
          {/* Layer 1: Lodge Image and Info */}
          <div className="details-layer1">
            <div className="lodge-image-carousel">
            <h2 className="lodge-name">{lodge.lodge_name || 'Unknown Lodge'}</h2>
              <img
                src={lodge.image || 'https://via.placeholder.com/150'}
                alt={lodge.lodge_name || 'Lodge'}
              />
            </div>
            <div className="lodge-info">
              <div className="lodge-info-item">
                <p>Vacancy</p>
                <strong>
                  {lodge.available_vacancy === 1
                    ? '1 room'
                    : lodge.available_vacancy > 1
                    ? `${lodge.available_vacancy} rooms`
                    : 'No Vacancy'}
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
              <div className="lodge-info-item">
                <p>Caretaker's number</p>
                <strong>{lodge.caretaker_number || 'Not available'}</strong>
              </div>
              
              <div className="average-rating1">
              <AverageRating lodgeId={id} />
              </div>
              
            </div>
          </div>
          <p className="disclaimer">
              Disclaimer: Campuslife Technologies does not collect any payments and is not
              responsible for any loss. Please visit the lodge and meet the caretaker in person
              before proceeding with any payment. Thank you!
            </p>
            <div className='details-layer2'> <ReviewSection /></div>
           
        </div>
      )}
    </div>
  );
};

export default LodgeDetail;

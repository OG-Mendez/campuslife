import React, { useState } from 'react';
import { FaStar } from 'react-icons/fa';
import { useParams } from 'react-router-dom';
import GetSection from './LikeDislikeButton';
import './ReviewSection.css';
import { API_BASE_URL } from '../../../config/api';

function ReviewSection() {
  const { id: lodgeId } = useParams(); 
  const [currentValue, setCurrentValue] = useState(0);
  const [hoverValue, setHoverValue] = useState(undefined);
  const [reviewText, setReviewText] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const stars = Array(5).fill(0);

  const handleClick = (value) => {
    setCurrentValue(value);
  };

  const handleMouseOver = (newHoverValue) => {
    setHoverValue(newHoverValue);
  };

  const handleMouseLeave = () => {
    setHoverValue(undefined);
  };

  const handleReviewChange = (e) => {
    setReviewText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const token = localStorage.getItem('token'); // Retrieve the token from localStorage
    if (!token) {
      setError('You must be logged in to submit a review.');
      console.error('No token found in localStorage.');
      return;
    }

    if (reviewText.trim() && currentValue === 0) {
      setError('Please provide a rating if submitting a review.');
      return;
    }

    if (!reviewText.trim() && currentValue === 0) {
      setError('You must provide a rating or a review.');
      return;
    }

    setIsSubmitting(true);

    try {
      const payload = {
        id: lodgeId,
        rating: currentValue,
        review_text: reviewText.trim() || " ", // Send null if no review text
      };

      console.log('Sending payload:', payload);

      const response = await fetch(`${API_BASE_URL}/create_review/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Error submitting review:', errorData);
        setError(errorData.detail || 'Failed to submit review. Please try again.');
        return;
      }

      setSuccess('Review submitted successfully!');
      setReviewText('');
    } catch (error) {
      console.error('Error submitting review:', error);
      setError('An error occurred while submitting your review. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="main-review">
      <div className="review-container">
        <h2>Rate this Lodge</h2>
        <p>Let others know what you think of this lodge</p>

        <div className="stars-container">
          {stars.map((_, index) => (
            <FaStar
              key={index}
              size={24}
              onClick={() => handleClick(index + 1)}
              onMouseOver={() => handleMouseOver(index + 1)}
              onMouseLeave={handleMouseLeave}
              color={(hoverValue || currentValue) > index ? '#FFBA5A' : '#a9a9a9'}
              style={{ marginRight: 10, cursor: 'pointer' }}
            />
          ))}
        </div>

        <h2 className="Wr">Write a review</h2>
        <p>
          Reviews will be displayed publicly on this <br />
          lodge’s details page. Please ensure to write <br />
          an honest review to help students make informed <br />
          decisions.
        </p>
        <textarea
          placeholder="What's your experience?"
          value={reviewText}
          onChange={handleReviewChange}
          className="review-textarea"
        />

        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}

        <button
          className="submit-button"
          onClick={handleSubmit}
          disabled={isSubmitting || (reviewText.trim() === '' && currentValue === 0)}
        >
          {isSubmitting ? 'Submitting...' : 'Submit Review'}
        </button>
      </div>

      <div className="get-container">
        <GetSection />
      </div>
    </div>
  );
}

export default ReviewSection;

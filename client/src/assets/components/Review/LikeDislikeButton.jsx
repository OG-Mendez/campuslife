import React, { useState, useEffect } from 'react';
import { FaThumbsUp, FaThumbsDown } from 'react-icons/fa';
import { useParams } from 'react-router-dom';
import './LikeDislikeButton.css';
import { API_BASE_URL } from '../../../config/api';

const GetSection = () => {
  const { id: lodgeId } = useParams(); // Numeric lodge ID
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/reviews/`);
        if (!response.ok) {
          throw new Error('Failed to fetch reviews.');
        }
        const data = await response.json();
        console.log('Fetched reviews:', data); // Debugging

        // Filter reviews by lodge_id
        const lodgeReviews = data.filter((review) => review.lodge_id === parseInt(lodgeId, 10));
        setReviews(lodgeReviews);
      } catch (err) {
        console.error('Error fetching reviews:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchReviews();
  }, [lodgeId]);

  const handleLikeDislike = async (reviewId, index, action) => {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('You must be logged in to like or dislike a review.');
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/like_review/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify({ id: reviewId, action }), // Send the action
    });

    if (!response.ok) {
      const errorData = await response.text();
      console.error('Error response:', errorData);
      throw new Error('Failed to update review.');
    }

    // Update frontend state based on the action
    const updatedReviews = [...reviews];
    const currentReview = updatedReviews[index];

    if (action === 'like') {
      if (currentReview.user_like_status) {
        // User already liked, remove like
        currentReview.total_likes = Math.max(0, currentReview.total_likes - 1);
        currentReview.user_like_status = false;
      } else {
        // Add like, and if disliked previously, remove dislike
        currentReview.total_likes += 1;
        if (currentReview.user_dislike_status) {
          currentReview.total_dislikes = Math.max(0, currentReview.total_dislikes - 1);
          currentReview.user_dislike_status = false;
        }
        currentReview.user_like_status = true;
      }
    } else if (action === 'dislike') {
      if (currentReview.user_dislike_status) {
        // User already disliked, remove dislike
        currentReview.total_dislikes = Math.max(0, currentReview.total_dislikes - 1);
        currentReview.user_dislike_status = false;
      } else {
        // Add dislike, and if liked previously, remove like
        currentReview.total_dislikes += 1;
        if (currentReview.user_like_status) {
          currentReview.total_likes = Math.max(0, currentReview.total_likes - 1);
          currentReview.user_like_status = false;
        }
        currentReview.user_dislike_status = true;
      }
    }

    setReviews(updatedReviews);
  } catch (error) {
    console.error(`Error updating review (${action}):`, error);
    alert(error.message || 'An error occurred. Please try again.');
  }
};


  if (loading) {
    return <div>Loading reviews...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="review-container">
      <h2>Reviews</h2>
      {reviews.length === 0 ? (
        <p>No reviews available for this lodge.</p>
      ) : (
        reviews.map((review, index) => (
          <div key={review.id} className="review-card">
            <h2>{review.created_by}</h2>
            <p>{review.review}</p>
            <div className="review-actions">
              <button
                className="review-button"
                onClick={() => handleLikeDislike(review.id, index, 'like')}
              >
                <FaThumbsUp className={review.user_like_status ? 'liked-icon' : ''} /> {review.total_likes}
              </button>
              <button
                className="review-button"
                onClick={() => handleLikeDislike(review.id, index, 'dislike')}
              >
                <FaThumbsDown className={review.user_dislike_status ? 'disliked-icon' : ''} /> {review.total_dislikes}
              </button>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default GetSection;

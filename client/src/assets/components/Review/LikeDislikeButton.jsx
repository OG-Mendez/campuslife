import React, { useState, useEffect } from 'react';
import { FaThumbsUp, FaThumbsDown } from 'react-icons/fa';
import { useParams } from 'react-router-dom';
import './LikeDislikeButton.css';

const GetSection = () => {
  const { id: lodgeId } = useParams(); // Numeric lodge ID
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch('https://campuslife-c9je.onrender.com/api/reviews/');
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

    // Determine the current state of like/dislike for the user
    const currentReview = reviews[index];
    const currentLikeStatus = currentReview.user_like_status; // Assuming this is stored in the review data
    const currentDislikeStatus = currentReview.user_dislike_status; // Assuming this is stored in the review data

    let updatedAction = action;
    if (action === 'like') {
      if (currentLikeStatus) {
        updatedAction = 'none'; // User already liked, so remove the like
      } else if (currentDislikeStatus) {
        updatedAction = 'dislike'; // User disliked, so toggle to like
      }
    } else if (action === 'dislike') {
      if (currentDislikeStatus) {
        updatedAction = 'none'; // User already disliked, so remove the dislike
      } else if (currentLikeStatus) {
        updatedAction = 'like'; // User liked, so toggle to dislike
      }
    }

    try {
      const response = await fetch('https://campuslife-c9je.onrender.com/api/like_review/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({ id: reviewId, action: updatedAction }), // Update to use `id`
      });

      if (!response.ok) {
        const errorData = await response.text();
        console.error('Error response:', errorData);
        throw new Error('Failed to update review.');
      }

      const updatedReviews = [...reviews];
      if (updatedAction === 'like') {
        updatedReviews[index].total_likes += 1;
        updatedReviews[index].total_dislikes = Math.max(0, updatedReviews[index].total_dislikes - 1); // Remove dislike if toggled
      } else if (updatedAction === 'dislike') {
        updatedReviews[index].total_dislikes += 1;
        updatedReviews[index].total_likes = Math.max(0, updatedReviews[index].total_likes - 1); // Remove like if toggled
      } else {
        // If action is 'none', remove like or dislike
        if (currentLikeStatus) updatedReviews[index].total_likes = Math.max(0, updatedReviews[index].total_likes - 1);
        if (currentDislikeStatus) updatedReviews[index].total_dislikes = Math.max(0, updatedReviews[index].total_dislikes - 1);
      }

      updatedReviews[index].user_like_status = updatedAction === 'like'; // Track the user's action (like/dislike)
      updatedReviews[index].user_dislike_status = updatedAction === 'dislike'; // Track the user's action (dislike)

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

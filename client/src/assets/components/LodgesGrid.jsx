import React, { useEffect, useState } from 'react';
import LodgeCard from './LodgeCard';
import './LodgesGrid.css';

const LodgesGrid = () => {
  const [lodges, setLodges] = useState([]);

// const staticLodges = [
//   {
//     lodge_name: "Lodge 1",
//     lodge_location: "Location 1",
//     lodge_price: 1000,
//     image: "/path/to/image1.jpg",
//   },
//   {
//     lodge_name: "Lodge 2",
//     lodge_location: "Location 2",
//     lodge_price: 1200,
//     image: "/path/to/image2.jpg",
//   },

// ];

// return (
//   <div className="lodges-grid">
//     {staticLodges.map((lodge) => (
//       <LodgeCard key={lodge.lodge_name} lodge={lodge} />
//     ))}
//   </div>
// );


  useEffect(() => {
    const fetchLodges = async () => {
      try {
        const response = await fetch('https://campuslife-c9je.onrender.com/api/pictures/');
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        setLodges(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchLodges();
  }, []);

  return (
    <div className="lodges-grid">
      {lodges.map((lodge) => (
        <LodgeCard key={lodge.id} lodge={lodge} />
      ))}
    </div>
  );
};

export default LodgesGrid;

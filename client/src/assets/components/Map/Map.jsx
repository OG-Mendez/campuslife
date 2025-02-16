// import React, { useState, useEffect, useRef } from 'react';
// import Map, { Marker, NavigationControl, Source, Layer } from 'react-map-gl';
// import mapboxgl from 'mapbox-gl';
// import MapboxGeocoder from '@mapbox/mapbox-gl-geocoder';
// import 'mapbox-gl/dist/mapbox-gl.css';
// import './Map.css';

// const MapboxMap = ({ isAdmin = false }) => {
//   const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_API_KEY;
//   const mapRef = useRef(null);
//   const geocoderContainerRef = useRef(null);
  
//   const [userLocation, setUserLocation] = useState({
//     latitude: 5.3927,
//     longitude: 6.9861,
//     zoom: 14,
//   });
//   const [markers, setMarkers] = useState([]);
//   const [distance, setDistance] = useState(null);
  
//   useEffect(() => {
//     if (navigator.geolocation) {
//       navigator.geolocation.getCurrentPosition(
//         (position) => {
//           setUserLocation({
//             latitude: position.coords.latitude,
//             longitude: position.coords.longitude,
//             zoom: 14,
//           });
//         },
//         (error) => console.error('Error fetching location:', error)
//       );
//     }
//   }, []);
  
//   useEffect(() => {
//     if (mapRef.current && geocoderContainerRef.current) {
//       const geocoder = new MapboxGeocoder({
//         accessToken: MAPBOX_TOKEN,
//         mapboxgl: mapboxgl,
//         marker: false,
//       });

//       geocoder.on('result', (event) => {
//         const { geometry, text } = event.result;
//         setMarkers([...markers, {
//           id: Date.now(),
//           name: text,
//           latitude: geometry.coordinates[1],
//           longitude: geometry.coordinates[0],
//         }]);
//       });
      
//       geocoderContainerRef.current.innerHTML = '';
//       geocoderContainerRef.current.appendChild(geocoder.onAdd(mapRef.current.getMap()));
//     }
//   }, [mapRef.current]);
  
//   const handleMapClick = (event) => {
//     if (!isAdmin) return;
//     const [longitude, latitude] = event.lngLat;
//     setMarkers([...markers, { id: Date.now(), latitude, longitude }]);
//   };
  
//   const handleMarkerDragEnd = (event, id) => {
//     if (!isAdmin) return;
//     const [longitude, latitude] = event.lngLat;
//     setMarkers(markers.map((marker) => marker.id === id ? { ...marker, latitude, longitude } : marker));
//   };

//   const calculateDistance = () => {
//     if (markers.length < 2) return;
//     const [marker1, marker2] = markers;
//     const R = 6371; // Radius of Earth in km
//     const dLat = (marker2.latitude - marker1.latitude) * (Math.PI / 180);
//     const dLon = (marker2.longitude - marker1.longitude) * (Math.PI / 180);
//     const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(marker1.latitude * (Math.PI / 180)) * Math.cos(marker2.latitude * (Math.PI / 180)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
//     const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
//     setDistance(R * c);
//   };
  
//   const resetMap = () => {
//     setMarkers([]);
//     setDistance(null);
//   };
  
//   return (
//     <div className="map-container">
//       <div className="geocoder-container" ref={geocoderContainerRef}></div>
//       <Map
//         {...userLocation}
//         onMove={(event) => setUserLocation(event.viewState)}
//         style={{ width: '100%', height: '100%' }}
//         mapStyle="mapbox://styles/mapbox/streets-v11"
//         mapboxAccessToken={MAPBOX_TOKEN}
//         onClick={handleMapClick}
//         ref={mapRef}
//       >
//         <NavigationControl position="top-right" />
//         {markers.map((marker) => (
//           <Marker
//             key={marker.id}
//             latitude={marker.latitude}
//             longitude={marker.longitude}
//             draggable={isAdmin}
//             onDragEnd={(event) => handleMarkerDragEnd(event, marker.id)}
//           />
//         ))}
//       </Map>
//       <div className="controls">
//         {markers.length >= 2 && <button onClick={calculateDistance}>Calculate Distance</button>}
//         <button onClick={resetMap}>Cancel</button>
//         {distance && <p>Distance: {distance.toFixed(2)} km</p>}
//       </div>
//     </div>
//   );
// };

// export default MapboxMap;



// Ensure framer-motion is installed:
// Run: npm install framer-motion

import React from 'react';
import { motion } from 'framer-motion';

export default function MapComponent() {
  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-100 p-6 rounded-lg shadow-lg border-4 border-transparent animate-border-rainbow">
      <motion.div
        initial={{ opacity: 0, y: 0 }}
        animate={{ opacity: 1, y: 400 }}
        
        transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
        className="text-center"
      >
        <h1 className="text-4xl font-bold text-gray-800 mb-4 animate-pulse">
          🚧 Map Is Coming Soon 🚧
        </h1>
        <p className="text-lg text-gray-600">
          We're working hard to bring this feature to life. Stay tuned!
        </p>
      </motion.div>

      <style>{`
        @keyframes border-rainbow {
          0% { border-color: rgb(255, 0, 0); }
          25% { border-color: rgb(0, 255, 0); }
          50% { border-color: rgb(0, 0, 255); }
          75% { border-color: rgb(255, 255, 0); }
          100% { border-color: rgb(255, 0, 0); }
        }
        .animate-border-rainbow {
          animation: border-rainbow 4s linear infinite;
        }
      `}</style>
    </div>
  );
}

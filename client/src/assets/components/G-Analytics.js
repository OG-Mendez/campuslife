// src/analytics.js
import ReactGA from 'react-ga4';

const TRACKING_ID = 'G-42YTB69VZX';
ReactGA.initialize(TRACKING_ID);

export const trackPageView = (path) => {
  ReactGA.send({ hitType: "pageview", page: path });
};

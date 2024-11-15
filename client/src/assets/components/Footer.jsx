import React from "react";
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        
        <div className="footer-section">
            <div className="main-name">
            <img
            src="./logo.svg"
            alt="Logo"
            width="30"
            height="24"
            className="d-inline-block align-text-top"
          />
          <h4 className="title1">Campuslife Technologies</h4>
            </div>
        </div>

        <div className="footer-section">
          <ul className="footer-links">
            <li>
              <a href=" ">About us</a>
            </li>
            <li>
              <a href=" ">Contact us</a>
            </li>
            <li>
              <a href=" ">FAQs</a>
            </li>
            <li>
              <a href="./src/assets/components/LodgeGrid.jsx">Back To Top</a>
            </li>
          </ul>
        </div>

        <div className="footer-section">
        <div className="socials">
        <a href="https://www.linkedin.com/company/campuslife-technologies/">
            <img
              src="./linkedinlogo.svg"
              alt=""
              width="20"
              height="25"
              className="d-inline-block align-text-top"
            />
          </a>

          <a href="https://www.linkedin.com/company/campuslife-technologies/">
            <img
              src="./xlogo.svg"
              alt=""
              width="20"
              height="25"
              className="d-inline-block align-text-top"
            />
          </a>

          <a href="https://www.linkedin.com/company/campuslife-technologies/">
            <img
              src="./facebooklogo.svg"
              alt=""
              width="20"
              height="25"
              className="d-inline-block align-text-top"
            />
          </a>
        </div>
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; Campuslife Technology 2024</p>
      </div>
    </footer>
  );
};

export default Footer;

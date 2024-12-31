import React from "react";
import { Link } from "react-router-dom"; // Import Link for routing
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <div className="main-name">
          <a href="/">
            <img
              src="/logo.svg"
              alt="Logo"
              width="30"
              height="24"
              className="d-inline-block align-text-top"
            />
            </a>
            <h4 className="title1">Campuslife Technologies</h4>
          </div>
        </div>

        <div className="footer-section">
          <ul className="footer-links">
            <li>
              <Link to="/about">About us</Link>{" "}
              {/* Use Link component for navigation */}
            </li>
            <li>
            <Link to="/contact">Contact us</Link>{" "}
              {/* <a href="/contact ">Contact us</a> */}
            </li>
            <li>
              <a href=" ">FAQs</a>
            </li>
            <li>
              <a
                href="javascript:void(0)"
                onClick={() => window.scrollTo(0, 0)}
              >
                Back To Top
              </a>
            </li>
          </ul>
        </div>

        <div className="footer-section">
          <div className="socials">
            <a href="https://www.linkedin.com/company/campuslife-technologies/">
              <img
                src="/linkedinlogo.svg"
                alt=""
                width="20"
                height="25"
                className="d-inline-block align-text-top"
              />
            </a>

            <a href="">
              <img
                src="/xlogo.svg"
                alt=""
                width="20"
                height="25"
                className="d-inline-block align-text-top"
              />
            </a>

            <a href="https://www.facebook.com/profile.php?id=61568747010778&mibextid=ZbWKwL">
              <img
                src="/facebooklogo.svg"
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
        <p>&copy; Campuslife Technologies 2024</p>
      </div>
    </footer>
  );
};

export default Footer;

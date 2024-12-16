import react from "react";
import './Contact.css'

const Contact = () => {
    return(
        <div className="contact-page">
            <h2>Contact Information</h2>
            {/* <p> Leave us a message</p> */}
        <div>
        <img
              src="./location.svg"
              alt="Logo"
              width="30"
              height="24"
              className="d-inline-block align-text-top"
            />
            <p> Federal University Of Technology Owerri,Imo state.</p>
        </div>
        
        <div>
        <img
              src="./Mail.svg"
              alt="Logo"
              width="30"
              height="24"
              className="d-inline-block align-text-top"
            />
            <p> info@campuslifetechnologies.com.ng</p>
        </div>

        <div>
        <img
              src="./Phone.svg"
              alt="Logo"
              width="30"
              height="24"
              className="d-inline-block align-text-top"
            />
            <p>+234 903 417 7344 (WhatsApp)</p>
        </div>

        <div>
        <img
              src="./linkedinlogo.svg"
              alt="Logo"
              width="30"
              height="24"
              className="d-inline-block align-text-top"
            />
            <p>Campuslife Technologies</p>
        </div>

        <div>
        <img
              src="./facebooklogo.svg"
              alt="Logo"
              width="30"
              height="24"
              className="d-inline-block align-text-top"
            />
            <p>Campuslife Technologies</p>
        </div>

        </div>

    );
};

export default Contact;
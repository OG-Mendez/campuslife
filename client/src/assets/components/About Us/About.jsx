import React, { useEffect } from "react";
import './About.css';

const About = () => {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    return(
        <div className="about-page">
            <div className="about">
                <h1>We’re building <span className="diff">solutions </span>to the problems students face in <span className="diff">campus</span></h1>
                <p>We're a technology company focused on solving problems faced by students in campus. We believe that most of the non-academic problems plaguing students are just unnecessary and can be solved at scale with the use of technology, so, we decided to fill that gap.  Building solutions for students while they focus on their academics. it sounded like win-win to us and that's why we're here.</p>
                 <h1>Our <span className="diff">Vision</span ></h1>
                 <p>Here’s what we see - 10 years from now, life in campus would be so tightly integrated with technology that one wouldn’t be able to imagine it another way. Compare it to how technology has revolutionized payments in Nigeria.
                 We strongly believe that students would heavily depend on technology from admission through convocation to improve their experiences in campus. <br />  <br />We are positioning ourselves to be a leader in the technology that’ll will make this possible. That’s where we’re going!</p>
            </div>
            <div>
                <footer className="about-footer">
                    <div> <h1>Our <span className="diff">Team</span></h1></div>
                    <div className="about-card">
                    <div>
                        <a href="https://www.linkedin.com/in/michael-ezechukwu-ab5210223?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app">
                        <img src="/images/sheer.jpg" alt="Michael" />
                        <h4>Michael Ezechukwu</h4>
                        <p>Co-founder & CEO</p>
                        </a>
                    </div>
                    
                    <div>
                    <a href="https://www.linkedin.com/in/david-uchenna/">
                        <img src="/images/pdavid.jpeg" alt="" />
                        <h4>David Uchenna</h4>
                        <p>Co-founder & Backend Developer</p>
                        </a>
                    </div>

                    <div>
                    <a href="http://linkedin.com/in/jeremiah-chukwuemeka-902b13276">
                        <img src="/images/jeremie.jpg" alt="" />
                        <h4>Jeremiah Chukwuemeka</h4>
                        <p>Co-founder & Frontend Developer</p>
                        </a>
                    </div>
                    </div>
                    
                </footer>
            </div>
        </div>
    );
};

export default About;
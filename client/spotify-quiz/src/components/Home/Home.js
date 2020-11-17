import React from "react";
import "./Home.scss";

const Home = (props) => {
  return (
    <div className="Home">
      <nav>
        <img className="logo" src={require('./../../assets/rock-on.svg')} />
        <div className="navSignIn">
        <a href="#">Sign In</a>
        </div>
      </nav>
      <div className="header">
        <h1 className="title">
          <span className="highlight">rock</span>on
        </h1>
        <h2 className="description">
          Generate and share a personalized quiz to put your music taste to the
          test. Powered by Spotify<span className="rightsReserved">®</span>.
        </h2>
      </div>
      <div className="sectionBottom">
        <div className="center">
          <a href="#" className="heroButton">
            Generate Quiz
          </a>
        </div>
      </div>
    </div>
  );
};

export default Home;
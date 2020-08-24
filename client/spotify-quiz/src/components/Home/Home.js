import React from 'react';
import './Home.css';


const Home = (props) => {

    return (
      <div className="Home">
      <nav className="topnav">
        <ul>
          <li>
            <a href="#">
              <img src={require('./../../assets/newlogo.svg')} />
            </a>
          </li>
          <li className="top-sign-in">
            <a href="/dashboard">Sign in</a>
          </li>
        </ul>
      </nav>

<div className="backing">
  <section>
    <div class="center-wrapper">
      <div class="flex-container">
        <div class="flex-child right">
          <img src={require('./../../assets/demo.svg')}/>
        </div>
        <div class="flex-child left" id="wcsa-section">
          <div class="title-wrapper">
            <h1>Spot On</h1>
          </div>
          <div class="description-wrapper">
            <p>Who knows your listening habits the best? Quiz yourself. Quiz your friends.</p>
          </div>

          <div class="head-b-wrapper">
            <a class="head-b-generate-quiz" id="button-main" href="/quiz">Sign in with Spotify</a>
          </div>

        </div>
      </div>
    </div>
</section>
</div>
</div>

    );
}

export default Home;

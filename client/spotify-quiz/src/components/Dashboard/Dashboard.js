
import React from 'react';
import './Dashboard.css';
import './bubbles.css';
import TitleHeader from '../TitleHeader/TitleHeader';
import Share from '../Share/Share';
import Respondent from '../Respondent/Respondent';

let respondent = {
  imageSrc: 'https://cdn.pixabay.com/photo/2018/10/30/16/06/water-lily-3784022__340.jpg',
  imageAlt: 'icon #1',
  name: 'Ben Lapidus',
  score: '9/10',
  url: '#'
};

let respondents = [
respondent, respondent, 
respondent, respondent,
respondent, respondent,  
respondent, respondent
];


function Dashboard() {

	return (
	<div className="dashboard-wrapper">
  <nav className="topnav-dashboard">
        <ul>
          <li>
            <a href="#">
              <img src={require('./../../assets/newlogo.svg')} />
            </a>
          </li>
          <li className="top-sign-in">
            <a href="/dashboard">Start quiz</a>
          </li>
        </ul>
      </nav>

<div class="animation-area">
    <TitleHeader />
    <Share />

  <ul class="box-area">
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
    <li></li>
  </ul>
</div>


    <Respondent respondents={respondents}/>
    </div>
  );
}

export default Dashboard;


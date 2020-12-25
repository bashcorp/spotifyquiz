
import React from 'react';
import './Dashboard.css';
import './bubbles.css';
import TitleHeader from '../TitleHeader/TitleHeader';
import Layout from '../Dash/Layout/Layout';
import Share from '../Share/Share';

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
	<div className="dashboard">

   {/*<div class="animation-area">
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


 <Respondent respondents={respondents}/>*/}
    <Layout />
    </div>
  );
}

export default Dashboard;


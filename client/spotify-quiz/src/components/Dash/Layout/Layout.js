import React from "react";
import "./Layout.scss";
import CardContainer from "../CardContainer/CardContainer";
import RespondentContainer from "../RespondentContainer/RespondentContainer";
import RespondentItem from '../RespondentItem/RespondentItem';

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
respondent, respondent, 
respondent, respondent, 
respondent, respondent, 
respondent, respondent
];


function Layout() {
	return (
		<div className="layout-wrapper">
			<h1 className="headerText">Dashboard</h1>
			<div className="row">
				<div className="column left">
					<CardContainer />
				</div>
				<div className="verticalLine"/>
				<div class="column right">





				 <RespondentContainer respondents={respondents}/>
				</div>
			</div>
		</div>
	);
}

export default Layout;
import React from 'react';
import './RespondentItem.css';


const RespondentItem = (props) => {
	let {respondent} = props;
		return(
			<div className="RespondentItem">

				<div className="respondent-image">
					<img src={respondent.imageSrc} alt={respondent.imageAlt}/>
				</div>

				<div className="respondent-name">
					<h3>{respondent.name}</h3>
				</div>

				<div className="respondent-score">
					<h3>{respondent.score}</h3>
				</div>
				<div className="respondent-url">
				<a href={respondent.url}>Full results</a>
				<svg xmlns="http://www.w3.org/2000/svg"><path d="M8.122 24l-4.122-4 8-8-8-8 4.122-4 11.878 12z"/></svg>
				</div>
			</div>
			);
	}


export default RespondentItem;

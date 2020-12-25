import React from 'react';


const RespondentItem = (props) => {
	let {respondent} = props;
		return(
			<div className="RespondentItem">

				{/*<div className="respondent-image">
					<img src={respondent.imageSrc} alt={respondent.imageAlt}/>
				</div>*/}

				<div className="respondent-name">
					<h3>{respondent.name}</h3>
				</div>

				<div className="respondent-score">
					<h3>{respondent.score}</h3>
				</div>
				<div className="respondent-url">
				<a href={respondent.url}>Full results</a>
				</div>
			</div>
			);
	}


export default RespondentItem;

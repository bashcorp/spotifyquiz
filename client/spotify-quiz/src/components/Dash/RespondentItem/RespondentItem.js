import React from 'react';
import "./RespondentItem.scss";

const RespondentItem = (props) => {
	let {respondent} = props;

	 var well={
            boxShadow: "0px 0px 2px 2px " + respondent.background,
            backgroundColor: respondent.background
        }
		return(
			<div className="RespondentItem">
				
				<div className="respondent-image" style={well}>

				<a href={respondent.url}>
				<p className="center-emoji">{respondent.emoji}</p>
				{/*<img src={respondent.imageSrc} alt={respondent.imageAlt}/>*/}
				</a>
				</div>
				

				
				<div className="respondent-name">
				<a href={respondent.url}>
					<h3>{respondent.name}</h3>
					</a>
				</div>
				

				
				<div className="respondent-score">
				<a href={respondent.url}>
					<h3>{respondent.score}<span className="out-of-ten">/10</span></h3>
				</a>
				</div>
				
				
				
			</div>
			);
	}


export default RespondentItem;

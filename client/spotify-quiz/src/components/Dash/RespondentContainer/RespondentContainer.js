import React from "react";
import "./RespondentContainer.scss";
import RespondentItem from "../RespondentItem/RespondentItem";

const RespondentContainer = (props) => {
	return (
		<div className="respondent-container">
			<form onsubmit="event.preventDefault();" role="search">
				<label for="search">Search for stuff</label>
				<input
					id="search"
					type="search"
					placeholder="Filter respondents..."
					autofocus
				/>
				<button type="submit">Clear</button>
			</form>
			<ul className="respondent-list">
				{props.respondents.map((respondent) => {
					return (
						<li className="respondent">
							<RespondentItem respondent={respondent} />
						</li>
					);
				})}
			</ul>
		</div>
	);
};

export default RespondentContainer;
import React from "react";
import "./CardContainer.scss";

function CardContainer() {
	return (
		<div className="card-container-wrapper">
			<div className="child">my quiz</div>
			<div className="child">share</div>
			<div className="child">respondents</div>
			<div className="child">settings</div>
			<div className="child">overview</div>
		</div>
	);
}

export default CardContainer;
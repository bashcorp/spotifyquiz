import React from "react";
import "./Choice.scss";

let value = "";

const Choice = ({ choice }) => {

	const [selected, setSelected] = React.useState();

	/*const handleSelectionClick = (selection) => {
		setSelected(selection);
		updateFinalSubmission(selection.id);
	}

	const updateFinalSubmission = (id) => {
		sendData(id);
	}*/

	return (
		
	
						<div data-glide-dir=">" className="list-item shadow-4" onClick={e => document.getElementById("right-butt").click()}>
						<img id="choice-img" src="http://www.w3.org/2008/site/images/logo-w3c-screen-lg" alt="" />
							<div className="list-content">
								<h2 id="choice-header">{choice.primary_text}</h2>
								<hr id="choice-underline-mid"/>
								<p id="choice-subheader">
									{choice.secondary_text}
								</p>
							</div>
						</div>
					
						

					
	);
};
export default Choice;
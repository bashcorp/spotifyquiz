import React from "react";
import "./Choice.scss";

let value = "";

const Choice = ({ choice, index }) => {

	const [selected, setSelected] = React.useState();

	const bgImg = {
		  background: "url('https://jooinn.com/images1280_/square.jpg')",
		  backgroundSize: "cover",
		  backgroundRepeat: "no-repeat"
	};

	/*const handleSelectionClick = (selection) => {
		setSelected(selection);
		updateFinalSubmission(selection.id);
	}

	const updateFinalSubmission = (id) => {
		sendData(id);
	}*/

	return (
		
	  <div class="square">
	  		<div style={bgImg} id="choice__bgImg" />
    		<div class="content shadow-3">
						<div data-glide-dir=">" className="list-item" id={"question__choice_" + index} onClick={e => document.getElementById("right-butt").click()}>
							<div className="list-content">
								<h2 id="choice-header">{choice.primary_text}</h2>
								<p id="choice-subheader">
									{choice.secondary_text}
								</p>
							</div>
						</div>
						</div>
						</div>
					
						

					
	);
};
export default Choice;
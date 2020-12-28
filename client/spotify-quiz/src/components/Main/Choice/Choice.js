import React from "react";
import "./Choice.scss";

let value = "";

const Choice = (props) => {
	let { questions } = props;

	const [selected, setSelected] = React.useState();

	/*const handleSelectionClick = (selection) => {
		setSelected(selection);
		updateFinalSubmission(selection.id);
	}

	const updateFinalSubmission = (id) => {
		sendData(id);
	}*/

	return (
		<div className="Choice">
				<div className="choice-container">
					<ul class="list">
						{questions.map((curr, index) => (
						<div data-glide-dir=">" className="list-item shadow-4" key={index} onClick={e => document.getElementById("right-butt").click()}>
						<img id="choice-img" src="http://www.w3.org/2008/site/images/logo-w3c-screen-lg" alt="" />
							<div className="list-content">
								<h2 id="choice-header">{curr}</h2>
								<hr id="choice-underline-mid"/>
								<p id="choice-subheader">
									Thoughts and prayers - A COLORS SHOW
								</p>
							</div>
						</div>
					))}
						

					</ul>

					
				</div>
		</div>
	);
};
export default Choice;
import React from "react";
import "./Choice.scss";

let value = "";


function Choice(props) {

	const [selected, setSelected] = React.useState();
	
	const button__select = {
		  border: "5px solid #fff",
		  background: "url('https://jooinn.com/images1280_/square.jpg')",
		  backgroundSize: "cover",
		  backgroundRepeat: "no-repeat"
	};

	const button__unSelect = {
		  border: "0px solid #fff",
		  background: "url('https://jooinn.com/images1280_/square.jpg')",
		  backgroundSize: "cover",
		  backgroundRepeat: "no-repeat"
	};

	function handleChange(key) {
		console.log("HEllo: " + key)
        props.onChange(key);
    }

	/*const handleSelectionClick = (selection) => {
		setSelected(selection);
		updateFinalSubmission(selection.id);
	}

	const updateFinalSubmission = (id) => {
		sendData(id);
	}*/

	return (

		<div class="square" onClick={e => handleChange(props.choice.id)}>
    		<div className="content">
    			<div style={props.isSelected ? button__select : button__unSelect} id="choice__bgImg" />
				<div data-glide-dir=">" className="list-item" id={"question__choice_" + props.index} onClick={e => document.getElementById("right-butt").click()}>
					<div className="list-content">
						<h2 id="choice-header">{props.choice.primary_text}</h2>
						<p id="choice-subheader">{props.choice.secondary_text}</p>
					</div>
				</div>
			</div>
		</div>					
	);
};
export default Choice;
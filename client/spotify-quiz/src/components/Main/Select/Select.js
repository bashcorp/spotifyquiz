import React from "react";
import "./Select.scss";

let value = "";

function Select(props) {
	const [selected, setSelected] = React.useState();

	const button__select = {
		transform: "scale(104%)",
	};

	const button__unSelect = {
		filter: "brightness(60%)",
	};

	const bgImg__style = {
		 background: "url(props.choice.image_url)",
	};

	function handleChange(key, questionNumber) {
		props.onChange(key,questionNumber);
	}

	return (
		<div className="square" onClick={(e) => handleChange(props.choice.id, props.questionNumber)}>
			<div
				className="content"
				style={props.isSelected ? button__select : button__unSelect}
			>
				<div className="bgImg__style"id="choice__bgImg" />
				<div
					className="list-item"
					id={"question__choice_" + props.index}
				>
					<div className="list-content">
						<h2 id="choice-header">{props.choice.primary_text}</h2>
						<p id="choice-subheader">
							{props.choice.secondary_text}
						</p>
					</div>
				</div>
			</div>
		</div>
	);
}
export default Select;
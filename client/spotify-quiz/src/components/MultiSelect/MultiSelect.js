import React from "react"; //142
import "./MultiSelect.css";


const MultiSelect = (props) => {
	let { sendData, answers, questionIndex } = props;

	const [first, setFirst] = React.useState(false);
	const [second, setSecond] = React.useState(false);
	const [third, setThird] = React.useState(false);
	const [fourth, setFourth] = React.useState(false);
	const [selected, setSelected] = React.useState([]);

	const handleSelectionClick = (option) => {
		let tmpArr = [];

		if (selected.includes(option.id)){
			tmpArr = selected.filter(e => e !== option.id);
			setSelected(tmpArr);
		} else {
			tmpArr = selected.concat(option.id);
			setSelected(selected);
		}
		updateFinalSubmission();
	};

	const updateFinalSubmission = () => {
		sendData(selected);
	};

	const onSubmit = (e) => {
		e.preventDefault();
	};

	return (

		<div className="MultipleChoice">
			<form onSubmit={onSubmit}>
			<span className="MultipleSelect">Select all correct answers</span>

			<ul>
				 {answers.choices.map(option => (

					<li style={{ boxShadow: (selected.includes(option.id) ? '0 6px 14px 0 #454545' : ''),
								 transform: (selected.includes(option.id) ? 'scale(1.07)' : '')}}
								 key={option.id} count={option} onClick={() => handleSelectionClick(option)}>
						<span>{option.primary_text}</span>
						<span className="artist">{option.secondary_text}</span>
					</li>
					))}
				</ul>
			</form>
		</div>
	);
};
export default MultiSelect;
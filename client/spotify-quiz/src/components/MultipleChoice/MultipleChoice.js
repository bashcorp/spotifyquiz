import React from 'react'; //142
import './MultipleChoice.css';

let value = "";

const MultipleChoice = (props) => {
	let { sendData, answers, questionIndex } = props;

	console.log(questionIndex)

	console.log("Answers: " + answers);

	const [selected, setSelected] = React.useState();



	const handleSelectionClick = (selection) => {
		setSelected(selection);
		updateFinalSubmission(selection.id);
	}

	const updateFinalSubmission = (id) => {
		sendData(id);
	}

	const onSubmit = (e) => {
		e.preventDefault();
	}

	return (
		<div className="MultipleChoice">
			<form onSubmit={onSubmit}>
				<ul>
				 {answers.choices.map(option => (
					<li style={{ boxShadow: (option===selected ? '0 6px 14px 0 #454545' : ''),
								 transform: (option===selected ? 'scale(1.07)' : '')}}
								 key={option.id} count={option} onClick={() => handleSelectionClick(option)}>
						<span>{option.primary_text}</span>
						<span className="artist">{option.secondary_text}</span>
					</li>
					))}
				</ul>
			</form>
		</div>
	);
}
export default MultipleChoice;
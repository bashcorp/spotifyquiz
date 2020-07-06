import React from 'react'; //142
import './MultipleChoice.css';

let value = "";

const MultipleChoice = (props) => {
	let { sendData, answers, questionIndex } = props;

	console.log(questionIndex)

	const [selected, setSelected] = React.useState();
	const optionNumber = ["first?"+questionIndex, "second?"+questionIndex, "third?"+questionIndex, "fourth?"+questionIndex];



	const handleSelectionClick = (selection) => {
		setSelected(selection);
		updateFinalSubmission(selection.split('?')[0]);
	}

	const updateFinalSubmission = (name) => {
		switch(name) {
			case 'first':
				sendData(answers['first'].title); //TODO: Find out what Cash wants to recieve for answer
				return;
			case 'second':
				sendData(answers['second'].title);
				return;
			case 'third':
				sendData(answers['third'].title);
				return;
			case 'fourth':
				sendData(answers['fourth'].title);
				return;
			default:
			return 'Invalid response. (#001)'
		}
	}



	

	const onSubmit = (e) => {
		e.preventDefault();
	}

	return (
		<div className="MultipleChoice">
			<form onSubmit={onSubmit}>
				<ul>
				 {optionNumber.map(option => (
					<li style={{ boxShadow: (option===selected ? '0 6px 14px 0 #454545' : ''),
								 transform: (option===selected ? 'scale(1.07)' : '')}}
								 key={option} count={option} onClick={() => handleSelectionClick(option)}>
						<span>{answers[option.split('?')[0]].title}</span>
						<span className="artist">{answers[option.split('?')[0]].artist}</span>
					</li>
					))}
				</ul>
			</form>
		</div>
	);
}
export default MultipleChoice;
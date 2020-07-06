import React from "react"; //142
import "./MultiSelect.css";

const MultiSelect = (props) => {
	let { sendData, answers, questionIndex } = props;

	const [first, setFirst] = React.useState(false);
	const [second, setSecond] = React.useState(false);
	const [third, setThird] = React.useState(false);
	const [fourth, setFourth] = React.useState(false);

	const optionNumber = [
		"0?" + questionIndex,
		"1?" + questionIndex,
		"2?" + questionIndex,
		"3?" + questionIndex,
	];

	const handleSelectionClick = (selection) => {
		switch (selection){
			case "first":
				setFirst(!first);
				break;
			case "second":
				setSecond(!second);
				break;
			case "third":
				setThird(!third);
				break;
			case "fourth":
				setFourth(!fourth);
				break;
			default:
				break;
		}
		
		updateFinalSubmission();
	};

	const updateFinalSubmission = () => {
		

		sendData(answers['first'].title);
	};

	const onSubmit = (e) => {
		e.preventDefault();
	};

	return (
		<div className="MultipleChoice">
			<form onSubmit={onSubmit}>
			<span className="MultipleSelect">Select all correct answers</span>
				<ul>
					<li
						style={{
							boxShadow: first ? "0 6px 14px 0 #454545":"",
							transform: first ? "scale(1.07)":"",
						}}
						
						onClick={() =>
							handleSelectionClick("first")
						}
					>
						<span>
							{answers["first"].title}
						</span>
						<span className="artist">
							{answers["first"].artist}
						</span>
					</li>
					<li
						style={{
							boxShadow: second ? "0 6px 14px 0 #454545":"",
							transform: second ? "scale(1.07)":"",
						}}
						
						onClick={() =>
							handleSelectionClick("second")
						}
					>
						<span>
							{answers["second"].title}
						</span>
						<span className="artist">
							{answers["second"].artist}
						</span>
					</li>
					<li
						style={{
							boxShadow: third ? "0 6px 14px 0 #454545":"",
							transform: third ? "scale(1.07)":"",
						}}
						
						onClick={() =>
							handleSelectionClick("third")
						}
					>
						<span>
							{answers["third"].title}
						</span>
						<span className="artist">
							{answers["third"].artist}
						</span>
					</li>
					<li
						style={{
							boxShadow: fourth ? "0 6px 14px 0 #454545":"",
							transform: fourth ? "scale(1.07)":"",
						}}
						
						onClick={() =>
							handleSelectionClick("fourth")
						}
					>
						<span>
							{answers["fourth"].title}
						</span>
						<span className="artist">
							{answers["fourth"].artist}
						</span>
					</li>
				</ul>
			</form>
		</div>
	);
};
export default MultiSelect;
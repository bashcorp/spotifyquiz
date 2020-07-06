import React from 'react';
import './Question.css';

class Question extends React.Component {
	render() {
		return(
			<div className="Question">
			<h3>{this.props.question}</h3>
			</div>
			);
	}
}
export default Question;
import React from "react";
import "./Quiz.scss";
import Question from "../Question/Question.js";
import QuestionSlider from "../QuestionSlider/QuestionSlider.js";
import Glide from "@glidejs/glide";

const Quiz = () => {
	const [index, setIndex] = React.useState("1");

	var questions = {
		questions: [
			{ id: 0, text: "plan 0", price: 0 },
			{ id: 1, text: "plan 1", price: 1 },
			{ id: 2, text: "plan 2", price: 2 },
			{ id: 3, text: "plan 2", price: 3 },
			{ id: 4, text: "plan 2", price: 4 },
			{ id: 5, text: "plan 2", price: 5 },
			{ id: 6, text: "plan 2", price: 6 },
			{ id: 7, text: "plan 3", price: 7 },
		],
	};
	const handleSelection = (id) => {
		console.log("handleOffer clicked, id: ", id);
		setIndex(id + 2);
	};

	const carouselOptions = {
		type: "track",
		gap: 150,
		perView: 1,
		peek: 225,
		startAt: 0,
		animationDuration: 400,
		dragThreshold: false,
		breakpoints: {
			1200: {
				perView: 1,
				gap: 30,
				peek: 100,
			},
		},
	};

	return (

		<div className="Quiz">
		<p id="watermark-index">{index}</p>
		<div className="home-section test">

	
			<QuestionSlider options={carouselOptions}>
				{questions.questions.map((plan) => (
					<Question
						key={plan.id}
						plan={plan}
						handleOffer={handleSelection}
					/>
				))}
			</QuestionSlider>
		</div>
		</div>
	);
};
export default Quiz;
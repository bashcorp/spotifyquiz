import React from "react";
import "./Layout.scss";
import CardContainer from "../CardContainer/CardContainer";
import RespondentContainer from "../RespondentContainer/RespondentContainer";
import RespondentItem from "../RespondentItem/RespondentItem";

var emoji = ["😂", "😝", "😁", "😱", "🍆", "🥺"];
var names = [
	"Mary Jane",
	"Tim Apple",
	"John Snow",
	"Joe Biden",
	"Julianne Morrison",
	"Michael Jackson",
];
var background = [
	"#d5f5ff",
	"#fff2ea",
	"#edc4ff",
	"#fef3db",
	"#fcf3ff",
	"#d5f5ff",
];
var score = ["4", "9", "10", "7", "8", "5"];

let respondents = [];

for (var i = 0; i < 35; i++) {
	var rand0 = Math.floor(Math.random() * 100);
	var rand1 = Math.floor(Math.random() * 100);
	var rand2 = Math.floor(Math.random() * 100);

	let respondent = {
		emoji: emoji[rand0 % 6],
		background: background[rand1 % 6],
		name: names[rand2 % 6],
		score: score[rand2 % 6],
		key: i,
		url: "#",
	};
	respondents.push(respondent);
}

function Layout() {
	return (
		<div className="layout-wrapper">
			<h1 className="headerText">Dashboard</h1>
			<div className="row">
				<div className="column left">
					<CardContainer />
				</div>

				<div className="column right">
					<RespondentContainer respondents={respondents} />
				</div>
			</div>
		</div>
	);
}

export default Layout;
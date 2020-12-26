import React from "react";
import "./RespondentContainer.scss";
import RespondentItem from "../RespondentItem/RespondentItem";

const RespondentContainer = (props) => {
	const [filter, setFilter] = React.useState("");

	const clearInput = () => {
    setFilter("");
    document.getElementById("filter-respondents").value = "";
  	}

	return (
		<div className="respondent-container">
			<form role="filter-respondents">
				<label htmlFor="filter-respondents">Search for stuff</label>
				<input
					id="filter-respondents"
					type="search"
					placeholder="Filter respondents..."
					autoFocus
					onChange={(e) => setFilter(e.target.value.toLowerCase())}
				/>
				<button onClick={(e) => clearInput()}>Clear</button>
			</form>

			<div className="wrapper">
				<div id="infoi"></div>

				<div className="respondent-items">
					{props.respondents.map((respondent) => {
						if (respondent.name.toLowerCase().includes(filter)) {
							console.log(filter);
							return (
								<RespondentItem
									key={respondent.key}
									respondent={respondent}
								/>
							);
						}
					})}
				</div>
			</div>
		</div>
	);
};

export default RespondentContainer;
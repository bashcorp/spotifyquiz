import React from 'react';
import './Respondent.css';
import RespondentItem from '../RespondentItem/RespondentItem';



class Respondent extends React.Component {

	render() {
		return (
<section>
			<div id="wave"/>
			<div/>


			<div className="Respondent">

			 <h2 id="responses-header">Results ({this.props.respondents.length})</h2>


			<ul className="respondent-list">{
				this.props.respondents.map(respondent => {
					return <li className="respondent"><RespondentItem respondent={respondent}/></li>;
				})
			}
			</ul>

			</div>
			</section>

			);
		}
}


export default Respondent;

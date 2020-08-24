import React from 'react';
import './Respondent.scss';
import RespondentItem from '../RespondentItem/RespondentItem';



class Respondent extends React.Component {

	render() {
		return (
			<div className="Respondent">
			    <div class="diagonal-box-respondent">
  					<div class="content-respondent">

			 <h2 id="responses-header">Results ({this.props.respondents.length})</h2>


			<ul className="respondent-list">{
				this.props.respondents.map(respondent => {
					return <li className="respondent"><RespondentItem respondent={respondent}/></li>;
				})
			}
			</ul>

			</div>
			</div>
			</div>

			);
		}
}


export default Respondent;

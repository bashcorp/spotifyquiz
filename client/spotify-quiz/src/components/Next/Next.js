import React from 'react';
import { useHistory } from "react-router-dom";
import { Route, Router } from "react-router-dom";
import Dashboard from "../Dashboard/Dashboard"

import './Next.css';

const Next = (props) => {

  const routeToResults = () => {
  	if (props.buttonText === "Submit") {
  		window.location.href = '/results'
  	}
  }
	
    return (
    		<div className="Next">
				<button onClick={() => routeToResults()} disabled={props.isNextDisabled}>{props.buttonText}</button>
			</div>
		);	
}
export default Next;
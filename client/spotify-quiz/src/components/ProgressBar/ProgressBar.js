import React from 'react';
import './ProgressBar.css';



export var ProgressBar = ({ width }) => {

 	 const [value, setValue] = React.useState(0);

		  React.useEffect(() => {
		    setValue(width);
		  });

		return (
			 <div className="progress-div" style={{width: 100+"%"}}>
           		<div style={{width: `${value}vw`}}className="progress"/>
      		 </div>

			);
	}



export default ProgressBar;
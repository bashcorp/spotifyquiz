import React from 'react';
import './Share.css';


function Share() {

	return (

    <div className="Share">


    <h2 id="my-quiz-header">My Quiz</h2>
    <ul className="share-wrapper">
		<li id="take-it">
		<div className="take-it">
	    	<div className="social-take-title">
		   		<h3>Take it</h3>
		   	</div>

		   	<p>How well do you know your music taste? We'll generate a quiz from your listening habits to put your knowledge to the test.</p>

		   	<div className="share-button-wrapper">
		   		<a className="share-button" href="/quiz">Start quiz</a>
		   	</div>
		</div>
		</li>
		
		<li id="link-it">
		<div className="link-it">
			<div className="social-link-title">
		   		<h3>Link it</h3>
		   	</div>

		   	<p className="quiz-url-description">Custom URL:</p>

			<div className="share-url-wrapper" id="copy-link">
		   	<span className="share-url">www.spot-on.app/quiz/74628492</span>
			</div>

		   	<div className="share-button-wrapper">
			   	<a className="share-button" href="#">Copy link</a>
			 </div>
			</div>

	   	</li>


		<li id="share-it">
	    <div className="share-title">
	   		<h3>Share it</h3>
	    </div>
	    <div>
	    	<ul className="social-wrapper">
	    		<li className="instagram-wrapper">
	    			<a>
						<svg className="instagram-icon" xmlns="http://www.w3.org/2000/svg"><path d="M11.984 16.815c2.596 0 4.706-2.111 4.706-4.707 0-1.409-.623-2.674-1.606-3.538-.346-.303-.735-.556-1.158-.748-.593-.27-1.249-.421-1.941-.421s-1.349.151-1.941.421c-.424.194-.814.447-1.158.749-.985.864-1.608 2.129-1.608 3.538 0 2.595 2.112 4.706 4.706 4.706zm.016-8.184c1.921 0 3.479 1.557 3.479 3.478 0 1.921-1.558 3.479-3.479 3.479s-3.479-1.557-3.479-3.479c0-1.921 1.558-3.478 3.479-3.478zm5.223.369h6.777v10.278c0 2.608-2.114 4.722-4.722 4.722h-14.493c-2.608 0-4.785-2.114-4.785-4.722v-10.278h6.747c-.544.913-.872 1.969-.872 3.109 0 3.374 2.735 6.109 6.109 6.109s6.109-2.735 6.109-6.109c.001-1.14-.327-2.196-.87-3.109zm2.055-9h-12.278v5h-1v-5h-1v5h-1v-4.923c-.346.057-.682.143-1 .27v4.653h-1v-4.102c-1.202.857-2 2.246-2 3.824v3.278h7.473c1.167-1.282 2.798-2 4.511-2 1.722 0 3.351.725 4.511 2h7.505v-3.278c0-2.608-2.114-4.722-4.722-4.722zm2.722 5.265c0 .406-.333.735-.745.735h-2.511c-.411 0-.744-.329-.744-.735v-2.53c0-.406.333-.735.744-.735h2.511c.412 0 .745.329.745.735v2.53z"/></svg>
	    			</a>
	    		</li>
	    		<li className="twitter-wrapper">
	    			<a>
						<svg className="twitter-icon" xmlns="http://www.w3.org/2000/svg"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg>
	    			</a>
	    		</li>
	    		<li className="facebook-wrapper">
	    			<a>
						<svg className="facebook-icon" xmlns="http://www.w3.org/2000/svg"><path d="M22.675 0h-21.35c-.732 0-1.325.593-1.325 1.325v21.351c0 .731.593 1.324 1.325 1.324h11.495v-9.294h-3.128v-3.622h3.128v-2.671c0-3.1 1.893-4.788 4.659-4.788 1.325 0 2.463.099 2.795.143v3.24l-1.918.001c-1.504 0-1.795.715-1.795 1.763v2.313h3.587l-.467 3.622h-3.12v9.293h6.116c.73 0 1.323-.593 1.323-1.325v-21.35c0-.732-.593-1.325-1.325-1.325z"/></svg>
	    			</a>
	    		</li>
	    		<li className="email-wrapper">
	    			<a>
						<svg className="email-icon" xmlns="http://www.w3.org/2000/svg"><path d="M12 12.713l-11.985-9.713h23.97l-11.985 9.713zm0 2.574l-12-9.725v15.438h24v-15.438l-12 9.725z"/></svg>
	    			</a>
	    		</li>
	    		<li className="text-wrapper">
	    			<a>
						<svg className="text-icon" xmlns="http://www.w3.org/2000/svg"><path d="M17.5 2c.276 0 .5.224.5.5v19c0 .276-.224.5-.5.5h-11c-.276 0-.5-.224-.5-.5v-19c0-.276.224-.5.5-.5h11zm2.5 0c0-1.104-.896-2-2-2h-12c-1.104 0-2 .896-2 2v20c0 1.104.896 2 2 2h12c1.104 0 2-.896 2-2v-20zm-9.5 1h3c.276 0 .5.224.5.501 0 .275-.224.499-.5.499h-3c-.275 0-.5-.224-.5-.499 0-.277.225-.501.5-.501zm1.5 18c-.553 0-1-.448-1-1s.447-1 1-1c.552 0 .999.448.999 1s-.447 1-.999 1zm5-3h-10v-13h10v13z"/></svg>
	    			</a>
	    		</li>
	    	</ul>
	    </div>
	    </li>
	   </ul>
    </div>
  );
}

export default Share;

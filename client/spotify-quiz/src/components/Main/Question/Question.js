import React from "react";
import Glide from "@glidejs/glide";
import Choice from "../Choice/Choice";
import Range from "../Range/Range";


import "./Question.scss";

const Question = ({ question, handleOffer }) => {
  return (
    <div>
      <div
        onClick={() => handleOffer(question.id)}
        className="question-wrapper"
      >
        <div className="question-card">
          <div className="question__grid-container">
            <div className="questionCard-top">
              <div>
                <h3 id="questionCard-header">question {question.id + 1}</h3>
                <hr id="questionCard-underline-top" />
              </div>

              <h2 id="questionCard-question">
                {question.text}
              </h2>
            </div>
            <div className="questionCard-bottom">
              <div className="ResponseContainer"> 

                
{ question.type == "mc" &&
                

                  <div class="square-container">

                    {question.choices.map((choice, index) => (
                      <Choice key={choice.id} choice={choice} index={index} />
                    ))}
                  </div>
               
}

{ question.type == "slider" &&
                
                <div className="range-container">
                      <Range key={question.id} range={question} />
            </div>
}

{ question.type == "select" &&
                <div className="card-container">
                  <ul classNamee="list">
                    {question.choices.map((choice) => (
                      <Choice key={choice.id} choice={choice} />
                    ))}
                  </ul>
                </div> 
}
              </div>  
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Question;
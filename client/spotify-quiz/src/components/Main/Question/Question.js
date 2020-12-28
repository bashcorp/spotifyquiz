import React from "react";
import Glide from "@glidejs/glide";
import Choice from "../Choice/Choice";

import "./Question.scss";

let questions = ["Fitz and the Tantrums", "THE DRIVER ERA", "I DONT KNOW HOW BUT THEY FOUND ME", "Maty Noyes" ]


const Question = ({ plan, handleOffer }) => {
  return (
    <div>
      <div onClick={() => handleOffer(plan.id)} className="question-wrapper">
        <div className="question-card shadow-5">
          <div class="grid-container">
            <div class="questionCard-top">
             <div>
            <h3 id="questionCard-header">question {plan.id + 1}</h3>
            <hr id="questionCard-underline-top" />
          </div>

          <h2 id="questionCard-question">
            {(plan.id % 2 === 0) ? "Lorem ipsum dolor sit amet consectetur adipisicing elit. Culpa, officia ullam ab hic ratione? Nemo, saepe." : "Lorem ipsum dolor sit amet consectetur adipisicing elit."}
          </h2>

            </div>
            <div class="questionCard-bottom">
            <hr id="questionCard-underline-mid" />
              <Choice questions={questions}/>

            </div>
          </div>

    
        </div>
      </div>
    </div>
  );
};

export default Question;
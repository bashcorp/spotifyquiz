import React from "react";
import Glide from "@glidejs/glide";
import Choice from "../Choice/Choice";
import Select from "../Select/Select";

import Range from "../Range/Range";

import "./Question.scss";

const Question = ({ key, question, passAnswer, questionNumber }) => {
  const [choiceResponse, setChoiceResponse] = React.useState("");
  const [selectResponses, setSelectResponses] = React.useState([]);
  const [rangeResponse, setRangeResponse] = React.useState([]);

  const answers = Array(10).fill(0);

  function handleAnswer(answer, questionNumber) {
    passAnswer(answer,questionNumber);
  }

  function handleChoice(newValue, questionNumber) {
    if (choiceResponse === newValue) {
      setChoiceResponse("");
    } else {
      setChoiceResponse(newValue);
    }

    handleAnswer(newValue, questionNumber);
  }


  function handleSelect(newValue, questionNumber) {
    var tempArray = selectResponses;
    if (tempArray.length === 0){
      tempArray = tempArray.concat(newValue);
      setSelectResponses(tempArray);
    } 

    //If not selected, select value
    else if (!tempArray.includes(newValue)) {
      tempArray = tempArray.concat(newValue);
      setSelectResponses(tempArray);
    }

    //If selected, de-select value
    else {
      const index = tempArray.indexOf(newValue);
      if (index > -1) {
        tempArray.splice(index, 1);
        tempArray = [...tempArray];
        setSelectResponses(tempArray);
      }
    }

    handleAnswer(tempArray, questionNumber);
  }

  function handleRange(newValue, questionNumber) {
    if (choiceResponse === newValue) {
      setChoiceResponse("");
    } else {
      setChoiceResponse(newValue);
    }
    
    handleAnswer(newValue, questionNumber);
  }

  return (
    <div>
      <div
        className="question-wrapper"
      >
        <div className="question-card">
          <div className="question__grid-container">
            <div className="questionCard-top">
              <div>
                <h3 id="questionCard-header">question {questionNumber + 1}</h3>
                <hr id="questionCard-underline-top" />
              </div>

              <h2 id="questionCard-question">{question.text}</h2>
            </div>
            <div className="questionCard-bottom">
              <div className="ResponseContainer">
                {question.type === "mc" && (
                  <div className="square-container">
                    {question.choices.map((choice, index) => (
                      <Choice
                        isSelected={choice.id === choiceResponse ? true : false}
                        onChange={handleChoice}
                        key={choice.id}
                        choice={choice}
                        index={index}
                        questionNumber={questionNumber}
                      />
                    ))}
                  </div>
                )}

                {question.type === "slider" && (
                  <div className="range-container">
                    <Range
                    key={question.id}
                    range={question}
                    questionNumber={questionNumber}
                    onChange={handleRange}
                    />
                  </div>
                )}

                {question.type === "select" && (
                  <div className="square-container">
                    {question.choices.map((choice, index) => (
                      <Select
                        isSelected={
                          selectResponses.includes(choice.id) === true
                            ? true
                            : false
                        }
                        onChange={handleSelect}
                        key={choice.id}
                        choice={choice}
                        index={index}
                        questionNumber={questionNumber}
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Question;
import React from "react";
import "./Quiz.scss";
import Question from "../Question/Question.js";
import QuestionSlider from "../QuestionSlider/QuestionSlider.js";
import Glide from "@glidejs/glide";

let answers = [];
/*let quiz = {
    user_id: "21a452hnlj6ppe3gcvy3yx3di",
    questions: [
      {
        id: 32,
        text: "What is their most listened to track in the last 6 months?",
        type: "select",
        choices: [
          {
            id: 106,
            primary_text: "Earthen Dweller",
            secondary_text: "Gnome",
            answer: true,
          },
          {
            id: 107,
            primary_text: "California Rain",
            secondary_text: "Silvertide",
            answer: false,
          },
          {
            id: 108,
            primary_text: "Superman",
            secondary_text: "Skee-Lo",
            answer: true,
          },
          {
            id: 109,
            primary_text: "Foxhole J.C.",
            secondary_text: "Silvertide",
            answer: false,
          },
        ],
      },

      {
        id: 34,
        text: "This is a slider question?",
        min: 0,
        max: 100,
        type: "slider",
      },

      {
        id: 32,
        text: "What is their most listened to track in the last 6 months?",
        type: "mc",
        choices: [
          {
            id: 106,
            primary_text: "Earthen Dweller",
            secondary_text: "Gnome",
            answer: true,
          },
          {
            id: 107,
            primary_text: "California Rain",
            secondary_text: "Silvertide",
            answer: false,
          },
          {
            id: 108,
            primary_text: "Superman",
            secondary_text: "Skee-Lo",
            answer: true,
          },
          {
            id: 109,
            primary_text: "Foxhole J.C.",
            secondary_text: "Silvertide",
            answer: false,
          },
        ],
      }
    ], };*/


const Quiz = () => {
let quiz = window.context.quiz;
console.log(quiz);
let id_list = quiz.questions.map(question => question.id);  
const [questionNumber, setQuestionNumber] = React.useState(0);


  //Store answers as the user completes quiz
  let answer_send = {
    'questions': answers
  }  

  function handleAnswer(newValue, questionNumber) {
    //Update Quiz component's question number
    setQuestionNumber(questionNumber);
    //Pull data from child component with user answer selections
    answer_send.questions[questionNumber] = {
      'question_id': id_list[questionNumber],
      'answer': newValue
    }
  }

  function postRequest() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/response/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
    'quiz_id': quiz.user_id,
    'name': "ben",
    'emoji': "😃",
    'background_color':'333333',
    answer_send
}));

    console.log(JSON.stringify({
    'quiz_id': quiz.user_id,
    'name': "ben",
    'emoji': "😃",
    'background_color':'333333',
    answer_send
}))
  }

  const carouselOptions = {
    type: "track",
    gap: 25,
    peek: 25,
    perView: 1,
    startAt: 0,
    animationDuration: 600,
    dragThreshold: false,
    breakpoints: {
      300: {
        perView: 1,
        gap: 30,
        peek: 100,
      },
    },
  };

  return (
    <div className="Quiz">
      <div className="quiz__grid-container">
        <div className="quiz__question">
          <div className="home-section">
            <QuestionSlider options={carouselOptions}>
              {quiz.questions.map((question, index) => (
                <Question
                  key={question.id}
                  question={question}
                  passAnswer={handleAnswer}
                  questionNumber={index}
                />
              ))}
            </QuestionSlider>
          </div>
        </div>
        <div className="quiz__nav left-shadow-nav">
        {console.log(questionNumber === quiz.questions.length)}
        {console.log("currQuestion: "+ questionNumber)}
        {console.log(quiz.questions.length - 1)}
          {questionNumber !== quiz.questions.length - 1 ?
          (<i onClick={e => document.getElementById("right-butt").click()} className="fas fa-chevron-circle-right"></i>):
          (<i onClick={postRequest} className="fas fa-check"> Finish</i>)}
        </div>
        <div className="quiz__right-nav left-shadow-nav"></div>
      </div>
    </div>
  );
};
export default Quiz;
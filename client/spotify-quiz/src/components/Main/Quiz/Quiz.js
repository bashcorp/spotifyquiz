import React from "react";
import "./Quiz.scss";
import Question from "../Question/Question.js";
import QuestionSlider from "../QuestionSlider/QuestionSlider.js";
import Glide from "@glidejs/glide";

const Quiz = () => {
  //let quiz = window.context.quiz;

  let answer = [];

  let quiz = {
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
      },
    ],
  };

  var questions = {
    questions: [
      { id: 0, text: "plan 0", price: 0 },
      { id: 1, text: "plan 1", price: 1 },
      { id: 2, text: "plan 2", price: 2 },
      { id: 3, text: "plan 2", price: 3 },
      { id: 4, text: "plan 2", price: 4 },
      { id: 5, text: "plan 2", price: 5 },
      { id: 6, text: "plan 2", price: 6 },
      { id: 7, text: "plan 3", price: 7 },
    ],
  };

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


  function handleAnswer(newValue, questionNumber) {
    answer[questionNumber] = newValue;
    console.log(answer);
  }

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
          <i onClick={e => document.getElementById("right-butt").click()} className="fas fa-chevron-circle-right"></i>
        </div>
        <div className="quiz__right-nav left-shadow-nav"></div>
      </div>
    </div>
  );
};
export default Quiz;
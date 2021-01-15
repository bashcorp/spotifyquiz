import React from "react";
import "./Quiz.scss";
import Question from "../Question/Question.js";
import QuestionSlider from "../QuestionSlider/QuestionSlider.js";
import Glide from "@glidejs/glide";

const Quiz = () => {
  const [index, setIndex] = React.useState("1");

  //let quiz = window.context.quiz;

  let quiz = {
    user_id: "21a452hnlj6ppe3gcvy3yx3di",
    questions: [


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

      {
        id: 34,
        text: "This is a slider question?",
        min: 3,
        max: 17,
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
  const handleSelection = (id) => {
    console.log("handleOffer clicked, id: ", id);
    setIndex(id + 1);
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

  return (
    <div className="Quiz">
      <div className="quiz__grid-container">
        <div class="quiz__question">
          <div className="home-section test">
            <QuestionSlider options={carouselOptions}>
              {quiz.questions.map((question) => (
                <Question
                  key={question.id}
                  question={question}
                  handleOffer={handleSelection}
                />
              ))}
            </QuestionSlider>
          </div>
        </div>
        <div class="quiz__nav"></div>
        <div class="quiz__right-nav"></div>
      </div>
    </div>
  );
};
export default Quiz;
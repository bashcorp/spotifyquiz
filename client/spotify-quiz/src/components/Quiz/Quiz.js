import React from 'react';
import './Quiz.css';
import Question from '../Question/Question';
import MultipleChoice from '../MultipleChoice/MultipleChoice';
import MultiSelect from '../MultiSelect/MultiSelect';
import Slider from '../Slider/Slider';
import Next from '../Next/Next';
import ProgressBar from '../ProgressBar/ProgressBar';


let questionIndex = 0;
let buttonText = "Next";
let returnArray = [];
let questionArray = [
{
  question: 'What\'s their favorite song?', 
  type: 'slider', 
  answer: '', 
  assets: { 
    one: "https://images.pexels.com/photos/20787/pexels-photo.jpg?auto=compress&cs=tinysrgb&h=350",
    two: "../../logo.svg", 
    three: "../../logo.svg"}, 
    first: {
     title:'Song #1',
     artist: 'Artist 1'}, 
    second: { title:'Song #2', 
      artist: 'Artist #2'},
    third: { 
      title:'Song #3',  
      artist: 'Artist #3'}, 
    fourth: { 
      title:'Song #4',
      artist: 'Artist #4'}, 
    },
    {
  question: 'What\'s their favorite song?', 
  type: 'multipleChoice', 
  answer: '', 
  assets: { 
    one: "https://images.pexels.com/photos/20787/pexels-photo.jpg?auto=compress&cs=tinysrgb&h=350",
    two: "../../logo.svg", 
    three: "../../logo.svg"}, 
    first: {
     title:'Song #1',
     artist: 'Artist 1'}, 
    second: { title:'Song #2', 
      artist: 'Artist #2'},
    third: { 
      title:'Song #3',  
      artist: 'Artist #3'}, 
    fourth: { 
      title:'Song #4',
      artist: 'Artist #4'}, 
    },
    {
  question: 'SECOND', 
  type: 'multipleSelect', 
  answer: '', 
  assets: { 
    one: "https://images.pexels.com/photos/20787/pexels-photo.jpg?auto=compress&cs=tinysrgb&h=350",
    two: "../../logo.svg", 
    three: "../../logo.svg"}, 
    first: {
     title:'Song #1',
     artist: 'Artist 1'}, 
    second: { title:'Song #2', 
      artist: 'Artist #2'},
    third: { 
      title:'Song #3',  
      artist: 'Artist #3'}, 
    fourth: { 
      title:'Song #4',
      artist: 'Artist #4'}, 
    }
  ];
  let currentProgress = Math.ceil((questionIndex+1/questionArray.length)*100);

const Quiz = (props) => {
  const [currentQuestion, setCurrentQuestion] = React.useState(questionArray[questionIndex]);
  const [nextDisabled, setNextDisabled] = React.useState(true);


  const getData = (val) => {
    returnArray[questionIndex] = val;
    setNextDisabled(false);
  }

  const nextQuestion = () => {
    if (questionArray.length > questionIndex + 1){
      questionIndex += 1;
      setNextDisabled(true);
      currentProgress += (1/questionArray.length)*100;
      currentProgress = Math.ceil(currentProgress);

      if (questionArray.length === questionIndex + 1){
        buttonText = "Submit";

      } 
    }
    setCurrentQuestion(questionArray[questionIndex]);
  }

    return (
    <div className="quiz-wrapper">
      <div className="Quiz">
      <Question question={currentQuestion.question}/>
      {currentQuestion.type === "multipleChoice" &&
        <MultipleChoice sendData={getData} answers={currentQuestion} questionIndex={questionIndex}/>
      }
      {currentQuestion.type === "multipleSelect" &&
        <MultiSelect sendData={getData} answers={currentQuestion} questionIndex={questionIndex}/>
      }
      {currentQuestion.type === "slider" &&
        <Slider sendData={getData} answers={currentQuestion} questionIndex={questionIndex}/>
      }
      <div className="nextButtonWrapper">
      <div className="nextButton" onClick={nextQuestion}>
        <Next isNextDisabled={nextDisabled} buttonText={buttonText}/>
      </div>
      </div>
      <ProgressBar width={currentProgress}/>
     
    </div>
    </div>

    );
}

export default Quiz;

import React from 'react';
import './Quiz.css';
import Question from '../Question/Question';
import MultipleChoice from '../MultipleChoice/MultipleChoice';
import MultiSelect from '../MultiSelect/MultiSelect';
import Slider from '../Slider/Slider';
import Modal from 'react-modal';
import Next from '../Next/Next';
import ProgressBar from '../ProgressBar/ProgressBar';
import { Beforeunload } from 'react-beforeunload';

let questionIndex = 0;
let buttonText = "Next";
let returnArray = [];

const customStyles = {
  content : {
    top                   : '50%',
    left                  : '50%',
    right                 : 'auto',
    bottom                : 'auto',
    marginRight           : '-50%',
    transform             : 'translate(-50%, -50%)',
    backgroundImage       : 'linear-gradient(225deg, #843df5 0%, #129ae2 74%)',
    padding               : "100vh",
    width                 : "35vh"
  }
};

const Quiz = (props) => {

  let quiz = window.context.quiz;
  let questions = quiz["questions"];
  let currentProgress = Math.ceil((questionIndex+1/questions.length)*100);

  const [currentQuestion, setCurrentQuestion] = React.useState(questions[questionIndex]);
  const [nextDisabled, setNextDisabled] = React.useState(true);
  const [modalIsOpen,setIsOpen] = React.useState(true);
  var subtitle;

  const getData = (val) => {
    returnArray[questionIndex] = val;
    setNextDisabled(false);
  }
 
  const afterOpenModal = () => {
    subtitle.style.color = "white";
  }
 
  const closeModal = () => {
    setIsOpen(false);
  }

  const nextQuestion = () => {
    if (questions.length > questionIndex + 1){
      questionIndex += 1;
      setNextDisabled(true);
      currentProgress += (1/questions.length)*100;
      currentProgress = Math.ceil(currentProgress);


      if (questions.length === questionIndex + 1){
        buttonText = "Submit";

      } 
    }
    setCurrentQuestion(questions[questionIndex]);
  }

    return (
      <>
            <Beforeunload onBeforeunload={() => "You'll lose your data!"} />

        <Modal
          class="modal"
          isOpen={modalIsOpen}
          onAfterOpen={afterOpenModal}
          style={customStyles}
          contentLabel="Example Modal"
           closeTimeoutMS={700}
        >
          <h2 class="modal-greeting" ref={_subtitle => (subtitle = _subtitle)}>Get Ready!</h2>
          <h3 class="modal-subtitle">Enter your name to get started.</h3>
          <form>
          <input autofocus class="name-entry" placeholder="e.g. Maya Angelou" />
            <div onClick={closeModal} className="share-button-wrapper">
            <a className="start-button" href="/quiz">Start quiz</a>
            </div>
          </form>
        </Modal>

    <div id="quiz-wrapper" className="quiz-wrapper">
        <div className="background-of-quiz">
      {Array(questionIndex + 1).fill(<span></span>)}
    </div>

      <div className="Quiz">

      <Question question={currentQuestion.text}/>
      {currentQuestion.type === "mc" &&
        <MultipleChoice sendData={getData} answers={currentQuestion} questionIndex={questionIndex}/>
      }
      {currentQuestion.type === "check" &&
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
    </>

    );
}

export default Quiz;

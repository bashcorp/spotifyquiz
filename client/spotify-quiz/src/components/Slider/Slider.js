import React, {useState} from 'react'; //142
import './Slider.css';

const Slider = (props) => {
	let { sendData, answers, questionIndex } = props;
	
	const [value, setValue] = useState(answers.min)

	const handleChange = (event) => {
		setValue(event.target.value);
		sendData(value);
	}

	return (
		<div className='sliderWrapper'>
        <input className="slider" id={answers.id} type="range" min={answers.min} max={answers.max} defaultValue={answers.min} step="1" onChange={handleChange}/>
        <div className='value'>{value}</div>
      </div>
	);
}
export default Slider;
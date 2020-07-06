import React, {useState} from 'react'; //142
import './Slider.css';

const Slider = (props) => {
	let { sendData, answers, questionIndex } = props;
	
	const [value, setValue] = useState(0)

	const handleChange = (event) => {
		setValue(event.target.value);
		sendData(value);
	}

	return (
		<div className='sliderWrapper'>
        <input className="slider" id="typeinp" type="range" min="0" max="5" defaultValue="0" step="1" onChange={handleChange}/>
        <div className='value'>{value}</div>
      </div>
	);
}
export default Slider;
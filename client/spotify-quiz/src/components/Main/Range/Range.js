import React from "react";
import "./Range.scss";
import Slider from "react-rangeslider";

const Range = (props) => {

  var max = props.range.max;
  var min = props.range.min;
  var mid = Math.ceil((max+min)/2);


  var labels = [min, max];

  const [value, setValue] = React.useState(mid);
  const [secondaryText, setSecondaryText] = React.useState("‏‏‎ ‎");

   const label = {
  [min]: "Low",
  [mid]: "Mid",
  [max]: "High"
}


  const handleOnChange = (value) => {
    setValue(value);
    switch (true) {
      case (value <= min + max * 0.1):
        setSecondaryText("1");
        break;
      case (value >= min + max * 0.25 && value <= min + max * 0.35):
        setSecondaryText("2");
        break;
      case (value >= min + max * 0.65 && value <= min + max * 0.75):
        setSecondaryText("3");
      break;
      case (value >= min + max * 0.9):
        setSecondaryText("4");
        break;
      default:
        setSecondaryText("‎‏‏‎ ‎");
        break;
    }

    props.onChange(value,props.questionNumber);

  };

  return (
    <div className="range">
      <div className="slider-displayValue">{value}</div>
      <div className="slider-displaySecondaryText">{secondaryText}</div>
      <div id="slider-wrapper">
        <Slider
          value={value}
          max={max}
          min={min}
          tooltip={false}
          labels={label}
          onChange={handleOnChange}
        />
      </div>
    </div>
  );
};
export default Range;
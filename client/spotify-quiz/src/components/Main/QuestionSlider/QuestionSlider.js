
import React, { Component } from "react";
import Glide from "@glidejs/glide";

export default class QuestionSlider extends Component {
  state = { id: null };

  componentDidMount = () => {
    // Generated random id
    this.setState(
      { id: `glide-${Math.ceil(Math.random() * 100)}` },
      this.initializeGlider,
      this.goRight
    );
  };

  initializeGlider = () => {
    this.slider = new Glide(`#${this.state.id}`, this.props.options);
    this.slider.mount();
  };

  componentWillReceiveProps = newProps => {
    if (this.props.options.startAt !== newProps.options.startAt) {
      this.slider.go(`=${newProps.options.startAt}`);
    }
  };

  render = () => (
    // controls
    <div id={this.state.id} className="slider">
      <div className="hidden" data-glide-el="controls">
        <button className="arrow-left" data-glide-dir="<" title="start">
          <span className="hidden">Start</span>
        </button>
        <button className="arrow-right" id="right-butt" data-glide-dir=">" title="end">
          <span className="hidden">End</span>
        </button>
      </div>
      {/* track  */}
      <div data-glide-el="track">
        <div style={{ display: "flex" }}>
          {this.props.children.map((slide, index) => {
            return React.cloneElement(slide, {
              key: index,
              className: `${slide.props.className} your_cutom_classname`
            });
          })}
        </div>
      </div>
      
    </div>
  );
}

QuestionSlider.defaultProps = {
  options: {}
};
